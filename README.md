# 数据库业务报错智能诊断系统（AIOps）

面向 **GaussDB 信创环境**的已知报错根因诊断：输入一条报错（7 张历史错误/报警表的记录或粘贴文本），
自动输出 **"问题是什么 + 怎么解决 + 可复核的证据链"**。

诊断内核为**确定性规则引擎**（20 类 runbook + 查库取证），高频报错零 token 秒判。
HTTP 默认**纯规则、零 token、数据不出内网**；仅当调用方显式 `escalate=true` 且部署允许时，
未识别类型才走 LLM 长尾兜底（D1 方案 C）。全链路无 ML 组件、可解释、可审计，支持内网私有化交付。

---

## 一、整体链路（去 ML，默认纯规则 + 可选升级）

```
一条报错（错误表记录 / 自由文本）
  │
  ├─ 入口过滤（noise_rules 关键词 + is_tech_error()，取数链路无噪音）
  ├─ 规则引擎 20 类型识别（errors.yaml 关键词打分）
  ├─ runbook 只读查 GaussDB 取证（参数化 SELECT 诊断树）
  ├─ 决策
  │     默认（escalate=false）：规则快速路径，零 token，不检索 KB/LLM
  │     显式升级（escalate=true 且部署允许）：
  │        规则命中仍走零 token 快路径；仅类型未识别走 LLM 兜底（领域知识卡 + 规则取证证据）
  └─ 结构化报告：问题是什么 + 证据链 + 怎么解决 + 降级可见化
        规则加载期 fail-fast：启动即校验全部 SQL 表/列，错误拒绝启动
        部署未允许升级：escalate=true 返回 409
        LLM 运行时不可用：200 自动降级为规则结论/诚实兜底，source 标注来源
```

## 二、证据模型（三证合一，规则为最终准绳）

| 证据 | 来源 | 回答 |
|---|---|---|
| 现场查库（事实） | 规则引擎只读 SQL | 现在库里到底是什么状态（最终准绳） |
| 领域知识（机制手册） | Dimple 知识库诊断卡 | 根因分支、成立/反证、处置边界 |
| LLM 综合（兜底） | 仅显式升级且未识别类型 | 长尾报错的综合推断与排查方向 |

诊断结论**以现场查库事实为准**；知识库只读 SQL 默认不执行、标注"未现场核实"；
证据不足时如实给低置信度与排查方向，禁止臆测、禁止改库。

## 三、目录结构（单包 src 布局）

```
AIOps/
├── pyproject.toml             uv 工程；console 脚本 ai-ops（Python 3.12）
├── Dockerfile / docker-compose.yml / .env.example   私有化容器化交付
├── config/
│   ├── db.yaml.example / llm.yaml.example / kb.yaml.example   配置模板（入库）
│   └── db.yaml / llm.yaml / kb.yaml      真实配置（gitignore，含密钥不入库）
├── src/ai_ops/                唯一随 wheel 发布的 Python 包
│   ├── cli.py                 统一命令行入口（ai-ops）
│   ├── pipeline.py            诊断编排 + 决策（稳定契约 diagnose(rec)；含 telemetry 打标）
│   ├── telemetry.py           观测基线：路径统计 / LLM 降本率汇总
│   ├── service.py             业务逻辑层（取数 → 诊断 → 组装报告；供 CLI/API/页面复用）
│   ├── api.py                 FastAPI 薄壳（/healthz /v1/diagnose /v1/batch-diagnose /v1/records /v1/rules）
│   ├── reporting.py           报告渲染（混合 / 纯规则，含降级提示）
│   ├── contract.py            TypedDict 数据契约
│   ├── paths.py / config.py   路径解析（AIOPS_* 环境变量 > var/ > /app）/ YAML 配置 + 环境覆盖
│   ├── rules_store.py         规则包加载（包内基线 + AIOPS_RULES_DIR 外挂覆盖）
│   ├── evidence.py            知识卡中立格式化
│   ├── engine/                db(只读封装) / parser(骨架归一) / rule_engine(20类型)
│   │                            error_records(7 表取数) / schema_check(977 表清单校验)
│   ├── kb/                    Dimple 知识库适配（本地 BM25、门禁、降级）
│   ├── llm/                   OpenAI 兼容客户端 + 兜底提示词
│   ├── assets/rules/          规则包资产（随 wheel 打包）
│   │   ├── errors.yaml / noise_rules.yaml
│   │   └── runbooks/          20 份只读诊断树（rb_*.yaml）
│   └── ops/                   常驻自检：doctor / llm_probe / kb_selftest
├── scripts/                   工程脚本（coverage_scan 覆盖率扫描；不打包）
├── tests/                     unit / integration（52 项，离线可跑）
└── var/                       运行时资产（gitignore）：reports/
```

## 四、环境与配置

```powershell
uv sync                      # 安装内核依赖（uv 0.12+，Python 3.12）
uv sync --extra api          # API 服务（fastapi/uvicorn/pydantic）
uv sync --extra demo         # Streamlit 演示前脸（汇报/演示用，可选）
```

- 内核依赖仅 `py-opengauss`（GaussDB 驱动）+ `pyyaml`；无任何 ML 依赖、无模型文件。
- 配置文件（真实配置含密钥/口令，已 gitignore，仓库只提供 `.example`）：
  - `config/db.yaml`：GaussDB 只读连接；可用 `AIOPS_DB_USER/PASSWORD/HOST/PORT/DATABASE` 环境变量覆盖；
  - `config/llm.yaml`：由 `llm.yaml.example` 复制，填 `base_url/api_key/model`；
    `allow_escalation` 控制 HTTP 是否允许 LLM 升级（默认 false，可用 `AIOPS_LLM_ALLOW_ESCALATION` 覆盖）；
    未配置 LLM 时自动降级为纯规则；其余字段支持 `AIOPS_LLM_*` 覆盖；
  - `config/kb.yaml`：由 `kb.yaml.example` 复制，指向 Dimple 知识快照根目录。
- **多环境（dev/test/prod）**：同一代码，靠环境变量/配置挂载切换——本地开发用 `config/*.yaml` +
  `AIOPS_*` 覆盖；容器部署用 `.env` 注入（见 docker-compose.yml）。
- 规则热覆盖：设置 `AIOPS_RULES_DIR` 指向外挂目录（runbook 同名整体覆盖、
  errors.yaml 按 id 合并、noise 去重追加），详见 `docs/adr/0001-单包src布局与目录约定.md`。

## 五、快速开始

```powershell
$env:PYTHONIOENCODING="utf-8"

uv run python -m ai_ops.ops.doctor                         # 环境/资产/连通一键自检
uv run ai-ops --text "本地报单号没有递增!"                  # 自由文本诊断（规则快路）
uv run ai-ops --source ftr_err --date 20261030             # 按来源/日期取数诊断
uv run ai-ops --text "..." --force-llm                    # 强制 LLM 兜底
uv run ai-ops --rule --text "[合约=>Au9999]结算价不存在"     # 纯规则模式
uv run ai-ops --source ftr_err --date 20261030 --limit 500 # 批量回放（尾部输出降本率观测行）
uv run pytest                                              # 77 项单元 + 集成测试（离线可跑）

# API 服务（uvicorn 单进程起步）
uvicorn ai_ops.api:app --host 0.0.0.0 --port 8000
#   文档 http://127.0.0.1:8000/docs；健康自检 GET /healthz

# 覆盖率扫描（数据驱动补规则入口；连 GaussDB）
uv run python scripts/coverage_scan.py
```

## 六、实测效果（7 张历史表，GaussDB 实测）

- 全量 11,416,341 条历史报错/报警文本，规则关键词识别率 **≈99.98%**（11,413,612 条），
  仅约 2,700 条低频语义未覆盖（单类 ≤44 条）；
- 核心错误表：**ftr_err 99.6%**、**quote_err 99.5%**；报警类表 alarm/quote_alarm/rule_alarm **≈100%**；
- 规则命中的报错走快速路径**零 token**；HTTP 默认纯规则，仅显式 `escalate=true` 且部署允许时才可能产生 LLM 调用；
- 覆盖率口径：按 TOP5000 高频骨架 + 长尾表全量 SQL LIKE 复核（此前 TOP200 抽样会低估 alarm 表）。
- 离线回归基线：77/77 测试全绿（含 runbook 与 977 表结构一致性 fail-fast 防线）。

## 七、安全与私有化

- **只读三重约束**：数据库只读账号 + 代码层写拦截（禁 INSERT/UPDATE/DELETE/DDL）+ 规则 SQL 白名单与参数化绑定。
- **规则加载期 fail-fast**：启动即校验每条取证 SQL 的表/列，错误拒绝启动（清单缺失时降级 warning，不阻断容器交付）。
- **知识库只读 SQL 默认不自动执行**：经人工审核并派生为 runbook 后才由规则引擎执行。
- **数据不出网**：HTTP 默认纯规则零 token；LLM 仅在显式升级且部署允许时调用，内网私有化部署（OpenAI 兼容接口）；知识库本地 BM25、纯标准库、离线。
- **可降级**：LLM、知识库任一缺失都不阻断主流程（200 优雅降级），降级原因在 `source`/报告/页面显式可见。
- **可审计**：报告逐步标注由 规则/知识库/LLM 完成，LLM 结论附证据；未允许升级时 `escalate=true` 返回 409。

## 八、产品形态（规划）

私有化内网 **Web 诊断工作台**（Streamlit 演示壳）+ 诊断 API（FastAPI）；业务存储 MySQL 8。
当前已落地：CLI 诊断内核 + FastAPI 服务（5 端点 + 契约测试）+ 容器化交付材料；
前端重做/监控平台与 IM 集成按工程推进方案顺序执行。

## 九、文档（`docs/`）

- 《AIOps工程推进方案-服务化与增强》——**当前主线**：阶段划分、进度表、执行顺序
- 《整体技术架构设计文档》——目标态系统总纲（分层、模块接口、数据模型、部署、技术决策）
- 《产品形态设计文档-私有化内网Web工作台》——产品形态、功能模块、部署与技术栈
- 《AIOps_GaussDB迁移_最优方案》——信创迁移方案与决策
- 《知识库集成说明》——Dimple 知识库接入、配置、安全边界、验证
- 《工程改造与未来方案-面向私有化交付》——私有化交付路线
- `adr/0001-单包src布局与目录约定.md`——结构决策与目录约定
- `error/GaussDB_dimple_全量表结构与字段含义清单.md`——977 表清单（fail-fast 校验的事实源）

## 十、如何新增一类报错

- **高频类型**：在 `src/ai_ops/assets/rules/runbooks/` 增加一份只读诊断树 YAML（`errors.yaml` 注册
  type + keywords），引擎不动；发布期可用 `AIOPS_RULES_DIR` 外挂覆盖，不必重新打包。
  也可从知识库诊断卡派生只读 SQL 模板，经专家审核后固化。
- **先观测再补**：跑 `coverage_scan.py` 看未覆盖高频骨架——若语义已被现有类型覆盖，补关键词即可
  （零新增 runbook）；确属新语义再写 runbook（取证逻辑需业务确认）。
- **未见类型**：显式升级走 LLM 兜底，并回流到开发侧补规则，形成数据驱动飞轮。
