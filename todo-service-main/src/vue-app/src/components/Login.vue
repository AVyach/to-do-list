<template>
    <div class="login-card card">
      <h2 class="card-title">Вход</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <input
          v-model="loginDTO.username"
          class="input-field"
          placeholder="Имя пользователя"
          required
        />
        <input
          v-model="loginDTO.password"
          class="input-field"
          type="password"
          placeholder="Пароль"
          required
        />
        <button type="submit" class="btn-submit">Войти</button>
      </form>
      <div v-if="error" class="error-message">{{ error.message }}</div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, toRaw } from "vue";
  import { useRouter } from "vue-router";
  import { useUserStore } from "../store/userStore";
  import AuthService from "../services/authService";
  import { LoginDTO } from "../dtos/authDTO";
  
  export default defineComponent({
    name: "Login",
    setup() {
      const router = useRouter();
      const userStore = useUserStore();
      const loginDTO = reactive<LoginDTO>({
        username: "",
        password: "",
      });
      const error = reactive({ message: "" });
  
      const handleLogin = async () => {
        try {
          const userData = await AuthService.login(toRaw(loginDTO));
          userStore.setUser(userData);
          router.push("/")
        } catch (err: any) {
          console.log(err)
        }
      };
  
      return {
        loginDTO,
        error,
        handleLogin,
      };
    },
  });
  </script>
<style src="src/assets/components/auth.scss"></style>