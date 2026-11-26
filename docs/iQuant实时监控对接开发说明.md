# iQuant 实时监控对接开发说明

按 Dimple 实时监控的「接口级拉模式」同构实现，对接 55 环境 iQuant 固收量化系统的
**事中风控事件（日间异常风控事件 DayAbnormalRiskEvent）**，单接口覆盖 7 类风控项。
默认关闭，启用后由进程内 APScheduler 定时增量拉取，复用诊断内核自动诊断并 best-effort 落库。

## 一、模块结构

| 文件 | 职责 |
| --- | --- |
| `src/ai_ops/iquant/client.py` | `IquantClient`：明文登录、token 缓存/刷新、分页查询，纯标准库 urllib |
| `src/ai_ops/iquant/collector.py` | 端点注册表、字段映射、嵌套 JSON 解析、游标幂等、调度入口 `run_realtime_collection` |
| `src/ai_ops/iquant/__init__.py` | 包导出 |
| `config/iquant.yaml.example` | 配置模板（真实 `iquant.yaml` 不入库） |
| `tests/unit/test_iquant_client.py` | 客户端单测（8 项） |
| `tests/unit/test_iquant_collector.py` | 采集器单测（11 项） |

统一实时页（前端 + 查询接口）改造文件：

| 文件 | 职责 |
| --- | --- |
| `src/ai_ops/store/diag_repo.py` | 新增 `_realtime_cond()` 与 `list_logs(realtime_only=...)`，匹配 `dimple_` 或 `iquant_` 前缀；列表排序改为按业务日期倒序（最新在前） |
| `src/ai_ops/api.py` | `/v1/diagnoses` 新增 `realtime_only` 查询参数并透传（保留 `dimple_only` 向后兼容） |
| `frontend/src/api/realtime.ts` | 实时请求由写死 `dimple_only` 改为 `realtime_only` |
| `frontend/src/api/diagnoses.ts` | 参数类型新增 `realtime_only` |
| `frontend/src/constants/sources.ts` | `REALTIME_SOURCE_LABELS` 增加 `iquant_day_abnormal_event` 标签 |
| `frontend/src/views/realtime/RealtimeView.vue` | 标题/描述/空状态/下拉 placeholder 通用化，来源下拉同时含 Dimple 与 iQuant |

诊断置信度增强（iQuant 专用规则）改造文件：

| 文件 | 职责 |
| --- | --- |
| `assets/rules/iquant_errors.yaml` | 7 类 iQuant 专用类型注册，标记 `self_evidence` 与精确中文关键词（不写死置信度） |
| `assets/rules/runbooks/rb_iquant_*.yaml` | 7 个自带证据 runbook，无业务 SQL，基于事件自带字段给参数化根因与处置建议 |
| `rules_store.py` | `load_registries` 合并加载 `iquant_errors.yaml`（支持外挂覆盖） |
| `engine/rule_engine.py` | `self_evidence` 类型置 `primary_evidence_ok=True`，不再输出写死置信度 |
| `engine/parser.py` | `ERROR_KW` 增加“告警”，iQuant 事件分类由 other 修正为 biz |
| `service.py` / `pipeline.py` | 统一调用 `pipeline.rule_confidence`，与 Dimple 同构 |
| `tests/unit/test_iquant_rules.py` | 类型注册、自带证据、精确分类与真实置信度档位单测（5 项） |

## 二、与 Dimple 的关键差异（均经实测）

| 维度 | Dimple | iQuant |
| --- | --- | --- |
| 登录密码 | RSA 公钥加密 + 密码反转 | **明文**提交，不调公钥、不加密 |
| 登录/业务成功码 | 000000 | 登录 000000，业务 **200000** |
| 分页请求体 | 扁平 `{pageNo,pageSize,...}` | `{pageNo,pageSize,data:{筛选条件}}` |
| 记录列表/总数 | `records` / `pages` | 顶层 **`data`** / `total`（无 pages，按 total 算页） |
| 时间格式 | 多为日期/时间戳 | ISO 字符串（`2026-11-20T09:25:48.377`）→ 业务日期 `20261120` |
| 增量指纹 | 纳入文本 | **只基于稳定主键 eventId**（事件会随 triggerCount 更新，纳入文本会重复诊断） |

- 嵌套 JSON 字符串 `triggerValue` / `thresholdValue` / `controlAction` 二次解析，
  原始字段保留、解析结果以 `*Parsed` 字段并存。
- 默认只诊断未闭环事件（`NEW` / `NOTIFIED`）；`HANDLED` / `IGNORED` 标记指纹后跳过，
  可由 `handle_closed: true` 放开。
- 落库由 `DiagnosticService` 内部按 `trigger_type=scheduled` 自动 upsert，
  采集器不直接写库；iQuant 来源不加入 `BUSINESS_SOURCES`，保证「仅真实异常」查询不被错误排除。

## 三、启用步骤

1. 复制配置并填写（口令建议走环境变量）：
   ```
   copy config\iquant.yaml.example config\iquant.yaml
   ```
2. 将 `enabled` 置为 `true`，确认 `base_url` / 账号 / 口令。
   也可用 `AIOPS_IQUANT_*` 环境变量覆盖（见 `.env.example`）。
3. 重启服务，FastAPI 启动时自动注册 `iquant_realtime` 定时任务，
   按 `interval_minutes`（默认 5 分钟）准实时采集。
4. 前端重新构建并部署（前端独立部署，非后端挂载）：
   在 `frontend/` 下执行 `npm run build`，用新 `dist/` 替换部署；
   若本地用 `npm run dev` 开发则热更新自动生效。
   之后「实时异常」页即可同时查看 Dimple 与 iQuant，来源下拉含「iQuant 事中风控事件」。

## 四、验证结果

- 后端全量单元测试 **164 项全部通过**（含 iquant 模块、iQuant 规则 5 项、实时来源过滤新增项），无回归。
- 前端单元测试 **22 项全部通过**，`vue-tsc` 类型检查通过。
- 真实 55 环境冒烟通过：明文登录拿到 token，`queryTable` 返回 200000、total 935，
  字段映射、嵌套 JSON 解析、中文文本渲染均正确。
- 真实端到端验证：**926 条未闭环 iQuant 事件已全部落库**；
  `realtime_only` 能查到 iQuant 记录（total 926），旧 `dimple_only` 对照返回 0，
  统一实时来源合计 1261 条（Dimple + iQuant）。
- 排序验证：列表改为 `ORDER BY business_date DESC NULLS LAST, created_at DESC, id DESC`，
  真实数据最前为最新业务日期 20261120，其后 20261119，严格按业务时间倒序；无业务日期的手工记录置末。
- 置信度验证：重算后 926 条全部 `class=biz`、`match_kind=keyword`、`confidence=1.0`，
  7 个专用类型与 riskItem 精确对应，无未识别、无 fuzzy 误路由（改造前 829 条未识别、95 条 fuzzy 误路由，置信度多为 0.4）。

## 五、诊断置信度机制（与 Dimple 完全同构，不写死）

**问题**：iQuant 事件最初大量落到「未识别类型 / other」，置信度仅 0.4；少量被字符 bigram 的 fuzzy
兜底错误路由到 Dimple 类型（头寸波动→净头寸告警、批量点击→自成交），且 Dimple runbook 的 SQL
依赖其业务库表与参数，iQuant 事件没有这些字段，主检查无法取证，置信度仍为 0.4。

**统一规则**：iQuant 事件是上游风控系统已判定、证据（命中值 `triggerValue`、阈值 `thresholdValue`、
管控动作 `controlAction`、风险级别、触发次数）自带的离散告警，无需也无法用 Dimple 业务库 SQL
反查根因。因此为 7 类 riskItem 各注册一个 `self_evidence: true` 的专用类型，并由统一函数
`pipeline.rule_confidence(rule_res)` 决定置信度，Dimple 与 iQuant 走同一套档位：

| 情形 | 置信度 |
| --- | --- |
| 精确关键词命中（`match_kind=keyword`）且主证据成功（Dimple 查库取证 / iQuant 事件自带证据） | **1.0** |
| 同义词召回（`match_kind=synonym`） | 0.8 |
| 字符模糊召回（`match_kind=fuzzy`） | 0.6 |
| 未识别类型（无 type），或精确命中但主证据无成功取证 | 0.4 |

- 采集文本“风控项 xxx”中的中文短语作为精确关键词，命中即确定性分类（`match_kind=keyword`），
  精确命中天然优先于 fuzzy，误路由随之消除；
- 配套 runbook 不跑业务 SQL（`steps: []`），由 `default` 基于事件字段给出参数化根因与处置建议；
- 引擎对自带证据类型置 `primary_evidence_ok=True`（事件自带证据视同主检查成功），精确命中即得 1.0；
  不在类型或引擎里写死任何置信度，匹配不上的事件按真实情况落到 0.8 / 0.6 / 0.4。

**靠补 runbook / 关键词消化长尾，而非调置信度**：当出现新的未识别风控项（落到 0.4、class=other）时，
正确做法是在 `iquant_errors.yaml` 补类型与精确关键词、在 `runbooks/` 补对应 runbook，让它“有东西可匹配”，
从而精确命中并回到 1.0；无需改代码，也不应人为把置信度统一抬高。

## 六、监控范围确认：为什么只有「事中风控事件」一个

基于 31 个已提供源码服务的全量 Controller 排查，iQuant 平台中唯一符合「实时产生、有状态流转
（NEW/NOTIFIED/HANDLED/IGNORED）、需主动监控的离散异常告警事件」语义的是 DayAbnormalRiskEvent。
其余名称相近的接口均不是离散告警事件：

| 接口 / 类 | 实际语义 | 为何不对接 |
| --- | --- | --- |
| RiskMonitor / MarketRiskMonitor / CreditRiskMonitor | 风险指标、限额监控看板 | 查询当前风险值与限额占用率，是连续指标快照，无事件状态流转，不是一条一条的告警 |
| TradeEventController（/risk/tradeEvent） | 存续期事件 | 债券生命周期信息：行权、提前还本、还本付息，按日期区间静态查询 |
| NoticeRiskController（/risk/notice） | 首页通知中心 | 风险限额/存续期/行情通知的聚合查询，底层仍引用上述数据 |
| DayAbnormalRiskNotifyController | 推送配置 | 通知开关、已读确认等配置管理 |
| DayAbnormalRiskRuleController | 规则管理 | 风控规则 CRUD 与审批 |
| DayAbnormalRiskCheckController | 风控检查入口 | 交易/报价链路内部同步调用，用于实时判定，非事件查询 |
| QtmTaskMonitor 等 | 任务/基础设施监控 | 任务状态、硬件资源占用，属运维基础设施而非业务告警 |

**边界说明**：以上结论覆盖已提供源码的 31 个服务；剩余 3–5 个未提供源码的服务理论上可能存在
未发现的事件源，待源码补齐后可再复核。新增事件源只需在 `collector.ENDPOINTS` 注册即可扩展。

## 七、待确认 / 后续事项

- 监控范围当前锁定事中风控事件单接口（7 类风控项已全覆盖）；如需接入更多事件接口，
  在 `collector.ENDPOINTS` 注册即可。
- iQuant 专用规则库已补齐，7 类事件均精确关键词命中、置信度 1.0；后续新增风控项时按第五章补类型/关键词/runbook 即可让其可匹配，并结合处置反馈持续优化根因与建议措辞。
- 测试/生产环境差异、网络白名单、上线流程待提供；当前结论基于 55 环境实测。
- 剩余 3–5 个服务源码暂未提供，不影响本次对接；如后续发现新的告警事件源再行扩展。
