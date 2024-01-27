import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8887',
});

export default api;
