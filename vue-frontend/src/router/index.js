import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import Room from '@/views/Room.vue'
import Login from '@/views/Login.vue'
import SignUp from '@/views/SignUp.vue'

const routes = [
  {
    path: '/',
    component: Main
  },
  {
    path: '/:id',
    component: Room
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/sign-up',
    component: SignUp
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
