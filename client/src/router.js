import { createRouter, createWebHistory, createMemoryHistory } from 'vue-router';
import { loadViews, applyMeta } from '@unrest/vue';
import auth from '@unrest/vue-auth';
import views from './views';

const routes = [
  ...auth.routes,
  ...loadViews(views),
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(applyMeta)
router.beforeEach(() => {
  // refresh any api calls after navigation 
})
export default router
