import { createApp } from 'vue'
import './style.css'
import './Style1.css'
// import './Script.js'
import App from './App.vue'
// import { createPinia } from 'pinia'
import { router } from './routes.js'
createApp(App).use(router).mount('#app')


