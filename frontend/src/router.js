import { createRouter, createWebHistory } from 'vue-router';
import ManageCase from './views/ManageCase.vue';
import UploadCase from './views/UploadCase.vue';
import AiGenerateCase from './views/AiGenerateCase.vue';

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
  },
  {
    path: '/ai-generate',
    name: 'AiGenerateCase',
    component: AiGenerateCase
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;