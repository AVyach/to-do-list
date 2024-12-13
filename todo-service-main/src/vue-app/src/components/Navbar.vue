<template>
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
        <img src="/public/logo.svg" alt="Logo" class="navbar-logo">
      </div>
        <div v-if="userStore.isAuthenticated" class="navbar-authenticated">
          <span class="username">{{ userStore.user?.username }}</span>
          <button class="logout-btn" @click="logout">Выйти</button>
          <router-link to="/" class="nav-link">Главная</router-link>
        </div>
        <div v-else class="navbar-unauthenticated">
          <router-link to="/register" class="nav-link">Регистрация</router-link>
          <router-link to="/login" class="nav-link">Вход</router-link>
        </div>
        
        
      </div>
    </nav>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { useUserStore } from "../store/userStore";
  import AuthService from "../services/authService";
  
  
  
  export default defineComponent({
    name: "Navbar",
    setup() {
  
      const userStore = useUserStore();
      const logout = () => {
        AuthService.logout();
        userStore.logout();
  
      };
  
      return {
        userStore,
        logout,
      };
    },
  });
  </script>

<style src="src/assets/components/navbar.scss"></style>
