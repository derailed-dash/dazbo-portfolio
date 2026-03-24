import apiClient from './api';
import type { Video } from '../types';

/**
 * Fetches the list of YouTube videos from the backend API.
 * @returns A promise that resolves to an array of Video objects.
 */
export const getVideos = async (): Promise<Video[]> => {
  const response = await apiClient.get<Video[]>('/api/videos');
  return response.data;
};
