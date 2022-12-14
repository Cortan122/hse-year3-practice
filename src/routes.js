const LoginPage = () => import('@/components/LoginPage')
const UndrawImage = () => import('@/components/UndrawImage')
const ProjectTasks = () => import('@/components/ProjectTasks')
const HomePage = () => import('@/components/HomePage')
const BasicChart = () => import('@/components/BasicChart')
const PieCharts = () => import('@/components/PieCharts')

const ProjectsPage = () => import('@/components/ProjectsPage')
const UsersPage = () => import('@/components/UsersPage')
const ClientsPage = () => import('@/components/ClientsPage')
const CompaniesPage = () => import('@/components/CompaniesPage')
const TasksPage = () => import('@/components/TasksPage')
const TagsPage = () => import('@/components/TagsPage')

export default [
  { path: '/', component: HomePage, authLevel: 0, name: 'Home' },
  { path: '/:catchAll([a-zA-Z0-9]+)', component: UndrawImage, props: { icon: "page_not_found", text: 'Ошибка 404. Нет такой страницы' } },
  { path: '/login', component: LoginPage },
  { path: '/home', component: UndrawImage, props: { icon: "blank_canvas", text: 'Проект пока не выбран' }, authLevel: 1, name: 'My Projects' },
  { path: '/project/:id', component: ProjectTasks, authLevel: 9, name: 'My Projects ' },
  { path: '/stats', component: BasicChart, authLevel: 1, name: 'Stats' },
  { path: '/stats/users/:id', component: PieCharts, authLevel: 9, name: 'Stats ', props: {
    url: '/api/stats/users', titletmpl: 'Графики пользователя', nametmpl: 'Пользователь' } },
  { path: '/stats/projects/:id', component: PieCharts, authLevel: 9, name: 'Stats  ', props: {
    url: '/api/stats/projects', titletmpl: 'Графики проекта', nametmpl: 'Проект' } },

  { path: '/projects', component: ProjectsPage, authLevel: 2, name: 'Projects' },
  { path: '/users', component: UsersPage, authLevel: 2, name: 'Users' },
  { path: '/clients', component: ClientsPage, authLevel: 2, name: 'Clients' },
  { path: '/companies', component: CompaniesPage, authLevel: 2, name: 'Companies' },
  { path: '/tasks', component: TasksPage, authLevel: 2, name: 'Tasks' },
  { path: '/tags', component: TagsPage, authLevel: 2, name: 'Tags' },
]
