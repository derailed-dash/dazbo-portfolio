import axios from 'axios';

export const getBlogs = async () => {
  const response = await axios.get('/blogs');
  return response.data;
};

export const getProjects = async () => {
  const response = await axios.get('/projects');
  return response.data;
};

export const getExperience = async () => {
  const response = await axios.get('/experience');
  return response.data;
};
