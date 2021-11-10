import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)
//import VueSocketIO from 'vue-socket.io'

Vue.config.productionTip = false


// Vue.use(new VueSocketIO({
//     debug: true,
//     connection: 'http://127.0.0.1:5000/',
//     vuex: {
//         store,
//         actionPrefix: 'SOCKET_',
//         mutationPrefix: 'SOCKET_'
//     },
//     // options: { path: "/my-app/" } //Optional options
// }))


new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

// this.sockets.subscribe('test', (data) => {
//     console.log(data)
// });
