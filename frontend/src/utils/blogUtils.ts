import { Blog } from '../types';

/**
 * Merges duplicate blog articles based on their title.
 * Articles from dev.to take precedence for metadata.
 * @param blogs List of blog articles from the backend.
 * @returns Deduplicated list of blog articles.
 */
export const mergeDuplicateArticles = (blogs: Blog[]): Blog[] => {
  const blogMap = new Map<string, Blog[]>();

  // Group blogs by title
  blogs.forEach((blog) => {
    const title = blog.title.trim();
    if (!blogMap.has(title)) {
      blogMap.set(title, []);
    }
    blogMap.get(title)!.push(blog);
  });

  const result: Blog[] = [];

  blogMap.forEach((duplicates, title) => {
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
      if (a.platform.toLowerCase().includes('dev.to')) return -1;
      if (b.platform.toLowerCase().includes('dev.to')) return 1;
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
