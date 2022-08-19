import HelloWorld from '@/components/HelloWorld'
import LoginPage from '@/components/LoginPage'
import UndrawImage from '@/components/UndrawImage'
import ProjectTasks from '@/components/ProjectTasks'

export default [
  { path: '/', component: HelloWorld, props: { msg: "Welcome to Your Vue.js App" }, authLevel: 0, name: 'Home' },
  { path: '/:catchAll([a-zA-Z0-9]+)', component: UndrawImage, props: { icon: "page_not_found", text: 'Ошибка 404. Нет такой страницы' } },
  { path: '/login', component: LoginPage },
  { path: '/home', component: UndrawImage, props: { icon: "blank_canvas", text: 'Проект пока не выбран' }, authLevel: 1, name: 'My Projects' },
  { path: '/project/:id', component: ProjectTasks, authLevel: 9, name: 'My Projects ' },
]
