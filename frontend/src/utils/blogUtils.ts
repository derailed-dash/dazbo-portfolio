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
    .replace(/\s+/g, ' ')                  // Replace multiple whitespaces with a single space
    .replace(/[^\w\s-]/g, '');             // Remove non-word, non-space, non-dash characters (optional, but safer)
};

/**
 * Merges duplicate blog articles based on their title.
 * Articles from dev.to take precedence for metadata.
 * @param blogs List of blog articles from the backend.
 * @returns Deduplicated list of blog articles.
 */
export const mergeDuplicateArticles = (blogs: Blog[]): Blog[] => {
  const blogMap = new Map<string, Blog[]>();

  // Group blogs by normalized title
  blogs.forEach((blog) => {
    const key = normalizeTitle(blog.title);
    if (!blogMap.has(key)) {
      blogMap.set(key, []);
    }
    blogMap.get(key)!.push(blog);
  });

  const result: Blog[] = [];

  blogMap.forEach((duplicates) => {
    if (duplicates.length === 1) {
      const blog = duplicates[0];
      result.push({
        ...blog,
        platforms: [{ name: blog.platform, url: blog.url }]
      });
      return;
    }

    // Sort to prioritize dev.to for metadata
    const sorted = [...duplicates].sort((a, b) => {
      const aDev = a.platform.toLowerCase().includes('dev.to');
      const bDev = b.platform.toLowerCase().includes('dev.to');
      if (aDev && !bDev) return -1;
      if (!aDev && bDev) return 1;
      return 0;
    });

    const primary = sorted[0];
    const platforms = duplicates.map((d) => ({
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
