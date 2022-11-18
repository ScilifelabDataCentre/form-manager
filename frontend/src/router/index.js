import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useUserStore } from 'stores/user'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach((to, from, next) => {
    const store = useUserStore();
    if (!store.loaded) {
      store.getUserInfo()
        .then(function () {
	  if (store.email === '') {
	    if (to.meta.loginRequired)
	      next({name: 'Login'})
	    else
	      next()
	  }
	  else if (to.name === 'Login')
	    next({name: 'FormBrowser'})
	  else
	    next()
	})
        .catch(() => next({name: 'Error', params: {message: 'Unable to get response from backend'}}));
    }
    else {
      if (store.email === '') {
	if (to.meta.loginRequired)
	  next({name: 'Login'})
	else
	  next()
      }
      else if (to.name === 'Login')
	next({name: 'FormBrowser'})
      else
	next()
    }
  })

  return Router
})
