# 数据库业务报错智能诊断系统（AIOps）

面向清算系统 Oracle 数据库的**已知报错根因诊断**：输入一条报错（TLOG 记录或粘贴文本），
自动输出 **"问题是什么 + 怎么解决 + 可复核的证据链"**。

采用 **LLM 为大脑 + ML 前置分流/相似召回 + 规则只读查库 + Dimple 官方知识库领域知识** 的混合架构
（三证合一）。高频问题由 ML/规则毫秒级处理（零 token），仅长尾升级 LLM；全程对生产库只读、
可内网私有化部署、可降级、可审计。

---

## 一、整体链路

```
一条报错
  │
  ├─ ML① 前置分流（字符 TF-IDF + 逻辑回归）
  │     noise/ora → ML 快速路径，直接分诊（拦掉约 94% 流量，不查库、不调 LLM）
  │     biz       → 放行
  ├─ ML② 相似案例召回（TF-IDF 余弦，Top5 历史相似案例 = 先验证据）
  ├─ 领域知识检索（Dimple 知识库，本地 BM25，按中文症状取 Top3 诊断卡 = 机制证据）
  ├─ 规则引擎只读查库（参数化 SELECT 诊断树 = 现场事实证据）
  ├─ 决策门
  │     高置信 + 规则命中 → 规则快速路径（零 token）
  │     低置信/未覆盖/长尾 → LLM 三证合一推理
  └─ 结构化报告：问题是什么 + 证据链（案例/知识卡/查库结果）+ 怎么解决 + 置信度
        LLM 不可用 → 自动回退规则结论；规则也未覆盖 → 诚实兜底并回流
```

## 二、三证合一证据模型

| 证据 | 来源 | 回答 |
|---|---|---|
| 历史相似案例（先验） | ML 相似召回 | 以前发生过多少次、长什么样 |
| 领域知识（机制手册） | Dimple 知识库诊断卡 | 根因分支、成立/反证、必收事实、只读 SQL、日志锚点、处置边界 |
| 现场查库（事实） | 规则引擎只读 SQL | 现在库里到底是什么状态（最终准绳） |

LLM 结论必须建立在三类证据之上，并**以现场查库事实为准**；知识库只读 SQL 默认不执行、
标注"未现场核实"；证据不足时如实给低置信度与排查方向，禁止臆测、禁止改库。

## 三、目录结构

```
AIOps/
├── hybrid_diagnose.py        混合诊断主入口（ML 分流→召回→知识库→规则→决策门→LLM）
├── diagnose.py               按 ID 取报错记录
├── config/
│   ├── db.yaml               Oracle 只读连接
│   ├── llm.yaml(.example)    LLM 配置（OpenAI 兼容；.example 为脱敏模板）
│   └── kb.yaml(.example)     Dimple 知识库配置（.example 为脱敏模板）
├── engine/                   确定性引擎
│   ├── db.py                 oracledb 只读封装 + 写操作拦截
│   ├── parser.py             噪音/ORA/业务判定、骨架归一、参数抽取、调用链解析
│   ├── rule_engine.py        规则引擎：类型匹配、参数绑定、只读 SQL 诊断树
│   └── report.py             报告渲染（含领域知识卡）
├── ml/                       机器学习层（sklearn，CPU 毫秒级）
│   ├── router.py             一级分流 + 业务类型路由
│   ├── retriever.py          相似案例召回
│   ├── dataset.py / train_router.py   数据集构建与离线训练
├── kb/client.py              Dimple 知识库适配（本地 BM25、门禁、降级、症状清洗）
├── llm/
│   ├── client.py             OpenAI 兼容客户端（urllib，无重依赖）+ 离线兜底
│   └── prompts.py            三证合一提示词
├── rules/                    规则包（可 diff、可版本化、可审计）
│   ├── errors.yaml / noise_rules.yaml
│   └── runbooks/             rb_settle_price / rb_defer_fee / rb_position
├── models/                   ML 模型（轻量 joblib，本地，不入库）
├── data/ml/dataset.csv       带标签数据集（本地，不入库）
└── tools/                    自检/回放/训练/联调工具（含 test_kb.py、llm_ping.py）
```

## 四、环境与配置

```powershell
pip install -r requirements.txt
```

- Python 3.10+；主要依赖 `scikit-learn`、`numpy`、`scipy`、`joblib`、`oracledb`、`pyyaml`。
- 配置文件（真实配置含密钥/本机路径，已 gitignore，仓库只提供 `.example`）：
  - `config/db.yaml`：Oracle 只读连接（默认只读，代码层拦截一切写 SQL）；
  - `config/llm.yaml`：由 `llm.yaml.example` 复制，填 `base_url/api_key/model`；不配置则自动降级为"规则 + 知识库"；
  - `config/kb.yaml`：由 `kb.yaml.example` 复制，指向 Dimple 知识快照根目录。

## 五、快速开始

```powershell
$env:PYTHONIOENCODING="utf-8"

python tools/test_kb.py                                # 知识库独立自测（不依赖 ML/数据/LLM/数据库）
python hybrid_diagnose.py --id <报错记录ID>            # 混合诊断（自动决策，报告含知识卡）
python hybrid_diagnose.py --id <报错记录ID> --llm      # 强制走 LLM（三证合一）
python hybrid_diagnose.py --id <报错记录ID> --fast     # 强制规则快速路径
python hybrid_diagnose.py --text "[合约=>Au9999]结算价不存在"   # 直接粘贴报错文本
```

LLM 连通性：`python tools/llm_ping.py`（最小自检）；模型训练：`python ml/dataset.py` 后 `python ml/train_router.py`。

## 六、实测效果（真实历史日志）

- 全量约 8.9 万条 FATAL/ERROR：噪音约 92.7%、Oracle 技术错误约 1.3%、业务报错约 5.9%（归一化后约 137 类）。
- ML 一级分流准确率 **99.98%**（业务报错召回率 100%），业务类型路由准确率 **99.72%**；模型仅约 1.7MB、纯 CPU。
- 高置信 + 规则快速路径覆盖绝大多数高频问题，**真正调用 LLM 的比例约 0.4%**（规则补齐 Top30 后）。
- 知识库按中文症状检索命中准确（持仓不足、结算价不存在、递延费率不存在、登录密码错误等）；
  数字错误码与知识库编码体系不一致，故检索统一使用中文症状。
- 端到端示例：持仓不足、结算价不存在（规则快速路径零 token）；长尾存续期变更失败（LLM 诚实给低置信度并给排查方向）。

## 七、安全与私有化

- **只读三重约束**：数据库只读账号 + 代码层写拦截（禁 INSERT/UPDATE/DELETE/DDL）+ 规则 SQL 白名单与参数化绑定。
- **知识库只读 SQL 默认不自动执行**：经人工审核并派生为 runbook 后才由规则引擎执行。
- **数据不出网**：LLM 内网私有化部署（vLLM/Ollama/网关，OpenAI 兼容接口）；知识库为本地 BM25、纯标准库、离线、无向量库。
- **可降级**：LLM、知识库任一缺失都不阻断主流程。
- **客户隔离**：知识按客户投影交付，内部全集不外发。
- **可审计**：报告逐步标注由 ML / 知识库 / 规则 / LLM 完成，LLM 结论附证据。

## 八、产品形态（规划）

私有化内网 **Web 诊断工作台**（唯一前端）+ 站内事件中心 + 诊断 API；业务存储 **MySQL 8**（InnoDB、
utf8mb4、ngram 中文全文索引）；Docker Compose 离线部署（规模化上 K8s）。不做 IM 机器人、不做实时监控大屏。
当前仓库已落地 CLI 诊断内核，服务化（FastAPI + Web + MySQL）按路线推进。

## 九、文档（`docs/`）

- 《整体技术架构设计文档》——目标态系统总纲（分层、模块接口、数据模型、部署、技术决策）
- 《产品形态设计文档-私有化内网Web工作台》——产品形态、功能模块、部署与技术栈
- 《混合架构MVP说明-LLM为主+ML分流》——诊断内核实现与实测
- 《知识库集成说明》——Dimple 知识库接入、配置、安全边界、验证
- 《训练数据标准化规范与报错类型盘点》——数据规范与类型盘点

## 十、如何新增一类报错

- 高频类型：在 `rules/runbooks/` 增加一份只读诊断树 YAML（`errors.yaml` 注册），引擎不动；
  也可从知识库诊断卡派生只读 SQL 模板，经专家审核后固化。
- 未见类型：ML 召回历史案例 + LLM 三证合一兜底，并回流到开发侧补规则/重训模型，形成数据飞轮。
