import LoginPage from '@/components/LoginPage'
import UndrawImage from '@/components/UndrawImage'
import ProjectTasks from '@/components/ProjectTasks'
import ProjectsPage from '@/components/ProjectsPage'
import UsersPage from '@/components/UsersPage'
import HomePage from '@/components/HomePage'

export default [
  { path: '/', component: HomePage, authLevel: 0, name: 'Home' },
  { path: '/:catchAll([a-zA-Z0-9]+)', component: UndrawImage, props: { icon: "page_not_found", text: 'Ошибка 404. Нет такой страницы' } },
  { path: '/login', component: LoginPage },
  { path: '/home', component: UndrawImage, props: { icon: "blank_canvas", text: 'Проект пока не выбран' }, authLevel: 1, name: 'My Projects' },
  { path: '/project/:id', component: ProjectTasks, authLevel: 9, name: 'My Projects ' },
  { path: '/projects', component: ProjectsPage, authLevel: 2, name: 'Projects' },
  { path: '/users', component: UsersPage, authLevel: 2, name: 'Users' },
]
