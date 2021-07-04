import auth from '@unrest/vue-auth'
import UrVue from '@unrest/vue'
import form from '@unrest/vue-form'
import '@unrest/tailwind/dist.css'

import AddChannel from '@/components/AddChannel'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './styles/base.scss'

auth.config.oauth_providers = ['github', 'google-oauth2']

createApp(App)
  .component('AddChannel', AddChannel)
  .use(router)
  .use(form.plugin)
  .use(auth.plugin)
  .use(UrVue.plugin)
  .use(store)
  .use(UrVue.ui)
  .mount('#app')
