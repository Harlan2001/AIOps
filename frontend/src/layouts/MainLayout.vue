<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  DashboardOutlined,
  HistoryOutlined,
  MedicineBoxOutlined,
  MenuFoldOutlined,
  MenuOutlined,
  MenuUnfoldOutlined,
  MonitorOutlined,
  ReloadOutlined,
  TableOutlined,
} from '@ant-design/icons-vue'

import { useHealthStore } from '@/stores/health'

const route = useRoute()
const router = useRouter()
const health = useHealthStore()

const selectedKeys = computed(() => [route.name as string])
const collapsed = ref(false)
const mobileOpen = ref(false)

const badgeStatus = computed<'processing' | 'success' | 'warning' | 'error'>(() => {
  if (health.loading && !health.data) return 'processing'
  if (health.error || !health.data) return 'error'
  return health.isDegraded ? 'warning' : 'success'
})

const badgeText = computed(() => {
  if (health.loading && !health.data) return '检查服务状态'
  if (health.error) return '健康检查失败'
  if (!health.data) return '状态未知'
  return health.isDegraded ? '服务降级' : '服务正常'
})

const menuItems = [
  { key: 'dashboard', icon: DashboardOutlined, label: '运维总览' },
  { key: 'diagnose', icon: MedicineBoxOutlined, label: '单条诊断' },
  { key: 'batch', icon: TableOutlined, label: '批量回放' },
  { key: 'realtime', icon: MonitorOutlined, label: '实时异常' },
  { key: 'history', icon: HistoryOutlined, label: '历史诊断' },
]

function onMenuClick({ key }: { key: string }) {
  mobileOpen.value = false
  if (route.name !== key) void router.push({ name: key })
}

function formatHealthTime(value?: string) {
  if (!value) return '—'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('zh-CN', { hour12: false })
}

const POLL_INTERVAL = 30000
let timer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  void health.refresh()
  timer = setInterval(() => void health.refresh(), POLL_INTERVAL)
})

watch(
  () => route.name,
  () => {
    mobileOpen.value = false
    void health.refresh()
  },
)

onBeforeUnmount(() => {
  if (timer !== null) clearInterval(timer)
})
</script>

<template>
  <a class="skip-link" href="#main-content">跳转到主要内容</a>
  <a-layout class="app-layout">
    <a-sider
      v-model:collapsed="collapsed"
      :width="232"
      :collapsed-width="76"
      :trigger="null"
      class="desktop-sider"
      theme="light"
    >
      <div class="brand" :class="{ 'brand-collapsed': collapsed }">
        <img class="brand-mark" src="/favicon.svg" alt="" />
        <div v-if="!collapsed" class="brand-text">
          <strong>DIMPLE AIOps</strong>
          <span>智能诊断工作台</span>
        </div>
      </div>
      <a-menu
        mode="inline"
        :selected-keys="selectedKeys"
        class="app-menu"
        @click="onMenuClick"
      >
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <component :is="item.icon" />
          <span>{{ item.label }}</span>
        </a-menu-item>
      </a-menu>
      <div v-if="!collapsed" class="sider-note">
        <span class="note-dot" />
        规则优先 · 按需智能升级
      </div>
    </a-sider>

    <a-layout class="workspace-layout">
      <a-header class="app-header">
        <div class="header-context">
          <a-button
            type="text"
            class="desktop-toggle"
            :aria-label="collapsed ? '展开侧栏' : '收起侧栏'"
            @click="collapsed = !collapsed"
          >
            <MenuUnfoldOutlined v-if="collapsed" />
            <MenuFoldOutlined v-else />
          </a-button>
          <a-button
            type="text"
            class="mobile-toggle"
            aria-label="打开导航"
            @click="mobileOpen = true"
          >
            <MenuOutlined />
          </a-button>
          <span class="workspace-name">智能诊断工作台</span>
        </div>

        <a-popover placement="bottomRight" trigger="click" overlay-class-name="health-popover">
          <template #title>服务健康详情</template>
          <template #content>
            <dl class="health-details">
              <div><dt>GaussDB</dt><dd>{{ health.data?.gauss.msg || health.error || '暂无信息' }}</dd></div>
              <div><dt>规则数量</dt><dd>{{ health.data?.rules_count ?? '—' }}</dd></div>
              <div><dt>噪音关键词</dt><dd>{{ health.data?.noise_keywords ?? '—' }}</dd></div>
              <div><dt>服务时间</dt><dd>{{ formatHealthTime(health.data?.time) }}</dd></div>
            </dl>
            <a-button size="small" :loading="health.loading" @click="health.refresh">
              <ReloadOutlined /> 重新检查
            </a-button>
          </template>
          <button type="button" class="health-button" aria-label="查看服务健康详情">
            <a-badge :status="badgeStatus" :text="badgeText" />
          </button>
        </a-popover>
      </a-header>

      <a-content class="app-content">
        <main id="main-content" class="page-shell" tabindex="-1">
          <router-view v-slot="{ Component }">
            <transition name="page" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </main>
      </a-content>
    </a-layout>
  </a-layout>

  <a-drawer
    v-model:open="mobileOpen"
    placement="left"
    :width="280"
    :closable="false"
    class="mobile-nav-drawer"
  >
    <div class="brand mobile-brand">
      <img class="brand-mark" src="/favicon.svg" alt="" />
      <div class="brand-text">
        <strong>DIMPLE AIOps</strong>
        <span>智能诊断工作台</span>
      </div>
    </div>
    <a-menu mode="inline" :selected-keys="selectedKeys" class="app-menu" @click="onMenuClick">
      <a-menu-item v-for="item in menuItems" :key="item.key">
        <component :is="item.icon" />
        <span>{{ item.label }}</span>
      </a-menu-item>
    </a-menu>
  </a-drawer>
</template>

<style scoped>
.skip-link {
  position: fixed;
  top: 8px;
  left: 8px;
  z-index: 2000;
  padding: 10px 16px;
  color: #fff;
  background: var(--brand-hover);
  border-radius: 8px;
  transform: translateY(-160%);
}

.skip-link:focus {
  transform: translateY(0);
}

.app-layout {
  display: flex;
  width: 100%;
  min-height: 100vh;
  flex-direction: row;
  background: var(--page-bg);
}

.desktop-sider {
  position: sticky !important;
  top: 0;
  z-index: 30;
  height: 100vh;
  overflow: hidden;
  border-right: 1px solid var(--border-soft);
  box-shadow: 2px 0 12px rgba(23, 32, 51, 0.025);
}

.brand {
  display: flex;
  height: 80px;
  padding: 16px 20px;
  gap: 11px;
  align-items: center;
}

.brand-collapsed {
  padding-inline: 20px;
  justify-content: center;
}

.brand-mark {
  width: 36px;
  height: 36px;
  flex: none;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(42, 120, 214, 0.18);
}

.brand-text {
  display: flex;
  min-width: 0;
  flex-direction: column;
  line-height: 1.25;
}

.brand-text strong {
  color: var(--text-primary);
  font-size: 15px;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.brand-text span {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: 12px;
  white-space: nowrap;
}

.app-menu {
  padding-top: 8px;
  border-inline-end: 0 !important;
}

.app-menu :deep(.ant-menu-item) {
  height: 44px;
  margin-block: 5px;
  line-height: 44px;
}

.app-menu :deep(.ant-menu-item-selected) {
  color: var(--brand-hover);
  background: var(--brand-soft);
  font-weight: 600;
}

.app-menu :deep(.ant-menu-item-selected::after) {
  position: absolute;
  top: 12px;
  right: 0;
  width: 3px;
  height: 20px;
  background: var(--brand);
  border-radius: 3px 0 0 3px;
  content: '';
}

.sider-note {
  position: absolute;
  right: 18px;
  bottom: 24px;
  left: 24px;
  display: flex;
  gap: 7px;
  align-items: center;
  color: var(--text-muted);
  font-size: 11px;
  white-space: nowrap;
}

.note-dot {
  width: 6px;
  height: 6px;
  background: var(--brand);
  border-radius: 50%;
}

.workspace-layout {
  width: 0;
  min-width: 0;
  flex: 1 1 auto;
  background: var(--page-bg);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  height: 64px;
  padding: 0 24px;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-soft);
  line-height: normal;
}

.header-context {
  display: flex;
  gap: 8px;
  align-items: center;
}

.workspace-name {
  margin-left: 4px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.mobile-toggle {
  display: none;
}

.health-button {
  padding: 8px 10px;
  color: var(--text-secondary);
  background: transparent;
  border: 0;
  border-radius: 8px;
  cursor: pointer;
}

.health-button:hover {
  background: var(--surface-subtle);
}

.health-details {
  width: min(340px, 72vw);
  margin: 0 0 12px;
}

.health-details > div {
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  gap: 12px;
  padding: 6px 0;
}

.health-details dt {
  color: var(--text-muted);
}

.health-details dd {
  margin: 0;
  color: var(--text-primary);
  overflow-wrap: anywhere;
}

.app-content {
  min-width: 0;
  padding: 28px;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 140ms ease, transform 140ms ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.page-leave-to {
  opacity: 0;
}

@media (max-width: 992px) {
  .desktop-sider,
  .desktop-toggle {
    display: none !important;
  }

  .mobile-toggle {
    display: inline-flex;
  }

  .app-header {
    height: 60px;
    padding-inline: 16px;
  }

  .app-content {
    padding: 20px;
  }
}

@media (max-width: 640px) {
  .workspace-name {
    display: none;
  }

  .app-content {
    padding: 16px;
  }

  .health-button {
    padding-inline: 4px;
  }
}
</style>

<style>
.mobile-nav-drawer .ant-drawer-body {
  padding: 0;
}

.mobile-nav-drawer .mobile-brand {
  border-bottom: 1px solid var(--border-soft);
}

.health-popover .ant-popover-inner-content {
  padding: 16px;
}
</style>
