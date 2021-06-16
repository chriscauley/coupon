import auth from '@unrest/vue-auth'
import UrVue from '@unrest/vue'
import form from '@unrest/form'
import '@unrest/tailwind/dist.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

auth.config.oauth_providers = ['github']

createApp(App)
  .use(router)
  .use(form.plugin)
  .use(auth.plugin)
  .use(UrVue.plugin)
  .use(UrVue.ui)
  .mount('#app')
