import { describe, it, expect } from 'vitest';
import { mergeDuplicateArticles } from './blogUtils';
import type { Blog } from '../types';

describe('blogUtils', () => {
  describe('mergeDuplicateArticles', () => {
    it('should return empty array if input is empty', () => {
      expect(mergeDuplicateArticles([])).toEqual([]);
    });

    it('should not change anything if there are no duplicates', () => {
      const blogs: Blog[] = [
        { title: 'Blog 1', platform: 'Medium', url: 'url1', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false },
        { title: 'Blog 2', platform: 'dev.to', url: 'url2', date: '2026-01-02', is_manual: false, metadata_only: false, is_private: false }
      ];
      expect(mergeDuplicateArticles(blogs)).toHaveLength(2);
    });

    it('should merge articles with the same title', () => {
      const blogs: Blog[] = [
        { title: 'Duplicate Blog', platform: 'Medium', url: 'medium-url', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false },
        { title: 'Duplicate Blog', platform: 'dev.to', url: 'devto-url', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false }
      ];
      const merged = mergeDuplicateArticles(blogs);
      expect(merged).toHaveLength(1);
    });

    it('should prefer dev.to metadata over Medium', () => {
      const blogs: Blog[] = [
        { 
          title: 'Duplicate Blog', 
          platform: 'Medium', 
          url: 'medium-url', 
          date: '2026-01-01', 
          summary: 'Medium Summary', 
          tags: ['medium'],
          is_manual: false, 
          metadata_only: false, 
          is_private: false 
        },
        { 
          title: 'Duplicate Blog', 
          platform: 'dev.to', 
          url: 'devto-url', 
          date: '2026-01-01', 
          summary: 'dev.to Summary', 
          tags: ['devto'],
          is_manual: false, 
          metadata_only: false, 
          is_private: false 
        }
      ];
      const merged = mergeDuplicateArticles(blogs);
      expect(merged[0].summary).toBe('dev.to Summary');
      expect(merged[0].tags).toContain('devto');
      expect(merged[0].tags).not.toContain('medium');
    });

    it('should merge articles with extremely similar titles (whitespace/dashes)', () => {
      const blogs: Blog[] = [
        { 
          title: 'How to Avoid an Unexpected Cloud Bill – Fully Automated', // em-dash
          platform: 'Medium', 
          url: 'medium-url', 
          date: '2026-01-01', 
          is_manual: false, 
          metadata_only: false, 
          is_private: false 
        },
        { 
          title: 'How to Avoid an Unexpected Cloud Bill — Fully Automated', // em-dash with different spacing
          platform: 'dev.to', 
          url: 'devto-url', 
          date: '2026-01-01', 
          is_manual: false, 
          metadata_only: false, 
          is_private: false 
        }
      ];
      const merged = mergeDuplicateArticles(blogs);
      expect(merged).toHaveLength(1);
      expect(merged[0].platforms).toHaveLength(2);
    });

    it('should NOT merge distinct technical titles (C# vs C)', () => {
      const blogs: Blog[] = [
        { title: 'C# Programming', platform: 'dev.to', url: 'url1', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false },
        { title: 'C Programming', platform: 'dev.to', url: 'url2', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false }
      ];
      expect(mergeDuplicateArticles(blogs)).toHaveLength(2);
    });

    it('should NOT merge distinct technical titles (Node.js vs Nodejs)', () => {
      const blogs: Blog[] = [
        { title: 'Node.js Guide', platform: 'dev.to', url: 'url1', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false },
        { title: 'Nodejs Guide', platform: 'dev.to', url: 'url2', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false }
      ];
      expect(mergeDuplicateArticles(blogs)).toHaveLength(2);
    });

    it('should provide platform icons in a prioritized order (dev.to first)', () => {
      const blogs: Blog[] = [
        { title: 'Duplicate Blog', platform: 'Medium', url: 'medium-url', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false },
        { title: 'Duplicate Blog', platform: 'dev.to', url: 'devto-url', date: '2026-01-01', is_manual: false, metadata_only: false, is_private: false }
      ];
      const merged = mergeDuplicateArticles(blogs);
      expect(merged[0].platforms![0].name).toBe('dev.to');
      expect(merged[0].platforms![1].name).toBe('Medium');
    });
  });
});
