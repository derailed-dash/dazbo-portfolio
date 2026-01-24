import apiClient from './api';
import type { Project, Blog, Application, Content } from '../types';

export const getBlogs = async (): Promise<Blog[]> => {
  const response = await apiClient.get<Blog[]>('/api/blogs');
  return response.data;
};

export const getProjects = async (): Promise<Project[]> => {
  const response = await apiClient.get<Project[]>('/api/projects');
  return response.data;
};

export const getApplications = async (): Promise<Application[]> => {
  const response = await apiClient.get<Application[]>('/api/applications');
  return response.data;
};

export const getExperience = async () => {
  const response = await apiClient.get('/api/experience');
  return response.data;
};

export const getContentBySlug = async (slug: string): Promise<Content> => {
  const response = await apiClient.get<Content>(`/api/content/${slug}`);
  return response.data;
};
