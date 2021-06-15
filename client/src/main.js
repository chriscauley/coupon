import auth from '@unrest/vue-auth'
import UrVue, { ui } from '@unrest/vue'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App)
  .use(router)
  .use(auth.plugin)
  .use(UrVue)
  .use(ui)
  .mount('#app')
