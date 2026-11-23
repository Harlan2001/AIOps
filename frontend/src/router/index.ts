import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    { path: '/', redirect: '/dashboard' },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/dashboard/DashboardView.vue'),
      meta: { title: '运维总览' },
    },
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
      path: '/realtime',
      name: 'realtime',
      component: () => import('@/views/realtime/RealtimeView.vue'),
      meta: { title: '实时异常' },
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/history/HistoryView.vue'),
      meta: { title: '历史诊断' },
    },
    {
      path: '/route-error',
      name: 'route-error',
      component: () => import('@/views/system/NotFoundView.vue'),
      meta: { title: '页面加载失败' },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/system/NotFoundView.vue'),
      meta: { title: '页面不存在' },
    },
  ],
})

router.afterEach((to) => {
  document.title = `${String(to.meta.title ?? '工作台')} · DIMPLE AIOps`
})

router.onError(() => {
  if (router.currentRoute.value.name !== 'route-error') {
    void router.replace({ name: 'route-error' })
  }
})

export default router
