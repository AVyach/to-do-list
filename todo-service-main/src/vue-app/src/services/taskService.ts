import apiClient from './apiClient';
import { AxiosResponse } from 'axios';

interface TaskDTO {
  name: string;
  tags?: string[];
  comments?: string;
  state: string;
  deadline?: Date | null | string;
  user_id: string;
}

interface TaskResponse {
  id: number;
  user_id: string;
  name: string;
  tags: string[];
  comments: string | null;
  created_at: string;
  state: string;
  deadline: string | null;
}

class TaskService {
  private readonly BASE_PATH = '/tasks';

  async createTask(taskData: TaskDTO): Promise<TaskResponse> {
    try {
      const response: AxiosResponse<TaskResponse> = await apiClient.post(
        this.BASE_PATH + "/add",
        taskData
      );
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Ошибка при создании задачи');
    }
  }

  async getTasks(): Promise<TaskResponse[]> {
    try {
      const response: AxiosResponse<TaskResponse[]> = await apiClient.get(
        this.BASE_PATH + "/all"
      );
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Ошибка при получении задач');
    }
  }

  async getTaskById(taskId: number): Promise<TaskResponse> {
    try {
      const response: AxiosResponse<TaskResponse> = await apiClient.get(
        `${this.BASE_PATH}/${taskId}`
      );
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Ошибка при получении задачи');
    }
  }

  async updateTask(taskId: number, taskData: Partial<TaskDTO>): Promise<TaskResponse> {
    try {
      const response: AxiosResponse<TaskResponse> = await apiClient.put(
        `${this.BASE_PATH}/${taskId}`,
        taskData
      );
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Ошибка при обновлении задачи');
    }
  }

  async deleteTask(taskId: number): Promise<void> {
    try {
      await apiClient.delete(`${this.BASE_PATH}/${taskId}`);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Ошибка при удалении задачи');
    }
  } 
}

export const taskService = new TaskService();
export type { TaskDTO, TaskResponse };