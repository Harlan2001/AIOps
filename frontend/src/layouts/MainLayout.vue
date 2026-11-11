<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  DashboardOutlined,
  MedicineBoxOutlined,
  TableOutlined,
} from '@ant-design/icons-vue'

import { useHealthStore } from '@/stores/health'

const route = useRoute()
const router = useRouter()
const health = useHealthStore()

const selectedKeys = computed(() => [route.name as string])

const menuItems = [
  { key: 'diagnose', icon: MedicineBoxOutlined, label: '单条诊断' },
  { key: 'batch', icon: TableOutlined, label: '批量回放' },
  { key: 'dashboard', icon: DashboardOutlined, label: '管理看板' },
]

function onMenuClick({ key }: { key: string }) {
  router.push({ name: key })
}

onMounted(() => {
  health.refresh()
})
</script>

<template>
  <a-layout class="app-layout">
    <a-sider breakpoint="lg" collapsible>
      <div class="logo">DIMPLE AIOps</div>
      <a-menu
        theme="dark"
        mode="inline"
        :selected-keys="selectedKeys"
        @click="onMenuClick"
      >
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <component :is="item.icon" />
          <span>{{ item.label }}</span>
        </a-menu-item>
      </a-menu>
    </a-sider>

    <a-layout>
      <a-header class="app-header">
        <span class="page-title">{{ route.meta.title }}</span>
        <a-badge
          :status="health.isDegraded ? 'warning' : 'success'"
          :text="health.isDegraded ? '服务降级' : '服务正常'"
        />
      </a-header>
      <a-content class="app-content">
        <router-view />
      </a-content>
    </a-layout>
  </a-layout>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.logo {
  height: 48px;
  margin: 16px;
  color: #fff;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 1px;
}

.app-header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
}

.app-content {
  margin: 24px;
}
</style>
