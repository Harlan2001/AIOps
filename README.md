# DIMPLE TLOG 业务报错智能诊断（运行时零模型 MVP）

面向 DIMPLE 期货/黄金清算系统 Oracle 库（`ULOG.TLOG`）的**数据库业务报错诊断**：
输入一条已知报错（TLOG 记录或粘贴文本），输出**问题是什么 + 证据 + 怎么解决**。

**核心约束：交付到客户的产品不含任何大模型/模型权重。** 大模型只在开发阶段把专家经验"蒸馏"成
YAML 规则（经人审固化）；运行时只有 `正则解析 + 规则引擎 + 只读查库 + 模板报告`，
离线可跑、零 token、毫秒级、结果可复现、可审计。

---

## 一、运行时处理链（全确定性）

```
TLOG 报错
  → 噪音过滤(noise_rules.yaml)        拦掉 92.7% 的"成功/无数据/完成"假报错
  → 类型识别(errors.yaml)             骨架关键词命中为必要条件，错误码辅助排序
  → 参数抽取(正则)                    [合约=>x] / [会员->x] / 尚缺<n>
  → 调用链解析(LSECTION)              定位 PKC包.SP过程:行号
  → 诊断树(runbooks/*.yaml)           按顺序执行参数化只读 SQL，主/次根因综合判定
  → 模板报告(report.py)               问题+证据+建议（模板填充，非生成）
  → 未命中兜底/回流                   未匹配类型进入待补规则清单
```

## 二、目录结构

```
dimple-tlog-diagnose/
├── config/db.yaml                 只读连接配置（无任何模型 endpoint）
├── engine/
│   ├── db.py                      python-oracledb 只读封装（含写操作拦截）
│   ├── parser.py                  噪音/ORA/业务分类、骨架归一化、参数抽取、调用链解析
│   ├── rule_engine.py             规则引擎：类型匹配、参数/日期解析、只读 SQL 诊断树
│   └── report.py                  文本报告模板
├── rules/                         ★ 规则包（核心资产，可 diff、可版本化、可审计）
│   ├── errors.yaml                报错类型注册（关键词/错误码/参数别名/runbook）
│   ├── noise_rules.yaml           噪音过滤规则
│   └── runbooks/
│       ├── rb_settle_price.yaml   结算价不存在
│       ├── rb_defer_fee.yaml      递延费率不存在
│       └── rb_position.yaml       平仓时持仓不足
├── tools/
│   ├── gen_rule_seed.py           从历史 TLOG 自动生成规则种子（纯规则，构建期用）
│   ├── replay.py                  历史回放：覆盖率统计 + 抽样端到端诊断
│   ├── verify_samples.py          用真实报错样本验证诊断 SQL
│   └── selfcheck.py               分类/匹配自测（不连库）
├── data/
│   ├── rule_seed.csv / .yaml      137 类业务报错种子（频次/错误码/模块/参数/样例）
│   ├── noise_seed.csv             16 种噪音模式
│   └── ora_seed.csv               Oracle 技术错误模式（备用）
└── diagnose.py                    命令行入口
```

## 三、环境与连接

- Python 3.10+（本机 3.13），依赖：`oracledb`、`pyyaml`、`jinja2`（均为开源库，非模型）
  `pip install oracledb pyyaml jinja2`
- 连接配置在 `config/db.yaml`，默认只读；`engine/db.py` 会拦截任何写 SQL。

## 四、快速开始

```powershell
$env:PYTHONIOENCODING="utf-8"
# 1) 按 TLOG 主键诊断（自动取数）
python diagnose.py --id 4811525544
# 2) 直接粘贴报错文本
python diagnose.py --text "[合约=>Ag(T+D)]结算价不存在" --ldate 2026-08-28
# 3) 逻辑自测（不连库）
python tools/selfcheck.py
# 4) 历史回放：覆盖率 + 每类抽样端到端诊断（参数=每类抽样条数）
python tools/replay.py 2
# 5) 重新从 TLOG 生成规则种子
python tools/gen_rule_seed.py
```

## 五、如何新增一类报错（扩展规则，全程不写代码）

以"[交易日=>20260828]不存在"为例：

1. 在 `rules/errors.yaml` 增加类型：
   ```yaml
   - id: trade_date_not_found
     title: 交易日不存在
     keywords: ["交易日", "不存在"]
     err_codes: [101027003]
     param_alias: {"交易日": "trade_date"}
     runbook: rb_trade_date
   ```
2. 在 `rules/runbooks/rb_trade_date.yaml` 写诊断树（参数化只读 SQL + 失败根因 + 处置建议），
   主检查节点加 `primary: true`，旁证用 `type: sql_query`。
3. 跑 `tools/replay.py` 看覆盖率与诊断结果；业务专家审核 SQL 与建议后定稿。

## 六、规则引擎要点（已在真实数据上验证）

- **类型识别以骨架关键词为必要条件**：错误码在不同业务场景会被复用（如结算价/递延费率共享
  101022001，库存不足与持仓不足场景相近），单靠错误码会误判；错误码只用于关键词命中后的排序。
- **诊断日期**：默认取日志日期；可在 runbook 用 `date_from` 从参数提取（如持仓不足从
  `成交编号` 前 8 位取业务日期）。每个数据缺失检查配"目标表最新数据日期"旁证，
  即使报错日期与数据快照不同步也能给出有意义结论。
- **诊断树跑完所有检查**：`primary: true` 的主检查失败作为主根因，其余失败作为"附带发现"。

## 七、POC 实测结果（2026-01 ~ 2026-10，共 89,454 条 FATAL/ERROR）

| 分类 | 数量 | 占比 | 处置 |
|---|---|---|---|
| 噪音（成功/无数据/完成流水） | 82,966 | 92.7% | 规则过滤，不诊断 |
| Oracle 技术错误（ORA） | 1,155 | 1.3% | 转 DBA（本期不做） |
| **业务报错** | **5,318** | 5.9% | 诊断对象 |
| 未分类 | 19 | 0.02% | 回流 |

- 业务报错归一化后仅 **137 种**；覆盖率：**Top10 85.7% / Top20 91.0% / Top50 96.4% / Top100 99.3%**。
- 粗分类：数据缺失 73.3%、操作失败 11.4%、业务规则校验 5.8%、流程未就绪 3.2%、权限登录 1.8%。
- 当前已落地 3 类 runbook（结算价/递延费率/持仓不足），端到端查库诊断均正确；
  其余类型已在 `data/rule_seed.csv` 中作为扩展种子，按 Top 排序补规则即可。
- 数据说明：测试库业务数据快照停在 2026-08-28，而日志持续到 2026-10；真实生产同日时
  诊断可直接命中，本库用"最新数据日期旁证"兜底。

## 八、下一步（把覆盖率从 5% 做到 90%+）

1. 按 `data/rule_seed.csv` 的 Top 顺序，用开发期 LLM 生成各类型 runbook 初稿（诊断树+只读
   SQL+建议），业务/DBA 逐类审核定稿（LLM 不进交付物）。
2. 优先补 Top10：存续期变更记录不存在、期权合约修改失败、到期日异常、记录不存在、
   业务提示代码不存在、角色数不一致、登录密码、境外成交未复核、未注册 IP、结算价类。
3. 未命中采集 → 离线补规则 → 版本化发版，形成闭环。
