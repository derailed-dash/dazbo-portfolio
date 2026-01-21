export interface ShowcaseItem {
  id: string;
  title: string;
  description: string;
  summary?: string;
  imageUrl?: string;
  tags?: string[];
  linkUrl?: string;
  repoUrl?: string;
  isPrivate?: boolean;
  sourceIcon?: string;
  sourceUrl?: string;
  type: 'blog' | 'project' | 'app';
}

export interface Project {
  id?: string;
  title: string;
  description: string;
  repo_url?: string;
  demo_url?: string;
  image_url?: string;
  tags: string[];
  featured: boolean;
  source_platform?: string;
  is_manual: boolean;
  metadata_only: boolean;
  created_at?: string;
}

export interface Blog {
  id?: string;
  title: string;
  summary?: string;
  date: string;
  platform: string;
  url: string;
  image_url?: string;
  source_platform?: string;
  is_manual: boolean;
  metadata_only: boolean;
  is_private: boolean;
  markdown_content?: string;
  ai_summary?: string;
  author_url?: string;
  tags?: string[];
  created_at?: string;
}

export interface ChatMessage {
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
}
