import HelloWorld from '@/components/HelloWorld.vue'
import LoginPage from '@/components/LoginPage.vue'

export default [
  { path: '/', component: HelloWorld, props: { msg: "Welcome to Your Vue.js App" }, authLevel: 0, name: 'Home' },
  { path: '/about', component: HelloWorld, props: { msg: "about!!" }, authLevel: 0, name: 'About' },
  { path: '/:catchAll([a-zA-Z0-9]+)', component: HelloWorld, props: { msg: "404!!" } },
  { path: '/login', component: LoginPage },
]
