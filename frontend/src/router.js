import { createRouter, createWebHistory } from 'vue-router';
import ManageCase from './views/ManageCase.vue';
import UploadCase from './views/UploadCase.vue';

const routes = [
  {
    path: '/',
    redirect: '/manage'
  },
  {
    path: '/manage',
    name: 'ManageCase',
    component: ManageCase
  },
  {
    path: '/upload',
    name: 'UploadCase',
    component: UploadCase
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;