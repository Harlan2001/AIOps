# AIOps 迁移 GaussDB 最优方案

> 目标：保持既有"混合智能诊断"技术架构不变，把数据源从 Oracle 整体切到 GaussDB；信创环境无全量日志（ULOG.TLOG 不存在），只有源码反推的报错清单 + 错误历史表。
> 范围：连接、取数、ML 分流、规则引擎、runbook、报告、CLI。LLM / KB 层基本不动。

## 1. 现有架构（Oracle 版）回顾

```
输入：ULOG.TLOG 记录 ID
  → ML 分流 Router（noise/biz/ora/other + Top30 业务类型）
      noise/ora → 快速路径（不查库、不调 LLM）
  → ML 相似案例召回（TF-IDF，dataset.csv）
  → KB 知识卡（BM25）
  → 规则引擎：errors.yaml 关键词匹配类型 → runbook 参数化 SQL 诊断树
  → 决策门：高置信 + 规则命中 → 规则快速路径；否则 LLM；LLM 不可用 → 兜底
  → 报告（纯模板）
```

模块清单：`engine/db.py`（oracledb 只读）、`engine/tlog.py`（按 ID 查 TLOG）、`engine/parser.py`（解析）、`ml/router.py`（2 个分类器）、`ml/retriever.py`（TF-IDF）、`engine/rule_engine.py`、`llm/client.py`、`kb/client.py`、`reporting.py`、`cli.py`。

## 2. 三个核心决策

### 2.1 去掉 ML 分流器（Router：routing + biz_type 两个分类器）

| 理由 | 说明 |
|---|---|
| 数据源变了 | TLOG 是"全量日志流"（含 91.57% 噪音），需要分流；GaussDB 错误表是"已筛选的错误记录"，**没有噪音、不需要分流** |
| 规则匹配更准 | 报错类型是源码里的固定集合（错误码/消息），规则匹配确定性 100%；ML 是概率分类（<100%），没理由用更差的 |
| 没有训练数据 | GaussDB 无全量日志，无法复制 Oracle 的训练集；错误表本身就是"已标注错误"，直接用规则即可，无需再训 |
| 可审计 | 运维诊断要求确定性、可追溯，规则匹配可解释，ML 黑盒不适合 |

> 连带：`ml/dataset.py`、`ml/train_router.py`、`var/models/*.joblib`、`var/data/ml/dataset.csv` 一并归档（代码可保留在 `ml/legacy/`，不删，方便回溯）。

### 2.2 保留并改造 ML 相似案例召回（retriever）

- 对错误历史表（reason 字段）建字符级 TF-IDF 索引，输入新错误 → 召回相似历史错误，为 LLM 提供证据。
- **不需要训练标签**，直接从错误记录建，成本低；对"未覆盖错误"找相似案例是规则无法替代的（规则只覆盖已知类型）。
- 数据源：`from_dataset()` → 改为 `from_error_tables()`（从错误记录表读，或从导出的错误记录 CSV 读）。

### 2.3 runbook 保留，改 SQL + 批量补

- 核心价值（查库取证 + 确定性结论、零 token 毫秒级）不变，只是 SQL 换方言、表换名。
- 现有 3 个 runbook 逻辑保留、SQL 改 GaussDB；再按源码清单批量补 A 档（候选 ≈290 条）。

## 3. 新架构（GaussDB 版）

```
输入：错误记录定位（trade_date + 错误记录主键；或日期范围批量扫描）
  → 【取数层】错误历史表取数 → 标准化诊断记录（text=reason，业务字段=member/client/contract...）
  → 【规则匹配】错误码/消息 → runbook（确定性，源码清单驱动，替代原 ML 分流）
  → 【规则引擎】runbook 参数化只读 SQL 诊断树（GaussDB 方言）
  → 【KB 知识卡】BM25（保留）
  → 【相似案例】TF-IDF 错误记录（保留）
  → 决策门：规则命中 → 快速路径；未覆盖/不确定 → LLM；LLM 不可用 → 兜底
  → 报告（纯模板，保留）
```

## 4. 模块改动清单

| 模块 | 改动 | 具体内容 |
|---|---|---|
| `engine/db.py` | 重写 | py-opengauss 驱动（`conn.prepare(sql)()`）；只读拦截保留；连接配置改 GaussDB |
| `config/db.yaml` | 改 | host/port/database/user/password（10.253.162.119:30100/xc_test） |
| `engine/tlog.py` | 重写 → `engine/error_records.py` | 从错误历史表取数（按日期+主键/批量），不再按 ID 查 TLOG |
| `ml/router.py` | 移除 | 归档到 `ml/legacy/` |
| `ml/dataset.py`、`ml/train_router.py` | 归档 | 不再训练分类器 |
| `ml/retriever.py` | 改造 | 数据源改错误历史表；TF-IDF 逻辑不变 |
| `engine/parser.py` | 微调 | 骨架/参数抽取保留；`is_ora` → `is_tech_error`（SQLSTATE） |
| `engine/rule_engine.py` | 微调 | 去掉 Router 依赖；类型匹配直接用；SQL 执行走新 db 接口 |
| `assets/rules/errors.yaml` | 扩充 | 按源码清单加类型（错误码/消息/关键词/runbook） |
| `assets/rules/runbooks/*.yaml` | 改 + 补 | 表名/方言改 GaussDB；按 A 档批量补 |
| `pipeline.py` | 改 | 去掉 ML 分流，直接规则匹配；快速路径/决策门/兜底逻辑保留 |
| `llm/client.py` | 保留 | 不变 |
| `kb/client.py` | 保留 | 不变 |
| `reporting.py` | 微调 | 无 LSECTION 位置字段，改为"错误来源表/记录主键" |
| `cli.py` | 改 | 输入从"记录 ID"改为"日期+错误记录/批量扫描" |
| `pyproject.toml` | 改 | 依赖 `oracledb` → `py-opengauss`；sklearn 保留（retriever 用） |

## 5. 数据 / 表映射

### 5.1 取数层：错误历史表（替代 TLOG）

| 错误域 | 表 | 报错文本字段 | 主键/过滤键 |
|---|---|---|---|
| 期货委托错误 | `dimple.tt_his_ftr_err_order`（81,962 行） | reason | trade_date+trader_no+local_no+purpose_code |
| 报价委托错误 | `dimple.tt_his_quote_err_order`（15,126 行） | reason | trade_date+trader_no+local_no |
| 敞口/止损报警 | `dimple.tc_his_alarm_note`（10.6M 行） | alarm_note | alarm_date+seq_no+alarm_type |
| 报价风控预警 | `dimple.tc_his_quote_alarm_note`（472,931 行） | risk_info | trade_date+seq_no |
| 合规报警 | `dimple.tc_his_rule_alarm_note`（60,095 行） | alarm_note | alarm_date+seq_no+member_id+alarm_type |
| 数据检查 | `dimple.tp_data_check_log`（33,276 行） | err_desc | seq_no+check_date |
| 结算前流程 | `dimple.tc_his_flow_control`（23,549 行） | err_msg | clear_date+flow_code+exch_code |

> 当日报错查当日表（tt_ftr_err_order / tt_quote_err_order / tc_alarm_note…），历史报错查 his 表。

### 5.2 runbook 核心表（现有 3 个）

| runbook | GaussDB 表 | 主键 |
|---|---|---|
| 结算价不存在 | `dimple.tc_clear_price`（435,880 行） | trade_date+contract_id |
| 递延费率不存在 | `dimple.tc_defer_fee_rate`（4,530 行）+ `tc_delivery_fee` | trade_date+member_id+contract_id |
| 平仓持仓不足 | `dimple.tc_clear_posi_detail`（19M 行） | trade_date+match_date+match_no+match_batch_no+exch_code+bs_flag |

### 5.3 SQL 方言差异（Oracle → GaussDB）

- 表名/字段：大写 → 小写（GaussDB 自动折叠小写，可不加引号）
- `ROWNUM` → `LIMIT n`；`NVL` → `COALESCE`；`SYSDATE` → `CURRENT_DATE`；`TO_CHAR(日期,'YYYY-MM-DD')` → `TO_CHAR(date,'YYYY-MM-DD')`（GaussDB 支持）
- 日期/时间字段是 varchar(8) 分开存（非 timestamp），SQL 直接按字符串比较
- 字符串拼接 `||` 保留；`''` 在 GaussDB 不视为 NULL（与 Oracle 差异注意）

## 6. 迁移步骤（分阶段）

| 阶段 | 内容 | 产出 |
|---|---|---|
| **M1 连接层** | db.py 改 py-opengauss、db.yaml 改配置、doctor 连通 | 能连上 GaussDB 并跑只读 SELECT |
| **M2 取数层** | 写 error_records.py（错误历史表取数 + 标准化）；CLI 改输入 | 能按日期/主键取错误记录并标准化 |
| **M3 规则层** | parser 微调；rule_engine 去 Router、走新 db；3 个 runbook SQL 改 GaussDB 跑通 | 3 个现有 runbook 在 GaussDB 端到端跑通 |
| **M4 管线改造** | pipeline 去 ML 分流、规则匹配替代；reporting 微调；retriever 改错误表 | 新管线跑通（规则快速路径 + LLM 兜底） |
| **M5 批量补 runbook** | 按源码清单 P0 Java 清算 → P1 C1 FD/CK → P2 B 模板 | A 档 runbook 批量落地 |
| **M6 验证** | 样本/错误记录回放，统计命中率，补边界 | 命中率报告 |

## 7. 风险与待确认

1. **错误记录覆盖域有限**：错误表只记"业务事件级错误"，C 侧/Java 部分报错（如校验拦截、内部异常）可能不落表 → 这些 runbook 写了也可能查不到运行记录，需在 runbook 里标注"无错误记录时的判定路径"。
2. **retriever 数据量**：tc_his_alarm_note 1063 万行，TF-IDF 全量建索引内存压力大，建议按日期窗口（如近 90 天）建。
3. **dimple_transfer 空库**：JDBC 配置指向它但无表，确认迁移是否到位/是否需要扫。
4. **双轨**：若非信创 Oracle 仍维护，runbook 需支持按部署形态过滤、SQL 维护两套方言（可在 runbook 里分 `oracle_sql` / `gauss_sql` 两段）。

## 8. 一句话总结

**架构骨架不动，只把"ML 分流"换成"规则匹配"、"TLOG 取数"换成"错误历史表取数"、"Oracle SQL"换成"GaussDB 方言"**；ML 分类器在无训练数据且规则更准的前提下应去掉，相似案例 TF-IDF 与 runbook/KB/LLM 全部保留。
