
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { 'loginRequired': true },
    children: [
      { path: '', name: "FormHandler", component: () => import('pages/FormHandler.vue')},
    ]
  },

  {
    path: '/login',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: "Login", component: () => import('pages/LoginPage.vue') },
    ]
  },

  {
    path: '/error',
    component: () => import('pages/Error.vue'),
    props: route => ({'message': route.params.message})
  },

  {
    path: '/success',
    alias: '/failure',
    component: () => import('pages/FormPostResult.vue'),
  },

  
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
