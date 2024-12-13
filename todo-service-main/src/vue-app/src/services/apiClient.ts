import axios, { AxiosInstance } from 'axios';
import { useUserStore } from '../store/userStore';


const refreshApiClient = axios.create({
  baseURL: `http://${import.meta.env.VITE_API_BASE_URL}`,
});

const apiClient: AxiosInstance = axios.create({
  baseURL: `http://${import.meta.env.VITE_API_BASE_URL}`,
});

let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

async function refreshToken() {
  const refreshToken = localStorage.getItem("refresh_token");
  if (!refreshToken) {
    throw new Error("No refresh token available");
  }
  
  const response = await refreshApiClient.post("/auth/token/refresh", {
    refresh_token: refreshToken,
  });

  const { access_token, refresh_token: newRefreshToken } = response.data;
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('refresh_token', newRefreshToken);
  return access_token;
}

apiClient.interceptors.request.use(

  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const userStore = useUserStore()

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers['Authorization'] = `Bearer ${token}`;
            return apiClient(originalRequest);
          })
          .catch(err => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newAccessToken = await refreshToken();
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        
        processQueue(null, newAccessToken);
        return apiClient(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        userStore.logout()
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_id");
        localStorage.removeItem("refresh_token");
        window.location.reload();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;