import Vue from 'vue'
import VueRouter from 'vue-router'
import ColumnReducer from '../views/ColumnReducer.vue'
import Landing from '../views/Landing.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/columnreducer',
    name: 'ColumnReducer',
    component: ColumnReducer
  },
  {
    path: '/',
    name: 'Landing',
    component: Landing
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
