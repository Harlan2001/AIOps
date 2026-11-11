# DIMPLE AIOps 诊断服务镜像（FastAPI 薄封装：规则引擎 + 查库取证 + LLM 长尾兜底，无 ML）
#
# 构建：docker build -t aiops:0.1.0 .
# 运行：docker run --rm -p 8000:8000 \
#         -v "$PWD/config:/app/config:ro" \
#         -e AIOPS_DB_HOST=db -e AIOPS_DB_PORT=5432 \
#         -e AIOPS_DB_DATABASE=dimple -e AIOPS_DB_USER=... -e AIOPS_DB_PASSWORD=... \
#         aiops:0.1.0
# 多环境：dev/test/prod 用同一镜像，仅环境变量/挂载配置不同（见 docker-compose.yml）。
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PYTHONIOENCODING=utf-8

# 依赖锁文件 + 工程元数据先行（利用层缓存）
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
# 仅拷贝配置模板；真实配置（含密钥）由挂载/环境变量注入，绝不打进镜像
COPY config/*.example ./config/

RUN uv sync --frozen --no-dev --extra api

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

# 存活 + 规则加载自检（对应 GET /healthz）
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)" || exit 1

CMD ["uvicorn", "ai_ops.api:app", "--host", "0.0.0.0", "--port", "8000"]
