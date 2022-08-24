import LoginPage from '@/components/LoginPage'
import UndrawImage from '@/components/UndrawImage'
import ProjectTasks from '@/components/ProjectTasks'
import HomePage from '@/components/HomePage'

import ProjectsPage from '@/components/ProjectsPage'
import UsersPage from '@/components/UsersPage'
import ClientsPage from '@/components/ClientsPage'
import CompaniesPage from '@/components/CompaniesPage'
import TasksPage from '@/components/TasksPage'
import TagsPage from '@/components/TagsPage'

export default [
  { path: '/', component: HomePage, authLevel: 0, name: 'Home' },
  { path: '/:catchAll([a-zA-Z0-9]+)', component: UndrawImage, props: { icon: "page_not_found", text: 'Ошибка 404. Нет такой страницы' } },
  { path: '/login', component: LoginPage },
  { path: '/home', component: UndrawImage, props: { icon: "blank_canvas", text: 'Проект пока не выбран' }, authLevel: 1, name: 'My Projects' },
  { path: '/project/:id', component: ProjectTasks, authLevel: 9, name: 'My Projects ' },

  { path: '/projects', component: ProjectsPage, authLevel: 2, name: 'Projects' },
  { path: '/users', component: UsersPage, authLevel: 2, name: 'Users' },
  { path: '/clients', component: ClientsPage, authLevel: 2, name: 'Clients' },
  { path: '/companies', component: CompaniesPage, authLevel: 2, name: 'Companies' },
  { path: '/tasks', component: TasksPage, authLevel: 2, name: 'Tasks' },
  { path: '/tags', component: TagsPage, authLevel: 2, name: 'Tags' },
]
