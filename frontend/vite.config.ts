import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

// 开发期 /v1、/healthz 代理到本地 FastAPI；可用 AIOPS_API_TARGET 避免本机端口冲突。
const apiTarget = process.env.AIOPS_API_TARGET ?? 'http://127.0.0.1:8000'

// 生产由 Nginx 反代，不读取此开发代理地址。
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/v1': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/healthz': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      reportsDirectory: './coverage',
      include: ['src/**/*.{ts,vue}'],
      exclude: ['src/**/*.spec.ts', 'src/env.d.ts'],
      // 干净安装的全源码基线约为 9% lines/statements；首版仅用于防止退化。
      // 补齐页面与组件测试后逐步提高，不通过缩小 include 范围抬高覆盖率。
      thresholds: {
        lines: 8,
        statements: 8,
        branches: 50,
        functions: 30,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    chunkSizeWarningLimit: 900,
    rollupOptions: {
      output: {
        // 第三方依赖拆分为独立 chunk，利于浏览器缓存与按需加载
        manualChunks: {
          vue: ['vue', 'vue-router', 'pinia'],
          antd: ['ant-design-vue', '@ant-design/icons-vue'],
          echarts: ['echarts'],
        },
      },
    },
  },
})
