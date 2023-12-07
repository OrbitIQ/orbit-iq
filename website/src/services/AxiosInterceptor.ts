// axios.js
import axios from 'axios';
import { apiURL } from '@/Constants/constants';
import { eventEmitter } from '../eventEmitter';

const api = axios.create({
  baseURL: apiURL,
});

// Request interceptor for API calls
api.interceptors.request.use(
  config => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user && user.access_token) {
      config.headers['Authorization'] = `Bearer ${user.access_token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);


// Response interceptor for API calls
api.interceptors.response.use(
  response => response,
  error => {
    console.log(error.response.status)
    if (error.response && error.response.status == 401 || (error.response.status == 422 && error.response.data.msg == 'Signature verification failed')) {
      // JWT expired or unauthorized access
      if (window.location.pathname !== '/login') {
        window.location.href = '/logout'; // Redirect to logout if not already on login page 
      }
    } else if (error.response && error.response.data && error.response.data.msg) {
      // Emit a custom event with the error message
      eventEmitter.emit('apiError', error.response.data.msg);
    }
    return Promise.reject(error);
  }
);

export default api;