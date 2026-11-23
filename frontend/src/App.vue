<script setup lang="ts">
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import MainLayout from '@/layouts/MainLayout.vue'

const theme = {
  token: {
    colorPrimary: '#2a78d6',
    colorInfo: '#2a78d6',
    colorSuccess: '#237804',
    colorWarning: '#ad6800',
    colorError: '#c93535',
    colorText: '#172033',
    colorTextSecondary: '#566174',
    colorBgLayout: '#f5f7fb',
    colorBorder: '#d9e0ea',
    colorBorderSecondary: '#e8edf3',
    borderRadius: 8,
    controlHeight: 38,
    fontSize: 14,
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif",
  },
  components: {
    Button: { borderRadius: 8, fontWeight: 500 },
    Card: { borderRadiusLG: 12 },
    Menu: { itemBorderRadius: 8, itemMarginInline: 12 },
    Table: { headerBg: '#f8fafc', headerColor: '#465164' },
    Layout: { headerBg: '#ffffff', siderBg: '#ffffff' },
  },
}
</script>

<template>
  <a-config-provider :locale="zhCN" :theme="theme">
    <MainLayout />
  </a-config-provider>
</template>
