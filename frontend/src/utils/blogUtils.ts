import type { Blog } from '../types';

/**
 * Normalizes a title for comparison by removing extra whitespace, 
 * converting to lowercase, and standardizing common characters like dashes.
 */
const normalizeTitle = (title: string): string => {
  return title
    .trim()
    .toLowerCase()
    .replace(/[\u2013\u2014\u2015]/g, '-') // Standardize different types of dashes (en, em, etc.)
    .replace(/\s+/g, ' ');                 // Replace multiple whitespaces with a single space
};

/**
 * Checks if two normalized titles represent the same article,
 * handling potential truncation with ellipses (e.g. from RSS feeds).
 */
const isDuplicateTitle = (t1: string, t2: string): boolean => {
  if (t1 === t2) return true;

  const stripEllipsis = (t: string): string | null => {
    if (t.endsWith('…')) {
      return t.slice(0, -1).trim();
    }
    if (t.endsWith('...')) {
      return t.slice(0, -3).trim();
    }
    return null;
  };

  const s1 = stripEllipsis(t1);
  if (s1 && s1.length >= 10 && t2.startsWith(s1)) return true;

  const s2 = stripEllipsis(t2);
  if (s2 && s2.length >= 10 && t1.startsWith(s2)) return true;

  return false;
};

/**
 * Merges duplicate blog articles based on their title.
 * Articles from dev.to take precedence for metadata and icon order.
 * @param blogs List of blog articles from the backend.
 * @returns Deduplicated list of blog articles.
 */
export const mergeDuplicateArticles = (blogs: Blog[]): Blog[] => {
  const groups: Blog[][] = [];

  blogs.forEach((blog) => {
    const norm = normalizeTitle(blog.title);
    
    // Check if it matches any existing group
    const matchedGroup = groups.find((group) => {
      const existingNorm = normalizeTitle(group[0].title);
      return isDuplicateTitle(existingNorm, norm);
    });

    if (matchedGroup) {
      matchedGroup.push(blog);
    } else {
      groups.push([blog]);
    }
  });

  const result: Blog[] = [];

  groups.forEach((duplicates) => {
    if (duplicates.length === 1) {
      const blog = duplicates[0];
      result.push({
        ...blog,
        platforms: [{ name: blog.platform, url: blog.url }]
      });
      return;
    }

    // Sort to prioritize dev.to for metadata AND icon order
    const sorted = [...duplicates].sort((a, b) => {
      const aDev = a.platform.toLowerCase().includes('dev.to');
      const bDev = b.platform.toLowerCase().includes('dev.to');
      if (aDev && !bDev) return -1;
      if (!aDev && bDev) return 1;
      return 0;
    });

    const primary = sorted[0];
    const platforms = sorted.map((d) => ({
      name: d.platform,
      url: d.url
    }));

    result.push({
      ...primary,
      platforms
    });
  });

  // Sort by date descending (standard for blogs)
  return result.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
};
