export interface ShowcaseItem {
  id: string;
  title: string;
  description: string;
  imageUrl?: string;
  tags?: string[];
  linkUrl?: string;
  repoUrl?: string;
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
  description?: string; // Fallback if summary is missing during mapping
  date: string;
  platform: string;
  url: string;
  image_url?: string; // Not in backend model yet, but used in frontend
  source_platform?: string;
  is_manual: boolean;
  metadata_only: boolean;
  tags?: string[];
  created_at?: string;
}

export interface ChatMessage {
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
}
