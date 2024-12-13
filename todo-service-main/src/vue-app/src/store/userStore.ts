import { defineStore } from 'pinia';
import { UserDTO } from '../dtos/authDTO';
export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null') as UserDTO | null, 
  }
),
  actions: {
    setUser(userData: UserDTO) {
      this.user = userData;
      localStorage.setItem('user', JSON.stringify(userData));
    },
    logout() {
      this.user = null;
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.user,
  },
});