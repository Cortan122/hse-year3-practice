import { createApp } from 'vue'
import * as VueRouter from 'vue-router'
import App from '@/App.vue'
import routes from '@/routes.js'
import '@/index.css'

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes, // short for `routes: routes`
})

createApp(App).use(router).mount('#app')
