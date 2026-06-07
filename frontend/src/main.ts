import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Search from './views/Search.vue'
import SkillDetail from './views/SkillDetail.vue'
import Publish from './views/Publish.vue'
import './assets/styles/base.css'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/search', name: 'search', component: Search },
  { path: '/skills/:name', name: 'skill-detail', component: SkillDetail, props: true },
  { path: '/publish', name: 'publish', component: Publish },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

const app = createApp(App)
app.use(router)
app.mount('#app')
