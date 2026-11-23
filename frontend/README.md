# AIOps 前端（Vue 3 + TypeScript + Vite）

面向银行内网的报错智能诊断工作台，替代原 Streamlit 演示页，通过 REST 对接 FastAPI 后端。

## 技术栈

Vue 3、TypeScript、Vite、Vue Router、Pinia、Ant Design Vue、ECharts、Axios。

## 本地开发

使用 Node.js 24（版本见仓库根目录 `.nvmrc`）。

```bash
npm ci
# 需先在本地启动后端：uvicorn ai_ops.api:app --port 8000
npm run dev
```

开发服务器默认运行在 http://localhost:5173 ，`/v1`、`/healthz` 已在 `vite.config.ts` 代理到 `127.0.0.1:8000`。

## 质量检查与构建

```bash
npm run lint           # ESLint，警告也会失败
npm run test:coverage  # Vitest + 全源码覆盖率门禁
npm run build          # 类型检查 + 产物输出到 dist/
```

将 `dist/` 交由 Nginx 托管，配置示例见 `deploy/nginx.conf`；Nginx 同时反向代理 `/v1`、`/healthz` 到 FastAPI。所有依赖与字体均本地化，不引用外网 CDN，满足银行内网离线交付。

## 目录

```
src/
├─ api/          # Axios 封装与接口调用
├─ components/   # 结果卡片、图表等通用组件
├─ constants/    # 错误来源等常量
├─ layouts/      # 整体布局
├─ router/       # 路由
├─ stores/       # Pinia 状态
├─ types/        # 契约类型
└─ views/        # 单条诊断 / 批量回放 / 管理看板
```
