import { createApp } from 'vue'
import * as VueRouter from 'vue-router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from '@/App'
import routes from '@/routes.js'
import '@/index.css'

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes, // short for `routes: routes`
})

createApp(App)
  .use(router)
  .use(VueAxios, axios)
  .mount('#app')
