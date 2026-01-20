import axios from 'axios';

const apiClient = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 429) {
      console.warn("You are sending requests too fast. Please wait a moment.");
    }
    return Promise.reject(error);
  }
);

export default apiClient;
