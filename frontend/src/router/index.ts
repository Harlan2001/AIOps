import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    { path: '/', redirect: '/diagnose' },
    {
      path: '/diagnose',
      name: 'diagnose',
      component: () => import('@/views/diagnose/DiagnoseView.vue'),
      meta: { title: '单条诊断' },
    },
    {
      path: '/batch',
      name: 'batch',
      component: () => import('@/views/batch/BatchView.vue'),
      meta: { title: '批量回放' },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/dashboard/DashboardView.vue'),
      meta: { title: '管理看板' },
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/history/HistoryView.vue'),
      meta: { title: '历史诊断' },
    },
    {
      path: '/realtime',
      name: 'realtime',
      component: () => import('@/views/realtime/RealtimeView.vue'),
      meta: { title: '实时监控' },
    },
  ],
})

export default router
