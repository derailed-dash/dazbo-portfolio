import axios from 'axios';
import type { Project, Blog } from '../types';

export const getBlogs = async (): Promise<Blog[]> => {
  const response = await axios.get<Blog[]>('/blogs');
  return response.data;
};

export const getProjects = async (): Promise<Project[]> => {
  const response = await axios.get<Project[]>('/projects');
  return response.data;
};

export const getExperience = async () => {
  const response = await axios.get('/experience');
  return response.data;
};
