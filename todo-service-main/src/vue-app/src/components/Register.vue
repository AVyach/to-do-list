<template>
    <div class="register-card card">
      <h2 class="card-title">Регистрация</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <input
          v-model="registerDTO.username"
          class="input-field"
          placeholder="Имя пользователя"
          required
        />
        <input
          v-model="registerDTO.email"
          class="input-field"
          type="email"
          placeholder="Email"
          required
        />
        <input
          v-model="registerDTO.password"
          class="input-field"
          type="password"
          placeholder="Пароль"
          required
        />
        <input
          v-model="registerDTO.confirmPassword"
          class="input-field"
          type="password"
          placeholder="Подтвердите пароль"
          required
        />
        <div v-if="passwordsMismatch" class="error-message">Пароли не совпадают</div>
        <button type="submit" class="btn-submit">Зарегистрироваться</button>
      </form>
      <div v-if="error" class="error-message">{{ error.message }}</div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, computed, toRaw } from "vue";
  import { useRouter } from "vue-router";
  import AuthService from "../services/authService";
  import { RegisterDTO } from "../dtos/authDTO";
  
  export default defineComponent({
    name: "Register",
    setup() {
      const router = useRouter();
      const registerDTO = reactive<RegisterDTO>({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
      });
      const error = reactive({ message: ""});
      const passwordsMismatch = computed(()=>{
          return registerDTO.password !== registerDTO.confirmPassword
      })
      const handleRegister = async () => {
        try {
          const payload = toRaw(registerDTO)
          await AuthService.register(payload);
          router.push("/login");
        } catch (err: any) {
  
          error.message = err.response.data.detail;
        }
      };
  
      return {
        registerDTO,
        error,
        handleRegister,
        passwordsMismatch,
      };
    },
  });
  </script>

<style src="src/assets/components/auth.scss"></style>