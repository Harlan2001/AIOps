<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isRouteError = computed(() => route.name === 'route-error')
</script>

<template>
  <div class="page-shell">
    <a-result
      :status="isRouteError ? '500' : '404'"
      :title="isRouteError ? '页面加载失败' : '没有找到这个页面'"
      :sub-title="isRouteError ? '页面资源暂时无法加载，请稍后重试。' : '地址可能已失效，请返回运维总览继续工作。'"
    >
      <template #extra>
        <a-button type="primary" @click="$router.push('/dashboard')">返回运维总览</a-button>
        <a-button v-if="isRouteError" @click="$router.go(0)">重新加载</a-button>
      </template>
    </a-result>
  </div>
</template>
