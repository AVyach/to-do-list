import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../store/userStore";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import TaskPage from "../components/TaskPage.vue";
const routes = [
  {
    path: "/login",
    name: "login", 
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: "/register",
    name: "register",
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'task-page',
    component: TaskPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
 ];
 
 const router = createRouter({
  history: createWebHistory(),
  routes,
 });
 
 router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresGuest = to.matched.some((record) => record.meta.requiresGuest);
 
  if (requiresAuth && !userStore.isAuthenticated) {
    next('/login');
    return;
  }
 
  if (requiresGuest && userStore.isAuthenticated) {
    next('/');
    return;
  }
 
  next();
 });
 
 export default router;
