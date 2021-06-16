import { createRouter, createWebHistory } from "vue-router";
import Unrest from "@unrest/vue";
import auth from "@unrest/vue-auth";
import views from "./views";

const { loadViews, applyMeta } = Unrest;

const routes = [...auth.routes, ...loadViews(views)];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(applyMeta);
router.beforeEach(() => {
  // refresh any api calls after navigation
});
export default router;
