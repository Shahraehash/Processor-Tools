import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
import ColumnReducer from '../views/ColumnReducer.vue'
import TrainTestSplit from '../views/TrainTestSplit.vue'
import Colinearity from '../views/Colinearity.vue'
import FeatureSelector from '../views/FeatureSelector.vue'
import Encoder from '../views/Encoder.vue'
import Diagnostics from '../views/Diagnostics.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/columnreducer',
    name: 'ColumnReducer',
    component: ColumnReducer
  },
  {
    path: '/colinearity',
    name: 'Colinearity',
    component: Colinearity
  },
  {
    path: '/featureselector',
    name: 'FeatureSelector',
    component: FeatureSelector
  },
  {
    path: '/traintestsplit',
    name: 'TrainTestSplit',
    component: TrainTestSplit
  },
  {
    path: '/encoder',
    name: 'Encoder',
    component: Encoder
  },
  {
    path: '/',
    name: 'Landing',
    component: Landing
  },
  {
    path: '/diagnostics',
    name: 'Diagnostics',
    component: Diagnostics
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
