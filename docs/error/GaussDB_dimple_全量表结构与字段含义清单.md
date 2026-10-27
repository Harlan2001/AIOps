# GaussDB xc_test · dimple Schema 全量表结构与字段含义清单

> 生成时间：2026-10-27 | 数据来源：`scan_gaussdb.py` 只读扫描（2026-10-26 09:54）
> 连接：`opengauss://dimple_test:***@10.253.162.119:30100/xc_test` | 表数：**977** | 字段数：**15183**

---

## 0. 总览

| 前缀 | 表数 | 典型含义 |
|---|---|---|
| tc_ | 635 | 结算/资金/风控相关（clear/settle） |
| tt_ | 134 | 交易/委托/行情相关（trade） |
| tp_ | 27 | 参数/字典/公共（public/para） |
| ts_ | 63 | 系统管理/登录/审计（system） |
| tmp_ | 70 | 临时表/导入表 |
| d_ | 22 | 平台/通信相关 |
| 其他 | 26 | 其余 |

---

## 1. dimple.auto_clear_execution_nodes　(7 字段)
> 表含义：自动化清算执行节点-状态表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| node_id | numeric | N | √ | 节点号 |
| node_name | varchar(100) | N |  | 节点名称 |
| node_status | varchar(2) | N |  | 节点状态：0-初始状态、1-完成、2-异常 |
| need_execute | varchar(1) | N |  | 该节点是否需要执行：0-不执行、1-执行 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(50) | Y |  | 操作员 |

---

## 2. dimple.d_boc_tran_dict　(4 字段)
> 表含义：字典表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| dict_type | nvarchar2(10) | N |  | 字典值type |
| dict_code | nvarchar2(50) | N |  | 字典值code |
| dict_name | nvarchar2(50) | N |  | 字典值name |
| dict_remark | nvarchar2(50) | N |  | 字典值描述 |

---

## 3. dimple.d_boc_tran_file_record　(14 字段)
> 表含义：导入文件记录表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| file_id | nvarchar2(40) | Y |  | UUID(用于删除和关联数据) |
| variety_code | nvarchar2(255) | Y |  | 交易标的合约 |
| date_time | nvarchar2(255) | Y |  | 数据日期 |
| option_type | nvarchar2(255) | Y |  | 波动率曲面-期权类型 |
| sys_file_name | nvarchar2(255) | Y |  | 系统文件名称(逻辑主键) |
| sys_file_index | nvarchar2(11) | Y |  | 系统文件下标(逻辑主键) |
| sys_file_id | nvarchar2(255) | Y |  | 系统文件ID(逻辑主键) |
| original_name | nvarchar2(255) | Y |  | 导入文件名称 |
| file_type | nvarchar2(4) | Y |  | 文件类型,1-波动率曲面,2-利率曲线 |
| create_time | nvarchar2(20) | Y |  | 创建时间&导入时间 |
| creater_name | nvarchar2(255) | Y |  | 创建人员&导入人员 |
| update_time | nvarchar2(20) | Y |  | 修改时间 |
| modifier_name | nvarchar2(255) | Y |  | 修改人 |
| is_delete | nvarchar2(4) | Y |  | 删除标识 1-未删除 2-已删除 |

---

## 4. dimple.d_boc_tran_his_bsm　(26 字段)
> 表含义：BSM计算器计算结果记录表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| bsm_history_id | nvarchar2(40) | N |  | BSM计算记录UUID |
| vol_file_id | nvarchar2(40) | N |  | BSM计算-波动率数据ID |
| vol_interp_id | nvarchar2(40) | N |  | BSM计算-波动率插值数据ID |
| rate_file_id | nvarchar2(40) | N |  | BSM计算-利率数据ID |
| rate_interp_id | nvarchar2(40) | N |  | BSM计算-利率插值数据ID |
| variety_code | nvarchar2(255) | N |  | 期权合约 |
| option_type | nvarchar2(255) | N |  | 期权类型 |
| option | nvarchar2(255) | N |  | 期权(标的期货+期权类型+执行价) |
| buy_flag | nvarchar2(10) | N |  | 买卖方向(Ask为买---Bid为卖) |
| option_value | nvarchar2(255) | Y |  | 期权价值 |
| delta | nvarchar2(255) | Y |  | Delta值 |
| gamma | nvarchar2(255) | Y |  | Gamma值 |
| vega | nvarchar2(255) | Y |  | Vega值 |
| theta | nvarchar2(255) | Y |  | Theta值 |
| sigma | nvarchar2(255) | Y |  | Sigma值 |
| last_price | nvarchar2(255) | N |  | 最新价 |
| term | nvarchar2(255) | N |  | 期限/当年交易天数 |
| no_risk_rate | nvarchar2(255) | N |  | 无风险利率 |
| no_risk_rate_type | nvarchar2(255) | N |  | 无风险利率类型;1-黄金拆借利率;2-人民币拆借利率;3-黄金兑人民币的掉期利率;4-手动输入 |
| profit_rate | nvarchar2(255) | N |  | 分红收益率 |
| profit_rate_type | nvarchar2(255) | N |  | 分红收益率类型;1-黄金拆借利率;2-人民币拆借利率;3-黄金兑人民币的掉期利率;4-手动输入 |
| create_time | nvarchar2(20) | N |  | 创建时间 |
| creater_name | nvarchar2(255) | N |  | 创建人员 |
| update_time | nvarchar2(20) | N |  | 修改时间 |
| modifier_name | nvarchar2(255) | N |  | 修改人 |
| is_delete | nvarchar2(4) | N |  | 删除标识 1-未删除 2-已删除 |

---

## 5. dimple.d_boc_tran_his_interp　(11 字段)
> 表含义：（无注释）　|　估算行数：**57**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| history_id | nvarchar2(40) | N |  | 历史UUID(用于数据查询) |
| file_id | nvarchar2(40) | N |  | 文件UUID |
| range | nvarchar2(10) | N |  | 插值区间 T_1 T_2 T_3 D_1 D_2 D_3 |
| low_bound | nvarchar2(255) | N |  | 插值起点 |
| high_bound | nvarchar2(255) | N |  | 插值终点 |
| type | nvarchar2(255) | N |  | 插值类型  cubic-三次样条插值  linear-线形插值 |
| create_time | nvarchar2(20) | N |  | 创建时间 |
| creater_name | nvarchar2(255) | N |  | 创建人 |
| update_time | nvarchar2(20) | N |  | 修改时间 |
| modifier_name | nvarchar2(255) | N |  | 修改人 |
| is_delete | nvarchar2(4) | N |  | 删除标识 1-未删除 2-已删除 |

---

## 6. dimple.d_boc_tran_his_interp_record　(7 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| history_id | nvarchar2(40) | N |  | 历史UUID(逻辑主键) |
| file_id | nvarchar2(40) | N |  | 文件UUID(用于数据查询) |
| create_time | nvarchar2(20) | N |  | 创建时间 |
| creater_name | nvarchar2(255) | N |  | 创建人 |
| update_time | nvarchar2(20) | N |  | 修改时间 |
| modifier_name | nvarchar2(255) | N |  | 修改人 |
| is_delete | nvarchar2(4) | N |  | 删除标识 1-未删除 2-已删除 |

---

## 7. dimple.d_boc_tran_his_mapping　(33 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| history_id | nvarchar2(40) | Y |  | UUID |
| variety_code | nvarchar2(255) | Y |  | 标的期货 |
| date_time | nvarchar2(255) | Y |  | 日期 |
| option_type | nvarchar2(255) | Y |  | 期权类型 |
| interest_file_id | nvarchar2(255) | Y |  | 利率曲线系统文件名称 |
| volatility_file_id | nvarchar2(255) | Y |  | 波动率曲面系统文件名称 |
| term | nvarchar2(255) | Y |  | 期限 |
| type | nvarchar2(30) | Y |  | 1-Delta-Bid,2-Delta-Ask,3-σ-Bid,4-σ-Ask |
| data75 | nvarchar2(30) | Y |  | 0.75对应数据 |
| data80 | nvarchar2(30) | Y |  | 0.80对应数据 |
| data85 | nvarchar2(30) | Y |  | 0.85对应数据 |
| data90 | nvarchar2(30) | Y |  | 0.90对应数据 |
| data95 | nvarchar2(30) | Y |  | 0.95对应数据 |
| data96 | nvarchar2(30) | Y |  | 0.96对应数据 |
| data97 | nvarchar2(30) | Y |  | 0.97对应数据 |
| data98 | nvarchar2(30) | Y |  | 0.98对应数据 |
| data99 | nvarchar2(30) | Y |  | 0.99对应数据 |
| data100 | nvarchar2(30) | Y |  | 1.00对应数据 |
| data101 | nvarchar2(30) | Y |  | 1.01对应数据 |
| data102 | nvarchar2(30) | Y |  | 1.02对应数据 |
| data103 | nvarchar2(30) | Y |  | 1.03对应数据 |
| data104 | nvarchar2(30) | Y |  | 1.04对应数据 |
| data105 | nvarchar2(30) | Y |  | 1.05对应数据 |
| data110 | nvarchar2(30) | Y |  | 1.10对应数据 |
| data115 | nvarchar2(30) | Y |  | 1.15对应数据 |
| data120 | nvarchar2(30) | Y |  | 1.20对应数据 |
| data125 | nvarchar2(30) | Y |  | 1.25对应数据 |
| create_time | nvarchar2(20) | Y |  | 创建时间 |
| creater_name | nvarchar2(255) | Y |  | 创建人员 |
| update_time | nvarchar2(20) | Y |  | 修改时间 |
| modifier_name | nvarchar2(255) | Y |  | 修改人 |
| is_delete | nvarchar2(4) | Y |  | 删除标识 1-未删除 2-已删除 |
| contract | varchar(255) | Y |  | 拼接合约 |

---

## 8. dimple.d_boc_tran_interest_data　(15 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| variety_code_gold | nvarchar2(255) | Y |  | 黄金合约 |
| variety_code_swap | nvarchar2(255) | Y |  | 掉期合约 |
| date_time | nvarchar2(255) | Y |  | 日期 |
| file_id | nvarchar2(255) | Y |  | id |
| buy_flag | nvarchar2(10) | Y |  | 买卖方向(Ask为买---Bid为卖) |
| term | nvarchar2(255) | Y |  | 期限 |
| weight | nvarchar2(11) | Y |  | 期限权重 |
| data_gold | nvarchar2(255) | Y |  | 黄金 |
| data_rmb | nvarchar2(255) | Y |  | 人民币 |
| data_swap | nvarchar2(255) | Y |  | 拆借 |
| create_time | nvarchar2(20) | Y |  | 创建时间&导入时间 |
| creater_name | nvarchar2(255) | Y |  | 创建人员&导入人员 |
| update_time | nvarchar2(20) | Y |  | 修改时间 |
| modifier_name | nvarchar2(255) | Y |  | 修改人 |
| is_delete | nvarchar2(4) | Y |  | 删除标识 1-未删除 2-已删除 |

---

## 9. dimple.d_boc_tran_python_log　(9 字段)
> 表含义：python通信日志记录表　|　估算行数：**57**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| log_id | nvarchar2(40) | N |  | 日志ID |
| req_msg | text | N |  | 请求包 |
| req_url | nvarchar2(255) | N |  | 请求的URL |
| res_msg | text | Y |  | 响应包 |
| err_msg | text | Y |  | 错误信息 |
| spend_time | numeric(20,0) | Y |  | 花费时间 |
| create_time | nvarchar2(20) | N |  | 创建时间 |
| creater_name | nvarchar2(50) | N |  | 创建人 |
| is_delete | nvarchar2(4) | N |  | 删除标识 1-未删除 2-已删除 |

---

## 10. dimple.d_boc_tran_vol_data　(12 字段)
> 表含义：波动率曲线数据表　|　估算行数：**3,344**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| file_id | nvarchar2(255) | N |  | 文件UUID(用于关联系统文件名称) |
| delta | nvarchar2(255) | N |  | delta值 |
| delta_weight | nvarchar2(11) | N |  | delta权重(用于排序) |
| buy_flag | nvarchar2(255) | N |  | 买卖方向(Ask为买---Bid为卖) |
| term | nvarchar2(255) | N |  | 期限 |
| term_weight | nvarchar2(11) | N |  | 期限权重(用于排序和筛选数据) |
| volatility_data | nvarchar2(255) | N |  | 波动率数据 |
| create_time | nvarchar2(20) | N |  | 创建时间&导入时间 |
| creater_name | nvarchar2(255) | N |  | 创建人员&导入人员 |
| update_time | nvarchar2(20) | N |  | 修改时间 |
| modifier_name | nvarchar2(255) | N |  | 修改人 |
| is_delete | nvarchar2(4) | N |  | 删除标识 1-未删除 2-已删除 |

---

## 11. dimple.d_boc_tran_vol_delta　(9 字段)
> 表含义：波动率曲线表头delta表　|　估算行数：**57**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| file_id | nvarchar2(255) | N |  | 文件UUID(用于关联系统文件名称) |
| option_type | nvarchar2(255) | N |  | 期权类型 |
| delta | nvarchar2(255) | N |  | delta值 |
| delta_weight | nvarchar2(11) | N |  | delta权重(用于排序) |
| create_time | nvarchar2(20) | N |  | 创建时间&导入时间 |
| creater_name | nvarchar2(255) | N |  | 创建人员&导入人员 |
| update_time | nvarchar2(20) | N |  | 修改时间 |
| modifier_name | nvarchar2(255) | N |  | 修改人 |
| is_delete | nvarchar2(4) | N |  | 删除标识 1-未删除 2-已删除 |

---

## 12. dimple.d_bohz_account_data　(23 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  |  |
| member_id | varchar(8) | N |  |  |
| client_id | varchar(16) | Y |  |  |
| voucher_no | varchar(12) | Y |  |  |
| buy_flag | varchar(4) | Y |  |  |
| amt | numeric(24,6) | Y |  |  |
| account_type | varchar(10) | N |  |  |
| account_child_type | varchar(10) | Y |  |  |
| sysno | varchar(100) | N |  |  |
| subject_no | varchar(10) | Y |  |  |
| account_no | varchar(40) | Y |  |  |
| unit | varchar(10) | Y |  |  |
| currency | varchar(3) | Y |  |  |
| note | varchar(100) | Y |  |  |
| core_status | varchar(2) | Y |  |  |
| if_account | varchar(2) | Y |  |  |
| if_intable | varchar(2) | Y |  |  |
| subject_type | varchar(1) | Y |  |  |
| remark | varchar(300) | Y |  |  |
| party_account_no | varchar(40) | Y |  |  |
| local_no | varchar(30) | Y |  |  |
| acctdept_code | varchar(8) | Y |  |  |
| tradedept_code | varchar(8) | Y |  |  |

---

## 13. dimple.d_cash_flow_gap　(6 字段)
> 表含义：现金流缺口　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cash_date | varchar(8) | N | √ | 现金流日期 |
| purpose_code | varchar(8) | N | √ | 投组代码 |
| delivery_variety | varchar(20) | N | √ | 交割品种 |
| trade_type | varchar(20) | N | √ | 交易类型 |
| trader_no | varchar(30) | N |  |  |
| cumulative_gap | numeric(20,8) | N |  | 累计缺口 |

---

## 14. dimple.d_clear_flow_config_test111　(1 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| flow_code | varchar(4) | Y |  |  |

---

## 15. dimple.d_history_exposure_statistics　(22 字段)
> 表含义：历史敞口统计表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| trader_no | varchar(16) | N | √ | 交易员 |
| trade_type | bpchar(1) | N | √ | 交易类型:交易类型:见tp_public_dict的001 |
| purpose_code | varchar(3) | N | √ | 交易目的/投组 |
| contract_id | varchar(20) | N | √ | 合约 |
| variety_id | varchar(3) | Y |  | 交割品种 |
| buy_weight | numeric(24,6) | Y |  | 买入重量 |
| sell_weight | numeric(24,6) | Y |  | 卖出重量 |
| accumulate_weight | numeric(24,6) | Y |  | 累计重量 |
| fx_delta_weight | numeric(24,6) | Y |  | 重量FX Delta |
| last_fx_delta_weight | numeric(24,6) | Y |  | 上一日重量FX Delta |
| currency | varchar(8) | N | √ | 结算货币币种 |
| buy_amount | numeric(24,6) | Y |  | 买入金额 |
| sell_amount | numeric(24,6) | Y |  | 卖出金额 |
| accumulate_amount | numeric(24,6) | Y |  | 累计金额 |
| fx_delta_amount | numeric(24,6) | Y |  | 金额FX Delta |
| last_fx_delta_amount | numeric(24,6) | Y |  | 上一日金额FX Delta |
| dv01_shibor | numeric(24,6) | Y |  | 拆借利率DV01(CNY) |
| dv01_libor | numeric(24,6) | Y |  | 拆借利率DV01 |
| last_dv01_shibor | numeric(24,6) | Y |  | 上一日拆借利率DV01(CNY) |
| last_dv01_libor | numeric(24,6) | Y |  | 上一日拆借利率DV01 |
| remark | varchar(2000) | Y |  | 备注(成交单号) |

---

## 16. dimple.d_internal_board_import_match　(23 字段)
> 表含义：询价国际板进口交易表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N |  | 席位号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_date | varchar(8) | N |  | 成交日期 |
| trade_time | varchar(8) | N |  | 成交时间 |
| match_no | varchar(20) | N |  | 成交单号-交易流水号 |
| match_type | varchar(3) | Y |  | 业务类型: 2-境外询价;9-信用型询价 |
| trader_no | varchar(40) | N |  | 交易员 |
| purpose_code | varchar(5) | N |  | 投组 |
| contract_id | varchar(20) | N |  | 合约号 |
| bs_flag | varchar(3) | N |  | 买卖方向:见tp_public_dict的002 |
| price | numeric(20,8) | Y |  | 成交价格 |
| weight | numeric(16,6) | Y |  | 成交重量 |
| amount | numeric(24,6) | Y |  | 成交金额 |
| due_date | varchar(8) | Y |  | 到期日 |
| operate_date | varchar(8) | Y |  | 操作日期 |
| operate_status | varchar(3) | Y |  | 操作类型：0-新增; 1-修改; 2-删除 |
| operate_user | varchar(30) | Y |  | 操作人员 |
| operate_time | varchar(8) | Y |  | 操作时间 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| create_user | varchar(30) | Y |  | 创建人员 |
| status | varchar(3) | Y |  | 状态:1-已录入; 0-已删除 |
| remark | varchar(255) | Y |  | 附加条款-备注 |

---

## 17. dimple.d_internal_ftr_match　(22 字段)
> 表含义：内部交易期货成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 成交号-交易流水号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码-内部交易 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_type | varchar(3) | Y |  | 交易类型/业务类型 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量(手) |
| weight | numeric(16,6) | Y |  | 成交重量 |
| amount | numeric(24,6) | Y |  | 成交金额 |
| trader_no | varchar(40) | Y |  | 本方交易员 |
| trade_party_no | varchar(40) | Y |  | 对方交易员 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| purpose_code | varchar(5) | Y |  | 本方交易目的 |
| status | varchar(3) | Y |  | 状态:1-已录入; 0-已删除 |
| remark | varchar(255) | Y |  | 备注 |
| operate_user | varchar(20) | Y |  | 操作员 |
| operate_date | varchar(8) | Y |  | 操作日期 |
| operate_time | varchar(12) | Y |  | 操作日期 |
| create_user | varchar(30) | Y |  | 创建人员 |
| create_date | varchar(8) | Y |  | 创建日期 |

---

## 18. dimple.d_internal_home_lease_match　(25 字段)
> 表含义：内部交易境内租赁成交　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 合同号-交易流水号 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| price | numeric(20,8) | Y |  | 租借价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向:B本方借出/C本方借入 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| interest_base | varchar(3) | Y |  | 计息基准:见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期:见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_total | numeric(24,8) | Y |  | 总利息 |
| purpose_code | varchar(5) | Y |  | 本方交易目的/投组编号 |
| trader_no | varchar(40) | Y |  | 本方交易员 |
| trade_party_no | varchar(40) | Y |  | 对方交易员 |
| trade_date | varchar(8) | Y |  | 交易日 |
| operate_user | varchar(40) | Y |  | 操作员 |
| operate_date | varchar(8) | Y |  | 操作日期 |
| operate_time | varchar(8) | Y |  | 录入时间 |
| status | varchar(3) | Y |  | 状态:1-已录入; 0-已删除 |
| remark | varchar(255) | Y |  | 备注 |
| create_user | varchar(30) | Y |  | 创建人员 |
| create_date | varchar(8) | Y |  | 创建日期 |

---

## 19. dimple.d_internal_inquire_match　(25 字段)
> 表含义：内部交易询价成交　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| match_no | varchar(20) | N |  | 成交单号-交易流水号 |
| match_type | varchar(3) | Y |  | 业务类型: 2-境外询价;9-信用型询价 |
| business_type | varchar(3) | Y |  | 业务类型: 0-即期;1-远期;2-掉期 |
| trader_no | varchar(40) | Y |  | 本方交易员 |
| purpose_code | varchar(5) | Y |  | 本方交易目的/投组编号 |
| trade_party_no | varchar(40) | Y |  | 对方交易员 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | Y |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型:见tp_public_dict的253只包含即期和远期 |
| fn_flag | varchar(3) | Y |  | 远近端:见tp_public_dict的250 |
| delivery_type | varchar(3) | Y |  | 交割方式: 内部交易为4-实物交割 |
| operate_date | varchar(8) | Y |  | 操作日期 |
| operate_user | varchar(30) | Y |  | 操作日期员 |
| operate_time | varchar(8) | Y |  | 操作日期时间 |
| status | varchar(3) | Y |  | 状态:1-已录入; 0-已删除 |
| remark | varchar(255) | Y |  | 附加条款-备注 |
| create_user | varchar(30) | Y |  | 创建人员 |
| create_date | varchar(8) | Y |  | 创建日期 |

---

## 20. dimple.d_shfe_warehouse_receipt_bs　(18 字段)
> 表含义：上期所仓单买卖信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| seq_no | varchar(8) | N |  | 流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 自营客户号 |
| trader_no | varchar(16) | N |  | 交易员 |
| variety_id | varchar(8) | N |  | 品种 |
| bs_flag | varchar(3) | N |  |  |
| contract_id | varchar(20) | N |  |  |
| std_qty | numeric(11,3) | N |  |  |
| real_qty | numeric(11,3) | Y |  |  |
| price | numeric(8,3) | N |  |  |
| amount | numeric(21,3) | N |  |  |
| purpose_code | varchar(3) | N |  |  |
| op_user | varchar(30) | Y |  |  |
| op_time | varchar(8) | Y |  |  |
| trade_volume | numeric(16,0) | Y |  |  |
| sh_flag | varchar(20) | Y |  |  |
| if_delete | varchar(1) | N |  |  |

---

## 21. dimple.d_shfe_warehouse_receipt_delivery　(19 字段)
> 表含义：上期所仓单交割信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| delivery_date | varchar(8) | N |  | 交割日期 |
| seq_no | varchar(8) | N | √ | 流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 自营客户号 |
| trader_no | varchar(16) | N |  | 交易员 |
| variety_id | varchar(8) | N |  | 品种 |
| bs_flag | varchar(3) | N |  | 交易类型：包括空头交收、多头交收，见tp_public_dict的266 |
| contract_id | varchar(20) | N |  | 合约号 |
| std_qty | numeric(11,3) | N |  | 标准重量 |
| real_qty | numeric(11,3) | Y |  | 实际重量 |
| price | numeric(8,3) | N |  | 价格 |
| amount | numeric(21,3) | N |  | 金额 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |
| trade_volume | numeric(16,0) | Y |  | 手数 |
| sh_flag | varchar(20) | Y |  | 投机套保:1-投机,3-保值 见tp_public_dict的004 |
| if_delete | varchar(1) | N |  | 是否删除 见tp_public_dict的027 |

---

## 22. dimple.d_trade_elem_jour　(31 字段)
> 表含义：交易要素流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N |  | 操作日期 |
| op_time | varchar(8) | N |  | 操作时间 |
| op_user | varchar(30) | N |  | 操作人员 |
| seq_no | numeric | N |  | 操作流水号 |
| match_no | varchar(4000) | Y |  | 成交号 |
| trade_type | varchar(3) | Y |  | 交易类型 |
| trade_date | varchar(8) | Y |  | 原交易日期 |
| bs_flag | varchar(1) | Y |  | 买卖标识 |
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| orig_trader_no | varchar(30) | Y |  | 原交易员 |
| new_trader_no | varchar(30) | Y |  | 新交易员 |
| orig_purpose_code | varchar(3) | Y |  | 原投组 |
| new_purpose_code | varchar(3) | Y |  | 新投组 |
| orig_contract | varchar(20) | Y |  | 原合约 |
| new_contract | varchar(20) | Y |  | 新合约 |
| orig_weight | numeric(16,6) | Y |  | 原交收重量 |
| new_weight | numeric(16,6) | Y |  | 新交收重量 |
| orig_price | numeric(20,8) | Y |  | 原价格 |
| new_price | numeric(20,8) | Y |  | 新价格 |
| orig_purpose_code2 | varchar(3) | Y |  | 原投组2 |
| new_purpose_code2 | varchar(3) | Y |  | 新投组2 |
| orig_contract2 | varchar(20) | Y |  | 原合约2 |
| new_contract2 | varchar(20) | Y |  | 新合约2 |
| orig_weight2 | numeric(16,6) | Y |  | 原交收重量2 |
| new_weight2 | numeric(16,6) | Y |  | 新交收重量2 |
| orig_price2 | numeric(20,8) | Y |  | 原价格2 |
| new_price2 | numeric(20,8) | Y |  | 新价格2 |
| note | varchar(200) | Y |  | 备注 |
| modified_table | varchar(64) | Y |  | 变更表表名 |
| related_seq_no | numeric | Y |  | 关联操作流水号 |

---

## 23. dimple.d_trader_statistics_setting　(4 字段)
> 表含义：交易员统计维度与展示维度设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(16) | N | √ | 交易员 |
| statistics_type | varchar(3) | N | √ | 统计维度的类型;1-敞口分析统计;2-损益统计分析 |
| setting_type | varchar(3) | N |  | 统计维度与展示维度 |
| operate_date | varchar(8) | N |  | 操作日期 |

---

## 24. dimple.delivery_receive_info_manage　(16 字段)
> 表含义：交收信息管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | varchar(24) | N | √ | 业务流水号 |
| trade_date | varchar(8) | N | √ | 原交易日期 |
| match_no | varchar(20) | N | √ | 原成交号 |
| trader_no | varchar(15) | N | √ | 原交易员 |
| member_id | varchar(8) | Y |  | 原会员号 |
| bs_flag | bpchar(1) | N | √ | 原买卖标志:见tp_public_dict的002 |
| purpose_code | varchar(3) | N | √ | 原交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| portfolio_code | varchar(3) | N |  | 投组 |
| direction | bpchar(1) | N |  | 方向:见tp_public_dict的002 |
| weight | numeric(15,3) | Y |  | 交收重量 |
| price | numeric(9,2) | Y |  | 价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| info_level | bpchar(3) | N | √ | 交收信息级别 |
| op_date | varchar(8) | N |  | 操作日期 |
| op_time | varchar(8) | N |  | 操作时间 |

---

## 25. dimple.dmp_obs_batch　(6 字段)
> 表含义：（无注释）　|　估算行数：**49,756**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| source_id | varchar(96) | N | √ |  |
| batch_id | varchar(64) | N | √ |  |
| batch_hash | varchar(64) | N |  |  |
| received_at | timestamp | N |  |  |
| accepted_count | numeric(32,0) | N |  |  |
| duplicate_count | numeric(32,0) | N |  |  |

---

## 26. dimple.dmp_obs_event　(6 字段)
> 表含义：（无注释）　|　估算行数：**31**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| source_id | varchar(96) | N | √ |  |
| event_id | varchar(64) | N | √ |  |
| event_hash | varchar(64) | N |  |  |
| event_json | varchar(4096) | N |  |  |
| fingerprint | varchar(64) | N |  |  |
| received_at | timestamp | N |  |  |

---

## 27. dimple.dmp_obs_quota　(3 字段)
> 表含义：（无注释）　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| quota_id | numeric(32,0) | N | √ |  |
| event_count | numeric(64,0) | N |  |  |
| batch_count | numeric(64,0) | N |  |  |

---

## 28. dimple.dmp_obs_source　(17 字段)
> 表含义：（无注释）　|　估算行数：**11**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| source_id | varchar(96) | N | √ |  |
| deployment_id | varchar(96) | N |  |  |
| service_name | varchar(96) | N |  |  |
| node_id | varchar(96) | N |  |  |
| parser_profile | varchar(96) | N |  |  |
| token_sha256 | varchar(64) | N |  |  |
| enabled | numeric(32,0) | N |  |  |
| owner_id | varchar(96) | N |  |  |
| fence | numeric(64,0) | N |  |  |
| lease_until | timestamp | Y |  |  |
| last_heartbeat | timestamp | Y |  |  |
| checkpoint_generation | varchar(64) | N |  |  |
| checkpoint_offset | numeric(64,0) | N |  |  |
| lag_bytes | numeric(64,0) | N |  |  |
| gap_count | numeric(64,0) | N |  |  |
| parse_failure_count | numeric(64,0) | N |  |  |
| duplicate_count | numeric(64,0) | N |  |  |

---

## 29. dimple.end_date_profit_loss_data　(17 字段)
> 表含义：日终损益数据表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| trader_no | varchar(16) | N |  | 交易员代码 |
| trade_type | bpchar(1) | N |  | 交易类型 |
| purpose_code | varchar(3) | N |  | 投组 |
| contract_id | varchar(20) | N |  | 合约 |
| day_realized_profit_loss | numeric(24,6) | Y |  | 当日已实现损益 |
| cumulitive_profit_loss | numeric(24,6) | Y |  | 累计实现损益 |
| unrealized_profit_loss | numeric(24,6) | Y |  | 未实现损益 |
| day_profit_loss | numeric(24,6) | Y |  | 日损益 |
| day_profit_loss_c | numeric(24,6) | Y |  | 日损益(CNY) |
| month_profit_loss | numeric(24,6) | Y |  | 月损益 |
| month_profit_loss_c | numeric(24,6) | Y |  | 月损益(CNY) |
| year_profit_loss | numeric(24,6) | Y |  | 年损益 |
| year_profit_loss_c | numeric(24,6) | Y |  | 年损益(CNY) |
| total_profit_loss | numeric(24,6) | Y |  | 总损益 |
| total_profit_loss_c | numeric(24,6) | Y |  | 总损益(CNY) |
| currency | varchar(8) | Y |  | 币种 |

---

## 30. dimple.grab_tps_limit_4spdb　(4 字段)
> 表含义：交易日内席位上交易员抢单TPS限额表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trading_day | bpchar(8) | N | √ | 交易日 |
| seat_id | varchar(16) | N | √ | 席位号 |
| trader_id | varchar(16) | N | √ | 交易员号 |
| grab_tps | numeric(3,0) | N |  | 抢单TPS |

---

## 31. dimple.grab_tps_limit_day_seat_4spdb　(3 字段)
> 表含义：交易日内席位抢单TPS限额表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trading_day | bpchar(8) | N | √ | 交易日 |
| seat_id | varchar(16) | N | √ | 席位号 |
| used_tps | numeric(3,0) | N |  | 已用额度 |

---

## 32. dimple.ks_sync_data　(2 字段)
> 表含义：同步记录表　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sync_tag | varchar(50) | N | √ | 同步标记 |
| last_opt_time | timestamp | N |  | 上次操作时间 |

---

## 33. dimple.other_business_quota_occupied　(9 字段)
> 表含义：其他业务额度占用表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| op_time | timestamp | N |  | 操作时间 |
| counterparty_no | varchar(30) | N | √ | 交易对手方代码 |
| counterparty_abbr | varchar(100) | N |  | 交易对手方简称 |
| quota_occupied | numeric(22,2) | N |  | 其他额度占用(元) |
| create_date | timestamp | N |  | 创建日期 |
| create_by | varchar(32) | Y |  | 创建人 |
| update_date | timestamp | N |  | 修改日期 |
| update_by | varchar(32) | Y |  | 修改人 |

---

## 34. dimple.risk_qtyweightconfigure　(16 字段)
> 表含义：事前风控交易笔数与重量限额配置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| param_name | varchar(128) | Y |  | 参数名称 |
| param_type | varchar(16) | N | √ | 参数类型：笔数：1、数量：2 |
| delivery | varchar(16) | N | √ | 交割品种 |
| exch | varchar(16) | N | √ | 交易所 |
| member | varchar(16) | N | √ | 席位号 |
| contract | varchar(255) | N | √ | 合约代码 |
| bsflag | varchar(4) | N | √ | 交易方向 |
| offset | varchar(4) | N | √ | 开平标志 |
| managelevel | varchar(16) | N | √ | 管控层级：会员级：1 |
| if_use | varchar(8) | Y |  | 是否启用 |
| threshold | numeric(24,8) | Y |  | 预警值 |
| limit_value | numeric(24,8) | Y |  | 极限值 |
| create_date | varchar(20) | Y |  | 设置时间 |
| setstaff | varchar(16) | Y |  | 设置人员 |
| use_status | varchar(3) | Y |  | 参数状态：0-新增，1-修改，2-删除 |
| seq_no | numeric(24,0) | N | √ | 流水号 |

---

## 35. dimple.risk_qtyweighthisuse　(17 字段)
> 表含义：事前风控交易笔数与重量限额历史占用表　|　估算行数：**123**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| param_name | varchar(128) | Y |  | 参数名称 |
| param_type | varchar(16) | Y |  | 参数类型：笔数：1、数量：2 |
| delivery | varchar(16) | N | √ | 品种 |
| exch | varchar(16) | N | √ | 交易所 |
| member | varchar(16) | N | √ | 席位号 |
| contract | varchar(255) | N | √ | 合约代码 |
| bsflag | varchar(4) | N | √ | 交易方向 |
| offset | varchar(4) | N | √ | 开平标志 |
| trader | varchar(16) | N | √ | 交易员 |
| if_use | varchar(8) | Y |  | 是否启用 |
| threshold | numeric(24,8) | Y |  | 预警值 |
| limit_value | numeric(24,8) | Y |  | 极限值 |
| frozen_limit | numeric(24,8) | Y |  | 实时冻结数据 |
| used_limit | numeric(24,8) | Y |  | 实时占用数据 |
| usable_limit | numeric(24,8) | Y |  | 可用额度 |
| create_date | varchar(8) | N | √ | 日期 |
| limit_sign | varchar(8) | Y |  | 超限标志 |

---

## 36. dimple.risk_qtyweightuse　(17 字段)
> 表含义：事前风控交易笔数与重量限额实时占用表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| param_name | varchar(128) | Y |  | 参数名称 |
| param_type | varchar(16) | Y |  | 参数类型：笔数：1、数量：2 |
| delivery | varchar(16) | N | √ | 品种 |
| exch | varchar(16) | N | √ | 交易所 |
| member | varchar(16) | N | √ | 席位号 |
| contract | varchar(255) | N | √ | 合约代码 |
| bsflag | varchar(4) | N | √ | 交易方向 |
| offset | varchar(4) | N | √ | 开平标志 |
| trader | varchar(16) | N | √ | 交易员 |
| if_use | varchar(8) | Y |  | 是否启用 |
| threshold | numeric(24,8) | Y |  | 预警值 |
| limit_value | numeric(24,8) | Y |  | 极限值 |
| frozen_limit | numeric(24,8) | Y |  | 实时冻结数据 |
| used_limit | numeric(24,8) | Y |  | 实时占用数据 |
| usable_limit | numeric(24,8) | Y |  | 可用额度 |
| create_date | varchar(20) | N | √ | 日期 |
| limit_sign | varchar(8) | Y |  | 超限标志 |

---

## 37. dimple.t_lock_resource　(4 字段)
> 表含义：分布式锁资源　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| resource_type | varchar(50) | N | √ |  |
| host_address | varchar(100) | Y |  |  |
| resource_version | varchar(10) | N |  |  |
| create_time | varchar(20) | N |  |  |

---

## 38. dimple.t_refresh_time　(6 字段)
> 表含义：实时监控参数设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(100) | N | √ | 用户id |
| refresh_time | numeric(16,0) | N |  | 刷新频率 |
| create_id | varchar(100) | Y |  | 创建人 |
| create_time | timestamp | Y |  | 创建时间 |
| update_id | varchar(100) | Y |  | 更新人 |
| update_time | timestamp | Y |  | 更新时间 |

---

## 39. dimple.tc_account_adjust　(19 字段)
> 表含义：调账表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| adjust_date | varchar(8) | N | √ | 调账日期 |
| seq_no | numeric(10,0) | N | √ | 序号 |
| account_date | varchar(8) | Y |  | 账务日期 |
| subject_id_in | varchar(20) | Y |  | 入账科目代码 |
| subject_name_in | varchar(200) | Y |  | 入账科目名称 |
| subject_in_amt | numeric(24,6) | Y |  | 入账金额 |
| subject_in_qty | numeric(16,6) | Y |  | 入账数量 |
| subject_in_cost_type | varchar(20) | Y |  | 入账成本类型 |
| subject_in_remark | varchar(255) | Y |  | 入账摘要 |
| subject_id_out | varchar(20) | Y |  | 出账科目代码 |
| subject_name_out | varchar(200) | Y |  | 出账科目名称 |
| subject_out_amt | numeric(24,6) | Y |  | 出账金额 |
| subject_out_qty | numeric(16,6) | Y |  | 出账数量 |
| subject_out_cost_type | varchar(20) | Y |  | 出账成本类型 |
| subject_out_remark | varchar(255) | Y |  | 出账摘要 |
| adjust_desc | varchar(254) | Y |  | 调账描述 |
| creater | varchar(16) | Y |  | 操作人 |
| create_date | varchar(8) | Y |  | 操作日期 |
| create_time | varchar(8) | Y |  | 操作时间 |

---

## 40. dimple.tc_account_balance　(12 字段)
> 表含义：账务科目余额表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| account_date | varchar(8) | N | √ | 账务日期 |
| sysno | varchar(40) | N | √ | 系统编号 |
| subject_id | varchar(80) | N | √ | 科目号 |
| subject_name | varchar(200) | Y |  | 科目名称 |
| subject_amt | numeric(24,6) | Y |  | 科目余额 |
| subject_qty | numeric(16,6) | Y |  | 科目余量 |
| subject_in_amt | numeric(24,6) | Y |  | 科目今入金额 |
| subject_in_qty | numeric(16,6) | Y |  | 科目今入数量 |
| subject_out_amt | numeric(24,6) | Y |  | 科目今出金额 |
| subject_out_qty | numeric(16,6) | Y |  | 科目今出数量 |
| subject_last_amt | numeric(24,6) | Y |  | 科目昨日余额 |
| subject_last_qty | numeric(16,6) | Y |  | 科目昨日余量 |

---

## 41. dimple.tc_account_check　(8 字段)
> 表含义：账户余额核对　|　估算行数：**265**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| exch_code | varchar(3) | Y |  | 交易所 |
| account_proj | varchar(40) | Y |  | 对账项目 |
| account | varchar(40) | N | √ | 内部账号 |
| account_remain | numeric(24,6) | Y |  | 账户余额 |
| expect_remain | numeric(24,6) | Y |  | 预期余额 |
| account_result | varchar(3) | Y |  | 对账结果 |
| routine_flag | varchar(3) | Y |  | 常规帐号标识:1-常规  0-非常规 |

---

## 42. dimple.tc_account_database　(16 字段)
> 表含义：账务数据源表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_type | varchar(3) | Y |  | 业务类型：交易所 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| bus_code | varchar(40) | N |  | 业务代码 |
| bus_name | varchar(100) | N |  | 业务名称 |
| amt | numeric(24,6) | N |  | 金额 |
| currency | varchar(3) | Y |  | 币种 |
| variety_id | varchar(4) | Y |  | 产品号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_no | varchar(100) | Y |  | 成交号 |
| qty | numeric(20,3) | Y |  | 数量 |
| cost_type | varchar(10) | Y |  | 成本中心： 见dict316 |
| account_type | varchar(3) | Y |  | 帐务类型：见dict313 |
| tradeglobalid | varchar(30) | Y |  | 全局流水号 |
| ismatched | varchar(2) | Y |  | 是否匹配 |
| iscancel | varchar(2) | Y |  | 是否冲销 |

---

## 43. dimple.tc_account_file　(3 字段)
> 表含义：帐务文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日 |
| line_no | float8 | N | √ | 行号 |
| file_values | varchar(355) | Y |  | 文件内容 |

---

## 44. dimple.tc_account_inputdata　(7 字段)
> 表含义：核心账户余额数据-给余额核对用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(3) | Y |  | 交易所 |
| account_proj | varchar(40) | Y |  | 对账项目 |
| account | varchar(40) | N | √ | 内部账号 |
| account_remain | varchar(40) | Y |  | 账户余额 |
| routine_flag | varchar(3) | Y |  | 常规帐号标识:1-常规  0-非常规 |
| cnsmrsysid | varchar(8) | Y |  | 消费方系统标识,固定GTM |
| cnltxncd | varchar(8) | Y |  | 渠道交易码字 |

---

## 45. dimple.tc_account_para　(16 字段)
> 表含义：账务参数　|　估算行数：**521**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| subject_id | varchar(20) | Y |  | 科目号 |
| subject_name | varchar(250) | Y |  | 科目名称 |
| currency | varchar(3) | Y |  | 币种 |
| account_no | varchar(30) | Y |  | 内部资金账户 |
| account_name | varchar(60) | Y |  | 账户名称 |
| account_type | varchar(3) | Y |  | 账户类型 |
| branch_code | varchar(20) | Y |  | 网点号 |
| remark | varchar(100) | Y |  | 备注 |
| exch_code | varchar(2) | N | √ | 交易所 |
| sysno | varchar(40) | N | √ | 系统编号 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| subject_type | varchar(3) | Y |  | 科目类型：0 正常；1 合约；2 品种 |
| member_id | varchar(8) | Y |  | 会员号：默认$ |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 46. dimple.tc_account_para_all　(3 字段)
> 表含义：统计账务参数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| subject_id | varchar(20) | Y |  | 科目号 |
| subject_name | varchar(250) | Y |  | 科目名称 |
| subject_lv | float8 | Y |  | 评级 |

---

## 47. dimple.tc_account_send　(35 字段)
> 表含义：账务管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_date | varchar(8) | N | √ | 日期 |
| batch_no | varchar(40) | N | √ | 批次号 |
| seq_no | varchar(40) | Y |  | 记账流水号 |
| business_type | varchar(40) | Y |  | 业务类型 |
| sub_type | varchar(100) | N | √ | 子类型 |
| buy_flag | varchar(3) | N | √ | 借贷收付：见tp_public_dict的276,301 |
| subject | varchar(80) | Y |  | 科目 |
| name | varchar(200) | Y |  | 名称 |
| account | varchar(40) | Y |  | 账号 |
| account_name | varchar(100) | Y |  | 账户名称 |
| branches | varchar(10) | Y |  | 网点号 |
| currency | varchar(40) | N | √ | 币种 |
| amt | numeric(24,6) | Y |  | 发生额 |
| remark | varchar(255) | Y |  | 摘要 |
| status | varchar(40) | Y |  | 处理状态：见tp_public_dict的304 |
| fail_reason | varchar(40) | Y |  | 失败原因 |
| main_no | varchar(40) | Y |  | 主机流水号 |
| main_date | varchar(8) | Y |  | 核心日期 |
| create_time | varchar(8) | Y |  | 生成时间 |
| sysno | varchar(40) | N | √ | 系统编号 |
| uuid | varchar(40) | Y |  | 唯一识别码 |
| del_flag | varchar(3) | N | √ | 是否冲销标志 |
| qty | numeric(20,3) | Y |  | 数量 |
| cost_type | varchar(10) | Y |  | 成本中心： 见dict316 |
| account_type | varchar(3) | Y |  | 帐务类型：见dict313 |
| contract_id | varchar(20) | Y |  | 合约号 |
| member_id | varchar(8) | N | √ | 会员号 默认$ |
| client_id | varchar(16) | Y |  | 客户号 |
| cnsmrsysid | varchar(8) | Y |  | 消费方系统标识,固定GTM |
| cnltxncd | varchar(8) | Y |  | 渠道交易码字 |
| sumflag | varchar(3) | Y |  | 是否外围合并记账:是-“Y”,否-空 |
| isnightsend | varchar(1) | Y |  | 是否夜间供数 |
| tradeglobalid | varchar(30) | Y |  | 全局流水号 |
| ismatched | varchar(2) | Y |  | 是否匹配 |
| iscancel | varchar(2) | Y |  | 是否冲销 |

---

## 48. dimple.tc_account_set　(13 字段)
> 表含义：账务管理设置表　|　估算行数：**1,734**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| database_code | varchar(40) | Y |  | 数据源 |
| database_type | varchar(10) | Y |  | 数据源类型 |
| contract_cmp | varchar(8) | Y |  | 比较合约 |
| business_type | varchar(3) | Y |  | 业务类型代码 |
| business_type_name | varchar(40) | Y |  | 业务类型 |
| sub_type_name | varchar(40) | Y |  | 子类型 |
| buy_flag | varchar(40) | Y |  | 借贷收付 |
| sysno | varchar(40) | Y |  | 系统编号 |
| account_name | varchar(100) | Y |  | 账户名称 |
| currency | varchar(40) | Y |  | 币种 |
| remark | varchar(100) | Y |  | 备注 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 49. dimple.tc_account_status_manage　(7 字段)
> 表含义：账务发生状态管理表　|　估算行数：**295**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 序号 |
| total_count | numeric(20,0) | Y |  | 总记录数 |
| send_count | numeric(20,0) | Y |  | 发送记录数 |
| status | varchar(3) | Y |  | 状态:1未生成;2 已生成未发送;3发送中;4发送成功;5发送失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 50. dimple.tc_account_type　(4 字段)
> 表含义：账务类型参数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| market_type | varchar(3) | N | √ | 业务类型 |
| market_name | varchar(40) | Y |  | 业务类型名称 |
| sub_type | varchar(3) | N | √ | 子类型 |
| sub_name | varchar(40) | Y |  | 子类型名称 |

---

## 51. dimple.tc_account_valuation　(5 字段)
> 表含义：账务估值表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| group_no | varchar(10) | N | √ | 组号 |
| valuation_amt | numeric(24,6) | Y |  | 估值金额 |
| valuation_qty | numeric(16,6) | Y |  | 估值数量 |
| valuation_profit | numeric(24,6) | Y |  | 估值盈亏 |

---

## 52. dimple.tc_aip_base　(13 字段)
> 表含义：黄金定投基础表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| amt | numeric(24,6) | Y |  | 申购金额 |
| qty | numeric(24,6) | Y |  | 赎回克重（克） |
| status | varchar(3) | Y |  | 状态:见tp_public_dict的254 |
| trader_no | varchar(30) | Y |  | 交易员 |
| creater | varchar(30) | Y |  | 操作员 |
| create_time | varchar(22) | Y |  | 操作时间 |
| updater | varchar(30) | Y |  | 复核员 |
| update_time | varchar(22) | Y |  | 复核时间 |
| calc_price | numeric(20,6) | Y |  | 估算价格 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |

---

## 53. dimple.tc_aip_calc　(8 字段)
> 表含义：定投测算表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| seq_no | float8 | N | √ | 测算次数 |
| calc_price | numeric(20,6) | Y |  | 预估成交价 |
| bs_flag | varchar(3) | Y |  | 预估买卖 |
| calc_num | numeric(24,6) | Y |  | 预估数量 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |

---

## 54. dimple.tc_aip_day_calc　(15 字段)
> 表含义：定投日结表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| trader_no | varchar(30) | N | √ | 交易员 |
| base_amt | numeric(24,6) | Y |  | 申购金额 |
| real_amt | numeric(24,6) | Y |  | 已申购金额 |
| base_qty | numeric(24,6) | Y |  | 赎回克重 |
| real_qty | numeric(24,6) | Y |  | 已赎回克重 |
| base_price | numeric(20,6) | Y |  | 定投报价 |
| real_price | numeric(20,6) | Y |  | 实际均价 |
| net_integrate | numeric(20,6) | Y |  | 当日净轧差头寸 |
| sum_net_integrate | numeric(20,6) | Y |  | 累计净轧差头寸 |
| net_amt | numeric(24,6) | Y |  | 当日净轧差金额 |
| sum_net_amt | numeric(24,6) | Y |  | 累计净轧差金额 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |

---

## 55. dimple.tc_alarm_note　(10 字段)
> 表含义：敞口/止损报警信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| alarm_type | bpchar(1) | N | √ | 报警类型(敞口/止损):见tp_public_dict的232 |
| alarm_time | varchar(8) | N |  | 报警时间 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| variety_id | varchar(4) | N |  | 品种 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| alarm_note | varchar(254) | Y |  | 报警信息 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 56. dimple.tc_alm_order_clear　(3 字段)
> 表含义：累计黄金投资成本表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| daily_turnover | numeric(20,6) | Y |  | 当日成交金额 |
| cumulative_gold_investment_cost | numeric(20,6) | Y |  | 累计黄金投资总成本 |

---

## 57. dimple.tc_amout_limit_config　(10 字段)
> 表含义：额度和限额参数管理表　|　估算行数：**6**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种:根据参数类型设置，默认- |
| contract_id | varchar(20) | N | √ | 合约代码:根据参数类型设置，默认- |
| config_type | varchar(4) | N | √ | 参数类型：见tp_public_dict的334 |
| alarm_value | numeric(18,2) | Y |  | 预警阀值 |
| limit_value | numeric(18,2) | Y |  | 极限值 |
| set_date | varchar(8) | N |  | 设置日期 |
| real_value | numeric(18,2) | Y |  | 实时数据 |
| if_over | varchar(3) | Y |  | 超限标志：见tp_public_dict的027 |

---

## 58. dimple.tc_boc_account_relation　(4 字段)
> 表含义：中行员工号账号信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| employeeid | varchar(40) | N |  | 员工号 |
| employeename | varchar(160) | Y |  | 员工姓名 |
| status | varchar(40) | Y |  | 员工状态 |
| oparedate | varchar(9) | Y |  | 最后修改时间 |

---

## 59. dimple.tc_bond_delivery_manager_jour　(16 字段)
> 表含义：债券交割分配流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N | √ | 录入日期 |
| input_seq_no | float8 | N | √ | 录入流水号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| seq_no | float8 | N | √ | 分配流水号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| variety_id | varchar(4) | Y |  | 品种代码 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| user_id | varchar(30) | Y |  | 交易员号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| qty | numeric(12,0) | Y |  | 数量 |
| oper_type | varchar(3) | Y |  | 操作类型：见数据字典267 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作员 |

---

## 60. dimple.tc_branches　(5 字段)
> 表含义：经营单位　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| branch_code | varchar(15) | N | √ | 网点号 |
| branch_abbr | varchar(150) | Y |  | 网点简称 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 61. dimple.tc_broker　(4 字段)
> 表含义：经纪机构信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| broker_no | varchar(10) | N | √ | 经纪机构代码 |
| broker_abbr | varchar(400) | N |  | 经纪机构简称 |
| broker_ename | varchar(100) | Y |  | 经纪机构英文简称 |
| broker_user | varchar(100) | Y |  | 经纪机构用户 |

---

## 62. dimple.tc_buy_ilease_match　(26 字段)
> 表含义：境内租赁买断成交　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| buy_no | varchar(30) | N | √ | 买断编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lease_flag | varchar(3) | Y |  | 拆借方向：B本方借出/C本方借入 见tp_public_dict的221 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记编号 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |

---

## 63. dimple.tc_buy_lease_match　(26 字段)
> 表含义：境内租赁买断成交　|　估算行数：**17**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| buy_no | varchar(30) | N | √ | 买断编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lease_flag | varchar(3) | Y |  | 拆借方向：B本方借出/C本方借入 见tp_public_dict的221 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记编号 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |

---

## 64. dimple.tc_buy_lease_match_jour　(26 字段)
> 表含义：境内租赁买断成交流水　|　估算行数：**72**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| buy_no | varchar(30) | Y |  | 买断编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lease_flag | varchar(3) | Y |  | 拆借方向：B本方借出/C本方借入 见tp_public_dict的221 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记编号 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |

---

## 65. dimple.tc_buy_lend_match　(28 字段)
> 表含义：境内买断成交　|　估算行数：**15**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| buy_no | varchar(30) | N | √ | 买断编号 |
| agreement_sn | varchar(30) | N | √ | 金交所租借登记号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| delivery_rate_tot | varchar(8) | Y |  | 利率（总部） |
| isimported | varchar(3) | Y |  | 是否导入 |

---

## 66. dimple.tc_buy_lend_match_jour　(26 字段)
> 表含义：境内买断成交流水　|　估算行数：**68**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| buy_no | varchar(30) | Y |  | 买断编号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |

---

## 67. dimple.tc_calc_storage　(11 字段)
> 表含义：客户库存流表　|　估算行数：**13**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| tdate | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |
| delivery_variety_name | varchar(90) | Y |  | 交割品种及名称 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| purpose_name | varchar(200) | Y |  | 交易目的名称 |
| st_origin | numeric(24,6) | Y |  | 期初库存量（千克） |
| st_in | numeric(24,6) | Y |  | 入库量（千克） |
| st_out | numeric(24,6) | Y |  | 出库量（千克） |
| st_final | numeric(24,6) | Y |  | 期末库存量（千克） |

---

## 68. dimple.tc_calendar_date　(12 字段)
> 表含义：日维度表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cal_date_id | numeric(12,0) | N | √ | 日标识 |
| cal_month_id | numeric(12,0) | Y |  | 月标识 |
| cal_week_id | numeric(12,0) | Y |  | 周标识 |
| cal_date | varchar(8) | Y |  | 日期 |
| day_of_week | varchar(80) | Y |  | 星期几 |
| day_nr_in_cal_mth | numeric(12,0) | Y |  | 月的第几天 |
| day_nr_in_cal_year | numeric(12,0) | Y |  | 年的第几天 |
| cal_month_nr | numeric(12,0) | Y |  | 日期所属的月份 |
| cal_year | numeric(12,0) | Y |  | 日期所属的年份 |
| cal_month_name | varchar(254) | Y |  | 月名称 |
| population_timestamp | varchar(8) | Y |  | 数据装载时间 |
| source_system_label | varchar(80) | Y |  | 源系统标签 |

---

## 69. dimple.tc_calendar_month　(6 字段)
> 表含义：月维度表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cal_month_id | numeric(12,0) | N | √ | 月标识 |
| cal_month_name | varchar(254) | Y |  | 月名称 |
| cal_month_nr | numeric(12,0) | Y |  | 月号码 |
| cal_year_id | numeric(12,0) | Y |  | 年标识 |
| population_timestamp | varchar(8) | Y |  | 数据装载时间 |
| source_system_label | varchar(80) | Y |  | 源系统标签 |

---

## 70. dimple.tc_calendar_week　(8 字段)
> 表含义：周维度表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cal_week_id | numeric(12,0) | N | √ | 周标识 |
| cal_week_name | varchar(254) | Y |  | 周名称 |
| cal_week_begin | varchar(8) | Y |  | 周的开始时间 |
| cal_week_end | varchar(8) | Y |  | 周的结束时间 |
| week_nr_in_cal_year | numeric(12,0) | Y |  | 周在一年的序数 |
| week_nr_in_all | numeric(12,0) | Y |  | 周的序数 |
| population_timestamp | varchar(8) | Y |  | 数据装载时间 |
| source_system_label | varchar(80) | Y |  | 源系统标签 |

---

## 71. dimple.tc_calendar_year　(4 字段)
> 表含义：年维度表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cal_year_id | numeric(12,0) | N | √ | 年标识 |
| cal_year | varchar(254) | Y |  | 年名称 |
| population_timestamp | varchar(8) | Y |  | 数据装载时间 |
| source_system_label | varchar(80) | Y |  | 源系统标签 |

---

## 72. dimple.tc_center_cost_manage　(8 字段)
> 表含义：成本中心参数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_code | varchar(40) | N | √ | 交易员代码 |
| exch_code | varchar(4) | N | √ | 交易所代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| center_desc | varchar(20) | Y |  | 成本中心 |
| center_port | varchar(20) | Y |  | PORT |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| trade_type | varchar(3) | N | √ | 交易类型：见tp_public_dict的001 |

---

## 73. dimple.tc_cffex_bond_delivery_match　(24 字段)
> 表含义：交割配对文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(20) | N |  | 导入日期 |
| apply_date | varchar(20) | Y |  | 匹配日期 |
| trade_date | varchar(20) | Y |  | 配对缴款日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(20) | Y |  | 买卖标志 |
| client_id | varchar(20) | Y |  | 客户号 |
| member_id | varchar(8) | Y |  | 会员号 |
| qty | numeric(12,0) | Y |  | 交割数量 |
| price | numeric(20,8) | Y |  | 交割结算价 |
| bond_id | varchar(20) | Y |  | 交割券代码 |
| bond_name | varchar(100) | Y |  | 交割券名称 |
| trans_conf | numeric(20,8) | Y |  | 转换因子 |
| accru_interest | numeric(22,2) | Y |  | 应缴应计利息 |
| delivery_amt | numeric(22,2) | Y |  | 应缴交割货款 |
| real_qty | numeric(12,0) | Y |  | 交割履约量 |
| real_accru_interest | numeric(22,2) | Y |  | 实际应计利息 |
| real_delivery_amt | numeric(22,2) | Y |  | 实际交割货款 |
| buy_breach_qty | numeric(12,0) | Y |  | 买交割违约量 |
| sell_breach_qty | numeric(12,0) | Y |  | 卖交割违约量 |
| both_breach_qty | numeric(12,0) | Y |  | 双方交割违约数量 |
| breach_amt | numeric(22,2) | Y |  | 罚金 |
| redee_amt_in | numeric(22,2) | Y |  | 收取补偿金 |
| redee_amt_out | numeric(22,2) | Y |  | 支付补偿金 |
| deliv_mode | varchar(8) | Y |  | 交割模式：见tp_public_dict的368 |

---

## 74. dimple.tc_cffex_bond_delivery_order　(13 字段)
> 表含义：交割匹配文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(20) | N |  | 导入日期 |
| seq_no | float8 | Y |  | 序号 |
| trade_date | varchar(20) | Y |  | 交易日期 |
| variety_id | varchar(20) | Y |  | 品种代码 |
| contract_id | varchar(20) | Y |  | 合约号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(20) | Y |  | 客户号 |
| bs_flag | varchar(20) | Y |  | 买卖标志 |
| order_qty | numeric(12,0) | Y |  | 申请数量 |
| qty | numeric(12,0) | Y |  | 匹配数量 |
| price | numeric(20,8) | Y |  | 价格 |
| delivery_margin | numeric(22,2) | Y |  | 交割保证金 |
| delivery_fee | numeric(22,2) | Y |  | 交割手续费 |

---

## 75. dimple.tc_cffex_delivery_money　(19 字段)
> 表含义： 中金所资金文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(20) | N |  | 导入日期 |
| seq_no | varchar(20) | Y |  | 编号 |
| trade_date | varchar(20) | Y |  | 交易日期 |
| variety_id | varchar(20) | Y |  | 品种代码 |
| contract_id | varchar(20) | Y |  | 合约号 |
| clear_member_id | varchar(20) | Y |  | 结算会员号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(20) | Y |  | 客户号 |
| bs_flag | varchar(20) | Y |  | 买卖标志 |
| trust_org | varchar(100) | Y |  | 托管机构 |
| bond_id | varchar(20) | Y |  | 债券编码 |
| delivery_qty | numeric(12,0) | Y |  | 交割数量 |
| breach_qty | numeric(12,0) | Y |  | 违约数量 |
| counter_breach_qty | numeric(12,0) | Y |  | 对手方违约数量 |
| price | numeric(20,8) | Y |  | 价格 |
| delivery_amt | numeric(22,2) | Y |  | 交割金额 |
| breach_amt | numeric(22,2) | Y |  | 违约金 |
| redee_amt | numeric(22,2) | Y |  | 支付补偿金 |
| real_redee_amt | numeric(22,2) | Y |  | 收取补偿金 |

---

## 76. dimple.tc_cffex_money_io_detail　(9 字段)
> 表含义：中金所:收入与付出资金明细栏　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 导入日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| sheet_no | varchar(50) | Y |  | 单据号 |
| money_type | varchar(50) | Y |  | 名称 |
| amt | varchar(50) | Y |  | 金额 |
| io_type | varchar(50) | Y |  | 收支方式 |
| input_date | varchar(8) | Y |  | 录入日期 |
| effect_date | varchar(8) | Y |  | 到帐日期 |

---

## 77. dimple.tc_cfg_account_purpose　(4 字段)
> 表含义：成本中心账务配置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | numeric(12,0) | N | √ | 序号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| account_type | varchar(3) | Y |  | 账务类型：见dict 313 |
| config_code | varchar(3) | N | √ | 银行配置: 见para的ACCOUNT_CTL_TYPE |

---

## 78. dimple.tc_cfg_account_tradetype　(5 字段)
> 表含义：成本中心账务配置表　|　估算行数：**81**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| para_type | varchar(3) | N | √ | 参数类型 001 交易类型 221 库存流水类型 |
| trade_type | varchar(3) | N | √ | 交易类型: 见dit 001 、221 |
| sub_type | varchar(3) | N | √ | 子类型：  见dict 253 |
| account_type | varchar(3) | Y |  | 账务类型：见dict 313 |
| config_code | varchar(3) | N | √ | 银行配置: 见para的ACCOUNT_CTL_TYPE |

---

## 79. dimple.tc_cfg_largeside_instgroup　(4 字段)
> 表含义：大边保证金品种组合表:仅包含中金所和上期所数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N |  | 交易所代码:见tp_public_dict的217 |
| group_no | numeric(10,0) | N |  | 组合代码 |
| group_name | varchar(20) | Y |  | 组合名称 |
| variety_id | varchar(4) | N |  | 品种代码 |

---

## 80. dimple.tc_cfg_storage　(18 字段)
> 表含义：库存计算控制表　|　估算行数：**4,162**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| config_code | varchar(3) | N | √ | 银行配置: 见para的ACCOUNT_CTL_TYPE |
| trans_type | varchar(3) | N | √ | 库存变化类型 |
| trans_name | varchar(60) | Y |  | 库存变化名称 |
| calc_lv | varchar(3) | N | √ | 计算级别:1 客户 2 交易员 |
| total_comput_type | varchar(3) | Y |  | 全部库存: -1 减 0 不变 1 加 |
| available_comput_type | varchar(3) | Y |  | 可用库存: -1 减 0 不变 1 加 |
| law_frozen_comput_type | varchar(3) | Y |  | 法律冻结库存/手工冻结库存: -1 减 0 不变 1 加 |
| pend_comput_type | varchar(3) | Y |  | 待提库存: -1 减 0 不变 1 加 |
| mort_comput_type | varchar(3) | Y |  | 质押库存: -1 减 0 不变 1 加 |
| etf_frozen_comput_type | varchar(3) | Y |  | ETF冻结库存: -1 减 0 不变 1 加 |
| cost_comput_type | varchar(3) | Y |  | 成本: -1 减 0 不变 1 加 |
| credit_comput_type | varchar(3) | Y |  | 是否计算买卖货款：0-否；1-是 |
| vaexp_comput_type | varchar(3) | Y |  | 敞口: -1 减 0 不变 1 加（未使用） |
| integrate_comput_type | varchar(3) | Y |  | 综合头寸: -1 减 0 不变 1 加 |
| calc_seq | varchar(3) | Y |  | 计算顺序：计算成本时先后顺序 |
| setoff_frz_comput_type | varchar(3) | Y |  | 充抵冻结库存:-1 减 0 不变 1 加 |
| transfer_frz_comput_type | varchar(3) | Y |  | 过户业务冻结库存:-1 减 0 不变 1 加 |
| if_support_current | varchar(3) | Y |  | 当前版本是否支持：0-否；1-是 |

---

## 81. dimple.tc_cfg_valueadded_tax_rate　(2 字段)
> 表含义：成本计算增值税率表：成本计算时使用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |
| tax_rate | numeric(24,6) | Y |  | 增值税税率 |

---

## 82. dimple.tc_check_purpose_config　(14 字段)
> 表含义：交易目的复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| check_status | varchar(1) | N |  | 复核状态:见tp_public_dict的494 |
| pcode | varchar(3) | N |  | 交易目的代码 |
| pname | varchar(40) | Y |  | 交易目的简称 |
| fcode | varchar(3) | Y |  | 上级交易目的代码 |
| status | varchar(3) | Y |  | 状态:见tp_public_dict的012 |
| remark | varchar(200) | Y |  | 类型描述 |
| op_type | varchar(1) | Y |  | 操作类型:见tp_public_dict的091 |
| operator | varchar(20) | Y |  | 操作人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_time | varchar(8) | Y |  | 复核时间 |
| strategy_id | varchar(10) | Y |  | 交易策略ID |

---

## 83. dimple.tc_check_srcb_account　(9 字段)
> 表含义：帐务核对表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 对账日期 |
| id | varchar(3) | Y |  | 物理ID |
| source_id | varchar(3) | Y |  | 数据来源 |
| content | varchar(60) | Y |  | 对应字段 |
| amount | numeric(24,6) | Y |  | 系统内金额 |
| account_sysno | varchar(30) | N | √ | 核心内部账户 |
| amount_hx | numeric(24,6) | Y |  | 核心金额 |
| check_result | varchar(3) | Y |  | 对账结果：见tp_public_dict 391 |
| difference_amount | numeric(24,6) | Y |  | 差异金额 |

---

## 84. dimple.tc_clear_date　(1 字段)
> 表含义：结算日期:日终结算时写入，总比交易日期晚一天。日终结算时产生持仓，资金数据的日期均是此表的最新日期。　|　估算行数：**91**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |

---

## 85. dimple.tc_clear_log　(6 字段)
> 表含义：结算日志表　|　估算行数：**138,061**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | float8 | N | √ | 流水号 |
| op_date | varchar(8) | N | √ | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_msg | varchar(1000) | Y |  | 操作内容 |
| status | bpchar(1) | Y |  | 状态 |
| sys_status | varchar(2) | Y |  | 系统状态:见tp_public_code的030 |

---

## 86. dimple.tc_clear_money　(35 字段)
> 表含义：结算资金表:2.4.4版本开始不再计算此表，作废　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| init_margin | numeric(18,2) | Y |  | 初始准备金:=上日结算余额 |
| delivery_margin | numeric(18,2) | Y |  | 交割保证金 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏:可从期货客户持仓表汇总得到 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏:可从期货客户持仓表汇总得到 |
| buy_premium | numeric(18,2) | Y |  | 权利金支出 |
| sell_premium | numeric(18,2) | Y |  | 权利金收入 |
| trade_fee | numeric(18,2) | Y |  | 手续费:可从期货客户持仓表汇总得到 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费:可从短线汇总表汇总得到 |
| margin | numeric(18,2) | Y |  | 交易保证金:可从持仓表汇总得到 |
| mort_amt | numeric(24,6) | Y |  | 质押金额:可从质押金额表得到 |
| money_in | numeric(18,2) | Y |  | 当日入金 |
| money_out | numeric(18,2) | Y |  | 当日出金 |
| cash | numeric(18,2) | Y |  | 现金:=上日结算余额＋上日交易保证金－上日质押金额＋当日入金－当日出金＋平仓盈亏＋持仓盈亏＋权利金收入－权利金支出＋其他金额－手续费＋返回手续费 (其中上日质押金额来自质押金额表) |
| other_money | numeric(18,2) | Y |  | 其他金额 |
| remain | numeric(18,2) | Y |  | 结算余额:=上日结算余额＋上日交易保证金＋当日入金－当日出金＋平仓盈亏＋持仓盈亏＋权利金收入－权利金支出＋其他金额－手续费＋返回手续费＋今日质押金额－上日质押金额－交易保证金 |
| prepare_margin | numeric(18,2) | Y |  | 开仓准备金:=结算余额 |
| last_margin | numeric(18,2) | Y |  | 昨日保证金 |
| call_margin | numeric(18,2) | Y |  | 追加保证金 |
| force_amt | numeric(24,6) | Y |  | 强平金额 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| frozen_profitloss | numeric(18,2) | Y |  | 盈亏冻结 |
| last_frozen_profitloss | numeric(18,2) | Y |  | 上日盈亏冻结 |
| frozen_amount | numeric(18,2) | Y |  | 货款冻结 |
| last_frozen_amount | numeric(18,2) | Y |  | 上日货款冻结 |
| ag_frozen_amount | numeric(18,2) | Y |  | 白银货款冻结 |
| manual_frozen_amount | numeric(18,2) | Y |  | 手工货款冻结 |
| last_ag_frozen_amount | numeric(18,2) | Y |  | 上日白银货款冻结 |
| last_manual_frozen_amount | numeric(18,2) | Y |  | 上日手工货款冻结 |
| last_trade_margin | numeric(18,2) | Y |  | 上日交易保证金 |
| last_delivery_margin | numeric(18,2) | Y |  | 上日交割保证金 |

---

## 87. dimple.tc_clear_posi_detail　(15 字段)
> 表含义：结算持仓明细表　|　估算行数：**19,016,509**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| match_batch_no | varchar(20) | N | √ | 成交批次号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| trader_no | varchar(16) | Y |  | 席位号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |

---

## 88. dimple.tc_clear_posi_detail_purpose　(16 字段)
> 表含义：交易目的结算持仓明细表　|　估算行数：**19,439**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| match_batch_no | varchar(20) | N |  | 成交批次号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 89. dimple.tc_clear_posi_detail_trader　(17 字段)
> 表含义：交易员结算持仓明细表　|　估算行数：**4,001,716**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| match_batch_no | varchar(20) | N |  | 成交批次号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 90. dimple.tc_clear_price　(6 字段)
> 表含义：结算价表:闭市后处理产生。数据来自于行情表和手工结算价表，日终结算使用此表数据。在最后交割日此表存放的是交割结算价。　|　估算行数：**435,880**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| last_clear_price | numeric(20,8) | N |  | 昨日结算价 |
| clear_price | numeric(20,8) | N |  | 结算价 |
| if_manual | varchar(3) | Y |  | 是否手工 |
| remark | varchar(255) | Y |  | 参考价格说明 |

---

## 91. dimple.tc_clear_state_ctrl　(6 字段)
> 表含义：结算状态控制表:记录闭市后处理到日终结算完成的状态，控制用。　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| start_date | varchar(8) | N |  | 开始结算日期 |
| end_date | varchar(8) | N |  | 终止结算日期 |
| run_status | varchar(2) | N |  | 运行状态:60,闭市后处理中;80,结算中;90,结算完成;99,结算中止;00,盘后结算结束 |
| if_repeat | bpchar(1) | N |  | 是否重复结算 |
| stop_flag | bpchar(1) | N |  | 停止标志:0,不停止;1,停止 |

---

## 92. dimple.tc_client_buyout_detial_clear　(15 字段)
> 表含义：境外客户买断明细表　|　估算行数：**24**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| buy_trade_date | varchar(8) | N | √ | 买断成交日期 |
| lend_trade_date | varchar(8) | N |  | 拆借成交日期 |
| match_no | varchar(30) | N | √ | 成交号 |
| seq_no | float8 | N | √ | 系统编号 |
| buy_no | varchar(30) | N | √ | 买断编号 |
| lend_flag | varchar(3) | N | √ | 拆借方向:public_dict的221只包含拆入和拆出 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 买断价格 |
| qty | numeric(16,6) | Y |  | 买断数量 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| profit | numeric(24,6) | Y |  | 盈亏 |
| trade_type | varchar(3) | N | √ | 交易类型：见tp_public_dict的298 |

---

## 93. dimple.tc_client_cash_detail_clear　(16 字段)
> 表含义：客户现金交割明细表　|　估算行数：**2,120**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| trade_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(30) | N | √ | 成交号 |
| bs_flag | varchar(3) | N | √ | 买卖方向:public_dict的002 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| delivery_variety_id | varchar(3) | Y |  | 品种号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(24,6) | Y |  | 成交价格 |
| qty | numeric(20,3) | Y |  | 成交数量 |
| match_type | varchar(3) | Y |  | 类型：1普通 |
| calc_price_type | varchar(3) | Y |  | 参考价格类型：1开盘价;2收盘价;3结算价;4基准价(上午);5基准价(下午);6固定值;7基准价夜市;9其他价格 |
| calc_price_date | varchar(8) | Y |  | 参考价格日期 |
| calc_price | numeric(24,6) | Y |  | 参考价格 |
| clear_price | numeric(24,6) | Y |  | 当日结算价 |
| profit | numeric(30,6) | Y |  | 盈亏 |

---

## 94. dimple.tc_client_contract_cost　(9 字段)
> 表含义：合约成本结算表 合约包括期货、递延　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| remain_qty | numeric(12,0) | Y |  | 剩余数量 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本 |
| realized_profitloss | numeric(18,2) | Y |  | 实现盈亏 |

---

## 95. dimple.tc_client_contract_cost_detail　(16 字段)
> 表含义：合约成本明细结算表 合约包括期货、递延　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| seq_no | varchar(10) | N | √ | 流水号 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| eo_flag | bpchar(1) | N |  | 开平标志:见tp_public_dict的003 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| amt | numeric(24,6) | Y |  | 金额 |
| last_remain_qty | numeric(12,0) | Y |  | 上次剩余数量 |
| remain_qty | numeric(12,0) | Y |  | 剩余数量 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本 |
| realized_profitloss | numeric(18,2) | Y |  | 实现盈亏 |

---

## 96. dimple.tc_client_cost_clear　(8 字段)
> 表含义：品种成本结算表 品种内容包含现货、境外黄金、期货、黄金T+D　|　估算行数：**32,727**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量（千克） |
| remain_cost | numeric(24,6) | Y |  | 剩余成本（元） |
| realized_profitloss | numeric(22,6) | Y |  | 实现盈亏 |

---

## 97. dimple.tc_client_cost_dayavg_clear　(13 字段)
> 表含义：品种每日平均成本结算表 品种内容包含现货、境外黄金、期货、黄金T+D　|　估算行数：**2,738**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |
| buy_qty | numeric(25,8) | Y |  | 当日买入量（千克） |
| buy_amt | numeric(24,6) | Y |  | 当日买入金额 |
| sell_qty | numeric(25,8) | Y |  | 当日卖出量（千克） |
| sell_amt | numeric(24,6) | Y |  | 当日卖出金额 |
| sell_cost | numeric(24,6) | Y |  | 当日卖出成本 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量（千克） |
| remain_cost | numeric(24,6) | Y |  | 剩余成本（元） |
| realized_profitloss | numeric(18,2) | Y |  | 实现盈亏 |

---

## 98. dimple.tc_client_cost_detail_clear　(19 字段)
> 表含义：品种成本明细结算表 品种内容包含现货、境外黄金、期货、黄金T+D　|　估算行数：**11,254**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |
| seq_no | varchar(10) | N | √ | 流水号 |
| exch_seq_no | varchar(16) | N |  | 交易所流水号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| trans_type | varchar(2) | Y |  | 库存变化类型:见tp_public_dict的221 |
| price | numeric(20,8) | Y |  | 价格：黄金为元/克，白银：元/千克；境外黄金为 美元/盎司 |
| qty | numeric(25,8) | Y |  | 数量:现货为千克；境外黄金为盎司 |
| amt | numeric(24,6) | Y |  | 成交金额（配置税率后不含税）:现货为元；境外黄金为美元 |
| amt_han | numeric(24,6) | Y |  | 成交金额（含税）:现货为元；境外黄金为美元 |
| last_remain_qty | numeric(25,8) | Y |  | 上次剩余数量（千克、盎司），卖空时为负 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量：现货为千克；境外黄金为盎司，卖空时为负 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：现货黄金为元/克，白银：元/千克；境外黄金为 美元/盎司 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：现货为元；境外黄金为美元 |
| realized_profitloss | numeric(22,6) | Y |  | 实现盈亏 |
| last_remain_cost | numeric(24,6) | Y |  | 上次剩余成本：现货为元；境外黄金为 美元 |
| last_weighted_price | numeric(20,8) | Y |  | 上次加权平均价：黄金为元/克，白银：元/千克 |

---

## 99. dimple.tc_client_member_purpose　(11 字段)
> 表含义：交易目的与交易编码对应关系表　|　估算行数：**18**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| exch_abbr | varchar(40) | Y |  | 交易所简称 |
| member_id | varchar(8) | N | √ | 会员号 |
| member_abbr | varchar(50) | Y |  | 会员号简称 |
| client_id | varchar(16) | N | √ | 客户号 |
| client_abbr | varchar(50) | Y |  | 客户号简称 |
| purpose_code | varchar(3) | N | √ | 交易目的代码 |
| purpose_name | varchar(200) | Y |  | 交易目的名称 |
| op_oper | varchar(30) | N |  | 操作员 |
| op_date | varchar(8) | N |  | 操作日期 |
| op_time | varchar(8) | N |  | 操作时间 |

---

## 100. dimple.tc_client_quote_posi_clear　(17 字段)
> 表含义：报价商持仓结算表　|　估算行数：**257**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | N | √ | 客户代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| last_buy_qty | numeric(18,0) | Y |  | 上一日多头持仓量 |
| last_sell_qty | numeric(18,0) | Y |  | 上一日空头持仓量 |
| buy_qty | numeric(18,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(18,0) | Y |  | 空头持仓量 |
| t_buy_qty | numeric(18,0) | Y |  | 今日买入量 |
| t_buy_amt | numeric(24,6) | Y |  | 今日买入金额 |
| t_sell_qty | numeric(18,0) | Y |  | 今日卖出量 |
| t_sell_amt | numeric(24,6) | Y |  | 今日卖出金额 |
| profitloss | numeric(24,6) | Y |  | 每日无负债交易盈亏:目前浦发出账使用;公式=今日每笔交易的损益+昨日交易轧差损益 |
| margin | numeric(20,2) | Y |  | 保证金 = 持仓头寸轧差*结算价*交易单位*报价单位*保证金率 |
| clear_price | numeric(20,6) | Y |  | 结算价 |
| buy_avg_price | numeric(20,6) | Y |  | 多头持仓均价 |
| sell_avg_price | numeric(20,6) | Y |  | 空头持仓均价 |

---

## 101. dimple.tc_client_storage　(12 字段)
> 表含义：客户交易库存表　|　估算行数：**28**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| frozen_storage | numeric(16,6) | Y |  | 冻结库存 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| etf_frozen_storage | numeric(16,6) | Y |  | 认申赎冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 102. dimple.tc_client_storage_adjust　(15 字段)
> 表含义：客户库存管理表 - 交行境外库存处理使用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 入库日期 |
| seq_no | varchar(10) | N | √ | 流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| trans_type | varchar(2) | N |  | 库存变化类型:见tp_public_dict的221 |
| qty | numeric(15,3) | N |  | 数量（千克） |
| price | numeric(20,8) | N |  | 价格 |
| amt | numeric(24,6) | N |  | 交易金额 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| origin_seq_no | varchar(10) | Y |  | 原交易所流水号 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |

---

## 103. dimple.tc_client_storage_clear　(12 字段)
> 表含义：客户结算库存表　|　估算行数：**20,916**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| etf_frozen_storage | numeric(16,6) | Y |  | 认申赎冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 104. dimple.tc_client_storage_jour　(21 字段)
> 表含义：客户库存流水表　|　估算行数：**2,952**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 入库日期 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号 |
| sheet_no | varchar(20) | Y |  | 票据号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| trans_type | varchar(2) | N |  | 库存变化类型:见tp_public_dict的221 |
| qty | numeric(15,3) | Y |  | 数量（千克） |
| price | numeric(20,8) | Y |  | 价格 |
| storage_flag | bpchar(1) | N |  | 库存标志:见tp_public_dict的229 |
| io_flag | bpchar(1) | N |  | 出入库标志:见tp_public_dict的230 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |
| amt | numeric(24,6) | Y |  | 原发票金额 |
| contract_id | varchar(20) | Y |  | 合约号 |
| stock_source | bpchar(1) | Y |  | 出入库性质,见tp_public_dict的236 |
| storage_no | varchar(4) | Y |  | 仓库号,见tp_public_dict的244 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| effect_date | varchar(8) | N | √ | 生效日期 |
| deal_amt | numeric(24,6) | Y |  | 交易金额 |

---

## 105. dimple.tc_cmb_account　(7 字段)
> 表含义：招行账务文件表　|　估算行数：**20**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | varchar(30) | Y |  | 流水号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| lend_account | varchar(20) | Y |  | 借方资金账号 |
| borrow_account | varchar(20) | Y |  | 贷方资金账号 |
| amt | numeric(24,6) | Y |  | 发生额 |
| remark | varchar(255) | Y |  | 备注 |
| exch_code | varchar(2) | Y |  | 交易所代码 |

---

## 106. dimple.tc_cmb_account_defer　(11 字段)
> 表含义：招商银行-账务递延买卖表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量 |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |

---

## 107. dimple.tc_cmb_account_future　(14 字段)
> 表含义：招商银行-账务债券期货业务　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 108. dimple.tc_cmb_account_manage　(7 字段)
> 表含义：招商银行-账务管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 序号 |
| total_count | numeric(20,0) | Y |  | 总记录数 |
| send_count | numeric(20,0) | Y |  | 发送记录数 |
| status | varchar(3) | Y |  | 状态:1未生成;2 已生成未发送;3发送中;4发送成功;5发送失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 109. dimple.tc_cmb_check_error　(19 字段)
> 表含义：招商银行-账务核对错误信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| error_type | varchar(5) | N | √ | 错误类型 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trade_date | varchar(11) | N | √ | 交易日期 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| amt | numeric(24,6) | Y |  | 金额 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| bus_type | varchar(20) | Y |  | 业务大类:竞价交易,询价成交,询价交割,询价期权 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| cfets_match_no | varchar(20) | Y |  | 外汇交易中心系统交易编号 |
| match_type | varchar(5) | Y |  | 业务类型 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| fn_flag | varchar(3) | Y |  | 近远端 |

---

## 110. dimple.tc_cmb_check_status　(7 字段)
> 表含义：招商银行-数据核对状态表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 序号 |
| total_count | numeric(20,0) | Y |  | 总记录数 |
| send_count | numeric(20,0) | Y |  | 发送记录数 |
| status | varchar(3) | Y |  | 状态:1未生成;2 已生成未发送;3发送中;4发送成功;5发送失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 111. dimple.tc_cmb_contract_mapping　(9 字段)
> 表含义：合约映射配置表(Murex信创)　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | numeric(32,0) | N | √ | 自增主键 |
| contract_id | varchar(20) | N |  | Dimple合约代码 |
| instrument | varchar(20) | N |  | Instrument商品标签(Murex) |
| mx_index | varchar(50) | N |  | mxIndex商品标的(Murex) |
| future_label | varchar(50) | Y |  | futureLabel期货标签(Murex) |
| variety_type | varchar(10) | Y |  | 品种类型(au-黄金,ag-白银) |
| unit | varchar(25) | Y |  | 商品单位 |
| create_time | timestamp | Y |  | 创建时间 |
| update_time | timestamp | Y |  | 更新时间 |

---

## 112. dimple.tc_cmb_fee_type_config　(9 字段)
> 表含义：费用类型配置文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | numeric(32,0) | N | √ | 自增主键 |
| murex_fee_type | varchar(10) | Y |  | Murex费用类型 |
| exch_fee_detail | varchar(500) | Y |  | 交易所费用明细（交易所枚举值，多个以逗号分隔） |
| portfolio | varchar(50) | Y |  | 投资组合 |
| acc_type | varchar(50) | Y |  | 账务类型 |
| acc_prd | varchar(20) | Y |  | 账务产品 |
| acc_stm | varchar(10) | Y |  | 账务状态 |
| create_time | timestamp | Y |  | 创建时间 |
| update_time | timestamp | Y |  | 更新时间 |

---

## 113. dimple.tc_cmb_his_account　(8 字段)
> 表含义：招行账务文件历史表　|　估算行数：**899**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| seq_no | varchar(30) | Y |  | 流水号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| lend_account | varchar(20) | Y |  | 借方资金账号 |
| borrow_account | varchar(20) | Y |  | 贷方资金账号 |
| amt | numeric(24,6) | Y |  | 发生额 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| remark | varchar(255) | Y |  | 备注 |

---

## 114. dimple.tc_cmb_his_account_defer　(10 字段)
> 表含义：招商银行-账务递延买卖历史表　|　估算行数：**421**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |

---

## 115. dimple.tc_cmb_his_account_future　(13 字段)
> 表含义：招商银行-账务债券期货业务历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |

---

## 116. dimple.tc_cmb_inq_match_after_clear　(38 字段)
> 表含义：招行询价登记单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| match_no | varchar(20) | N | √ | 成交单号 |
| agreement_sn | varchar(30) | Y |  | 报价单编号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| match_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的253 |
| trade_type | varchar(3) | N | √ | 交易类型：见tp_public_dict的253只包含即期和远期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| member_id | varchar(8) | N | √ | 会员号 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| trade_party | varchar(40) | Y |  | 对手方代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| inquire_type | varchar(3) | Y |  | 交易类别：见Dict的325 |
| qty | numeric(24,6) | Y |  | 数量：单位Au为克 Ag为千克 =手数*合约乘数 |
| price | numeric(20,8) | Y |  | 近端价格:Au 人民币元/克、Ag 人民币元/千克 |
| amt | numeric(20,2) | Y |  | 近端金额：手数*价格*unit |
| delivtype | varchar(3) | Y |  | 近端交割方式：见tp_public_dict的051 |
| reference_type | varchar(3) | Y |  | 近端参考价类型：见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 近端参考价日期 |
| reference_price | numeric(20,8) | Y |  | 近端参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 近端参考价格调整项 |
| due_date | varchar(8) | Y |  | 近端到期日 |
| far_price | numeric(20,8) | Y |  | 远端价格:Au 人民币元/克、Ag 人民币元/千克 |
| far_amt | numeric(20,2) | Y |  | 远端金额：手数*价格*unit |
| far_delivtype | varchar(3) | Y |  | 远端交割方式：见tp_public_dict的051 |
| far_reference_type | varchar(3) | Y |  | 远端参考价类型：见tp_public_dict的288 |
| far_reference_date | varchar(8) | Y |  | 远端参考价日期 |
| far_reference_price | numeric(20,8) | Y |  | 远端参考价格 |
| far_reference_adjust | numeric(20,8) | Y |  | 远端参考价格调整项 |
| far_due_date | varchar(8) | Y |  | 远端到期日 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |

---

## 117. dimple.tc_cmb_inq_opt_after_clear　(53 字段)
> 表含义：招行询价期权登记单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| inq_match_no | varchar(20) | Y |  | 询价系统成交编号 |
| match_no | varchar(20) | Y |  | 主系统成交编号/报价单编号 |
| contract_id | varchar(20) | Y |  | 期权合约代码 |
| member_id | varchar(8) | Y |  | 本方会员席位代码 |
| party_member_id | varchar(8) | Y |  | 对手方会员席位代码 |
| trader_no | varchar(16) | Y |  | 本方交易员代码 |
| bs_flag | varchar(3) | Y |  | 本方交易方向 |
| match_date | varchar(8) | Y |  | 询价成交日期 |
| qty | numeric(12,0) | Y |  | 成交数量 |
| opt_trade_type | varchar(3) | Y |  | 期权交易类型 |
| exec_type | varchar(3) | Y |  | 行权方式 |
| exec_price | numeric(12,6) | Y |  | 行权价格 |
| exec_date | varchar(8) | Y |  | 行权日 |
| exec_clear_date | varchar(8) | Y |  | 结算日期 |
| opt_amt | numeric(20,2) | Y |  | 期权权利金 |
| opt_pay_date | varchar(8) | Y |  | 期权权利金支付日期 |
| delivery_type | varchar(3) | Y |  | 到期结算交割方式 |
| reference_type | varchar(3) | Y |  | 现金交割参考价格类型 |
| reference_price | numeric(20,8) | Y |  | 现金交割参考价格 |
| reference_adjust | numeric(12,6) | Y |  | 现金调整项 |
| reference_date | varchar(8) | Y |  | 现金交割参考价格日期 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| match_type | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| weight | numeric(12,6) | Y |  | 重量（千克） |
| period | varchar(10) | Y |  | 期限 |
| pay_status | varchar(4) | Y |  | 权利金支付状态：见tp_public_dict的348 |
| clear_status | varchar(4) | Y |  | 权利金清算信息：见tp_public_dict的355 |
| exec_match_no | varchar(20) | Y |  | 行权交易成交单号 |
| opt_status | varchar(4) | Y |  | 期权成交状态：见tp_public_dict的349 |
| exec_status | varchar(4) | Y |  | 行权状态：见tp_public_dict的350 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| act_exec_date | varchar(8) | Y |  | 实际行权日 |
| act_clear_date | varchar(8) | Y |  | 实际结算日期 |
| unit | numeric(10,0) | Y |  | 交易单位 |
| amt | numeric(20,2) | Y |  | 金额：手数*价格*unit |
| act_pay_date | varchar(8) | Y |  | 实际权利金支付日 |
| offset_opt_amt | numeric(20,2) | Y |  | 平仓权利金 |
| offset_pay_status | varchar(4) | Y |  | 平仓权利金支付状态：见tp_public_dict的348 |
| offset_clear_status | varchar(4) | Y |  | 平仓权利金清算信息：见tp_public_dict的355 |
| offset_opt_pay_date | varchar(8) | Y |  | 平仓权利金支付日期 |
| offset_act_pay_date | varchar(8) | Y |  | 实际平仓权利金支付日 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| offset_fee_status | varchar(4) | Y |  | 平仓收费状态：见tp_public_dict的343 |
| offset_fee_date | varchar(8) | Y |  | 平仓收费日期：清算收费成功后填写当日日期 |
| center_desc | varchar(20) | Y |  | 成本中心 |
| center_port | varchar(20) | Y |  | 端口 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |

---

## 118. dimple.tc_cmb_inq_opt_match_detail　(53 字段)
> 表含义：招行询价期权登记单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| inq_match_no | varchar(20) | Y |  | 询价系统成交编号 |
| match_no | varchar(20) | Y |  | 主系统成交编号/报价单编号 |
| contract_id | varchar(20) | Y |  | 期权合约代码 |
| member_id | varchar(8) | Y |  | 本方会员席位代码 |
| party_member_id | varchar(8) | Y |  | 对手方会员席位代码 |
| trader_no | varchar(16) | Y |  | 本方交易员代码 |
| bs_flag | varchar(3) | Y |  | 本方交易方向 |
| match_date | varchar(8) | Y |  | 询价成交日期 |
| qty | numeric(12,0) | Y |  | 成交数量 |
| opt_trade_type | varchar(3) | Y |  | 期权交易类型 |
| exec_type | varchar(3) | Y |  | 行权方式 |
| exec_price | numeric(12,6) | Y |  | 行权价格 |
| exec_date | varchar(8) | Y |  | 行权日 |
| exec_clear_date | varchar(8) | Y |  | 结算日期 |
| opt_amt | numeric(20,2) | Y |  | 期权权利金 |
| opt_pay_date | varchar(8) | Y |  | 期权权利金支付日期 |
| delivery_type | varchar(3) | Y |  | 到期结算交割方式 |
| reference_type | varchar(3) | Y |  | 现金交割参考价格类型 |
| reference_price | numeric(20,8) | Y |  | 现金交割参考价格 |
| reference_adjust | numeric(12,6) | Y |  | 现金调整项 |
| reference_date | varchar(8) | Y |  | 现金交割参考价格日期 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| match_type | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| weight | numeric(12,6) | Y |  | 重量（千克） |
| period | varchar(10) | Y |  | 期限 |
| pay_status | varchar(4) | Y |  | 权利金支付状态：见tp_public_dict的348 |
| clear_status | varchar(4) | Y |  | 权利金清算信息：见tp_public_dict的355 |
| exec_match_no | varchar(20) | Y |  | 行权交易成交单号 |
| opt_status | varchar(4) | Y |  | 期权成交状态：见tp_public_dict的349 |
| exec_status | varchar(4) | Y |  | 行权状态：见tp_public_dict的350 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| act_exec_date | varchar(8) | Y |  | 实际行权日 |
| act_clear_date | varchar(8) | Y |  | 实际结算日期 |
| unit | numeric(10,0) | Y |  | 交易单位 |
| amt | numeric(20,2) | Y |  | 金额：手数*价格*unit |
| act_pay_date | varchar(8) | Y |  | 实际权利金支付日 |
| offset_opt_amt | numeric(20,2) | Y |  | 平仓权利金 |
| offset_pay_status | varchar(4) | Y |  | 平仓权利金支付状态：见tp_public_dict的348 |
| offset_clear_status | varchar(4) | Y |  | 平仓权利金清算信息：见tp_public_dict的355 |
| offset_opt_pay_date | varchar(8) | Y |  | 平仓权利金支付日期 |
| offset_act_pay_date | varchar(8) | Y |  | 实际平仓权利金支付日 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| offset_fee_status | varchar(4) | Y |  | 平仓收费状态：见tp_public_dict的343 |
| offset_fee_date | varchar(8) | Y |  | 平仓收费日期：清算收费成功后填写当日日期 |
| center_desc | varchar(20) | Y |  | 成本中心 |
| center_port | varchar(20) | Y |  | 端口 |
| status | varchar(6) | Y |  |  |

---

## 119. dimple.tc_cmb_inquire_match　(38 字段)
> 表含义：招行询价登记单　|　估算行数：**166**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| match_no | varchar(20) | N | √ | 成交单号 |
| agreement_sn | varchar(30) | Y |  | 报价单编号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| match_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的253 |
| trade_type | varchar(3) | N | √ | 交易类型：见tp_public_dict的253只包含即期和远期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| member_id | varchar(8) | N | √ | 会员号 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| trade_party | varchar(40) | Y |  | 对手方代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| inquire_type | varchar(3) | Y |  | 交易类别：见Dict的325 |
| qty | numeric(24,6) | Y |  | 数量：单位Au为克 Ag为千克 =手数*合约乘数 |
| price | numeric(20,8) | Y |  | 近端价格:Au 人民币元/克、Ag 人民币元/千克 |
| amt | numeric(20,2) | Y |  | 近端金额：手数*价格*unit |
| delivtype | varchar(3) | Y |  | 近端交割方式：见tp_public_dict的051 |
| reference_type | varchar(3) | Y |  | 近端参考价类型：见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 近端参考价日期 |
| reference_price | numeric(20,8) | Y |  | 近端参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 近端参考价格调整项 |
| due_date | varchar(8) | Y |  | 近端到期日 |
| far_price | numeric(20,8) | Y |  | 远端价格:Au 人民币元/克、Ag 人民币元/千克 |
| far_amt | numeric(20,2) | Y |  | 远端金额：手数*价格*unit |
| far_delivtype | varchar(3) | Y |  | 远端交割方式：见tp_public_dict的051 |
| far_reference_type | varchar(3) | Y |  | 远端参考价类型：见tp_public_dict的288 |
| far_reference_date | varchar(8) | Y |  | 远端参考价日期 |
| far_reference_price | numeric(20,8) | Y |  | 远端参考价格 |
| far_reference_adjust | numeric(20,8) | Y |  | 远端参考价格调整项 |
| far_due_date | varchar(8) | Y |  | 远端到期日 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |

---

## 120. dimple.tc_cmb_inquire_match_clear　(23 字段)
> 表含义：招行询价交割单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(30) | N |  | 询价即远掉到期清算单编号 |
| inquire_no | varchar(20) | Y |  | 成交单编号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(10) | N |  | 客户号 |
| bs_flag | varchar(3) | N |  | 买卖方向 |
| contract_id | varchar(20) | N |  | 合约号 |
| price | numeric(24,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| weight | numeric(24,6) | Y |  | 重量（千克） |
| amt | numeric(18,2) | Y |  | 金额 |
| delivery_type | varchar(3) | N |  | 交割方式：1实物交割;2现金交割 |
| calc_price | numeric(24,8) | Y |  | 参考价格 |
| receive_money | numeric(24,6) | Y |  | 本方收到资金金额(元)：元；本方收到，数值为正；本方支出，数值为负。 |
| receive_weight | numeric(24,6) | Y |  | 本方收到实物重量(千克)：元；本方收到，数值为正；本方支出，数值为负。 |
| if_breach_apply | varchar(4) | Y |  | 是否违约申报：见tp_public_dict的338 |
| clear_status | varchar(4) | Y |  | 清算信息：见tp_public_dict的355 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| center_desc | varchar(20) | Y |  | 成本中心 |
| center_port | varchar(20) | Y |  | 端口 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |

---

## 121. dimple.tc_cmb_match　(26 字段)
> 表含义：招商银行-实时成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(30) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_time | varchar(12) | N |  | 成交时间 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| purpose_name | varchar(40) | Y |  | 交易目的 |
| margin_rate | numeric(10,6) | Y |  | 保证金率 |
| trade_fee | numeric(22,6) | Y |  | 手续费率 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |
| amt | numeric(24,6) | Y |  | 金额 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号,为了区分递延的替代交割而增加,其他默认为NORMAL |

---

## 122. dimple.tc_cmb_match_after_clear　(26 字段)
> 表含义：招商银行-盘后成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(30) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_time | varchar(12) | N |  | 成交时间 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| purpose_name | varchar(40) | Y |  | 交易目的 |
| margin_rate | numeric(10,6) | Y |  | 保证金率 |
| trade_fee | numeric(22,6) | Y |  | 手续费率 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |
| amt | numeric(24,6) | Y |  | 金额 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号,为了区分递延的替代交割而增加,其他默认为NORMAL |

---

## 123. dimple.tc_cmb_match_send_status　(19 字段)
> 表含义：成交单供数状态记录表(Murex信创)　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | numeric(64,0) | N | √ | 自增主键 |
| business_type | varchar(32) | N |  | 业务类型(comSpotFwd/comSwap/comFuture/comOption/comOptionOnFuture/simpleCashFlows) |
| match_no | varchar(64) | N |  | 成交单编号/业务键值 |
| trade_date | varchar(8) | N |  | 交易日期 |
| bs_flag | varchar(2) | Y |  | 买卖标志 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| member_id | varchar(20) | Y |  | 会员编号 |
| client_id | varchar(20) | Y |  | 客户编号 |
| send_status | varchar(10) | N |  | 发送状态(0-未发送,1-已发送,2-失败) |
| send_error_msg | varchar(500) | Y |  | 发送错误信息 |
| murex_deal_status | varchar(20) | Y |  | Murex处理状态 |
| murex_error_msg | varchar(1800) | Y |  | Murex错误信息 |
| business_id | varchar(254) | Y |  | 业务键值/报文businessId |
| send_time | timestamp | Y |  | 发送时间 |
| resp_time | timestamp | Y |  | 响应时间 |
| retry_count | numeric(32,0) | Y |  | 重试次数 |
| create_time | timestamp | Y |  | 创建时间 |
| update_time | timestamp | Y |  | 更新时间 |

---

## 124. dimple.tc_cmb_opics_fee　(12 字段)
> 表含义：费用信息　|　估算行数：**61**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(6) | Y |  | 交易所 |
| fee_type | varchar(3) | Y |  | 费用类型:1-手续费；2-递延费 |
| amt | numeric(24,6) | Y |  | 金额 |
| contract_id | varchar(20) | Y |  | 合约 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 125. dimple.tc_cmb_opt_match　(25 字段)
> 表含义：招商银行-实时期货期权成交表　|　估算行数：**72**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(30) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_time | varchar(12) | N |  | 成交时间 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| purpose_name | varchar(40) | Y |  | 交易目的 |
| margin_rate | numeric(10,6) | Y |  | 保证金率 |
| trade_fee | numeric(22,6) | Y |  | 手续费率 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |
| amt | numeric(24,6) | Y |  | 金额 |
| delivery_date | varchar(8) | Y |  | 交割日期 |

---

## 126. dimple.tc_cmb_opt_match_clear　(25 字段)
> 表含义：招商银行-盘后期货期权成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(30) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_time | varchar(12) | N |  | 成交时间 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| purpose_name | varchar(40) | Y |  | 交易目的 |
| margin_rate | numeric(10,6) | Y |  | 保证金率 |
| trade_fee | numeric(22,6) | Y |  | 手续费率 |
| cost_center | varchar(20) | Y |  | 成本中心 |
| port | varchar(20) | Y |  | 端口 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |
| amt | numeric(24,6) | Y |  | 金额 |
| delivery_date | varchar(8) | Y |  | 交割日期 |

---

## 127. dimple.tc_cmb_reference_price_config　(6 字段)
> 表含义：参考价类型配置文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | numeric(32,0) | N | √ | 自增主键 |
| dimple_ref_type | varchar(10) | Y |  | dimple参考价类型（可配置） |
| dimple_ref_name | varchar(100) | Y |  | dimple参考价类型定义（可配置） |
| murex_ref_type | varchar(100) | Y |  | murex参考价类型（可配置） |
| create_time | timestamp | Y |  | 创建时间 |
| update_time | timestamp | Y |  | 更新时间 |

---

## 128. dimple.tc_cmb_risk_recalc_defer　(10 字段)
> 表含义：招行日终重估业务-递延　|　估算行数：**91**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |

---

## 129. dimple.tc_cmb_risk_recalc_future　(10 字段)
> 表含义：招行日终重估业务-国债　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |

---

## 130. dimple.tc_cmb_risk_recalc_spot　(6 字段)
> 表含义：招行日终重估业务-现货　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(12,0) | Y |  | 库存量（克） |
| avg_price | numeric(20,8) | Y |  | 加权平均价 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 131. dimple.tc_contract_matchup　(3 字段)
> 表含义：合约对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 主合约 |
| matchup_contract_id | varchar(20) | N | √ | 对应合约 |
| matchup_type | varchar(3) | N | √ | 对应关系类型：1-报价合约对应平盘货币对 |

---

## 132. dimple.tc_contract_ralation　(2 字段)
> 表含义：金交所、外汇合约对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cfets_contact_id | varchar(20) | N | √ | 外汇合约 |
| cffex_contact_id | varchar(20) | N | √ | 金交所合约 |

---

## 133. dimple.tc_contract_tot　(36 字段)
> 表含义：合约统计表:结算后续处理产生.　|　估算行数：**1,207,567**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| today_match_qty | numeric(12,0) | Y |  | 当日成交量 |
| today_match_amt | numeric(24,6) | Y |  | 当日成交额 |
| month_match_qty | numeric(12,0) | Y |  | 月累计成交量 |
| month_match_amt | numeric(24,6) | Y |  | 月累计成交额 |
| year_match_qty | numeric(12,0) | Y |  | 年累计成交量 |
| year_match_amt | numeric(24,6) | Y |  | 年累计成交额 |
| today_fee | numeric(18,2) | Y |  | 当日手续费 |
| month_fee | numeric(18,2) | Y |  | 月手续费 |
| year_fee | numeric(18,2) | Y |  | 年手续费 |
| max_match_qty | numeric(12,0) | Y |  | 最大成交量 |
| max_match_qty_date | varchar(8) | Y |  | 最大成交量发生日期 |
| min_match_qty | numeric(12,0) | Y |  | 最小成交量 |
| min_match_qty_date | varchar(8) | Y |  | 最小成交量发生日期 |
| max_posi_qty | numeric(12,0) | Y |  | 最大持仓量 |
| max_posi_qty_date | varchar(8) | Y |  | 最大持仓量发生日期 |
| high_price | numeric(20,8) | Y |  | 最高价 |
| high_price_date | varchar(8) | Y |  | 最高价发生日期 |
| low_price | numeric(20,8) | Y |  | 最低价 |
| low_price_date | varchar(8) | Y |  | 最低价发生日期 |
| trade_days | float8 | Y |  | 合约到目前为止的交易天数 |
| today_total_profitloss | numeric(18,2) | Y |  | 当日盈亏 |
| month_total_profitloss | numeric(18,2) | Y |  | 月累计盈亏 |
| year_total_profitloss | numeric(18,2) | Y |  | 年累计盈亏 |
| today_match_qty_buy | numeric(12,0) | Y |  | 当日买入量：期货、现货为手；境外黄金为 盎司 |
| month_match_qty_buy | numeric(12,0) | Y |  | 月累计买入量：期货、现货为手；境外黄金为 盎司 |
| today_match_qty_sell | numeric(12,0) | Y |  | 当日卖出量：期货、现货为手；境外黄金为 盎司 |
| month_match_qty_sell | numeric(12,0) | Y |  | 月累计卖出量：期货、现货为手；境外黄金为 盎司 |
| today_match_amt_buy | numeric(24,6) | Y |  | 当日买入金额 |
| month_match_amt_buy | numeric(24,6) | Y |  | 月累计买入金额 |
| today_match_amt_sell | numeric(24,6) | Y |  | 当日卖出金额 |
| month_match_amt_sell | numeric(24,6) | Y |  | 月累计卖出金额 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 134. dimple.tc_control_process　(8 字段)
> 表含义：流程控制表　|　估算行数：**8**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| pro_id | numeric(6,0) | N | √ | 流程号 |
| pro_seq | numeric(6,0) | Y |  | 流程序号 |
| pro_name | varchar(40) | Y |  | 流程名称 |
| pro_model | varchar(20) | Y |  | 流程所属模块 |
| process_status | varchar(3) | Y |  | 流程状态:0 初始化(无色) 1 进行中(黄色) 2 成功(绿色) 3 失败(红色) |
| pro_remark | varchar(250) | Y |  | 流程备注 |
| operator | varchar(30) | Y |  | 操作人员 |
| oper_time | varchar(8) | Y |  | 操作时间 |

---

## 135. dimple.tc_cost_system_adjust　(22 字段)
> 表含义：成本补录表 - 平安银行使用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| seq_no | float8 | N | √ | 序列号 |
| input_type | varchar(3) | N | √ | 录入类型：1人民币成本 2美元成本 3成本转换 |
| trade_type | varchar(3) | Y |  | 业务类型:见public_dict的310 |
| currency | varchar(3) | Y |  | 币种:见public_dict的036 |
| delivery_variety_id | varchar(3) | Y |  | 交割品种 |
| qty_kg | numeric(20,3) | Y |  | 重量：kg |
| qty_oz | numeric(25,8) | Y |  | 重量：oz |
| price | numeric(24,6) | Y |  | 价格：根据录入类型 |
| amt_rmb | numeric(38,8) | Y |  | 金额：人民币 |
| amt_usd | numeric(38,8) | Y |  | 金额：美元 |
| user_id | varchar(16) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| op_user | varchar(16) | Y |  | 操作用户 |
| create_user | varchar(16) | Y |  | 新建人 |
| create_date | varchar(21) | Y |  | 新建日期:格式YYYY-MM-DD HH24:mi:ss |
| update_user | varchar(16) | Y |  | 修改人 |
| update_date | varchar(21) | Y |  | 修改日期:格式YYYY-MM-DD HH24:mi:ss |
| remark | varchar(100) | Y |  | 备注 |
| contract_id | varchar(20) | N |  | 合约号 |

---

## 136. dimple.tc_counterparty　(26 字段)
> 表含义：交易对手方信息　|　估算行数：**140**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| counterparty_no | varchar(10) | N |  | 交易对手方代码 |
| counterparty_type | varchar(3) | N |  | 类型：见tp_public_dict的279/农商行见366 |
| counterparty_abbr | varchar(30) | N |  | 交易对手方简称 |
| counterparty_name | varchar(100) | N |  | 交易对手方名称 |
| client_id | varchar(16) | Y |  | 行内客户号 |
| contact_person | varchar(20) | Y |  | 联系人 |
| contact_phone | varchar(15) | Y |  | 联系电话 |
| money_account | varchar(40) | Y |  | 对手方资金划拨账号 |
| counterparty_swift_no | varchar(20) | Y |  | 对方SWIFT号 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| member_id | varchar(10) | N | √ | 交易对手方席位号 |
| mmb_id | varchar(6) | Y |  | 交易对手方会员号 |
| if_tpgagency | varchar(3) | Y |  | 是否为第三方担保机构：1是/0否 见tp_public_dict的027 |
| counterparty_client_id | varchar(16) | N | √ | 交易对手方客户号 |
| member_abbr | varchar(30) | Y |  | 交易对手方席位简称 |
| client_abbr | varchar(30) | Y |  | 交易对手方客户简称 |
| home_foreign_type | varchar(3) | Y |  | 境内外属性:见tp_public_dict的401 |
| organization_type | varchar(3) | Y |  | 机构类型:见tp_public_dict的402 |
| ecif_id | varchar(16) | Y |  | 行内ECIF号 |
| client_laundering_risk_level | varchar(3) | Y |  | 客户洗钱风险等级：见tp_public_dict的452 |
| murex_sys_abbr | varchar(51) | Y |  | MUREX系统简称 |
| protocol_type | varchar(11) | Y |  | 协议类型 |
| protocol_year | varchar(4) | Y |  | 协议年份 |
| beneficiarymsg202 | varchar(34) | Y |  | 202报文受益人 |

---

## 137. dimple.tc_counterparty_amt_limit　(14 字段)
> 表含义：交易对手方限额　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| counterparty_no | varchar(10) | N | √ | 对手方代码 |
| counterparty_abbr | varchar(30) | N |  | 对手方简称 |
| currency | varchar(3) | N | √ | 币种：见tp_public_dict的036 |
| trade_type | varchar(3) | N | √ | 类型：见tp_public_dict的280 |
| end_date | varchar(8) | N |  | 到期日 |
| counterparty_name | varchar(100) | Y |  | 对手方名称 |
| limit_amt | numeric(24,6) | Y |  | 限额 |
| used | numeric(24,6) | Y |  | 已用额度 |
| overtime | numeric(24,6) | Y |  | 超期占用额度 |
| remain | numeric(24,6) | Y |  | 剩余额度 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(20) | Y |  | 操作员 |
| op_type | varchar(3) | Y |  | 操作类型：见tp_public_dict的068,导入：99 |

---

## 138. dimple.tc_counterparty_amt_rate　(10 字段)
> 表含义：交易对手方占用额度系数　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| variety | varchar(20) | Y |  | 品种 |
| currency | varchar(3) | Y |  | 币种：见tp_public_dict的036 |
| trade_type | varchar(3) | Y |  | 业务类型：见tp_public_dict的280 |
| timelimit_begin | numeric(3,0) | Y |  | 期限开始 |
| timelimit_end | numeric(3,0) | Y |  | 期限结束 |
| timelimit | varchar(20) | Y |  | 期限 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 139. dimple.tc_counterparty_ex_relation　(7 字段)
> 表含义：交易对手方对应关系　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| type | varchar(8) | N |  | 类型：见tp_public_dict的279/农商行见366 |
| counterparty | varchar(30) | N |  | 交易对手方 |
| counterparty_ex | varchar(100) | N |  | 外部交易对手方 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 140. dimple.tc_cp_amt_limit_jour　(15 字段)
> 表含义：交易对手方限额　|　估算行数：**259**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 交易对手方限额流水 |
| counterparty_no | varchar(10) | N |  | 对手方代码 |
| counterparty_abbr | varchar(30) | Y |  | 对手方简称 |
| currency | varchar(3) | Y |  | 币种：见tp_public_dict的036 |
| trade_type | varchar(3) | Y |  | 类型：见tp_public_dict的280 |
| end_date | varchar(8) | Y |  | 到期日 |
| counterparty_name | varchar(50) | Y |  | 对手方名称 |
| limit_amt | numeric(24,6) | Y |  | 限额 |
| used | numeric(24,6) | Y |  | 已用额度 |
| overtime | numeric(24,6) | Y |  | 超期占用额度 |
| remain | numeric(24,6) | Y |  | 剩余额度 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(20) | Y |  | 操作员 |
| op_type | bpchar(1) | Y |  | 操作类型：见tp_public_dict的068,导入：99 |

---

## 141. dimple.tc_cp_origin_match　(19 字段)
> 表含义：交易所成交数据整理表:对账功能使用　|　估算行数：**6**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | Y |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖标志 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| contract_id | varchar(30) | Y |  | 合约号 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| price | numeric(20,8) | Y |  | 价格 |
| match_time | varchar(12) | Y |  | 成交时间 |
| app_type | varchar(3) | Y |  | 定价成交申报类型:0-默认,见tp_public_dict330 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| trader_no | varchar(16) | Y |  | 交易员号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| match_type | bpchar(1) | Y |  | 成交类型:见tp_public_dict237 |
| middle_flag | bpchar(1) | Y |  | 是否为中立仓:见tp_public_dict027;递延交割成交使用 |
| local_no | varchar(16) | Y |  | 本地委托号:递延交割成交、报价成交使用 |

---

## 142. dimple.tc_csc_cfex_inquire_data　(5 字段)
> 表含义：外汇交易中心询价数据表（即期/远期/掉期）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期（YYYYMMDD） |
| cfets_match_no | varchar(30) | N | √ | 外汇成交单号（对应境内询价表cfets_match_no） |
| match_type | varchar(2) | N |  | 业务类型：0-即期 1-远期 2-掉期 |
| trader_no | varchar(40) | Y |  | 本方交易员号（外汇交易中心交易员） |
| clear_date | varchar(8) | Y |  | 结算日期（YYYYMMDD） |

---

## 143. dimple.tc_ctl_data_input　(4 字段)
> 表含义：数据导入配置表表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| input_type | varchar(3) | Y |  | 导入文件类型: 1:交易所 2:CTP 3:保证金接口 |
| input_file_num | numeric(6,0) | Y |  | 导入文件数量 |

---

## 144. dimple.tc_ctl_data_input_status　(5 字段)
> 表含义：数据导入状态表　|　估算行数：**523**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| member_id | varchar(8) | Y |  | 会员号 |
| file_name | varchar(60) | Y |  | 文件名：金交所对应节点名 |
| input_time | varchar(8) | Y |  | 导入时间 |

---

## 145. dimple.tc_customize_category　(5 字段)
> 表含义：业务数据字典类别表:存放常量的大类，可分部门管理。见constant.xml　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sort | varchar(4) | N | √ | 类别 |
| type_name | varchar(80) | Y |  | 名称 |
| ename | varchar(80) | Y |  | 英文名称 |
| dept_code | varchar(10) | Y |  | 部门代码:指由谁来维护 |
| if_fixed | bpchar(1) | Y |  | 是否固化 |

---

## 146. dimple.tc_customize_dict　(5 字段)
> 表含义：业务数据字典表:存放常量值　|　估算行数：**64**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sort | varchar(4) | N | √ | 类别 |
| type | varchar(10) | N | √ | 类型 |
| code_name | varchar(80) | Y |  | 名称 |
| ename | varchar(80) | Y |  | 英文名称 |
| exch_code | varchar(20) | Y |  | 交易所定制:见clear.tc_customize_dict的235 |

---

## 147. dimple.tc_dams_home_inquire_match　(39 字段)
> 表含义：农行DAMS直通接口：境内询价成交单　|　估算行数：**429**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| cmid | varchar(20) | Y |  | 记录ID |
| dealbillid | varchar(20) | N |  | 成交编号 |
| buyorsell | varchar(4) | Y |  | 交易方向：买0001，卖0002 |
| qtty | varchar(42) | Y |  | 交易数量 |
| price | varchar(42) | Y |  | 交易价格 |
| dealamt | varchar(42) | Y |  | 交易金额 |
| custid | varchar(40) | Y |  | 交易对手 |
| dealdate | varchar(30) | Y |  | 交易日 |
| valuedate | varchar(30) | Y |  | 起息日 |
| updatetime | varchar(30) | Y |  | 更新时间 |
| dealtype | varchar(4) | Y |  | 交易类型：即期2053，远期2054，掉期2055 |
| farvaluedate | varchar(30) | Y |  | 远端起息日 |
| farbuyorsell | varchar(4) | Y |  | 远端交易方向：买0001，卖0002 |
| farqtty | varchar(42) | Y |  | 远端交易数量 |
| farprice | varchar(42) | Y |  | 远端交易价格 |
| fardealamt | varchar(42) | Y |  | 远端交易金额 |
| ccypairid | varchar(12) | Y |  | 货币对ID |
| spotdate | varchar(30) | Y |  | 即期日期 |
| spotprice | varchar(42) | Y |  | 即期价格 |
| points | varchar(42) | Y |  | 近端掉期点 |
| farpoints | varchar(42) | Y |  | 远端掉期点  |
| dealpoints | varchar(42) | Y |  | 交易掉期点 |
| spread | numeric(10,0) | Y |  | 期限 |
| isvalid | varchar(4) | Y |  | 是否为有效记录：见tp_public_dict的027 |
| desk | varchar(10) | Y |  | 组合 |
| book | varchar(4) | Y |  | 账户 |
| detailtype | varchar(4) | Y |  | 交易具体类别 |
| remark | varchar(500) | Y |  | 备注 |
| creationdate | varchar(30) | Y |  | 记录创建时间 |
| fxdealsys | varchar(4) | Y |  | FXD交易来源 ：金交所0009 |
| supplementflg | varchar(4) | Y |  | SUP补录标志 |
| supplementdate | varchar(30) | Y |  | SUP补录日期 |
| instid | varchar(20) | Y |  | 合约品种ID |
| posdate | varchar(30) | Y |  | 敞口归属日 |
| dialogstate | varchar(4) | Y |  | 对话状态：0001未导入交易表，0002已导入交易表 |
| membercode | varchar(30) | Y |  | 席位号 |
| membername | varchar(256) | Y |  | 交易户名 |
| memberdealcode | varchar(20) | Y |  | 交易编码 |
| status | varchar(3) | Y |  | 发送状态：见tp_public_dict 的277 |

---

## 148. dimple.tc_defer_day_report　(22 字段)
> 表含义：延期交易交割日报表　|　估算行数：**22,222**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| month_no | varchar(8) | N | √ | 月份 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_open_qty | numeric(15,3) | Y |  | 多头开仓量 |
| buy_open_amt | numeric(24,6) | Y |  | 多头开仓金额 |
| buy_offset_qty | numeric(15,3) | Y |  | 多头平仓量 |
| buy_offset_amt | numeric(24,6) | Y |  | 多头平仓金额 |
| sell_open_qty | numeric(15,3) | Y |  | 空头开仓量 |
| sell_open_amt | numeric(24,6) | Y |  | 空头开仓金额 |
| sell_offset_qty | numeric(15,3) | Y |  | 空头平仓量 |
| sell_offset_amt | numeric(24,6) | Y |  | 空头平仓金额 |
| defer_out_qty | numeric(15,3) | Y |  | 递延交割交货量 |
| defer_in_qty | numeric(15,3) | Y |  | 递延交割收货量 |
| middle_out_qty | numeric(15,3) | Y |  | 中立仓交货量 |
| middle_in_qty | numeric(15,3) | Y |  | 中立仓收货量 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| day_buy_qty | numeric(15,3) | Y |  | 当日多头持仓量变化量 |
| day_buy_amt | numeric(24,6) | Y |  | 当日多头持仓金额变化量 |
| day_sell_qty | numeric(15,3) | Y |  | 当日空头持仓量变化量 |
| day_sell_amt | numeric(24,6) | Y |  | 当日空头持仓金额变化量 |

---

## 149. dimple.tc_defer_delivery_match　(13 字段)
> 表含义：递延交割申报成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| match_time | varchar(8) | Y |  | 成交时间 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| middle_flag | bpchar(1) | Y |  | 是否为中立仓: 0否,1是 |
| trader_no | varchar(15) | N | √ | 席位号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 150. dimple.tc_defer_fee_rate　(8 字段)
> 表含义：递延补偿费率表　|　估算行数：**4,530**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| pay_flag | bpchar(1) | Y |  | 支付方向:见tp_public_dict的222 |
| defer_fee | numeric(22,6) | Y |  | 递延费率 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 151. dimple.tc_defer_month_report　(25 字段)
> 表含义：延期交易交割月报表　|　估算行数：**3,215**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| month_no | varchar(8) | N | √ | 月份 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| init_buy_qty | numeric(15,3) | Y |  | 期初多头持仓量 |
| init_buy_amt | numeric(24,6) | Y |  | 期初多头持仓金额 |
| init_sell_qty | numeric(15,3) | Y |  | 期初空头持仓量 |
| init_sell_amt | numeric(24,6) | Y |  | 期初空头持仓金额 |
| buy_open_qty | numeric(15,3) | Y |  | 多头开仓量 |
| buy_open_amt | numeric(24,6) | Y |  | 多头开仓金额 |
| buy_offset_qty | numeric(15,3) | Y |  | 多头平仓量 |
| buy_offset_amt | numeric(24,6) | Y |  | 多头平仓金额 |
| sell_open_qty | numeric(15,3) | Y |  | 空头开仓量 |
| sell_open_amt | numeric(24,6) | Y |  | 空头开仓金额 |
| sell_offset_qty | numeric(15,3) | Y |  | 空头平仓量 |
| sell_offset_amt | numeric(24,6) | Y |  | 空头平仓金额 |
| defer_out_qty | numeric(15,3) | Y |  | 递延交割交货量 |
| defer_in_qty | numeric(15,3) | Y |  | 递延交割收货量 |
| middle_out_qty | numeric(15,3) | Y |  | 中立仓交货量 |
| middle_in_qty | numeric(15,3) | Y |  | 中立仓收货量 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| remain_buy_qty | numeric(15,3) | Y |  | 期末多头持仓量 |
| remain_buy_amt | numeric(24,6) | Y |  | 期末多头持仓金额 |
| remain_sell_qty | numeric(15,3) | Y |  | 期末空头持仓量 |
| remain_sell_amt | numeric(24,6) | Y |  | 期末空头持仓金额 |

---

## 152. dimple.tc_delivery_bond_manage　(25 字段)
> 表含义：交割券管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| op_seq_no | float8 | N | √ | 流水号 |
| reg_date | varchar(8) | Y |  | 申报日期 |
| match_date | varchar(8) | Y |  | 配对日 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | Y |  | 买卖标志位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| qty | numeric(12,0) | Y |  | 配对量 |
| price | numeric(20,8) | Y |  | 交割结算价 |
| bond_code | varchar(10) | Y |  | 债券代码 |
| bond_name | varchar(100) | Y |  | 债券名称 |
| exchange_rate | numeric(20,8) | Y |  | 转换因子 |
| interest | numeric(20,8) | Y |  | 应计利息 |
| delivery_amt | numeric(24,6) | Y |  | 交割款 |
| publish_amt | numeric(20,8) | Y |  | 应付罚金 |
| pay_amt | numeric(20,8) | Y |  | 应付补偿金 |
| effect_date | varchar(8) | Y |  | 起息日 |
| transfer_date | varchar(8) | Y |  | 到帐日 |
| status | varchar(3) | Y |  | 现券划转状态 |
| creater | varchar(30) | Y |  | 创建人 |
| create_time | varchar(30) | Y |  | 创建时间 |
| updater | varchar(30) | Y |  | 更新人 |
| update_time | varchar(30) | Y |  | 更新时间 |

---

## 153. dimple.tc_delivery_fee　(14 字段)
> 表含义：品种交割手续费率　|　估算行数：**2,245**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| delivery_fee | numeric(22,6) | N |  | 交割手续费率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| exch_code | varchar(6) | N | √ | 交易所代码 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 154. dimple.tc_delivery_fee_check　(18 字段)
> 表含义：品种交割手续费率复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 序号：自增 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| delivery_fee | numeric(22,6) | N |  | 交割手续费率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| exch_code | varchar(6) | N |  | 交易所代码 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 155. dimple.tc_delivery_margin_rate　(12 字段)
> 表含义：交割保证金率表　|　估算行数：**1,135**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| margin_flag | bpchar(1) | N | √ | 保证金标志:见tp_public_dict的223 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| margin_rate | numeric(22,6) | N |  | 保证金率 |
| margin_type | varchar(2) | Y |  | 保证金类型:见tp_public_dict的092 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 156. dimple.tc_delivery_margin_rate_check　(16 字段)
> 表含义：交割保证金率复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| contract_id | varchar(20) | N |  | 合约号 |
| margin_flag | bpchar(1) | N |  | 保证金标志:见tp_public_dict的223 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| margin_rate | numeric(22,6) | N |  | 保证金率 |
| margin_type | varchar(2) | Y |  | 保证金类型:见tp_public_dict的092 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 157. dimple.tc_delivery_posi　(30 字段)
> 表含义：期货交割持仓表:记录期转现，滚动交割，一次性交割的平仓量和相应资金.日终结算产生　|　估算行数：**1,832**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| match_date | varchar(8) | N | √ | 配对日 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| delivery_way | varchar(2) | N | √ | 交割方式:见tp_public_dict的051 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| ahead_buy_qty | numeric(12,0) | Y |  | 提前买交割量 |
| ahead_sell_qty | numeric(12,0) | Y |  | 提前卖交割量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_margin | numeric(18,2) | N |  | 买保证金:仅对滚动交割和一次性交割有效；指买方转货款；此字段仅用来查询。 |
| sell_margin | numeric(18,2) | N |  | 卖保证金:仅对滚动交割和一次性交割有效；指卖方转交割保证金；此字段仅用来查询。 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| wrap_price | numeric(20,8) | Y |  | 包装物价格 |
| delivery_fee | numeric(18,2) | Y |  | 交割手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| clear_account_no | varchar(14) | Y |  | 结算子帐号 |
| delivery_date | varchar(8) | Y |  | 交割日 |
| buy_deli_margin_exch | numeric(18,2) | N |  | 交易所买交割保证金 |
| sell_deli_margin_exch | numeric(18,2) | N |  | 交易所卖交割保证金 |
| remain_buy_margin | numeric(18,2) | Y |  | 剩余买交割保证金 |
| remain_sell_margin | numeric(18,2) | Y |  | 剩余卖交割保证金 |
| remain_buy_margin_exch | numeric(18,2) | Y |  | 剩余交易所买交割保证金 |
| remain_sell_margin_exch | numeric(18,2) | Y |  | 剩余交易所卖交割保证金 |
| last_buy_margin | numeric(18,2) | Y |  | 上日剩余买保证金 |
| last_sell_margin | numeric(18,2) | Y |  | 上日剩余卖保证金 |
| last_buy_margin_exch | numeric(18,2) | Y |  | 上日交易所剩余买保证金 |
| last_sell_margin_exch | numeric(18,2) | Y |  | 上日交易所剩余卖保证金 |

---

## 158. dimple.tc_dept_money_report　(17 字段)
> 表含义：部门资金表　|　估算行数：**2,210**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| dept_code | varchar(10) | N | √ | 部门代码 |
| last_remain | numeric(18,2) | Y |  | 上日资金余额 |
| last_margin | numeric(18,2) | Y |  | 上日保证金 |
| margin | numeric(18,2) | Y |  | 当日保证金 |
| profitloss | numeric(18,2) | Y |  | 当日盈亏 |
| buy_amount | numeric(18,2) | Y |  | 当日买货款 |
| sell_amount | numeric(18,2) | Y |  | 当日卖货款 |
| money_in | numeric(24,6) | Y |  | 当日入金 |
| money_out | numeric(24,6) | Y |  | 当日出金 |
| trade_fee | numeric(24,6) | Y |  | 交易费用 |
| delivery_fee | numeric(24,6) | Y |  | 交割费用 |
| defer_fee | numeric(24,6) | Y |  | 递延费 |
| overdue_fee | numeric(24,6) | Y |  | 超期费 |
| otr_fee | numeric(24,6) | Y |  | 其他费用 |
| remain | numeric(18,2) | Y |  | 当日资金余额 |
| remark | varchar(255) | Y |  | 备注 |

---

## 159. dimple.tc_discount_rate_date　(10 字段)
> 表含义：贴现率公式，日期中间表　|　估算行数：**28,946**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 清算日期 |
| calc_type | varchar(3) | Y |  | 计算类型：1：+0; 2:+2 |
| calc_ref_type | varchar(20) | Y |  | 类型描述 |
| calc_dict_type | varchar(3) | Y |  | 贴现率类型：见tp_public_dict的289 |
| calc_date | varchar(8) | Y |  | 计算日期 |
| calc_days | numeric(10,0) | Y |  | 计算日年化天数 |
| next_calc_ref_type | varchar(20) | Y |  | 类型描述 |
| next_calc_dict_type | varchar(3) | Y |  | 贴现率类型：见tp_public_dict的289 |
| next_calc_date | varchar(8) | Y |  | 下一计算日期 |
| next_calc_days | numeric(10,0) | Y |  | 下一计算日年化天数 |

---

## 160. dimple.tc_discount_relation　(3 字段)
> 表含义：贴现估值对应关系：品种、询价合约　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种号 |
| cfets_contact_id | varchar(20) | N |  | 外汇合约 |

---

## 161. dimple.tc_email_send_record　(12 字段)
> 表含义：邮件发送记录表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| record_id | varchar(36) | N | √ | 记录ID |
| send_date | varchar(8) | N |  | 发送日期 |
| send_time | varchar(8) | N |  | 发送时间 |
| notice_type | varchar(3) | N |  | 通知事项^485 |
| subject | varchar(500) | Y |  | 邮件标题 |
| content | varchar(1000) | Y |  | 通知内容 |
| attachment_id | varchar(20) | Y |  | 附件ID |
| status | varchar(3) | Y |  | 状态^489 |
| email_suffix | varchar(50) | Y |  | 邮箱地址后缀 |
| to_receivers | varchar(6000) | Y |  | 收件人 |
| cc_receivers | varchar(6000) | Y |  | 抄送人 |
| bcc_receivers | varchar(6000) | Y |  | 密送人 |

---

## 162. dimple.tc_email_template_manage　(19 字段)
> 表含义：邮件模板管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| notice | varchar(3) | N | √ | 通知事项^485 |
| template_no | numeric(6,0) | N | √ | 模板编号 |
| template_name | varchar(100) | N |  | 模板名称 |
| email_title | varchar(500) | N |  | 邮件标题 |
| ts_roles | varchar(300) | Y |  | 收件角色 |
| ts_users | varchar(2000) | Y |  | 收件用户 |
| ts_out_users | varchar(2000) | Y |  | 收件外部用户 |
| cs_roles | varchar(300) | Y |  | 抄送角色 |
| cs_users | varchar(2000) | Y |  | 抄送用户 |
| cs_out_users | varchar(2000) | Y |  | 抄送外部用户 |
| ms_roles | varchar(300) | Y |  | 密送角色 |
| ms_users | varchar(2000) | Y |  | 密送用户 |
| ms_out_users | varchar(2000) | Y |  | 密送外部用户 |
| email_suffix | varchar(50) | Y |  | 邮箱地址后缀 |
| status | varchar(3) | N |  | 生效状态^027 |
| op_user | varchar(50) | Y |  | 操作人 |
| op_date | varchar(8) | Y |  | 更新日期 |
| op_time | varchar(8) | Y |  | 更新时间 |
| remark | varchar(1000) | Y |  | 备注 |

---

## 163. dimple.tc_err_etf_match　(29 字段)
> 表含义：ETF错单表-存放未完成成交记录　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N | √ | 录入日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| trader_no | varchar(30) | N | √ | 交易员 |
| self_local_no | varchar(30) | Y |  | fund编号 |
| local_seq_no | varchar(20) | N | √ | 本地编号 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| qty_1 | numeric(20,6) | Y |  | 重量1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| qty_2 | numeric(20,6) | Y |  | 重量2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| qty_3 | numeric(20,6) | Y |  | 重量3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| qty_4 | numeric(20,6) | Y |  | 重量4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| qty_5 | numeric(20,6) | Y |  | 重量5 |
| status | varchar(4) | Y |  | 状态:见tp_public_dict的269 |
| confirm_date | varchar(8) | Y |  | 确认日期 |
| err_type | varchar(3) | Y |  | 错误类型: 11对账(系统多余记录) 12对账(系统待修正记录) 2撤单 3错单 |

---

## 164. dimple.tc_etf_client　(16 字段)
> 表含义：ETF账户管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | Y |  | 请求日期 |
| op_time | varchar(8) | Y |  | 请求时间 |
| seq_no | varchar(20) | Y |  | 本地编号 |
| exch_seq_no | varchar(20) | Y |  | ETF账户备案流水 |
| client_name | varchar(80) | Y |  | 投资人名称 |
| client_type | varchar(4) | Y |  | 投资人类型:见public_dict274 |
| paper_type | varchar(4) | Y |  | 投资人证件类型:见public_dict275 |
| paper_no | varchar(30) | Y |  | 投资人证件号码 |
| client_code | varchar(50) | Y |  | 法人组织机构代码 |
| client_id | varchar(20) | N | √ | 投资人黄金账号 |
| member_id | varchar(8) | N | √ | 会员代码 |
| member_name | varchar(80) | Y |  | 黄金账号指定会员名称 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| etf_code | varchar(8) | N | √ | ETF基金代码 |
| trade_type | varchar(4) | Y |  | 业务类型:见public_dict272 |
| confirm_type | varchar(4) | Y |  | 确认标志:见public_dict270 |

---

## 165. dimple.tc_etf_client_jour　(19 字段)
> 表含义：ETF账户管理流水表　|　估算行数：**74**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 请求日期 |
| seq_no | varchar(20) | N | √ | 本地编号 |
| exch_seq_no | varchar(20) | Y |  | ETF账户备案流水 |
| client_name | varchar(80) | Y |  | 投资人名称 |
| client_type | varchar(4) | Y |  | 投资人类型:见public_dict274 |
| paper_type | varchar(4) | Y |  | 投资人证件类型:见public_dict275 |
| paper_no | varchar(30) | Y |  | 投资人证件号码 |
| client_code | varchar(50) | Y |  | 法人组织机构代码 |
| client_id | varchar(20) | N |  | 投资人黄金账号 |
| member_id | varchar(8) | N |  | 会员代码 |
| member_name | varchar(80) | Y |  | 黄金账号指定会员名称 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| etf_code | varchar(8) | N |  | ETF基金代码 |
| trade_type | varchar(4) | N |  | 业务类型:见public_dict272 |
| confirm_type | varchar(4) | Y |  | 确认标志:见public_dict270 |
| request_time | varchar(8) | Y |  | 请求时间 |
| confirm_time | varchar(8) | Y |  | 响应时间 |
| return_code | varchar(20) | Y |  | 响应状态 |
| return_msg | varchar(60) | Y |  | 响应信息 |

---

## 166. dimple.tc_etf_fee_detail　(11 字段)
> 表含义：ETF当日手续费明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| trader_no | varchar(30) | Y |  | 交易员 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| money_type | varchar(3) | N | √ | 费用类型:见public_dict 273 |
| amt | numeric(24,6) | Y |  | 金额 |

---

## 167. dimple.tc_etf_fee_rate　(12 字段)
> 表含义：ETF费率管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| trade_type | varchar(4) | N | √ | 交易类型：见数据字典268 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| fee_rate | numeric(10,4) | Y |  | 费率 |
| status | varchar(3) | N | √ | 状态 |
| create_id | varchar(30) | Y |  | 创建者 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 操作员 |
| update_date | varchar(8) | Y |  | 操作日期 |
| update_time | varchar(8) | Y |  | 操作时间 |

---

## 168. dimple.tc_etf_list　(23 字段)
> 表含义：ETF明细清单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| etf_code | varchar(8) | N | √ | ETF基金代码 |
| member_id | varchar(8) | N | √ | 会员代码 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| calc_amt_1 | numeric(24,6) | Y |  | T日预估现金差额1 |
| amt_1 | numeric(24,6) | Y |  | T-1日现金差额1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| calc_amt_2 | numeric(24,6) | Y |  | T日预估现金差额2 |
| amt_2 | numeric(24,6) | Y |  | T-1日现金差额2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| calc_amt_3 | numeric(24,6) | Y |  | T日预估现金差额3 |
| amt_3 | numeric(24,6) | Y |  | T-1日现金差额3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| calc_amt_4 | numeric(24,6) | Y |  | T-1日现金差额4 |
| amt_4 | numeric(24,6) | Y |  | T日预估现金差额4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| calc_amt_5 | numeric(24,6) | Y |  | T日预估现金差额5 |
| amt_5 | numeric(24,6) | Y |  | T-1日现金差额5 |
| min_qty | numeric(12,0) | Y |  | 最小申购赎回重量 |
| max_apply_qty | numeric(12,0) | Y |  | 当日申购上限 |
| max_ransom_qty | numeric(12,0) | Y |  | 当日赎回上限 |
| if_ar | varchar(3) | Y |  | 当日是否允许申购/赎回标志:见数据字典027 |
| etf_unit | numeric(16,6) | Y |  | 每份黄金ETF基金对应的黄金重量 |

---

## 169. dimple.tc_etf_match_detail　(20 字段)
> 表含义：ETF成交展开表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| confirm_date | varchar(8) | Y |  | 确认日期 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| trader_no | varchar(30) | N |  | 交易员 |
| local_seq_no | varchar(20) | N |  | 本地编号 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| delivery_variety_id | varchar(3) | Y |  | 交割品种 |
| qty | numeric(20,6) | Y |  | 重量 |
| calc_type | varchar(3) | Y |  | 计算类型:见public_dict 273 |
| calc_value | numeric(24,6) | Y |  | 计算值 |

---

## 170. dimple.tc_etf_match_manage_jour　(33 字段)
> 表含义：认申赎分配流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| seq_no | float8 | N | √ | 流水号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| local_seq_no | varchar(20) | N |  | 本地编号 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| user_id_old | varchar(30) | Y |  | 原交易员号 |
| user_id | varchar(30) | Y |  | 交易员号 |
| purpose_code_old | varchar(3) | Y |  | 交易目的 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| qty_1 | numeric(20,6) | Y |  | 重量1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| qty_2 | numeric(20,6) | Y |  | 重量2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| qty_3 | numeric(20,6) | Y |  | 重量3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| qty_4 | numeric(20,6) | Y |  | 重量4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| qty_5 | numeric(20,6) | Y |  | 重量5 |
| status | varchar(4) | Y |  | 状态:见tp_public_dict的269 |
| oper_type | varchar(3) | Y |  | 操作类型：见数据字典267 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作员 |

---

## 171. dimple.tc_exch_date_margin_rate　(18 字段)
> 表含义：交易所日期梯度保证金率表:存储关于时间梯度的保证金率信息　|　估算行数：**1,311**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约代码:$表示所有合约 |
| margin_type | bpchar(1) | N |  | 保证金类型:预留，用于确定保证金率是比率值还是固定值。参考常量表。－》见tp_public_dict的092。 |
| month | float8 | N | √ | 月份: -1普通月份 1 交割前一月 0 交割月份 |
| day | float8 | N | √ | 天:对于普通月份该值为-1，其他月份为交割日 |
| spec_buy_rate | numeric(10,6) | N |  | 投机买率 |
| spec_sell_rate | numeric(10,6) | N |  | 投机卖率 |
| hedge_buy_rate | numeric(10,6) | N |  | 套保买率 |
| hedge_sell_rate | numeric(10,6) | N |  | 套保卖率 |
| arbi_buy_rate | numeric(10,6) | N |  | 套利买率 |
| arbi_sell_rate | numeric(10,6) | N |  | 套利卖率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| recheck_date | varchar(8) | Y |  | 审核日期:对于品种合约保证金管理，该项即操作日期;对于特殊结算帐号保证金管理，该项即审核日期 |
| recheck_oper | varchar(30) | Y |  | 审核员:对于品种合约保证金管理，该项即操作员;对于特殊结算帐号保证金管理，该项即审核操作的操作员 |
| if_update_byimp | varchar(2) | Y |  | 是否根据清算文件导入时自动更新：tp_public_dict的027 目前仅金交所使用 |

---

## 172. dimple.tc_exch_intl_money　(8 字段)
> 表含义：金交所国际版：系统客户资金表　|　估算行数：**1,954**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| client_id | varchar(16) | N | √ | 客户代码 |
| member_id | varchar(8) | N | √ | 席位代码 |
| buy_amount | numeric(18,2) | Y |  | 成交买入金额：元 |
| sell_amount | numeric(18,2) | Y |  | 成交卖岀金额：元 |
| margin | numeric(18,2) | Y |  | 交易所保证金：元 |
| delivery_margin | numeric(18,2) | Y |  | 交割保证金：元 |
| profit | numeric(18,2) | Y |  | 盯市盈余：元 |

---

## 173. dimple.tc_exch_margin_rate　(14 字段)
> 表含义：交易所保证金率表　|　估算行数：**70**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号:中金所时使用，其他时刻为$ |
| contract_id | varchar(80) | N |  | 合约代码 |
| sh_flag | varchar(3) | N |  | 交易编码属性:见tp_public_dict263 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| margin_type | bpchar(1) | N |  | 保证金类型:预留，用于确定保证金率是比率值还是固定值。参考常量表。－》见tp_public_dict的092。 |
| buy_rate | numeric(10,6) | N |  | 买率 |
| sell_rate | numeric(10,6) | N |  | 卖率 |
| buy_fix | numeric(22,6) | N |  | 买固定值：非报价合约保留2位小数 |
| sell_fix | numeric(22,6) | N |  | 卖固定值：非报价合约保留2位小数 |
| remark | varchar(254) | Y |  | 备注:在备注字段中记录保证金率取值来源 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 174. dimple.tc_exch_money　(61 字段)
> 表含义：结算会员资金表　|　估算行数：**7,801**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| clear_member_id | varchar(8) | N | √ | 结算会员号:填写999 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| currency | varchar(2) | N | √ | 币种 |
| init_margin | numeric(19,2) | Y |  | 初始准备金 |
| delivery_margin | numeric(19,2) | Y |  | 交割保证金 |
| offset_profitloss | numeric(19,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(19,2) | Y |  | 持仓盈亏 |
| buy_premium | numeric(19,2) | Y |  | 权利金支出 |
| sell_premium | numeric(19,2) | Y |  | 权利金收入 |
| trade_fee | numeric(19,2) | Y |  | 交易手续费 |
| clear_fee | numeric(19,2) | Y |  | 结算手续费 |
| delivery_fee | numeric(19,2) | Y |  | 交割手续费 |
| move_posi_fee | numeric(19,2) | Y |  | 移仓手续费 |
| ret_fee | numeric(19,2) | Y |  | 返还手续费 |
| margin | numeric(19,2) | Y |  | 交易保证金 |
| mort_amt | numeric(24,6) | Y |  | 利息 |
| money_in | numeric(19,2) | Y |  | 当日入金 |
| money_out | numeric(19,2) | Y |  | 当日出金 |
| cash | numeric(19,2) | Y |  | 现金 |
| other_money | numeric(19,2) | Y |  | 其他金额 |
| remain | numeric(19,2) | Y |  | 结算余额 |
| prepare_margin | numeric(19,2) | Y |  | 开仓准备金 |
| last_margin | numeric(19,2) | Y |  | 昨日保证金 |
| call_margin | numeric(19,2) | Y |  | 追加保证金 |
| buy_amount | numeric(19,2) | Y |  | 买货款 |
| sell_amount | numeric(19,2) | Y |  | 卖货款 |
| frozen_profitloss | numeric(19,2) | Y |  | 盈亏冻结 |
| last_frozen_profitloss | numeric(19,2) | Y |  | 上日盈亏冻结 |
| frozen_amount | numeric(19,2) | Y |  | 货款冻结 |
| last_frozen_amount | numeric(19,2) | Y |  | 上日货款冻结 |
| last_delivery_margin | numeric(19,2) | Y |  | 上日交割保证金 |
| free_trade_fee | numeric(19,2) | Y |  | 减免交易手续费 |
| total_rights | numeric(19,2) | Y |  | 总权益 |
| setoff_out_limit | numeric(19,2) | Y |  | 充抵出金限制金额：金交所 |
| setoff_quota | numeric(19,2) | Y |  | 当日实际充抵额度：金交所 |
| setoff_usedquota | numeric(19,2) | Y |  | 当日已用充抵额度：金交所 |
| setoff_avaliablequota | numeric(19,2) | Y |  | 当日剩余充抵额度：金交所 |
| cash_occupied | numeric(19,2) | Y |  | 当日货币交易保证金占用：金交所 |
| quota_occupied | numeric(19,2) | Y |  | 当日额度交易保证金占用：金交所 |
| cash_balance | numeric(19,2) | Y |  | 当日货币交易可报价余额：金交所 |
| quota_balance | numeric(19,2) | Y |  | 当日额度交易可报价余额：金交所 |
| available | numeric(19,2) | Y |  | 当日可提资金：金交所 |
| deposit | numeric(19,2) | Y |  | 当日实有货币资金余额：上期所、金交所 |
| pt_frozen_amount | numeric(19,2) | Y |  | 当日铂金冻结金额 |
| last_trights | numeric(19,2) | Y |  | 上日总权益 |
| last_deposit | numeric(19,2) | Y |  | 上日实有货币资金：金交所 |
| last_setoff_quota | numeric(19,2) | Y |  | 上日实际充抵额度：金交所 |
| last_setoff_usedquota | numeric(19,2) | Y |  | 上日已用充抵额度：金交所 |
| last_cash_occupied | numeric(19,2) | Y |  | 上日货币交易保证金占用：金交所 |
| last_quota_occupied | numeric(19,2) | Y |  | 上日额度交易保证金占用：金交所 |
| last_cash_balance | numeric(19,2) | Y |  | 上日货币交易可报价余额：金交所 |
| last_quota_balance | numeric(19,2) | Y |  | 上日额度交易可报价余额：金交所 |
| last_available | numeric(19,2) | Y |  | 上日可提资金：金交所 |
| ag_frozen_amount | numeric(19,2) | Y |  | 白银货款冻结 |
| manual_frozen_amount | numeric(19,2) | Y |  | 手工货款冻结 |
| last_ag_frozen_amount | numeric(19,2) | Y |  | 上日白银货款冻结 |
| last_manual_frozen_amount | numeric(19,2) | Y |  | 上日手工货款冻结 |
| law_last_forzen_amt | numeric(19,2) | Y |  | 上日司法冻结金额 |
| law_forzen_amt | numeric(19,2) | Y |  | 当日司法冻结金额 |

---

## 175. dimple.tc_exch_money_check　(4 字段)
> 表含义：费用类型检查表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(4) | Y |  | 交易所代码 |
| fee_code | varchar(20) | Y |  | 费用编码 |
| fee_name | varchar(100) | Y |  | 费用名称 |
| check_flag | varchar(3) | Y |  | 检查标志：0不检查；1检查 |

---

## 176. dimple.tc_exch_money_io　(19 字段)
> 表含义：结算会员出入金表　|　估算行数：**13,470**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 流水号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| bill_no | varchar(15) | N |  | 票号:手工输入，唯一 |
| currency | varchar(2) | N | √ | 币种 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| money_in | numeric(18,2) | Y |  | 入金 |
| money_out | numeric(18,2) | Y |  | 出金 |
| bank_id | varchar(3) | Y |  | 银行代码 |
| bank_account_no | varchar(40) | Y |  | 银行帐号:存放尾数 |
| operator1 | varchar(30) | Y |  | 操作员1 |
| operator2 | varchar(30) | Y |  | 操作员2 |
| op_time1 | varchar(8) | Y |  | 操作时间1 |
| op_time2 | varchar(8) | Y |  | 操作时间2 |
| money_type | varchar(3) | Y |  | 资金类型:见tp_public_dict的233 |
| io_type | varchar(2) | N |  | 录入性质:见tp_public_dict的039 |
| status | varchar(2) | N |  | 状态:见tp_public_dict的030 |
| note | varchar(254) | Y |  | 备注 |

---

## 177. dimple.tc_exch_money_io_temp　(15 字段)
> 表含义：结算会员出入金临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 流水号 |
| bill_no | varchar(15) | N |  | 票号:手工输入，唯一 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| money_in | numeric(18,2) | Y |  | 入金 |
| money_out | numeric(18,2) | Y |  | 出金 |
| bank_id | varchar(3) | Y |  | 银行代码 |
| bank_account_no | varchar(40) | Y |  | 银行帐号:存放尾数 |
| operator | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |
| money_type | varchar(3) | Y |  | 资金类型:见tp_public_dict的233 |
| io_type | varchar(2) | N |  | 录入性质:见tp_public_dict的039 |
| note | varchar(254) | Y |  | 备注 |
| recheck_status | bpchar(1) | Y |  | 复核状态:见tp_public_dict的096 |

---

## 178. dimple.tc_exch_posi　(33 字段)
> 表含义：结算会员持仓表　|　估算行数：**33,598**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| clear_member_id | varchar(8) | N | √ | 结算会员号:填写999 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量-今日交割平仓(交割持仓表)＋期权执行期货建仓量（期权执行期货建仓表），计算时可直接从成交表，盘后成交表，交割匹配表统一计算 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数:先投机后保值 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏:根据期货平仓盈亏表计算 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| open_fee | numeric(18,2) | Y |  | 开仓结算手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| t_open_fee | numeric(18,2) | Y |  | 开仓交易手续费 |
| t_offset_fee | numeric(18,2) | Y |  | 平仓交易手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费:来自对期货短线明细表的汇总 |
| buy_margin | numeric(18,2) | Y |  | 买保证金 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |

---

## 179. dimple.tc_exch_rfq_deli_posi_clear　(10 字段)
> 表含义：席位保证金询价交割持仓表　|　估算行数：**367**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| due_date | varchar(8) | N | √ | 到期日 |
| buy_qty | numeric(12,0) | Y |  | 多头交割量：手 |
| sell_qty | numeric(12,0) | Y |  | 空头交割量：手 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| amount | numeric(18,2) | Y |  | 交割货款 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 180. dimple.tc_exch_rfq_posi_clear　(20 字段)
> 表含义：席位保证金询价持仓表　|　估算行数：**3,762**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| due_date | varchar(8) | N | √ | 到期日 |
| last_buy_qty | numeric(12,0) | Y |  | 上日多头持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日空头持仓量 |
| last_net_qty | numeric(12,0) | Y |  | 上日净持仓 |
| t_buy_qty | numeric(12,0) | Y |  | 当日买量 |
| t_sell_qty | numeric(12,0) | Y |  | 当日卖量 |
| t_buy_amt | numeric(18,2) | Y |  | 当日买金额 |
| t_sell_amt | numeric(18,2) | Y |  | 当日卖金额 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| net_qty | numeric(12,0) | Y |  | 净持仓 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| delivery_margin | numeric(18,2) | Y |  | 交割保证金：到期日=下一交易日 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| buy_amt | numeric(18,2) | Y |  | 买额 |
| sell_amt | numeric(18,2) | Y |  | 卖额 |

---

## 181. dimple.tc_exchange_rate　(7 字段)
> 表含义：汇率表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| trade_time | varchar(8) | N |  | 交易时间 |
| paris_currency | varchar(8) | N |  | 货币对 |
| bid | numeric(9,4) | N |  | 买入价 |
| ask | numeric(9,4) | N |  | 卖出价 |
| price | numeric(20,8) | N |  | 最新价 |
| price_cny | numeric(9,4) | N |  | 最新价 克/元 |

---

## 182. dimple.tc_exg_cost_adjust　(15 字段)
> 表含义：结售汇补录表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | varchar(40) | N | √ | 序列号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| exg_type | varchar(3) | N | √ | 结售汇类型：1结汇 2售汇 |
| amt_usd | numeric(38,8) | Y |  | 美元 |
| amt_rmb | numeric(38,8) | Y |  | 人民币 |
| exchange_rate | numeric(24,8) | Y |  | 汇率 |
| del_flag | varchar(3) | Y |  | 是否冲销 |
| del_date | varchar(8) | Y |  | 冲销日期 |
| op_user | varchar(16) | Y |  | 操作用户 |
| create_user | varchar(16) | Y |  | 新建人 |
| create_date | varchar(21) | Y |  | 新建日期:格式YYYY-MM-DD HH24:mi:ss |
| update_user | varchar(16) | Y |  | 修改人 |
| update_date | varchar(21) | Y |  | 修改日期:格式YYYY-MM-DD HH24:mi:ss |

---

## 183. dimple.tc_exposure_check　(22 字段)
> 表含义：品种敞口额度复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| user_id | varchar(30) | N |  | 交易员号 |
| member_id | varchar(8) | N |  | 会员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| frozen_exposure | numeric(22,6) | Y |  | 冻结敞口额度 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| buy_frozen_exposure | numeric(22,6) | Y |  | 买冻结敞口 |
| sell_frozen_exposure | numeric(22,6) | Y |  | 卖冻结敞口 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| ifcheck | varchar(1) | Y |  | 是否设置检查 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 184. dimple.tc_exposure_jour　(13 字段)
> 表含义：敞口额度流水表　|　估算行数：**1,023**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| seq_no | float8 | N | √ | 流水号:ORACLE的seq |
| user_id | varchar(30) | N |  | 交易员号 |
| member_id | varchar(8) | N |  | 会员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| day_ep_chg | numeric(22,6) | Y |  | 日中敞口额度变化值 |
| on_ep_chg | numeric(22,6) | Y |  | 隔夜敞口额度变化值 |
| op_type | varchar(2) | N |  | 信用额度流水操作类型:见tp_public_dict的068 |
| status | varchar(1) | Y |  | 流水状态:见tp_public_dict的209 |
| operator | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 185. dimple.tc_extra_exch_posi　(22 字段)
> 表含义：导入原始持仓文件表　|　估算行数：**27**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| clear_member_id | varchar(8) | N |  | 结算会员号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_turnover | numeric(18,2) | Y |  | 今日买成交额 |
| sell_turnover | numeric(18,2) | Y |  | 今日卖成交额 |
| t_buy_qty | numeric(12,0) | Y |  | 投机买持仓量 |
| b_buy_qty | numeric(12,0) | Y |  | 保值买持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量合计 |
| t_sell_qty | numeric(12,0) | Y |  | 投机卖持仓量 |
| b_sell_qty | numeric(12,0) | Y |  | 保值卖持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量合计 |
| margin | numeric(18,2) | Y |  | 交易保证金 |
| profitloss | numeric(18,2) | Y |  | 当日盈亏 |
| fee | numeric(18,2) | Y |  | 手续费 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 186. dimple.tc_extra_nomatch_posi　(22 字段)
> 表含义：导入原始持仓成交不匹配表　|　估算行数：**22**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_abbr | varchar(40) | Y |  | 交易所简称 |
| clear_date | varchar(8) | N | √ | 结算日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_turnover | numeric(18,2) | Y |  | 今日买成交额 |
| sell_turnover | numeric(18,2) | Y |  | 今日卖成交额 |
| t_buy_qty | numeric(12,0) | Y |  | 投机买持仓量 |
| b_buy_qty | numeric(12,0) | Y |  | 保值买持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量合计 |
| t_sell_qty | numeric(12,0) | Y |  | 投机卖持仓量 |
| b_sell_qty | numeric(12,0) | Y |  | 保值卖持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量合计 |
| margin | numeric(18,2) | Y |  | 交易保证金 |
| profitloss | numeric(18,2) | Y |  | 当日盈亏 |
| fee | numeric(18,2) | Y |  | 手续费 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 187. dimple.tc_extra_origin_posi　(26 字段)
> 表含义：导入原始持仓文件表　|　估算行数：**19,506**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(30) | N |  | 合约号 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量/今日空头平仓 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量/今日多头平仓 |
| buy_turnover | numeric(19,2) | Y |  | 今日买成交额 |
| sell_turnover | numeric(19,2) | Y |  | 今日卖成交额 |
| t_buy_qty | numeric(12,0) | Y |  | 投机买持仓量 |
| b_buy_qty | numeric(12,0) | Y |  | 保值买持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量合计 |
| t_sell_qty | numeric(12,0) | Y |  | 投机卖持仓量 |
| b_sell_qty | numeric(12,0) | Y |  | 保值卖持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量合计 |
| margin | numeric(19,2) | Y |  | 交易保证金 |
| profitloss | numeric(19,2) | Y |  | 当日盈亏 |
| fee | numeric(19,2) | Y |  | 手续费 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| defer_fee | numeric(19,2) | Y |  | 递延费 |
| buy_open_turnover | numeric(19,2) | Y |  | 买开成交额：上期所 |
| sell_open_turnover | numeric(19,2) | Y |  | 卖开成交额：上期所 |
| buy_offset_turnover | numeric(19,2) | Y |  | 买平成交额：上期所 |
| sell_offset_turnover | numeric(19,2) | Y |  | 卖平成交额：上期所 |

---

## 188. dimple.tc_fcurve_discount_price　(6 字段)
> 表含义：远期曲线贴现价格表：根据金交所场外询价接口-远期价格曲线推算　|　估算行数：**1,214**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| due_date | varchar(8) | N | √ | 到期日 |
| contract_id | varchar(20) | N | √ | 合约号 |
| discount_rate | numeric(20,8) | Y |  | 贴现价格 |
| day_count | numeric(10,0) | Y |  | 天数差 |
| bs_flag | bpchar(1) | N | √ | 买卖标志：见tp_public_dict的368 |

---

## 189. dimple.tc_fcvtrader_posi_detail_clear　(23 字段)
> 表含义：交易员询价持仓明细表:远期曲线算法　|　估算行数：**1,094**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 结算日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| due_date | varchar(8) | Y |  | 到期日期 |
| bus_type | varchar(3) | N | √ | 业务类型：1境内询价,2境外询价 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253 |
| delivery_type | varchar(3) | Y |  | 交割类型：见tp_public_dict的051 |
| match_no | varchar(30) | N | √ | 成交号 |
| seq_no | numeric(20,0) | N | √ | 流水号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(16,6) | Y |  | 数量 |
| float_profit | numeric(24,6) | Y |  | 合约盈亏 |
| calc_price | numeric(20,8) | Y |  | 公允价 |
| last_calc_price | numeric(20,8) | Y |  | 上日公允价 |
| fn_flag | varchar(3) | Y |  | 远近端：见tp_public_dict的250 |
| convert_rate | numeric(20,8) | Y |  | 汇率 |
| calc_amt | numeric(24,6) | Y |  | 估值金额 |
| move_flag | varchar(3) | N | √ | 调转标志(0:非调转 1:调入 2:调出) |

---

## 190. dimple.tc_flow_control　(8 字段)
> 表含义：结算前判断控制表　|　估算行数：**9**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| flow_code | varchar(3) | N | √ | 判断类型 |
| exch_code | varchar(3) | N | √ | 交易所：00#中金所，01#上期所，02#金交所 |
| oper_name | varchar(40) | N |  | 判断名称 |
| oper_flag | varchar(1) | N |  | 是否判断标志，0-不判断，1-判断 |
| oper_time | varchar(8) | Y |  | 操作时间 |
| oper_result | varchar(1) | Y |  | 操作结果,0-对账不成功，1-origin对账成功, 2-对账成功, 3-初始化 |
| err_msg | varchar(80) | Y |  | 错误原因 |
| operator | varchar(30) | Y |  | 操作人员 |

---

## 191. dimple.tc_fn_buy_lend_match_jour　(26 字段)
> 表含义：境外买断成交流水　|　估算行数：**22**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| buy_no | varchar(30) | Y |  | 买断编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 192. dimple.tc_fn_client_cost_clear　(8 字段)
> 表含义：境外品种成本结算表　|　估算行数：**183**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量（千克） |
| remain_cost | numeric(24,6) | Y |  | 剩余成本（元） |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |

---

## 193. dimple.tc_fn_client_cost_detail_clear　(22 字段)
> 表含义：境外品种成本明细结算表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 交割品种 |
| rank_no | float8 | N | √ | 序列号 |
| seq_no | float8 | N |  | 流水号 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| trans_type | varchar(2) | Y |  | 库存变化类型:见tp_public_dict的221 |
| price | numeric(20,8) | Y |  | 价格：境外黄金为 美元/盎司 |
| qty | numeric(16,6) | Y |  | 数量: 境外黄金为盎司 |
| amt | numeric(24,6) | Y |  | 成交金额: 境外黄金为美元 |
| last_remain_qty | numeric(16,6) | Y |  | 上次剩余数量（盎司），卖空时为负 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量（盎司），卖空时为负 |
| last_weighted_price | numeric(20,8) | Y |  | 上次加权平均价（美元/盎司） |
| weighted_price | numeric(20,8) | Y |  | 加权平均价（美元/盎司） |
| last_remain_cost | numeric(24,6) | Y |  | 上次剩余成本（美元） |
| remain_cost | numeric(24,6) | Y |  | 剩余成本（美元） |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |
| bill_no | varchar(30) | Y |  | 合同号 |
| cost_price | numeric(20,8) | Y |  | 还出时原拆入成本价 |
| match_type | varchar(3) | Y |  | 询价的业务类型：见tp_public_dict的253 |
| ret_no | varchar(30) | Y |  | 归还编号 |

---

## 194. dimple.tc_fn_client_storage_clear　(8 字段)
> 表含义：境外会员结算库存表　|　估算行数：**183**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| real_storage | numeric(16,6) | Y |  | 实际拥有库存量 |

---

## 195. dimple.tc_fn_def_lend_match_jour　(33 字段)
> 表含义：境外展期成交流水　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| delay_no | varchar(30) | Y |  | 展期编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| clear_price | numeric(20,8) | Y |  | 展期结算价 |
| trade_qty | numeric(16,6) | Y |  | 展期重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_base | varchar(3) | Y |  | 计息基准 |
| interest_period | varchar(3) | Y |  | 付息周期 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 196. dimple.tc_fn_discount_price　(6 字段)
> 表含义：贴现价格表　|　估算行数：**14,273**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| due_date | varchar(8) | N | √ | 到期日 |
| contract_id | varchar(20) | N | √ | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志：见tp_public_dict的002 |
| discount_rate | numeric(20,8) | Y |  | 贴现价格 |
| day_count | numeric(10,0) | Y |  | 天数差 |

---

## 197. dimple.tc_fn_offset_profit_clear　(14 字段)
> 表含义：境外平仓盈亏表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| user_id | varchar(16) | Y |  | 交易员 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(16,6) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(16,6) | Y |  | 卖平仓量 |
| profitloss | numeric(24,6) | Y |  | 盈亏 |
| contract_profitloss | numeric(24,6) | Y |  | 合约盈亏 |
| match_no | varchar(20) | Y |  | 成交号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 198. dimple.tc_fn_posi_move　(33 字段)
> 表含义：交易员境外持仓内部调转表　|　估算行数：**17**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N |  | 系统编号 |
| move_no | varchar(30) | N | √ | 调拨流水号 |
| match_no | varchar(30) | N |  | 成交单号 |
| match_date | varchar(8) | N |  | 成交日期 |
| hf_flag | varchar(3) | N |  | 境内外标志(1：境内，2：境外) |
| bus_type | varchar(3) | N |  | 业务类型:见tp_public_dict的253 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| fn_flag | varchar(3) | N |  | 近远端标志:见tp_public_dict的250 |
| counterparty_no | varchar(10) | Y |  | 交易对手方 |
| counterparty_abbr | varchar(20) | Y |  | 交易对手方简称 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_qty | numeric(24,6) | N |  | 原交易数量 |
| trade_price | numeric(20,8) | N |  | 原成交价格 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| reference_type | varchar(3) | Y |  | 参考价类型：见tp_public_dict的288 |
| reference_price | numeric(20,8) | Y |  | 参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| qty | numeric(24,6) | N |  | 调拨数量 |
| price | numeric(20,8) | N |  | 调拨价格 |
| user_id_out | varchar(16) | N |  | 交易员调出方 |
| user_id_in | varchar(16) | N |  | 交易员调入方 |
| purpose_code_in | varchar(3) | N |  | 调入交易目的 |
| purpose_code_out | varchar(3) | N |  | 调出交易目的 |
| notes | varchar(254) | Y |  | 备注 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |

---

## 199. dimple.tc_fn_ret_lend_match_jour　(23 字段)
> 表含义：境外归还成交流水　|　估算行数：**27**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| ret_no | varchar(30) | Y |  | 归还编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：见tp_public_dict的221.还入和还出 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 200. dimple.tc_fn_storage_move　(17 字段)
> 表含义：交易员境外库存内部调拨表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N |  | 系统编号 |
| move_no | varchar(30) | N | √ | 调拨流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约代码 |
| user_id_out | varchar(16) | N |  | 交易员调出方 |
| user_id_in | varchar(16) | N |  | 交易员调入方 |
| purpose_code_in | varchar(3) | N |  | 调入交易目的 |
| purpose_code_out | varchar(3) | N |  | 调出交易目的 |
| qty | numeric(24,6) | N |  | 调拨数量 |
| price | numeric(20,8) | Y |  | 调拨价格 |
| notes | varchar(254) | Y |  | 备注 |
| if_calc | varchar(3) | N |  | 是否用于拆借:见dict的027 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |

---

## 201. dimple.tc_fn_trader_cost_clear　(10 字段)
> 表含义：交易员合约成本结算表 品种内容仅限于现货、境外黄金　|　估算行数：**604**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| user_id | varchar(30) | N | √ | 交易员 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量：现货为手；境外黄金为 盎司 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：现货为元；境外黄金为 美元 |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 202. dimple.tc_fn_trader_cost_detail_clear　(22 字段)
> 表含义：境外品种成本明细结算表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| rank_no | float8 | N | √ | 序列号 |
| seq_no | float8 | N |  | 流水号 |
| match_no | varchar(30) | N |  | 成交号 |
| user_id | varchar(30) | N | √ | 交易员 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| trans_type | varchar(3) | Y |  | 库存变化类型:1：入库；k：出库 |
| price | numeric(20,8) | Y |  | 价格：境外黄金为 美元/盎司 |
| qty | numeric(16,6) | Y |  | 数量:境外黄金为盎司 |
| amt | numeric(24,6) | Y |  | 成交金额:境外黄金为美元 |
| last_remain_qty | numeric(16,6) | Y |  | 上次剩余数量（盎司），卖空时为负 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量：境外黄金为盎司，卖空时为负 |
| last_weighted_price | numeric(20,8) | Y |  | 上次加权平均价：境外黄金为 美元/盎司 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：境外黄金为 美元/盎司 |
| last_remain_cost | numeric(24,6) | Y |  | 上次剩余成本：境外黄金为美元 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：境外黄金为美元 |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| ret_no | varchar(30) | Y |  | 归还编号 |

---

## 203. dimple.tc_fn_trader_storage_clear　(10 字段)
> 表含义：交易员结算库存表　|　估算行数：**605**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| contract_id | varchar(20) | N | √ | 合约 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| real_storage | numeric(16,6) | Y |  | 实际拥有库存量 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 204. dimple.tc_foreign_buy_lend_match　(25 字段)
> 表含义：境外买断成交　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| buy_no | varchar(30) | N | √ | 买断编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| buy_price | numeric(20,8) | Y |  | 买断价格 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| buy_amt | numeric(24,6) | Y |  | 买断金额 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 205. dimple.tc_foreign_clear_price　(8 字段)
> 表含义：外部结算价　|　估算行数：**77**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| contract_id | varchar(20) | N | √ | 合约 |
| bs_flag | varchar(3) | N | √ | 买卖标志：见tp_public_dict的002 |
| reference_type | varchar(3) | N | √ | 参考价类型：见tp_public_dict的288 |
| price | numeric(20,8) | N |  | 价格 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 206. dimple.tc_foreign_discount_rate　(8 字段)
> 表含义：外部结算价贴现率　|　估算行数：**2,869**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| contract_id | varchar(20) | N | √ | 合约 |
| bs_flag | bpchar(1) | N | √ | 买卖标志：见tp_public_dict的002 |
| reference_type | varchar(3) | N | √ | 贴现率类型：见tp_public_dict的289 |
| price | numeric(20,8) | N |  | 价格 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 207. dimple.tc_foreign_inquire_match　(36 字段)
> 表含义：境外询价成交　|　估算行数：**245**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N |  | 成交单号 |
| seq_no | float8 | N | √ | 系统流水号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量:盎司 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量:盎司 |
| price | numeric(20,8) | Y |  | 成交价格:美元/盎司 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| deal_type | varchar(3) | Y |  | 处理方式：见tp_public_dict的248 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 一级复核人员 |
| check_date | varchar(8) | Y |  | 一级复核日期 |
| check_time | varchar(8) | Y |  | 一级复核时间 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| remark | varchar(500) | Y |  | 备注 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| send_status | varchar(3) | Y |  | 电文发送状态：见tp_public_dict的294 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |

---

## 208. dimple.tc_foreign_inquire_match_jour　(34 字段)
> 表含义：境外询价成交　|　估算行数：**2,885**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N |  | 成交单号 |
| seq_no | float8 | N | √ | 系统流水号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量:盎司 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量:盎司 |
| price | numeric(20,8) | Y |  | 成交价格:美元/盎司 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| deal_type | varchar(3) | Y |  | 处理方式：见tp_public_dict的248 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 一级复核人员 |
| check_date | varchar(8) | Y |  | 一级复核日期 |
| check_time | varchar(8) | Y |  | 一级复核时间 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| remark | varchar(500) | Y |  | 备注 |
| coefficient | numeric(5,4) | Y |  | 系数 |

---

## 209. dimple.tc_foreign_lend_match　(40 字段)
> 表含义：境外拆借成交　|　估算行数：**25**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| exchange | numeric(12,8) | Y |  | 汇率 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| is_finish | varchar(3) | Y |  | 是否已了结:见tp_public_dict的027 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |

---

## 210. dimple.tc_foreign_lend_match_jour　(40 字段)
> 表含义：境外询价成交流水　|　估算行数：**160**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| exchange | numeric(12,8) | Y |  | 汇率 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| coefficient | numeric(5,4) | Y |  | 系数? |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |

---

## 211. dimple.tc_foreign_message　(28 字段)
> 表含义：电文管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_date | varchar(8) | N |  | 交易日期 |
| seq_no | varchar(40) | N |  | 业务流水号 |
| business_type | varchar(3) | N |  | 业务类型 |
| sub_type | varchar(3) | N |  | 子类型 |
| business_no | varchar(30) | N |  | 交易编号 |
| debit_name | varchar(40) | Y |  | 借方账号 |
| debit_type | varchar(3) | Y |  | 借方币种 |
| debit_date | varchar(8) | Y |  | 借方起息日 |
| credit_type | varchar(3) | Y |  | 贷方币种 |
| business_amt | varchar(40) | Y |  | 交易金额 |
| remitter_name | varchar(40) | Y |  | 汇款人名称 |
| remitter_addr | varchar(40) | Y |  | 汇款人地址 |
| remitter_account | varchar(40) | Y |  | 汇款人账号 |
| payee_name | varchar(40) | Y |  | 收款人名称 |
| payee_addr | varchar(40) | Y |  | 收款人地址 |
| payee_account | varchar(40) | Y |  | 收款人账号 |
| payee_bank | varchar(40) | Y |  | 收款银行 |
| intermidiary_bank | varchar(40) | Y |  | 中间行 |
| remark | varchar(40) | Y |  | 汇款附言 |
| create_date | varchar(8) | Y |  | 生成日期 |
| create_time | varchar(8) | Y |  | 生成时间 |
| deal_status | varchar(3) | Y |  | 处理状态 |
| uuid | varchar(60) | Y |  | swfit-uuid |
| send_seq_no | varchar(40) | Y |  | 发送流水号 |
| ft_code | varchar(40) | Y |  | 核心交易流水号 |
| member_id | varchar(8) | Y |  | 会员号 |
| cnsmrsysid | varchar(8) | Y |  | 消费方系统标识,固定GTM |
| cnltxncd | varchar(8) | Y |  | 渠道交易码字 |

---

## 212. dimple.tc_foreign_ret_lend_match　(23 字段)
> 表含义：境外归还成交　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| ret_no | varchar(30) | N | √ | 归还编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| contract_id | varchar(20) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：见tp_public_dict的221.还入和还出 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_sec_id | varchar(30) | Y |  | 二级复核人员 |
| check_sec_date | varchar(8) | Y |  | 二级复核日期 |
| check_sec_time | varchar(8) | Y |  | 二级复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 213. dimple.tc_foreign_trader_relation　(8 字段)
> 表含义：交易员与外部交易员对应关系　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| trader | varchar(40) | N |  | 交易员 |
| foreign_trader | varchar(40) | N |  | 外部交易员 |
| isactive | varchar(3) | Y |  | 是否有效:见tp_public_dict的027 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| foreign_trader_source | varchar(2) | Y |  | 外部交易员来源：1-上金所 2-上期所 3-外汇交易中心 |

---

## 214. dimple.tc_ftr_client_posi_clear　(29 字段)
> 表含义：期货客户结算持仓表:日终结算时计算，也是次日持仓初始数据的来源。　|　估算行数：**31,349**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量-今日交割平仓(交割持仓表)＋期权执行期货建仓量（期权执行期货建仓表），计算时可直接从成交表，盘后成交表，交割匹配表统一计算 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数:先投机后保值 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏:根据期货平仓盈亏表计算 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| open_fee | numeric(18,2) | Y |  | 开仓结算手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| t_open_fee | numeric(18,2) | Y |  | 开仓交易手续费 |
| t_offset_fee | numeric(18,2) | Y |  | 平仓交易手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费:来自对期货短线明细表的汇总 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |

---

## 215. dimple.tc_ftr_fee　(25 字段)
> 表含义：期货手续费率表:分为四个级别，品种，特殊合约，特殊结算帐号和特殊交易编码　|　估算行数：**1,542**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码:$表示所有合约 |
| clear_account_no | varchar(14) | Y |  | 结算子帐号:$表示所有结算帐号 |
| client_id | varchar(16) | N | √ | 客户号:$表示所有客户 |
| member_id | varchar(8) | N | √ | 会员号:$表示所有会员 |
| open_fee | numeric(22,6) | N |  | 开仓结算手续费 |
| offset_fee | numeric(22,6) | N |  | 平仓结算手续费 |
| t_open_fee | numeric(22,6) | N |  | 开仓交易手续费 |
| t_offset_fee | numeric(22,6) | N |  | 平仓交易手续费 |
| short_open_fee | numeric(22,6) | N |  | 短线开仓手续费 |
| short_offset_fee | numeric(22,6) | N |  | 短线平仓手续费 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| spot_fee | numeric(22,6) | Y |  | 现货手续费 |
| attr | varchar(3) | N | √ | 交易编码属性::$-代表全部,见tp_public_dict263 |
| app_type | varchar(3) | N | √ | 定价成交申报类型:0-默认,见tp_public_dict330 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 216. dimple.tc_ftr_fee_check　(27 字段)
> 表含义：交易所手续费率复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| exch_code | varchar(2) | N |  | 交易所 |
| variety_id | varchar(4) | N |  | 品种代码 |
| contract_id | varchar(20) | N |  | 合约代码:$表示所有合约 |
| clear_account_no | varchar(14) | Y |  | 结算子帐号:$表示所有结算帐号 |
| client_id | varchar(16) | N |  | 客户号:$表示所有客户 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| open_fee | numeric(22,6) | N |  | 开仓结算手续费 |
| offset_fee | numeric(22,6) | N |  | 平仓结算手续费 |
| t_open_fee | numeric(22,6) | N |  | 开仓交易手续费 |
| t_offset_fee | numeric(22,6) | N |  | 平仓交易手续费 |
| short_open_fee | numeric(22,6) | N |  | 短线开仓手续费 |
| short_offset_fee | numeric(22,6) | N |  | 短线平仓手续费 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| attr | varchar(3) | N |  | 交易编码属性::$-代表全部,见tp_public_dict263 |
| app_type | varchar(3) | N |  | 定价成交申报类型:0-默认,见tp_public_dict330 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 217. dimple.tc_ftr_match_manage_jour　(17 字段)
> 表含义：成交管理流水表　|　估算行数：**57,921**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(30) | Y |  | 合约号 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖标志 |
| user_id_old | varchar(30) | Y |  | 原交易员号 |
| user_id | varchar(30) | Y |  | 交易员号 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作员 |
| qty | numeric(12,0) | Y |  | 数量 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| purpose_code_old | varchar(3) | Y |  | 原交易目的 |
| oper_type | varchar(3) | Y |  | 操作类型：见数据字典267 |
| notes | varchar(250) | Y |  | 备注 |
| isnote_flag | varchar(2) | Y |  | 是否备注 |

---

## 218. dimple.tc_ftr_match_short_tmp　(15 字段)
> 表含义：期货短线成交临时表：供短线认定使用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| match_no | varchar(20) | N |  | 成交号 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| remain_qty | numeric(12,0) | Y |  | 计算剩余数量（手） |
| sort_id | bpchar(1) | Y |  | 排序 |
| offset_id | bpchar(1) | Y |  | 分组 |
| unit | float8 | N |  | 合约乘数 |
| short_flag | bpchar(1) | N |  | 是否短线标志：见tp_public_dict的027 |

---

## 219. dimple.tc_ftr_match_short_trader_tmp　(17 字段)
> 表含义：交易员期货短线成交临时表：供短线认定使用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| trader_no | varchar(16) | N |  | 席位号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| match_no | varchar(20) | N |  | 成交号 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| remain_qty | numeric(12,0) | Y |  | 计算剩余数量（手） |
| sort_id | bpchar(1) | Y |  | 排序 |
| offset_id | bpchar(1) | Y |  | 分组 |
| unit | float8 | N |  | 合约乘数 |
| short_flag | bpchar(1) | N |  | 是否短线标志：见tp_public_dict的027 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 220. dimple.tc_ftr_purpose_posi_clear　(33 字段)
> 表含义：交易目的期货结算持仓表　|　估算行数：**1,637**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额 |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| buy_float_profitloss | numeric(18,2) | Y |  | 买持仓盈亏 |
| sell_float_profitloss | numeric(18,2) | Y |  | 卖持仓盈亏 |
| buy_margin | numeric(18,2) | Y |  | 买保证金 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金 |
| buy_margin_exch | numeric(18,2) | Y |  | 交易所买保证金 |
| sell_margin_exch | numeric(18,2) | Y |  | 交易所卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| float_profitloss_tot | numeric(18,2) | Y |  | 累积持仓盈亏 |
| buy_offset_profitloss | numeric(18,2) | Y |  | 买平仓盈亏 |
| sell_offset_profitloss | numeric(18,2) | Y |  | 卖平仓盈亏 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 221. dimple.tc_ftr_short_detail　(27 字段)
> 表含义：期货短线明细表:记录短线成交明细。此表数据从成交明细以及短线手续费率中得到。仅保留当天　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| open_match_no | varchar(20) | N | √ | 开仓成交号 |
| offset_match_no | varchar(20) | N | √ | 平仓成交号 |
| open_bs_flag | bpchar(1) | N | √ | 开仓买卖标志:见tp_public_dict的002 |
| open_qty | numeric(12,0) | Y |  | 开仓数量 |
| open_price | numeric(20,8) | Y |  | 开仓价 |
| open_fee_rate | numeric(22,6) | Y |  | 开仓手续费率 |
| short_open_fee_rate | numeric(22,6) | Y |  | 短线开仓手续费率 |
| open_match_time | varchar(12) | Y |  | 开仓成交时间 |
| offset_bs_flag | bpchar(1) | Y |  | 平仓买卖标志:见tp_public_dict的002 |
| offset_qty | numeric(12,0) | Y |  | 平仓数量 |
| offset_price | numeric(20,8) | Y |  | 平仓价 |
| offset_fee_rate | numeric(22,6) | Y |  | 平仓手续费率 |
| short_offset_fee_rate | numeric(22,6) | Y |  | 短线平仓手续费率 |
| offset_match_time | varchar(12) | Y |  | 平仓成交时间 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| short_qty | numeric(12,0) | Y |  | 短线量 |
| short_fee | numeric(18,2) | Y |  | 短线手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费 |
| exch_open_fee_rate | numeric(22,6) | Y |  | 交易所开仓手续费率 |
| exch_short_open_fee_rate | numeric(22,6) | Y |  | 交易所短线开仓手续费率 |
| exch_offset_fee_rate | numeric(22,6) | Y |  | 交易所平仓手续费率 |
| exch_short_offset_fee_rate | numeric(22,6) | Y |  | 交易所短线平仓手续费率 |
| exch_short_fee | numeric(18,2) | Y |  | 交易所短线手续费 |
| exch_ret_fee | numeric(18,2) | Y |  | 交易所返还手续费 |

---

## 222. dimple.tc_ftr_trader_posi　(31 字段)
> 表含义：交易员期货交易持仓表:更新交易员持仓时，需要更新此表。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |
| buy_margin_rate | numeric(18,2) | Y |  | 买固定保证金 |
| sell_margin_rate | numeric(18,2) | Y |  | 卖固定保证金 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| buy_offset_profitloss | numeric(18,2) | Y |  | 买平仓盈亏 |
| sell_offset_profitloss | numeric(18,2) | Y |  | 卖平仓盈亏 |
| buy_defer_qty | numeric(12,0) | Y |  | 买递延冻结数量 |
| sell_defer_qty | numeric(12,0) | Y |  | 卖递延冻结数量 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 223. dimple.tc_ftr_trader_posi_clear　(38 字段)
> 表含义：交易员期货结算持仓表　|　估算行数：**43,937**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额 |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| open_fee | numeric(18,2) | Y |  | 开仓结算手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| t_open_fee | numeric(18,2) | Y |  | 开仓交易手续费 |
| t_offset_fee | numeric(18,2) | Y |  | 平仓交易手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费 |
| buy_margin | numeric(18,2) | Y |  | 买保证金 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金 |
| buy_margin_exch | numeric(18,2) | Y |  | 交易所买保证金 |
| sell_margin_exch | numeric(18,2) | Y |  | 交易所卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| float_profitloss_tot | numeric(18,2) | Y |  | 累积持仓盈亏 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| buy_offset_profitloss | numeric(18,2) | Y |  | 买平仓盈亏 |
| sell_offset_profitloss | numeric(18,2) | Y |  | 卖平仓盈亏 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 224. dimple.tc_his_account_database　(14 字段)
> 表含义：账务数据源表　|　估算行数：**39,724**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| exch_type | varchar(3) | Y |  | 业务类型：交易所 |
| bus_code | varchar(40) | N |  | 业务代码 |
| bus_name | varchar(100) | N |  | 业务名称 |
| amt | numeric(24,6) | N |  | 金额 |
| currency | varchar(3) | Y |  | 币种 |
| variety_id | varchar(4) | Y |  | 产品号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_no | varchar(100) | Y |  | 成交号 |
| qty | numeric(20,3) | Y |  | 数量 |
| cost_type | varchar(10) | Y |  | 成本中心： 见dict316 |
| account_type | varchar(3) | Y |  | 帐务类型：见dict313 |

---

## 225. dimple.tc_his_alarm_note　(11 字段)
> 表含义：报警信息历史表　|　估算行数：**10,637,390**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| alarm_date | varchar(8) | N | √ | 报警日期 |
| seq_no | float8 | N | √ | 流水号 |
| alarm_type | bpchar(1) | N | √ | 报警类型(敞口/止损):见tp_public_dict的232 |
| alarm_time | varchar(8) | N |  | 报警时间 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| variety_id | varchar(4) | N |  | 品种 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| alarm_note | varchar(254) | Y |  | 报警信息 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 226. dimple.tc_his_bond_delivery　(11 字段)
> 表含义：国债交割数据 - 国债交割导入表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 导入日期 |
| exch_code | varchar(4) | Y |  | 交易所编号 |
| clear_member_id | varchar(14) | Y |  | 结算会员号 |
| clear_member_abbr | varchar(14) | Y |  | 结算会员简称 |
| delivery_variety_id | varchar(8) | Y |  | 交割合约 |
| clear_account_no | varchar(12) | Y |  | 资金账号 |
| propertie | varchar(12) | Y |  | 属性 |
| clear_price | varchar(14) | Y |  | 交割结算价 |
| buy_qty | varchar(14) | Y |  | 买入量 |
| sell_qty | varchar(14) | Y |  | 卖出量 |
| delivery_fee | varchar(14) | Y |  | 交割手续费 |

---

## 227. dimple.tc_his_control_process　(9 字段)
> 表含义：流程控制表　|　估算行数：**10,736**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| pro_id | numeric(6,0) | N | √ | 流程号 |
| pro_seq | numeric(6,0) | Y |  | 流程序号 |
| pro_name | varchar(40) | Y |  | 流程名称 |
| pro_model | varchar(20) | Y |  | 流程所属模块 |
| process_status | varchar(3) | Y |  | 流程状态:0 初始化(无色) 1 进行中(黄色) 2 成功(绿色) 3 失败(红色) |
| pro_remark | varchar(250) | Y |  | 流程备注 |
| operator | varchar(30) | Y |  | 操作人员 |
| oper_time | varchar(8) | Y |  | 操作时间 |

---

## 228. dimple.tc_his_cparty_amt_limit　(11 字段)
> 表含义：交易对手方限额历史表　|　估算行数：**1,044**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 统计日期 |
| counterparty | varchar(10) | N | √ | 对手方代码 |
| cp_abbr | varchar(30) | Y |  | 对手方简称 |
| currency | varchar(3) | N | √ | 币种：见tp_public_dict的036 |
| trade_type | varchar(3) | N | √ | 类型：见tp_public_dict的280 |
| end_date | varchar(8) | Y |  | 到期日 |
| cp_name | varchar(100) | Y |  | 对手方名称 |
| limit_amt | numeric(24,6) | Y |  | 限额 |
| used_amt | varchar(20) | Y |  | 已用额度 |
| overtime_amt | varchar(20) | Y |  | 超期占用额度 |
| remain_amt | numeric(24,6) | Y |  | 剩余额度 |

---

## 229. dimple.tc_his_defer_delivery_match　(13 字段)
> 表含义：递延交割申报成交历史表　|　估算行数：**932**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| match_time | varchar(8) | Y |  | 成交时间 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| middle_flag | bpchar(1) | Y |  | 是否为中立仓: 0否,1是 |
| trader_no | varchar(15) | N | √ | 席位号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 230. dimple.tc_his_delivery_fee　(15 字段)
> 表含义：品种交割手续费率历史表　|　估算行数：**1,747,162**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| delivery_fee | numeric(22,6) | N |  | 交割手续费率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| exch_code | varchar(6) | N | √ | 交易所代码 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 231. dimple.tc_his_delivery_margin_rate　(8 字段)
> 表含义：历史交割保证金率表　|　估算行数：**1,426,761**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| margin_flag | bpchar(1) | N | √ | 保证金标志:见tp_public_dict的223 |
| margin_rate | numeric(22,6) | N |  | 保证金率 |
| margin_type | varchar(2) | Y |  | 保证金类型:见tp_public_dict的092 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 232. dimple.tc_his_etf_fee_detail　(12 字段)
> 表含义：ETF当日手续费明细历史表　|　估算行数：**207**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| seq_no | float8 | N | √ | 序号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| trader_no | varchar(30) | Y |  | 交易员 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| money_type | varchar(3) | N | √ | 费用类型:见public_dict 273 |
| amt | numeric(24,6) | Y |  | 金额 |

---

## 233. dimple.tc_his_etf_list　(24 字段)
> 表含义：ETF明细历史清单　|　估算行数：**280**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| member_id | varchar(8) | Y |  | 会员代码 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| calc_amt_1 | numeric(24,6) | Y |  | T日预估现金差额1 |
| amt_1 | numeric(24,6) | Y |  | T-1日现金差额1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| calc_amt_2 | numeric(24,6) | Y |  | T日预估现金差额2 |
| amt_2 | numeric(24,6) | Y |  | T-1日现金差额2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| calc_amt_3 | numeric(24,6) | Y |  | T日预估现金差额3 |
| amt_3 | numeric(24,6) | Y |  | T-1日现金差额3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| calc_amt_4 | numeric(24,6) | Y |  | T-1日现金差额4 |
| amt_4 | numeric(24,6) | Y |  | T日预估现金差额4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| calc_amt_5 | numeric(24,6) | Y |  | T日预估现金差额5 |
| amt_5 | numeric(24,6) | Y |  | T-1日现金差额5 |
| min_qty | numeric(12,0) | Y |  | 最小申购赎回重量 |
| max_apply_qty | numeric(12,0) | Y |  | 当日申购上限 |
| max_ransom_qty | numeric(12,0) | Y |  | 当日赎回上限 |
| if_ar | varchar(3) | Y |  | 当日是否允许申购/赎回标志:见数据字典027 |
| etf_unit | numeric(16,6) | Y |  | 每份黄金ETF基金对应的黄金重量 |

---

## 234. dimple.tc_his_etf_match　(28 字段)
> 表含义：ETF成交明细历史表　|　估算行数：**410**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| trader_no | varchar(30) | N | √ | 交易员 |
| self_local_no | varchar(30) | Y |  | Fund成交编号 |
| local_seq_no | varchar(20) | N | √ | 本地编号 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| member_id | varchar(8) | N | √ | 会员代码 |
| client_id | varchar(16) | N | √ | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| qty_1 | numeric(20,6) | Y |  | 重量1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| qty_2 | numeric(20,6) | Y |  | 重量2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| qty_3 | numeric(20,6) | Y |  | 重量3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| qty_4 | numeric(20,6) | Y |  | 重量4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| qty_5 | numeric(20,6) | Y |  | 重量5 |
| status | varchar(4) | Y |  | 状态:见tp_public_dict的269 |
| system_status | varchar(3) | Y |  | 系统状态:见tp_public_dict的271 |
| confirm_date | varchar(8) | Y |  | 确认日期 |

---

## 235. dimple.tc_his_etf_match_detail　(21 字段)
> 表含义：ETF历史成交展开表　|　估算行数：**230**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| seq_no | float8 | N | √ | 序号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| confirm_date | varchar(8) | Y |  | 确认日期 |
| trader_no | varchar(30) | Y |  | 交易员 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| local_seq_no | varchar(20) | Y |  | 本地编号 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| delivery_variety_id | varchar(3) | Y |  | 交割品种 |
| qty | numeric(20,6) | Y |  | 重量 |
| calc_type | varchar(3) | Y |  | 计算类型:见public_dict 273 |
| calc_value | numeric(24,6) | Y |  | 计算值 |

---

## 236. dimple.tc_his_exch_margin_rate　(14 字段)
> 表含义：交易所保证金率历史表　|　估算行数：**47,743**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号:中金所时使用，其他时刻为$ |
| contract_id | varchar(80) | N | √ | 合约代码 |
| sh_flag | varchar(3) | N | √ | 交易编码属性:见tp_public_dict263 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| margin_type | bpchar(1) | N |  | 保证金类型:预留，用于确定保证金率是比率值还是固定值。参考常量表。－》见tp_public_dict的092。 |
| buy_rate | numeric(10,6) | N |  | 买率 |
| sell_rate | numeric(10,6) | N |  | 卖率 |
| buy_fix | numeric(22,6) | N |  | 买固定值：非报价合约保留2位小数 |
| sell_fix | numeric(22,6) | N |  | 卖固定值：非报价合约保留2位小数 |
| remark | varchar(254) | Y |  | 备注:在备注字段中记录保证金率取值来源 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 237. dimple.tc_his_exchange_rate　(7 字段)
> 表含义：汇率历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| trade_time | varchar(8) | N |  | 交易时间 |
| paris_currency | varchar(8) | N |  | 货币对 |
| bid | numeric(9,4) | N |  | 买入价 |
| ask | numeric(9,4) | N |  | 卖出价 |
| price | numeric(20,8) | N |  | 最新价 |
| price_cny | numeric(9,4) | N |  | 最新价 克/元 |

---

## 238. dimple.tc_his_flow_control　(9 字段)
> 表含义：结算前判断控制历史表　|　估算行数：**23,549**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| flow_code | varchar(3) | N | √ | 判断类型 |
| exch_code | varchar(3) | N | √ | 交易所：00#中金所，01#上期所，02#金交所 |
| oper_name | varchar(40) | N |  | 判断名称 |
| oper_flag | varchar(1) | N |  | 是否判断标志，0-不判断，1-判断 |
| oper_time | varchar(8) | Y |  | 操作时间 |
| oper_result | varchar(1) | Y |  | 操作结果,0-对账不成功，1-origin对账成功, 2-对账成功 |
| err_msg | varchar(120) | Y |  | 错误原因 |
| operator | varchar(30) | Y |  | 操作人员 |

---

## 239. dimple.tc_his_ftr_fee　(25 字段)
> 表含义：期货手续费率历史表　|　估算行数：**1,305,708**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码:$表示所有合约 |
| clear_account_no | varchar(14) | Y |  | 结算子帐号:$表示所有结算帐号 |
| client_id | varchar(16) | N | √ | 客户号:$表示所有客户 |
| member_id | varchar(8) | N | √ | 会员号:$表示所有会员 |
| open_fee | numeric(22,6) | N |  | 开仓结算手续费 |
| offset_fee | numeric(22,6) | N |  | 平仓结算手续费 |
| t_open_fee | numeric(22,6) | N |  | 开仓交易手续费 |
| t_offset_fee | numeric(22,6) | N |  | 平仓交易手续费 |
| short_open_fee | numeric(22,6) | N |  | 短线开仓手续费 |
| short_offset_fee | numeric(22,6) | N |  | 短线平仓手续费 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| spot_fee | numeric(22,6) | Y |  | 现货手续费 |
| attr | varchar(3) | N |  | 交易编码属性::$-代表全部,见tp_public_dict263 |
| app_type | varchar(3) | N | √ | 定价成交申报类型:0-默认,见tp_public_dict330 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 240. dimple.tc_his_ftr_match　(22 字段)
> 表含义：历史期货成交表:闭市后将交易中的数据同步到此表。　|　估算行数：**712,466**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| tid | numeric(10,0) | N |  | 事务编号 |
| contract_id | varchar(20) | N |  | 合约号 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| trader_no | varchar(16) | N | √ | 席位号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| app_type | varchar(3) | N | √ | 定价成交申报类型:0-默认,见tp_public_dict330 |
| org_trade_type | bpchar(1) | N |  | 成交类型:0-普通成交,见tp_public_dict497 |

---

## 241. dimple.tc_his_hz_account　(23 字段)
> 表含义：杭州银行账务管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| batch_no | varchar(40) | N | √ | 批次号 |
| seq_no | varchar(40) | N | √ | 记账流水号 |
| business_type | varchar(40) | Y |  | 业务类型 |
| sub_type | varchar(40) | Y |  | 子类型 |
| buy_flag | varchar(40) | N | √ | 借贷收付 |
| subject | varchar(40) | Y |  | 科目 |
| name | varchar(40) | Y |  | 名称 |
| account | varchar(20) | Y |  | 账号 |
| account_name | varchar(40) | Y |  | 账户名称 |
| branches | varchar(10) | Y |  | 网点号 |
| currency | varchar(40) | Y |  | 币种 |
| amt | numeric(38,8) | Y |  | 发生额 |
| remark | varchar(100) | Y |  | 摘要 |
| send_status | varchar(10) | Y |  | 发送状态 |
| status | varchar(10) | Y |  | 处理状态:见tp_public_dict的311 |
| fail_reason | varchar(40) | Y |  | 失败原因 |
| main_no | varchar(40) | Y |  | 主机流水号 |
| main_date | varchar(8) | Y |  | 核心日期 |
| create_time | varchar(8) | Y |  | 生成时间 |
| sysno | varchar(40) | Y |  | 系统编号 |
| uuid | varchar(40) | Y |  | 唯一识别码 |
| del_flag | varchar(3) | Y |  | 是否冲销标志 |

---

## 242. dimple.tc_his_inquire_itgt_client　(9 字段)
> 表含义：客户询价综合头寸历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_int | numeric(15,3) | Y |  | 买头寸 |
| buy_amt | numeric(24,6) | Y |  | 买金额 |
| sell_int | numeric(15,3) | Y |  | 卖头寸 |
| sell_amt | numeric(24,6) | Y |  | 卖金额 |
| net_int | numeric(15,3) | Y |  | 净头寸 |
| net_amt | numeric(24,6) | Y |  | 净金额 |

---

## 243. dimple.tc_his_inquire_itgt_trader　(11 字段)
> 表含义：交易员询价综合头寸历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| trader_no | varchar(40) | N | √ | 交易员 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| buy_int | numeric(15,3) | Y |  | 买头寸 |
| buy_amt | numeric(24,6) | Y |  | 买金额 |
| sell_int | numeric(15,3) | Y |  | 卖头寸 |
| sell_amt | numeric(24,6) | Y |  | 卖金额 |
| net_int | numeric(15,3) | Y |  | 净头寸 |
| net_amt | numeric(24,6) | Y |  | 净金额 |

---

## 244. dimple.tc_his_inquire_match　(22 字段)
> 表含义：询价成交历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| cfets_match_no | varchar(20) | Y |  | 外汇交易所成交号 |
| match_folder | varchar(10) | Y |  | 交易目录 |
| match_seq_no | varchar(20) | N | √ | 成交流水号 |
| trader_no | varchar(40) | Y |  | 交易员 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| spot_price | numeric(20,8) | Y |  | 即期价格 |
| tick | numeric(16,8) | Y |  | 点数 |
| price | numeric(20,8) | Y |  | 成交价格 |
| qty | numeric(12,0) | Y |  | 成交数量（克） |
| amt | numeric(24,6) | Y |  | 成交金额 |
| reg_date | varchar(8) | Y |  | 登记日 |
| end_date | varchar(8) | Y |  | 到期日 |
| fn_flag | varchar(3) | Y |  | 近远端:见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源:见tp_public_dict的249 |
| deal_type | varchar(3) | N |  | 处理方式:见tp_public_dict的248 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| match_type | varchar(3) | N | √ | 交易类型:见tp_public_dict的251 |
| trade_mode | varchar(3) | Y |  | 成交模式:0-即期;1-远期;2-掉期 |

---

## 245. dimple.tc_his_inquire_match_checked　(24 字段)
> 表含义：询价成交历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| cfets_match_no | varchar(20) | Y |  | 外汇交易所成交号 |
| match_folder | varchar(10) | Y |  | 交易目录 |
| match_seq_no | varchar(20) | Y |  | 成交流水号 |
| trader_no | varchar(40) | Y |  | 交易员 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| spot_price | numeric(20,8) | Y |  | 即期价格 |
| tick | numeric(16,8) | Y |  | 点数 |
| price | numeric(20,8) | Y |  | 成交价格 |
| qty | numeric(12,0) | Y |  | 成交数量（克） |
| amt | numeric(24,6) | Y |  | 成交金额 |
| reg_date | varchar(8) | Y |  | 登记日 |
| end_date | varchar(8) | Y |  | 到期日 |
| fn_flag | varchar(3) | Y |  | 近远端:见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源:见tp_public_dict的249 |
| deal_type | varchar(3) | N | √ | 处理方式:见tp_public_dict的248 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| match_type | varchar(3) | Y |  | 交易类型:见tp_public_dict的251 |
| trade_mode | varchar(3) | Y |  | 成交模式:0-即期;1-远期;2-掉期 |

---

## 246. dimple.tc_his_kondor_match　(18 字段)
> 表含义：境外成交历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| seq_no | numeric(8,0) | N | √ | 流水号 |
| bs_flag | bpchar(1) | N |  | 买卖方向:见tp_public_dict的002 |
| trade_date | varchar(8) | N | √ | 交易日 |
| match_time | varchar(20) | Y |  | 录入时间 |
| price_usa | numeric(20,8) | Y |  | 价格(美元/盎司) |
| exchange_rate | numeric(9,4) | Y |  | 实时汇率 |
| price_cny | numeric(20,8) | Y |  | 价格(元/克) |
| qty | numeric(15,2) | Y |  | 数量（盎司） |
| amt | numeric(24,6) | Y |  | 交易金额（美元） |
| paris_currency | varchar(8) | N |  | 货币对 |
| trader_no | varchar(16) | Y |  | 交易员简称 |
| trader_dir | varchar(16) | Y |  | 交易目录 |
| counterparty_name | varchar(16) | Y |  | 交易对手方 |
| add_type | bpchar(1) | Y |  | 增加方式:见tp_public_dict的034 |
| op_type | bpchar(1) | N | √ | 操作方式:见tp_public_dict的091 |
| his_trade_date | varchar(8) | Y |  | 历史成交日期 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 247. dimple.tc_his_maintenance　(7 字段)
> 表含义：结算准备金最低余额历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| clear_account_no | varchar(14) | N | √ | 结算子帐号:$表示所有结算帐号 |
| account_type | varchar(4) | N | √ | 帐号类型:见tp_public_dict的038 |
| call_low_bal | numeric(18,2) | Y |  | 追保下限 |
| rule_low_bal | numeric(18,2) | Y |  | 强平下限 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 248. dimple.tc_his_offset_order_match　(20 字段)
> 表含义：平盘委托成交历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_time | varchar(12) | Y |  | 时间 |
| offset_type | varchar(2) | N |  | 平盘类型：见tp_public_dict的405 |
| paris_currency | varchar(8) | N |  | 货币对 |
| offset_mode | varchar(2) | N |  | 平盘模式：见tp_public_dict的034 |
| offset_strategy | varchar(2) | Y |  | 平盘策略: 见tp_public_dict的406，手工没有平盘策略，自动默认1-普通 |
| offset_channel | varchar(50) | Y |  | 平盘方: 标注外资行,可为空 |
| member_id | varchar(8) | Y |  | 平盘席位号:美元平盘不填 |
| client_id | varchar(16) | Y |  | 平盘客户号:美元平盘不填 |
| local_no | varchar(64) | N | √ | 本地报单号 |
| order_id | varchar(64) | Y |  | 订单号:接口返回，等同于外系统报单号 |
| global_seq_no | varchar(64) | Y |  | 全局流水号 |
| offset_flag | varchar(2) | N |  | 平盘方向: 见tp_public_dict的002 |
| offset_qty1 | numeric(24,8) | Y |  | 平盘重量(克)：美元平盘不填 |
| offset_qty2 | numeric(24,8) | Y |  | 平盘重量(盎司)：美元平盘不填 |
| price | numeric(24,8) | Y |  | 成交价格：即成交汇率 |
| offset_amt1 | numeric(24,8) | Y |  | 平盘金额(元)：贵金属平盘不填 |
| offset_amt2 | numeric(24,8) | Y |  | 平盘金额(美元) |
| trade_state | varchar(2) | Y |  | 交易状态：见tp_public_dict的407 |
| trader_no | varchar(16) | Y |  | 操作员 |

---

## 249. dimple.tc_his_other_fee　(9 字段)
> 表含义：其他费率历史表　|　估算行数：**186,708**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| fee_type | bpchar(1) | N | √ | 手续费类型:见tp_public_dict的092 |
| fee_kind | varchar(8) | N | √ | 费率类型:见tp_public_dict的354 |
| fee_rate | numeric(22,6) | N |  | 费率 |

---

## 250. dimple.tc_his_pingan_account　(24 字段)
> 表含义：平安历史账务文件表　|　估算行数：**4,559**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| seq_no | varchar(30) | Y |  | 流水号 |
| group_no | varchar(30) | Y |  | 组号 |
| trade_logno | varchar(30) | Y |  | 交易流水号 |
| currency | varchar(10) | Y |  | 币种 |
| direction | varchar(2) | Y |  | 借贷方向：D借，C贷 |
| org | varchar(20) | Y |  | 机构代码 |
| account | varchar(50) | Y |  | 账号 |
| subject | varchar(20) | Y |  | 科目 |
| amt | numeric(24,6) | Y |  | 发生额 |
| remark | varchar(255) | Y |  | 备注 |
| isrecal | varchar(2) | Y |  | 是否为日终估值账务：0否；1是 |
| accounting_no | varchar(9) | Y |  | ICS产生的传票号 |
| account_date | varchar(9) | Y |  | 会计日期 |
| trans_status | varchar(2) | Y |  | 发送状态：0未发送；1 成功；2失败 |
| trans_result | varchar(20) | Y |  | 发送返回代码 |
| trans_msg | varchar(100) | Y |  | 发送返回信息 |
| check_status | varchar(2) | Y |  | 对账状态：0未对账；1已对账 |
| check_result | varchar(20) | Y |  | 对账返回代码 |
| check_msg | varchar(100) | Y |  | 对账返回信息 |
| exg_seq_no | varchar(40) | Y |  | 结售汇流水号 |
| del_flag | varchar(3) | Y |  | 冲销标志：N普通 R冲销 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 251. dimple.tc_his_quote_alarm_note　(7 字段)
> 表含义：报价风控信息历史表　|　估算行数：**472,931**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 席位代码：根据业务规则，部分风控指标类型不填 |
| contract_id | varchar(20) | N |  | 合约 |
| risk_type | varchar(10) | N |  | 风控指标类型：见tp_public_dict的409 |
| seq_no | float8 | N | √ | 序列号 |
| risk_time | varchar(8) | Y |  | 预警时间 |
| risk_info | varchar(255) | Y |  | 预警信息 |

---

## 252. dimple.tc_his_quote_match　(13 字段)
> 表含义：报价交易成交历史表　|　估算行数：**7,806**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 成交日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| match_time | varchar(12) | Y |  | 成交时间 |
| match_no | varchar(20) | N | √ | 报价成交编号 |
| bs_flag | varchar(3) | N | √ | 买卖方向:见tp_public_dict的002 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| price | numeric(20,8) | Y |  | 价格：元/克 |
| qty | numeric(12,0) | Y |  | 数量：手 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | Y |  | 本地委托号 |

---

## 253. dimple.tc_his_risk_control　(6 字段)
> 表含义：风控预警历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| risk_date | varchar(8) | N | √ | 预警日期 |
| risk_time | varchar(8) | N | √ | 预警时间 |
| risk_type | varchar(3) | N | √ | 预警类型：见dict 317 |
| risk_value | numeric(24,6) | Y |  | 当前预警值 |
| risk_info | varchar(254) | Y |  | 预警信息 |
| if_alarm | varchar(3) | Y |  | 是否预警 |

---

## 254. dimple.tc_his_rule_alarm_note　(8 字段)
> 表含义：合规管理历史报警信息表　|　估算行数：**60,095**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| alarm_date | varchar(8) | N | √ | 报警日期 |
| seq_no | float8 | N | √ | 流水号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| alarm_type | bpchar(1) | N | √ | 报警类型:见tp_public_dict的232 |
| alarm_time | varchar(8) | N |  | 报警时间 |
| exch_code | varchar(30) | N |  | 交易所代码 |
| alarm_note | varchar(254) | Y |  | 报警信息 |

---

## 255. dimple.tc_his_rule_cancel　(8 字段)
> 表含义：撤单参数历史表　|　估算行数：**16,577**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| cancel_times | numeric(10,0) | Y |  | 撤单次数 |
| alarm_times | numeric(10,0) | Y |  | 预警阀值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作人员 |

---

## 256. dimple.tc_his_rule_large_cancel　(9 字段)
> 表含义：大额撤单参数历史表　|　估算行数：**10,897**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| variety_id | varchar(4) | N |  | 品种代码 |
| contract_id | varchar(20) | N |  | 合约代码 |
| cancel_times | numeric(10,0) | Y |  | 撤单次数 |
| alarm_times | numeric(10,0) | Y |  | 预警阀值 |
| alarm_qty_times | numeric(10,0) | Y |  | 撤单手数阀值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作人员 |

---

## 257. dimple.tc_his_rule_selfmatch　(7 字段)
> 表含义：自成交参数历史表　|　估算行数：**2,426**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| alarm_type | varchar(3) | N | √ | 预警类型:见Dict 319 |
| selfmatch_times | numeric(10,0) | Y |  | 自成交次数 |
| alarm_times | numeric(10,0) | Y |  | 预警阀值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作人员 |

---

## 258. dimple.tc_his_srcb_account　(13 字段)
> 表含义：上海农商行历史帐务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | numeric(10,0) | Y |  | 凭证组号 |
| id | varchar(3) | Y |  | 物理ID |
| trade_date | varchar(8) | Y |  | 交易日期 |
| member_id | varchar(8) | Y |  | 席位代码 |
| voucher_no | varchar(12) | Y |  | 凭证号 |
| account_sysno | varchar(30) | Y |  | 账号/科目系统编号 |
| buy_flag | varchar(4) | Y |  | 借贷标识：见tp_public_dict 276 |
| currency | varchar(3) | Y |  | 币种:默认CNY |
| amount | numeric(24,6) | Y |  | 金额 |
| remark | varchar(100) | Y |  | 摘要 |
| sub_type | varchar(3) | Y |  | 业务类型 |
| note | varchar(100) | Y |  | 备注 |
| status | varchar(3) | Y |  | 记账状态：见tp_public_dict 304 |

---

## 259. dimple.tc_his_task_check　(11 字段)
> 表含义：任务检查配置历史表　|　估算行数：**175**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| bank_no | varchar(4) | N | √ | 银行代码: 参考interface.tp_para表的ACCOUNT_CTL_TYPE参数值，写入对应代码，上海银行代码为7 |
| task_id | varchar(10) | N | √ | 任务代码 |
| task_desc | varchar(255) | Y |  | 任务说明 |
| checked_time | varchar(4) | N | √ | 检查时机：1-结算前检查；2-日终对账后检查；3-交易初始化前检查； |
| customized | varchar(4) | N |  | 是否定制化任务: 0-否；1-是 |
| forced | varchar(4) | N |  | 是否允许强制通过: 0-否；1-是 |
| date_exec | varchar(8) | N | √ | 执行日期 |
| time_exec | varchar(22) | Y |  | 执行时间 |
| finished | varchar(4) | N |  | 执行完成标志: 0-未执行；1-执行完成；2-执行失败；3-强制跳过 |
| times | numeric(10,0) | N |  | 执行次数 |
| exec_desc | varchar(255) | Y |  | 执行说明 |

---

## 260. dimple.tc_home_ilease_match　(58 字段)
> 表含义：境内租赁成交　|　估算行数：**74**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：B本方借出/C本方借入 见tp_public_dict的221 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate_han | numeric(12,8) | Y |  | 利率（经办） |
| delivery_rate_tot | numeric(12,8) | Y |  | 利率（总部） |
| interest_han | numeric(24,6) | Y |  | 利息（经办） |
| interest_tot | numeric(24,6) | Y |  | 利息（总部） |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest_total | numeric(24,8) | Y |  | 总利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| if_send_exch | varchar(3) | Y |  | 是否发送交易所：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构 |
| local_no | varchar(16) | Y |  | 本地申报单编号 |
| apply_sheet_no | varchar(20) | Y |  | 租借申报编号 |
| if_hedging | varchar(3) | Y |  | 是否套保：1是/0否 见tp_public_dict的027 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |
| agreement_sn_pre | varchar(30) | Y |  | 前接租借登记编号 |
| agreement_sn_next | varchar(30) | Y |  | 后接租借登记编号 |
| apply_date | varchar(8) | Y |  | 申报自然日期 |
| rsp_code | varchar(20) | Y |  | 响应代码 |
| rsp_msg | varchar(100) | Y |  | 响应消息 |
| contract_no | varchar(30) | Y |  | 租借合约编号 |
| lease_preapply_no | varchar(30) | Y |  | 租借预申报编号 |

---

## 261. dimple.tc_home_inq_durmanage_jour　(28 字段)
> 表含义：境内询价成交存续期管理表　|　估算行数：**9,158**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N | √ | 入表日期 |
| jour_id | float8 | N | √ | 流水表流水号 |
| apply_date | varchar(8) | N |  | 申请日期 |
| inquire_id | float8 | Y |  | 询价上下行流水号 |
| manage_type | varchar(2) | N |  | 存续期变动类型：见tp_public_dict的383 |
| member_id | varchar(8) | Y |  | 会员席位号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| seq_no | float8 | N |  | 询价成交表成交流水号 |
| fn_flag | varchar(3) | N |  | 远近端：见tp_public_dict的250 |
| match_no | varchar(20) | Y |  | 成交单号 |
| reference_price | numeric(20,8) | Y |  | 原参考价格 |
| ref_price_new | numeric(20,8) | Y |  | 新参考价格 |
| broker_no | varchar(10) | Y |  | 原本方经纪机构代码：近远端相同 |
| broker_no_new | varchar(10) | Y |  | 新本方经纪机构代码：近远端相同 |
| party_broker_no | varchar(10) | Y |  | 原对手方经纪机构代码：近远端相同 |
| party_broker_no_new | varchar(10) | Y |  | 新对手方经纪机构代码：近远端相同 |
| storage_no | varchar(4) | Y |  | 原指定仓库代码,白银合约时字段有值 |
| storage_no_new | varchar(4) | Y |  | 新指定仓库代码,白银合约时字段有值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(30) | Y |  | 录入人员 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| apply_operate | varchar(2) | Y |  | 申请操作：见tp_public_dict的394 |
| apply_status | varchar(3) | Y |  | 系统申请状态：见tp_public_dict的395 |
| party_apply_status | varchar(3) | Y |  | 本方申请状态：见tp_public_dict的396 |
| counterparty_apply_status | varchar(3) | Y |  | 对手方申请状态：见tp_public_dict的397 |

---

## 262. dimple.tc_home_inqmatch_durmanage　(26 字段)
> 表含义：境内询价成交存续期管理表　|　估算行数：**515**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| apply_date | varchar(8) | N | √ | 申请日期 |
| inquire_id | float8 | N | √ | 询价上下行流水号 |
| manage_type | varchar(2) | N |  | 存续期变动类型：见tp_public_dict的383 |
| member_id | varchar(8) | Y |  | 会员席位号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 询价成交表成交流水号 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| match_no | varchar(20) | Y |  | 成交单号 |
| reference_price | numeric(20,8) | Y |  | 原参考价格 |
| ref_price_new | numeric(20,8) | Y |  | 新参考价格 |
| broker_no | varchar(10) | Y |  | 原本方经纪机构代码：近远端相同 |
| broker_no_new | varchar(10) | Y |  | 新本方经纪机构代码：近远端相同 |
| party_broker_no | varchar(10) | Y |  | 原对手方经纪机构代码：近远端相同 |
| party_broker_no_new | varchar(10) | Y |  | 新对手方经纪机构代码：近远端相同 |
| storage_no | varchar(4) | Y |  | 原指定仓库代码,白银合约时字段有值 |
| storage_no_new | varchar(4) | Y |  | 新指定仓库代码,白银合约时字段有值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(30) | Y |  | 录入人员 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| apply_operate | varchar(2) | Y |  | 申请操作：见tp_public_dict的394 |
| apply_status | varchar(3) | Y |  | 系统申请状态：见tp_public_dict的395 |
| party_apply_status | varchar(3) | Y |  | 本方申请状态：见tp_public_dict的396 |
| counterparty_apply_status | varchar(3) | Y |  | 对手方申请状态：见tp_public_dict的396 |

---

## 263. dimple.tc_home_inquire_dir_jour　(53 字段)
> 表含义：境内交易类询价流水表　|　估算行数：**4,839**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水表流水号 |
| trader_no | varchar(40) | Y |  | 本方交易员号 |
| seat_no | varchar(20) | Y |  | 本方席位号 |
| client_id | varchar(16) | Y |  | 本方客户号 |
| member_id | varchar(8) | Y |  | 本方会员号 |
| party_seat_no | varchar(6) | Y |  | 对手方席位号 |
| party_trader_no | varchar(10) | Y |  | 对手方交易员号 |
| party_client_id | varchar(10) | Y |  | 对手方客户号 |
| party_client_abbr | varchar(20) | Y |  | 对手方客户中文简称 |
| party_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| order_no | varchar(20) | Y |  | 报单编号 |
| bs_flag | varchar(3) | Y |  | 买卖标志;见tp_public_dict002 |
| fn_flag | varchar(3) | N | √ | 近远端;见tp_public_dict250 |
| match_type | varchar(3) | Y |  | 询价交易类型;见tp_public_dict253 |
| directional_type | varchar(1) | Y |  | 定向询价/定向报价;见tp_public_dict446 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| qty | numeric(24,6) | Y |  | 数量 |
| weight | numeric(24,6) | Y |  | 重量 |
| spot_price | numeric(20,8) | Y |  | SPOT价格 |
| forward_price | numeric(20,8) | Y |  | 远期点价格 |
| period | varchar(10) | Y |  | 期限;见tp_public_dict344 |
| trade_time | varchar(22) | Y |  | 交易时间,发起方为接受时间，应答方为应答推送时间 |
| due_date | varchar(8) | Y |  | 到期日 |
| delivery_type | varchar(3) | Y |  | 结算方式;见tp_public_dict的051 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金;见tp_public_dict的027 |
| reference_type | varchar(3) | Y |  | 参考价类型;见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| other_ref_price | numeric(20,8) | Y |  | 其他参考价 |
| other_ref_price_info | varchar(50) | Y |  | 其他参考价格说明 |
| storage_no | varchar(4) | Y |  | 白银指定仓库 |
| orignal_order_no | varchar(20) | Y |  | 公开报价报单编号 |
| local_order_no_2 | varchar(20) | Y |  | 旧报单编号 |
| remark | varchar(254) | Y |  | 附加条款 |
| reply_valid_time | numeric(4,0) | Y |  | 应答有效时间 |
| role | varchar(4) | N | √ | 本方角色;见tp_public_dict的340 |
| input_date | varchar(8) | N | √ | 新增记录日期 |
| local_seq_no | numeric(10,0) | N | √ | 序号;多个对手方的序号 |
| cmd_no | float8 | Y |  | 上场序号 |
| op_status | varchar(3) | Y |  | 操作类型 |
| op_time | varchar(8) | Y |  | 操作时间 |
| inquire_id | float8 | Y |  | 询价上下行流水号 |
| inquire_status | varchar(3) | Y |  | 本地询价状态;见tp_public_dirc的447 |
| op_date | varchar(8) | Y |  | 操作日期 |
| bid_valid_time | numeric(4,0) | Y |  | 报价有效时间 |
| quote_time | varchar(22) | Y |  | 发起时间 |
| party_seat_name | varchar(100) | Y |  | 对手方席位名称 |
| party_member_id | varchar(8) | Y |  | 对手方会员代码 |
| purpose_code | varchar(5) | Y |  | 交易目的 |
| client_abbr | varchar(20) | Y |  | 本方客户中文简称 |
| client_eabbr | varchar(20) | Y |  | 本方客户英文简称 |
| reply_time | varchar(22) | Y |  | 应答时间 |
| match_no | varchar(20) | Y |  | 成交单号 |

---

## 264. dimple.tc_home_inquire_dir_unmatch　(49 字段)
> 表含义：境内交易类询价待成交表　|　估算行数：**3,770**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 待成交表流水号 |
| trader_no | varchar(40) | Y |  | 本方交易员号 |
| seat_no | varchar(20) | Y |  | 本方席位号 |
| client_id | varchar(16) | Y |  | 本方客户号 |
| member_id | varchar(8) | Y |  | 本方会员号 |
| party_seat_no | varchar(6) | Y |  | 对手方席位号 |
| party_trader_no | varchar(10) | Y |  | 对手方交易员号 |
| party_client_id | varchar(10) | Y |  | 对手方客户号 |
| party_client_abbr | varchar(20) | Y |  | 对手方客户中文简称 |
| party_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| order_no | varchar(20) | Y |  | 报单编号 |
| bs_flag | varchar(3) | Y |  | 买卖标志;见tp_public_dict002 |
| fn_flag | varchar(3) | N | √ | 近远端;见tp_public_dict250 |
| match_type | varchar(3) | Y |  | 询价交易类型;见tp_public_dict253 |
| directional_type | varchar(1) | Y |  | 定向询价/定向报价;见tp_public_dict446 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| qty | numeric(24,6) | Y |  | 数量 |
| weight | numeric(24,6) | Y |  | 重量 |
| spot_price | numeric(20,8) | Y |  | SPOT价格 |
| forward_price | numeric(20,8) | Y |  | 远期点价格 |
| period | varchar(10) | Y |  | 期限;见tp_public_dict344 |
| trade_time | varchar(22) | Y |  | 交易时间,发起方为接受时间，应答方为应答推送时间 |
| due_date | varchar(8) | Y |  | 到期日 |
| delivery_type | varchar(3) | Y |  | 结算方式;见tp_public_dict的051 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金;见tp_public_dict的027 |
| reference_type | varchar(3) | Y |  | 参考价类型;见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| other_ref_price | numeric(20,8) | Y |  | 其他参考价 |
| other_ref_price_info | varchar(50) | Y |  | 其他参考价格说明 |
| storage_no | varchar(4) | Y |  | 白银指定仓库 |
| orignal_order_no | varchar(20) | Y |  | 公开报价报单编号 |
| local_order_no_2 | varchar(20) | Y |  | 旧报单编号 |
| remark | varchar(254) | Y |  | 附加条款 |
| reply_valid_time | numeric(4,0) | Y |  | 应答有效时间 |
| role | varchar(4) | N | √ | 本方角色;见tp_public_dict的340 |
| input_date | varchar(8) | N | √ | 新增记录日期 |
| local_seq_no | numeric(10,0) | N | √ | 序号;多个对手方的序号 |
| cmd_no | float8 | Y |  | 上场序号 |
| inquire_status | varchar(3) | Y |  | 本地询价状态;见tp_public_dirc的447 |
| bid_valid_time | numeric(4,0) | Y |  | 报价有效时间 |
| quote_time | varchar(22) | Y |  | 发起时间 |
| party_seat_name | varchar(100) | Y |  | 对手方席位名称 |
| party_member_id | varchar(8) | Y |  | 对手方会员代码 |
| purpose_code | varchar(5) | Y |  | 交易目的 |
| client_abbr | varchar(20) | Y |  | 本方客户中文简称 |
| client_eabbr | varchar(20) | Y |  | 本方客户英文简称 |
| reply_time | varchar(22) | Y |  | 应答时间 |
| match_no | varchar(20) | Y |  | 成交单号 |

---

## 265. dimple.tc_home_inquire_match　(101 字段)
> 表含义：境内询价成交　|　估算行数：**6,646**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | Y |  | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| seq_no | float8 | N | √ | 成交流水号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| member_id | varchar(8) | Y |  | 会员席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| reference_type | varchar(3) | Y |  | 参考价类型：见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| reference_price | numeric(20,8) | Y |  | 参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| deal_type | varchar(3) | Y |  | 处理方式：见tp_public_dict的248 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| sys_inquire_status | varchar(3) | Y |  | 系统询价状态：见tp_public_dict的385 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| agreement_sn | varchar(30) | Y |  | 系统登记单编号/报价单编号 |
| inquire_type | varchar(3) | Y |  | 询价类型：见Dict的325 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码：见tp_public_dict的382 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码：见tp_public_dict的382 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| related_match_no | varchar(20) | Y |  | 相关成交单号:用来记录行权的期权成交单号，或为未来其他业务备用 |
| period | varchar(10) | Y |  | 期限：见tp_public_dict的344 |
| price_unit | varchar(4) | Y |  | 报价单位：见tp_public_dict的357 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| status | varchar(4) | Y |  | 成交单状态：见tp_public_dict的342 |
| clear_status | varchar(4) | Y |  | 清算信息：见tp_public_dict的355 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367；询价上下行版本后废弃 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| input_date | varchar(8) | N |  | 新增记录日期 |
| storage_no | varchar(4) | Y |  | 指定仓库代码,白银合约时字段有值 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构:交易对手方代码 |
| inquire_id | float8 | Y |  | 询价上下行流水号 |
| trade_volume | numeric(16,0) | Y |  | 交易手数 |
| refprice_info | varchar(75) | Y |  | 其他参考价格说明 |
| remark | varchar(500) | Y |  | 附加条款 |
| member_confirm | varchar(1) | Y |  | 会员确认结果：见tp_public_dict的378 |
| client_confirm | varchar(1) | Y |  | 客户确认状态：见tp_public_dict的379 |
| sge_confirm | varchar(1) | Y |  | 交易所确认结果：见tp_public_dict的380 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| if_send_exch | varchar(1) | Y |  | 是否发送交易所：见tp_public_dict的027 |
| party_member_id | varchar(8) | Y |  | 对手方席位号 |
| act_due_date | varchar(8) | Y |  | 实际到期日 |
| offline_date | varchar(8) | Y |  | GEMS3线下成交日期 |
| mmb_id | varchar(8) | Y |  | 本方会员号 |
| party_mmb_id | varchar(8) | Y |  | 对手方会员号 |
| client_broker | varchar(20) | Y |  | 本方经纪机构用户 |
| party_client_broker | varchar(20) | Y |  | 对手方经纪机构用户 |
| unit | numeric(12,6) | Y |  | 交易单位 |
| if_publicoffer_flag | varchar(1) | Y |  | 是否公开报价成交：见tp_public_dict的027 |
| regist_state | varchar(1) | Y |  | 确认状态：见tp_public_dict的386 |
| reply_valid_time | numeric(4,0) | Y |  | 确认时间有效期 |
| member_type | varchar(1) | Y |  | 本方会员类型：见tp_public_dict的387 |
| party_member_type | varchar(1) | Y |  | 对手方会员类型：见tp_public_dict的387 |
| exch_trader_no | varchar(15) | Y |  | 交易所本方交易员代码 |
| if_breach | varchar(1) | Y |  | 是否存续期违约：见tp_public_dict的027 |
| channel_type | varchar(1) | Y |  | 外汇交易中心询价渠道类型:见tp_public_dict的429 |
| isentermanually | varchar(1) | Y |  | 是否手工录入:见tp_public_dict的027 |
| confirm_date | varchar(8) | Y |  | 交易所确认日期 |
| confirm_time | varchar(8) | Y |  | 交易所确认时间 |
| directional_type | varchar(1) | Y |  | 定向交易类型:见tp_public_dict的446 |
| weight | numeric(24,6) | Y |  | 重量 |
| trade_time | varchar(8) | Y |  | 交易时间,发起方为接受时间，应答方为应答推送时间 |
| delivery_rate_han | varchar(10) | Y |  | 利率（代客） |
| delivery_rate_tot | varchar(10) | Y |  | 利率（总部） |
| reg_type | varchar(2) | Y |  | 登记提交方 464 |
| strategy_id | varchar(8) | Y |  | 策略编号 |
| eoa_approval_status | varchar(1) | Y |  | EOA审批状态: 见tp_public_dict的495 |
| trade_flag | numeric(1,0) | Y |  | 交易方向 |
| file_id | varchar(20) | Y |  | 试算强制通过文件编号 |

---

## 266. dimple.tc_home_inquire_match_confirm　(93 字段)
> 表含义：境内询价成交确认表　|　估算行数：**1,133**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | Y |  | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| seq_no | float8 | N | √ | 成交流水号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| member_id | varchar(8) | Y |  | 会员席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| reference_type | varchar(3) | Y |  | 参考价类型：见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| reference_price | numeric(20,8) | Y |  | 参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| deal_type | varchar(3) | Y |  | 处理方式：见tp_public_dict的248 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| sys_inquire_status | varchar(3) | Y |  | 系统询价确认状态：见tp_public_dict的388 |
| sys_inqconf_operate | varchar(3) | Y |  | 系统询价确认操作：见tp_public_dict的399 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| agreement_sn | varchar(30) | Y |  | 系统登记单编号/报价单编号 |
| inquire_type | varchar(3) | Y |  | 询价类型：见Dict的325 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码：见tp_public_dict的382 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码：见tp_public_dict的382 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| related_match_no | varchar(20) | Y |  | 相关成交单号:用来记录行权的期权成交单号，或为未来其他业务备用 |
| period | varchar(10) | Y |  | 期限：见tp_public_dict的344 |
| price_unit | varchar(4) | Y |  | 报价单位：见tp_public_dict的357 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| status | varchar(4) | Y |  | 成交单状态：见tp_public_dict的342 |
| clear_status | varchar(4) | Y |  | 清算信息：见tp_public_dict的355 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367；询价上下行版本后废弃 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| input_date | varchar(8) | N |  | 新增记录日期 |
| storage_no | varchar(4) | Y |  | 指定仓库代码,白银合约时字段有值 |
| trade_volume | numeric(16,0) | Y |  | 交易手数 |
| refprice_info | varchar(75) | Y |  | 其他参考价格说明 |
| remark | varchar(500) | Y |  | 附加条款 |
| member_confirm | varchar(1) | Y |  | 会员确认结果：见tp_public_dict的378 |
| client_confirm | varchar(1) | Y |  | 客户确认状态：见tp_public_dict的379 |
| sge_confirm | varchar(1) | Y |  | 交易所确认结果：见tp_public_dict的380 |
| regist_state | varchar(1) | Y |  | 确认状态：见tp_public_dict的386 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| party_member_id | varchar(40) | Y |  | 对手方席位号 |
| act_due_date | varchar(8) | Y |  | 实际到期日 |
| offline_date | varchar(8) | Y |  | GEMS3线下成交日期 |
| mmb_id | varchar(8) | Y |  | 本方会员号 |
| party_mmb_id | varchar(8) | Y |  | 对手方会员号 |
| client_broker | varchar(20) | Y |  | 本方经纪机构用户 |
| party_client_broker | varchar(20) | Y |  | 对手方经纪机构用户 |
| unit | numeric(12,6) | Y |  | 交易单位 |
| if_publicoffer_flag | varchar(1) | Y |  | 是否公开报价成交：见tp_public_dict的027 |
| reply_valid_time | numeric(4,0) | Y |  | 确认时间有效期 |
| member_type | varchar(1) | Y |  | 本方会员类型：见tp_public_dict的387 |
| party_member_type | varchar(1) | Y |  | 对手方会员类型：见tp_public_dict的387 |
| exch_trader_no | varchar(15) | Y |  | 交易所本方交易员代码 |
| channel_type | varchar(1) | Y |  | 外汇交易中心询价渠道类型:见tp_public_dict的429 |
| isentermanually | varchar(1) | Y |  | 是否手工录入:见tp_public_dict的027 |
| errorfields | varchar(250) | Y |  | 下行错误字段 |
| iserrormsgtype | varchar(1) | Y |  | 是否下行错误MsgType |
| delivery_rate_han | varchar(10) | Y |  | 利率代客 |
| delivery_rate_tot | varchar(10) | Y |  | 利率总分 |
| reg_type | varchar(2) | Y |  | 登记提交方 464 |
| strategy_id | varchar(8) | Y |  |  |
| is_sys_confirmed | numeric(1,0) | N |  | 系统内确认 |
| file_id | varchar(20) | Y |  | 试算强制通过文件编号 |

---

## 267. dimple.tc_home_inquire_match_jour　(94 字段)
> 表含义：境内询价成交　|　估算行数：**23,620**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | Y |  | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| seq_no | float8 | N | √ | 成交流水号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| reference_type | varchar(3) | Y |  | 参考价类型：见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| reference_price | numeric(20,8) | Y |  | 参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| deal_type | varchar(3) | Y |  | 处理方式：见tp_public_dict的248 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| sys_inquire_status | varchar(3) | Y |  | 系统询价状态：见tp_public_dict的385 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| agreement_sn | varchar(30) | Y |  | 系统登记单编号/报价单编号 |
| inquire_type | varchar(3) | Y |  | 询价类型：见Dict的325 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码：见tp_public_dict的382 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码：见tp_public_dict的382 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| related_match_no | varchar(20) | Y |  | 相关成交单号:用来记录行权的期权成交单号，或为未来其他业务备用 |
| period | varchar(10) | Y |  | 期限：见tp_public_dict的344 |
| price_unit | varchar(4) | Y |  | 报价单位：见tp_public_dict的357 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| status | varchar(4) | Y |  | 成交单状态：见tp_public_dict的342 |
| clear_status | varchar(4) | Y |  | 清算信息：见tp_public_dict的355 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367；询价上下行版本后废弃 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| input_date | varchar(8) | Y |  | 新增记录日期 |
| storage_no | varchar(4) | Y |  | 指定仓库代码,白银合约时字段有值 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构:交易对手方代码 |
| inquire_seq_no | float8 | Y |  | 原记录成交流水号 |
| cmd_no | float8 | Y |  | 上场序号 |
| cmd_status | varchar(1) | Y |  | 上场流水状态:见tp_public_dict的209 |
| inquire_id | float8 | Y |  | 询价上下行流水号 |
| trade_volume | numeric(16,0) | Y |  | 交易手数 |
| refprice_info | varchar(75) | Y |  | 其他参考价格说明 |
| remark | varchar(500) | Y |  | 附加条款 |
| member_confirm | varchar(1) | Y |  | 会员确认结果：见tp_public_dict的378 |
| client_confirm | varchar(1) | Y |  | 客户确认状态：见tp_public_dict的379 |
| sge_confirm | varchar(1) | Y |  | 交易所确认结果：见tp_public_dict的380 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| if_send_exch | varchar(1) | Y |  | 是否发送交易所：见tp_public_dict的027 |
| party_member_id | varchar(8) | Y |  | 对手方席位号 |
| act_due_date | varchar(8) | Y |  | 实际到期日 |
| offline_date | varchar(8) | Y |  | GEMS3线下成交日期 |
| mmb_id | varchar(8) | Y |  | 本方会员号 |
| party_mmb_id | varchar(8) | Y |  | 对手方会员号 |
| client_broker | varchar(20) | Y |  | 本方经纪机构用户 |
| party_client_broker | varchar(20) | Y |  | 对手方经纪机构用户 |
| unit | numeric(12,6) | Y |  | 交易单位 |
| if_publicoffer_flag | varchar(1) | Y |  | 是否公开报价成交：见tp_public_dict的027 |
| regist_state | varchar(1) | Y |  | 确认状态：见tp_public_dict的386 |
| reply_valid_time | numeric(4,0) | Y |  | 确认时间有效期 |
| member_type | varchar(1) | Y |  | 本方会员类型：见tp_public_dict的387 |
| party_member_type | varchar(1) | Y |  | 对手方会员类型：见tp_public_dict的387 |
| exch_trader_no | varchar(15) | Y |  | 交易所本方交易员代码 |
| if_breach | varchar(1) | Y |  | 是否存续期违约：见tp_public_dict的027 |
| channel_type | varchar(1) | Y |  | 外汇交易中心询价渠道类型:见tp_public_dict的429 |
| strategy_id | varchar(8) | Y |  | 策略编号 |
| weight | numeric(24,6) | Y |  | 重量 |
| trade_flag | numeric(1,0) | Y |  | 交易方向 |

---

## 268. dimple.tc_home_lease_detail　(5 字段)
> 表含义：境内租赁物明细表　|　估算行数：**609**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 租赁记录系统流水号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| variety_id | varchar(3) | N | √ | 交易品种 |
| storage_no | varchar(4) | N | √ | 仓库代码 |
| qty | numeric(16,6) | Y |  | 租借重量 |

---

## 269. dimple.tc_home_lease_match　(61 字段)
> 表含义：境内租赁成交　|　估算行数：**81**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| branches | varchar(15) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：B本方借出/C本方借入 见tp_public_dict的221 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate_han | numeric(12,8) | Y |  | 利率（经办） |
| delivery_rate_tot | numeric(12,8) | Y |  | 利率（总部） |
| interest_han | numeric(24,6) | Y |  | 利息（经办） |
| interest_tot | numeric(24,6) | Y |  | 利息（总部） |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest_total | numeric(24,8) | Y |  | 总利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| if_send_exch | varchar(3) | Y |  | 是否发送交易所：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构 |
| local_no | varchar(16) | Y |  | 本地申报单编号 |
| apply_sheet_no | varchar(20) | Y |  | 租借申报编号 |
| if_hedging | varchar(3) | Y |  | 是否套保：1是/0否 见tp_public_dict的027 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |
| agreement_sn_pre | varchar(30) | Y |  | 前接租借登记编号 |
| agreement_sn_next | varchar(30) | Y |  | 后接租借登记编号 |
| apply_date | varchar(8) | Y |  | 申报自然日期 |
| rsp_code | varchar(20) | Y |  | 响应代码 |
| rsp_msg | varchar(150) | Y |  | 响应消息 |
| contract_no | varchar(30) | Y |  | 租借合约编号 |
| lease_preapply_no | varchar(30) | Y |  | 租借预申报编号 |
| strategy_no | varchar(4) | Y |  | 投资策略 |
| eoa_status | varchar(2) | Y |  | EOA审批状态：见tp_public_dict的493 |
| file_id | varchar(30) | Y |  | 试算通过文件编号 |

---

## 270. dimple.tc_home_lease_match_jour　(58 字段)
> 表含义：境内租赁成交　|　估算行数：**1,904**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| branches | varchar(15) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：B本方借出/C本方借入 见tp_public_dict的221 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate_han | numeric(12,8) | Y |  | 利率（经办） |
| delivery_rate_tot | numeric(12,8) | Y |  | 利率（总部） |
| interest_han | numeric(24,6) | Y |  | 利息（经办） |
| interest_tot | numeric(24,6) | Y |  | 利息（总部） |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest_total | numeric(24,6) | Y |  | 总利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| if_send_exch | varchar(3) | Y |  | 是否发送交易所：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构 |
| local_no | varchar(16) | Y |  | 本地申报单编号 |
| if_hedging | varchar(3) | Y |  | 是否套保：1是/0否 见tp_public_dict的027 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |
| agreement_sn_pre | varchar(30) | Y |  | 前接租借登记编号 |
| agreement_sn_next | varchar(30) | Y |  | 后接租借登记编号 |
| apply_sheet_no | varchar(20) | Y |  | 租借申报编号 |
| apply_date | varchar(8) | Y |  | 申报自然日期 |
| rsp_code | varchar(20) | Y |  | 响应代码 |
| rsp_msg | varchar(150) | Y |  | 响应消息 |
| contract_no | varchar(30) | Y |  | 租借合约编号 |
| lease_preapply_no | varchar(30) | Y |  | 租借预申报编号 |
| strategy_no | varchar(4) | Y |  | 投资策略 |

---

## 271. dimple.tc_home_lend_match　(92 字段)
> 表含义：境内拆借成交　|　估算行数：**1,359**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| delivery_rate_tot | varchar(8) | Y |  | 利率（总部） |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算利息 |
| source_id | varchar(3) | Y |  | 来源:1会服,2拆借平台 |
| sheet_no | varchar(20) | Y |  | 主系统黄金过户单编号 |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(30) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(10) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| qty | numeric(10,0) | Y |  | 数量：手 |
| interest_base_unit | varchar(4) | Y |  | 计息基准价单位：元/克、元/千克 |
| period | varchar(10) | Y |  | 期限 |
| lend_status | varchar(4) | Y |  | 借金状态：见tp_public_dict的345 |
| ret_type | varchar(4) | Y |  | 还金类型：见tp_public_dict的346 |
| ret_status | varchar(4) | Y |  | 还金状态：见tp_public_dict的347 |
| pay_status | varchar(4) | Y |  | 付息状态：见tp_public_dict的348 |
| ret_deli_variety_id | varchar(15) | Y |  | 还金交割品种 |
| agreement_sn_pre | varchar(30) | Y |  | 前接成交单编号 |
| agreement_sn_next | varchar(30) | Y |  | 后续成交单编号 |
| status | varchar(4) | Y |  | 状态：见tp_public_dict的342 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| input_date | varchar(8) | N |  | 新增记录日期 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构:交易对手方代码 |
| isimported | varchar(3) | Y |  | 是否导入 |
| party_member_id | varchar(6) | Y |  | 对手方席位代码 |
| storage_no | varchar(4) | Y |  | 借金仓库 |
| storage_no_re | varchar(4) | Y |  | 还金仓库 |
| actual_due_date | varchar(8) | Y |  | 实际到期日 |
| actual_pay_date | varchar(8) | Y |  | 实际付息日 |
| public_flag | varchar(3) | Y |  | 是否公开报价成交 |
| inst_unit | numeric(12,6) | Y |  | 交易单位数量 |
| broker_user_no | varchar(20) | Y |  | 本方经济机构用户 |
| party_broker_user_no | varchar(20) | Y |  | 对手方经济机构用户 |
| fail_info | varchar(20) | Y |  | 过户失败原因 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| offline_match_date | varchar(8) | Y |  | 线下成交日期 |
| order_no | varchar(20) | Y |  | 报单编号 |
| contract_id | varchar(30) | Y |  | 合约 |
| note | varchar(200) | Y |  | 附加条款 |
| lend_mode | varchar(15) | Y |  | 拆借模式 |
| remark | varchar(256) | Y |  | 备注 |
| mort_check_status | varchar(20) | Y |  | 质押复核状态 |
| if_exception | varchar(3) | Y |  | 是否到期异常：1是/0否 见tp_public_dict的027 |
| reg_summit | varchar(3) | Y |  | 登记提交方,见TP_PUBLIC_DICT的464 |

---

## 272. dimple.tc_home_lend_match_bak　(93 字段)
> 表含义：境内拆借成交　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| agreement_sn | varchar(30) | Y |  | 拆借成交单号 |
| member_id | varchar(8) | N |  | 本方席位号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 计息基准价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_status | varchar(3) | Y |  | 系统拆借状态:见tp_public_dict的415 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| coefficient | numeric(5,4) | Y |  | 系数 |
| purpose_code | varchar(5) | Y |  | 交易目的/投组编号 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算利息 |
| source_id | varchar(3) | Y |  | 来源:见tp_public_dict的417 |
| sheet_no | varchar(20) | Y |  | 主系统黄金过户单编号 |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(30) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(10) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| qty | numeric(10,0) | Y |  | 数量：手 |
| interest_base_unit | varchar(4) | Y |  | 计息基准价单位：元/克、元/千克 |
| period | varchar(10) | Y |  | 期限 |
| lend_status | varchar(4) | Y |  | 借金状态：见tp_public_dict的345 |
| ret_type | varchar(4) | Y |  | 还金类型：见tp_public_dict的346 |
| ret_status | varchar(4) | Y |  | 还金状态：见tp_public_dict的347 |
| pay_status | varchar(4) | Y |  | 付息状态：见tp_public_dict的348 |
| ret_deli_variety_id | varchar(15) | Y |  | 还金交割品种 |
| agreement_sn_pre | varchar(30) | Y |  | 前接成交单编号 |
| agreement_sn_next | varchar(30) | Y |  | 后续成交单编号 |
| status | varchar(4) | Y |  | 状态：见tp_public_dict的342 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| input_date | varchar(8) | N |  | 新增记录日期 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构:交易对手方代码 |
| if_publicoffer_flag | varchar(1) | Y |  | 是否公开报价:见tp_public_dict的027 |
| if_send_exch | varchar(1) | Y |  | 是否发送交易所:见tp_public_dict的027 |
| party_member_id | varchar(8) | Y |  | 对手方席位号 |
| contract_id | varchar(20) | Y |  | 拆借合约 |
| buyer_role | varchar(6) | Y |  | 拆入方角色:见tp_public_dict的340,拆借默认为空 |
| warehouseid | varchar(4) | Y |  | 借金仓库 |
| remark | varchar(254) | Y |  | 附加条款 |
| act_due_date | varchar(8) | Y |  | 实际到期日 |
| offline_date | varchar(8) | Y |  | 线下成交日期 |
| regtime | varchar(8) | Y |  | 登记时间 |
| orderno | varchar(16) | Y |  | 报单编号 |
| commit_party | varchar(16) | Y |  | 登记提交方:见tp_public_dict的418 |
| member_confirm | varchar(1) | Y |  | 会员确认状态：见tp_public_dict的378 |
| client_confirm | varchar(1) | Y |  | 客户确认状态：见tp_public_dict的379 |
| sge_confirm | varchar(1) | Y |  | 交易所确认状态：见tp_public_dict的380 |
| mmb_id | varchar(8) | Y |  | 本方会员号 |
| party_mmb_id | varchar(8) | Y |  | 对手方会员号 |
| regdate | varchar(8) | Y |  | 登记日期 |
| regist_state | varchar(1) | Y |  | 确认状态：见tp_public_dict的386 |
| inquire_type | varchar(3) | Y |  | 询价交易类型：见tp_public_dict的376 |
| reply_valid_time | numeric(4,0) | Y |  | 确认时间有效期 |
| opwarehouseid | varchar(4) | Y |  | 还金仓库 |
| if_hedging | varchar(3) | Y |  | 是否套保：1是/0否 见tp_public_dict的027 |

---

## 273. dimple.tc_home_lend_match_jour　(72 字段)
> 表含义：境内拆借成交流水　|　估算行数：**11,131**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统流水号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| interest_period | varchar(3) | Y |  | 付息周期：见tp_public_dict的287 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| coefficient | numeric(5,4) | Y |  | 系数? |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算利息 |
| source_id | varchar(3) | Y |  | 来源 |
| sheet_no | varchar(20) | Y |  | 主系统黄金过户单编号 |
| is_finish | varchar(3) | Y |  | 是否已了结 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| bill_no_pre | varchar(30) | Y |  | 前接编号 |
| bill_no_next | varchar(30) | Y |  | 后接编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(30) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(10) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| qty | numeric(10,0) | Y |  | 数量：手 |
| interest_base_unit | varchar(4) | Y |  | 计息基准价单位：元/克、元/千克 |
| period | varchar(10) | Y |  | 期限 |
| lend_status | varchar(4) | Y |  | 借金状态：见tp_public_dict的345 |
| ret_type | varchar(4) | Y |  | 还金类型：见tp_public_dict的346 |
| ret_status | varchar(4) | Y |  | 还金状态：见tp_public_dict的347 |
| pay_status | varchar(4) | Y |  | 付息状态：见tp_public_dict的348 |
| ret_deli_variety_id | varchar(15) | Y |  | 还金交割品种 |
| agreement_sn_pre | varchar(30) | Y |  | 前接成交单编号 |
| agreement_sn_next | varchar(30) | Y |  | 后续成交单编号 |
| status | varchar(4) | Y |  | 状态：见tp_public_dict的342 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| input_date | varchar(8) | Y |  | 新增记录日期 |
| if_tpgagency | varchar(3) | Y |  | 是否占用第三方担保机构：1是/0否 见tp_public_dict的027 |
| tpgagency | varchar(10) | Y |  | 第三方担保机构:交易对手方代码 |
| isimported | varchar(3) | Y |  | 是否导入 |
| delivery_rate_tot | numeric(12,8) | Y |  | 利率（总部） |

---

## 274. dimple.tc_home_lend_unmatch　(62 字段)
> 表含义：境内询价拆借待成交表　|　估算行数：**1,055**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 待成交表流水号 |
| role_type | varchar(3) | N | √ | 本方角色，见tp_public_dict的340 |
| trader_no | varchar(40) | Y |  | 本方交易员号 |
| seat_no | varchar(20) | Y |  | 本方席位号 |
| client_id | varchar(15) | Y |  | 本方客户号 |
| member_id | varchar(10) | Y |  | 本方会员号 |
| party_seat_no | varchar(6) | Y |  | 对手方席位号 |
| party_trader_no | varchar(10) | Y |  | 对手方交易员号 |
| party_client_id | varchar(15) | Y |  | 对手方客户号 |
| party_client_abbr | varchar(20) | Y |  | 对手方客户简称 |
| party_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| party_member_id | varchar(8) | Y |  | 对手方会员号 |
| local_seq_no | float8 | N | √ | 序号 |
| order_no | varchar(20) | Y |  | 报单编号 |
| lend_type | varchar(3) | Y |  | 借金类型，见tp_public_dict的463 |
| lend_flag | varchar(3) | Y |  | 拆借方向，见tp_public_dict的221 |
| trade_init_mode | varchar(3) | Y |  | 报价类型，见tp_public_dict的446 |
| match_type | varchar(3) | Y |  | 询价交易类型，见tp_public_dict的253 |
| contract_id | varchar(32) | Y |  | 询价合约代码 |
| qty | float8 | Y |  | 数量 |
| clear_price | numeric(20,8) | Y |  | 计息基准价 |
| interest_base | varchar(3) | Y |  | 计息基准 |
| period | varchar(10) | Y |  | 期限 |
| quote_time | varchar(21) | Y |  | 报价时间 |
| due_date | varchar(8) | Y |  | 到期日 |
| pay_date | varchar(8) | Y |  | 付息日 |
| agreement_sn_pre | varchar(20) | Y |  | 前接成交单编号 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| storage_no | varchar(4) | Y |  | 借金仓库 |
| note | varchar(200) | Y |  | 信用型询价附加条款 |
| original_order_no | varchar(20) | Y |  | 公开报价报单编号 |
| bid_valid_time | float8 | Y |  | 报价有效时间 |
| input_date | varchar(8) | N | √ | 交易日期 |
| status | varchar(3) | Y |  | 状态，登记类型见tp_public_dict的385，交易类型见tp_public_dict的447 |
| reply_valid_time | float8 | Y |  | 应答有效时间 |
| reply_time | varchar(21) | Y |  | 应答时间 |
| purpose_code | varchar(5) | Y |  | 交易目的 |
| match_no | varchar(20) | Y |  | 成交单号 |
| interest | numeric(24,6) | Y |  | 利息 |
| offline_date | varchar(8) | Y |  |  |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| broker_no | varchar(30) | Y |  | 本方经济机构代码 |
| party_broker_no | varchar(30) | Y |  | 对手方经济机构代码 |
| party_role_type | varchar(3) | Y |  | 对手方角色 |
| if_publicoffer_flag | varchar(3) | Y |  | 是否公开报价成交 |
| fail_reason | varchar(20) | Y |  | 登记失败原因 |
| client_confirm | varchar(3) | Y |  | 客户确认状态，见tp_public_dict的379 |
| member_confirm | varchar(3) | Y |  | 会员确认状态，见tp_public_dict的378 |
| sge_confirm | varchar(3) | Y |  | 交易所确认状态，见tp_public_dict的380 |
| regist_state | varchar(3) | Y |  | 登记状态，见tp_public_dict的386 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| reg_date | varchar(8) | Y |  | 起息日 |
| storage_no_re | varchar(4) | Y |  | 还金仓库 |
| variety_id | varchar(4) | Y |  | 还金交割品种代码 |
| regist_date | varchar(8) | Y |  | 登记日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| regist_time | varchar(8) | Y |  | 登记时间 |
| trade_time | varchar(22) | Y |  | 交易时间 |
| trade_reg | varchar(3) | N | √ | 交易/登记：见tp_public_dict的341 |
| reg_summit | varchar(3) | Y |  | 登记提交方,见TP_PUBLIC_DICT的464 |

---

## 275. dimple.tc_home_lend_unmatch_jour　(35 字段)
> 表含义：境内询价拆借待成交表　|　估算行数：**585**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 待成交表流水号 |
| role_type | varchar(3) | N | √ | 本方角色，见tp_public_dict的340 |
| trader_no | varchar(40) | Y |  | 本方交易员号 |
| seat_no | varchar(20) | Y |  | 本方席位号 |
| client_id | varchar(15) | Y |  | 本方客户号 |
| member_id | varchar(10) | Y |  | 本方会员号 |
| party_seat_no | varchar(6) | Y |  | 对手方席位号 |
| party_trader_no | varchar(10) | Y |  | 对手方交易员号 |
| party_client_id | varchar(15) | Y |  | 对手方客户号 |
| party_client_abbr | varchar(20) | Y |  | 对手方客户简称 |
| party_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| party_member_id | varchar(8) | Y |  | 对手方会员号 |
| local_seq_no | float8 | N | √ | 序号 |
| order_no | varchar(20) | Y |  | 报单编号 |
| lend_type | varchar(3) | Y |  | 借金类型，见tp_public_dict的463 |
| lend_flag | varchar(3) | Y |  | 拆借方向，见tp_public_dict的221 |
| trade_init_mode | varchar(3) | Y |  | 报价类型，见tp_public_dict的446 |
| match_type | varchar(3) | Y |  | 询价交易类型，见tp_public_dict的376 |
| contract_id | varchar(32) | Y |  | 询价合约代码 |
| qty | float8 | Y |  | 数量 |
| clear_price | numeric(20,8) | Y |  | 计息基准价 |
| interest_base | varchar(3) | Y |  | 计息基准 |
| period | varchar(10) | Y |  | 期限 |
| quote_time | varchar(21) | Y |  | 报价时间 |
| due_date | varchar(8) | Y |  | 到期日 |
| pay_date | varchar(8) | Y |  | 付息日 |
| agreement_sn_pre | varchar(20) | Y |  | 前接成交单编号 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| storage_no | varchar(4) | Y |  | 借金仓库 |
| note | varchar(200) | Y |  | 信用型询价附加条款 |
| original_order_no | varchar(20) | Y |  | 公开报价报单编号 |
| bid_valid_time | float8 | Y |  | 报价有效时间 |
| input_date | varchar(8) | N | √ | 交易日期 |
| status | varchar(3) | Y |  | 状态 |

---

## 276. dimple.tc_home_lenmatch_durmanage　(21 字段)
> 表含义：境内拆借成交存续期管理表　|　估算行数：**38**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| apply_date | varchar(8) | N | √ | 申请日期 |
| lend_id | float8 | N | √ | 流水号 |
| manage_type | varchar(2) | N |  | 存续期变动类型：见tp_public_dict的383 |
| member_id | varchar(8) | Y |  | 会员席位号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| agreement_sn | varchar(30) | N | √ | 拆借成交单号 |
| variety_id | varchar(3) | Y |  | 原还金品种代码 |
| variety_id_new | varchar(3) | Y |  | 新还金品种代码 |
| storage_no | varchar(4) | Y |  | 原还金仓库编号 |
| storage_no_new | varchar(4) | Y |  | 新还金仓库编号 |
| ret_type | varchar(4) | Y |  | 还金类型：见tp_public_dict的346 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(30) | Y |  | 录入人员 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| apply_operate | varchar(2) | Y |  | 申请操作：见tp_public_dict的394 |
| apply_status | varchar(2) | Y |  | 系统申请状态：见tp_public_dict的395 |
| party_apply_status | varchar(3) | Y |  | 本方申请状态：见tp_public_dict的396 |
| counterparty_apply_status | varchar(3) | Y |  | 对手方申请状态：见tp_public_dict的396 |

---

## 277. dimple.tc_home_opt_dir_unmatch　(110 字段)
> 表含义：境内期权定向询价待确认表　|　估算行数：**755**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| role | varchar(1) | N |  | 本方角色：340 |
| trader_id | varchar(40) | Y |  | 发起方交易员代码 |
| seat_id | varchar(6) | Y |  | 发起方交易席位代码 |
| client_id | varchar(10) | Y |  | 发起方客户代码 |
| member_id | varchar(6) | Y |  | 发起方会员代码 |
| client_abbr | varchar(20) | Y |  | 发起方客户简称 |
| client_eabbr | varchar(20) | Y |  | 发起方客户英文简称 |
| trader_id_1 | varchar(40) | Y |  | 应答方交易员代码1 |
| seat_id_1 | varchar(6) | Y |  | 应答方交易席位代码1 |
| client_id_1 | varchar(10) | Y |  | 应答方客户代码1 |
| member_id_1 | varchar(6) | Y |  | 应答方会员代码1 |
| client_abbr_1 | varchar(20) | Y |  | 应答方客户简称1 |
| client_eabbr_1 | varchar(20) | Y |  | 应答方客户英文简称1 |
| local_seqno_1 | varchar(1) | Y |  | 序号1 |
| trade_volume_1 | float8 | Y |  | 数量1 |
| weight_1 | numeric(18,6) | Y |  | 重量1 |
| option_money_1 | numeric(24,8) | Y |  | 权利金1 |
| reply_time_1 | varchar(21) | Y |  | 应答方报价时间1 |
| reply_valid_time_1 | varchar(4) | Y |  | 应答方报价有效时间1 |
| reply_state_1 | varchar(1) | Y |  | 询价状态1：见tp_public_dict的447 |
| match_date_1 | varchar(21) | Y |  | 成交时间1 |
| match_no_1 | varchar(24) | Y |  | 成交单号1 |
| trader_id_2 | varchar(40) | Y |  | 应答方交易员代码2 |
| seat_id_2 | varchar(6) | Y |  | 应答方交易席位代码2 |
| client_id_2 | varchar(10) | Y |  | 应答方客户代码2 |
| member_id_2 | varchar(6) | Y |  | 应答方会员代码2 |
| client_abbr_2 | varchar(20) | Y |  | 应答方客户简称2 |
| client_eabbr_2 | varchar(20) | Y |  | 应答方客户英文简称2 |
| local_seqno_2 | varchar(1) | Y |  | 序号2 |
| trade_volume_2 | float8 | Y |  | 数量2 |
| weight_2 | numeric(18,6) | Y |  | 重量2 |
| option_money_2 | numeric(24,8) | Y |  | 权利金2 |
| reply_time_2 | varchar(21) | Y |  | 应答方报价时间2 |
| reply_valid_time_2 | varchar(4) | Y |  | 应答方报价有效时间2 |
| reply_state_2 | varchar(1) | Y |  | 询价状态2：见tp_public_dict的447 |
| match_date_2 | varchar(21) | Y |  | 成交时间2 |
| match_no_2 | varchar(24) | Y |  | 成交单号2 |
| trader_id_3 | varchar(40) | Y |  | 应答方交易员代码3 |
| seat_id_3 | varchar(6) | Y |  | 应答方交易席位代码3 |
| client_id_3 | varchar(10) | Y |  | 应答方客户代码3 |
| member_id_3 | varchar(6) | Y |  | 应答方会员代码3 |
| client_abbr_3 | varchar(20) | Y |  | 应答方客户简称3 |
| client_eabbr_3 | varchar(20) | Y |  | 应答方客户英文简称3 |
| local_seqno_3 | varchar(1) | Y |  | 序号3 |
| trade_volume_3 | float8 | Y |  | 数量3 |
| weight_3 | numeric(18,6) | Y |  | 重量3 |
| option_money_3 | numeric(24,8) | Y |  | 权利金3 |
| reply_time_3 | varchar(21) | Y |  | 应答方报价时间3 |
| reply_valid_time_3 | varchar(4) | Y |  | 应答方报价有效时间3 |
| reply_state_3 | varchar(1) | Y |  | 询价状态3：见tp_public_dict的447 |
| match_date_3 | varchar(21) | Y |  | 成交时间3 |
| match_no_3 | varchar(24) | Y |  | 成交单号3 |
| trader_id_4 | varchar(40) | Y |  | 应答方交易员代码4 |
| seat_id_4 | varchar(6) | Y |  | 应答方交易席位代码4 |
| client_id_4 | varchar(10) | Y |  | 应答方客户代码4 |
| member_id_4 | varchar(6) | Y |  | 应答方会员代码4 |
| client_abbr_4 | varchar(20) | Y |  | 应答方客户简称4 |
| client_eabbr_4 | varchar(20) | Y |  | 应答方客户英文简称4 |
| local_seqno_4 | varchar(1) | Y |  | 序号4 |
| trade_volume_4 | float8 | Y |  | 数量4 |
| weight_4 | numeric(18,6) | Y |  | 重量4 |
| option_money_4 | numeric(24,8) | Y |  | 权利金4 |
| reply_time_4 | varchar(21) | Y |  | 应答方报价时间4 |
| reply_valid_time_4 | varchar(4) | Y |  | 应答方报价有效时间4 |
| reply_state_4 | varchar(1) | Y |  | 询价状态4：见tp_public_dict的447 |
| match_date_4 | varchar(21) | Y |  | 成交时间4 |
| match_no_4 | varchar(24) | Y |  | 成交单号4 |
| trader_id_5 | varchar(40) | Y |  | 应答方交易员代码5 |
| seat_id_5 | varchar(6) | Y |  | 应答方交易席位代码5 |
| client_id_5 | varchar(10) | Y |  | 应答方客户代码5 |
| member_id_5 | varchar(6) | Y |  | 应答方会员代码5 |
| client_abbr_5 | varchar(20) | Y |  | 应答方客户简称5 |
| client_eabbr_5 | varchar(20) | Y |  | 应答方客户英文简称5 |
| local_seqno_5 | varchar(1) | Y |  | 序号5 |
| trade_volume_5 | float8 | Y |  | 数量5 |
| weight_5 | numeric(18,6) | Y |  | 重量5 |
| option_money_5 | numeric(24,8) | Y |  | 权利金5 |
| reply_time_5 | varchar(21) | Y |  | 应答方报价时间5 |
| reply_valid_time_5 | varchar(4) | Y |  | 应答方报价有效时间5 |
| reply_state_5 | varchar(1) | Y |  | 询价状态5：见tp_public_dict的447 |
| match_date_5 | varchar(21) | Y |  | 成交时间5 |
| match_no_5 | varchar(24) | Y |  | 成交单号5 |
| order_no | varchar(24) | Y |  | 报单编号 |
| bs_flag | varchar(3) | Y |  | 交易方向 |
| trade_init_mode | varchar(1) | Y |  | 报价类型 |
| otc_trade_type | varchar(2) | Y |  | 交易类型 |
| option_type | varchar(1) | Y |  | 期权类型 328 |
| inst_id | varchar(8) | Y |  | 询价合约代码 |
| exe_type | varchar(1) | Y |  | 行权方式 |
| trade_volume | float8 | Y |  | 数量 |
| weight | numeric(18,6) | Y |  | 重量 |
| option_money | numeric(24,8) | Y |  | 权利金 |
| price | numeric(24,8) | Y |  | 行权价 |
| period | varchar(10) | Y |  | 期限 |
| settle_accounts_date | varchar(8) | Y |  | 结算日 |
| exe_date | varchar(8) | Y |  | 行权日 |
| settle_accouts_type | varchar(1) | Y |  | 结算方式 |
| ref_price_type | varchar(1) | Y |  | 现金结算期权参考价格类型 |
| ref_price_updown | numeric(12,6) | Y |  | 参考价格调整项 |
| warehouse_id | varchar(4) | Y |  | 指定仓库 |
| orignal_order_no | varchar(16) | Y |  | 公开报价报单编号 |
| otc_remark | varchar(256) | Y |  | 信用型询价附加条款 |
| trade_purpose | varchar(3) | Y |  | 交易目的 |
| quote_time | varchar(21) | Y |  | 发起方报价时间 |
| quote_valid_time | varchar(4) | Y |  | 发起方报价有效时间 |
| quote_state | varchar(1) | Y |  | 报单状态：见tp_public_dict的448 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 本地流水号 |
| local_order_no | varchar(24) | Y |  | 本地报单号 |
| exec_deadline | varchar(8) | Y |  | 行权截止时间 |

---

## 278. dimple.tc_home_option_match　(86 字段)
> 表含义：期权境内询价成交　|　估算行数：**354**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(24) | Y |  | 成交单编号 |
| unmatch_no | varchar(24) | Y |  | 待确认成交单编号 |
| order_no | varchar(24) | Y |  | 报单编号 |
| apply_date | varchar(8) | Y |  | 自然日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| otc_reg_confirm_time | varchar(21) | Y |  | 登记时间 |
| public_offer_flag | varchar(1) | Y |  | 是否公开报价成交 |
| offline_match_date | varchar(8) | Y |  | 线下成交日期 |
| member_id | varchar(6) | Y |  | 本方会员号 |
| seat_id | varchar(6) | Y |  | 本方席位号 |
| trader_id | varchar(40) | Y |  | 本方交易员代码 |
| client_id | varchar(12) | Y |  | 本方客户号 |
| client_abbr | varchar(20) | Y |  | 本方客户简称 |
| client_eabbr | varchar(20) | Y |  | 本方客户英文简称 |
| broker_id | varchar(10) | Y |  | 本方经纪机构代码 |
| otc_broker_user_id | varchar(20) | Y |  | 本方经纪机构用户 |
| source | varchar(1) | Y |  | 本方渠道代码 |
| role | varchar(6) | Y |  | 本方席位角色 |
| partner_member_id | varchar(6) | Y |  | 对手方会员号 |
| partner_seat_id | varchar(6) | Y |  | 对手方席位号 |
| partner_trader_id | varchar(40) | Y |  | 对手方交易员代码 |
| partner_client_id | varchar(12) | Y |  | 对手方客户号 |
| partner_client_abbr | varchar(30) | Y |  | 对手方客户简称 |
| partner_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| partner_broker_id | varchar(10) | Y |  | 对手方经纪机构代码 |
| partner_otc_broker_user_id | varchar(20) | Y |  | 对手方经纪机构用户 |
| partner_source | varchar(1) | Y |  | 对手方渠道代码 |
| partner_role | varchar(6) | Y |  | 对手方席位角色 |
| inst_id | varchar(8) | Y |  | 合约代码 |
| trade_or_registe | varchar(1) | Y |  | 交易/登记:见tp_public_dict的341 |
| exe_type | varchar(1) | Y |  | 行权方式:见tp_public_dict的324 |
| option_type | varchar(1) | Y |  | 期权类型:见tp_public_dict的328 |
| inst_unit | numeric(12,6) | Y |  | 交易单位数量 |
| trade_volume | float8 | Y |  | 数量 |
| otc_std_weight | numeric(18,6) | Y |  | 发生标准重量 |
| period | varchar(10) | Y |  | 期限 |
| price_unit | varchar(1) | Y |  | 权利金和行权价报价单位 |
| price | numeric(24,8) | Y |  | 行权价 |
| exe_date | varchar(8) | Y |  | 行权日 |
| otc_exercise_time | varchar(8) | Y |  | 行权截止时间 |
| actual_exercise_date | varchar(8) | Y |  | 实际行权日 |
| contract_period | varchar(2) | Y |  | 实物交割标的合约期限 |
| settle_accounts_date | varchar(8) | Y |  | 结算日 |
| actual_interest_date | varchar(8) | Y |  | 实际结算日 |
| option_money | numeric(24,8) | Y |  | 权利金 |
| option_payment_state | varchar(1) | Y |  | 权利金支付状态：见tp_public_dict的472 |
| option_payment_clear_info | varchar(2) | Y |  | 权利金清算信息 |
| option_paydate | varchar(8) | Y |  | 权利金支付日 |
| actual_option_paydate | varchar(8) | Y |  | 实际权利金支付日 |
| clos_amount | numeric(12,6) | Y |  | 平仓权利金 |
| clos_payment_state | varchar(1) | Y |  | 平仓权利金支付状态 |
| clos_payment_clear_info | varchar(2) | Y |  | 平仓权利金清算信息 |
| clos_paydate | varchar(8) | Y |  | 平仓权利金支付日 |
| actual_clos_paydate | varchar(8) | Y |  | 实际平仓权利金支付日 |
| exercise_regno | varchar(20) | Y |  | 行权交易成交单号 |
| settle_accounts_type | varchar(1) | Y |  | 结算方式 |
| ref_price_type | varchar(1) | Y |  | 现金结算期权参考价格类型 |
| ref_price_updown | numeric(12,6) | Y |  | 现金结算期权参考价格调整项 |
| warehouse_id | varchar(4) | Y |  | 指定仓库 |
| otc_remark | varchar(256) | Y |  | 信用型询价附加条款 |
| option_exercise_status | varchar(1) | Y |  | 行权状态：见tp_public_dict的350 |
| feeing_state | varchar(1) | Y |  | 收费状态 343 |
| account_date | varchar(8) | Y |  | 收费日期 |
| closfeeing_state | varchar(1) | Y |  | 平仓收费状态 |
| closfeeing_date | varchar(8) | Y |  | 平仓收费日期 |
| trader_no | varchar(10) | Y |  | 发起方交易员 |
| institution_id | varchar(10) | Y |  | 发起方交易席位 |
| trade_purpose | varchar(3) | Y |  | 交易目的 |
| trade_type | varchar(3) | Y |  | 交易类型 |
| bs_flag | varchar(3) | N |  | 发起方交易方向：见tp_public_dict的002 |
| weight | numeric(18,6) | Y |  | 重量 |
| seq_no | float8 | N | √ | 本地流水号 |
| member_confirm_state | varchar(1) | Y |  | 会员确认结果：见tp_public_dict的378 |
| client_confirm_state | varchar(1) | Y |  | 客户确认状态：见tp_public_dict的379 |
| sge_confirm_state | varchar(1) | Y |  | 交易所确认结果：见tp_public_dict的380 |
| registe_state | varchar(1) | Y |  | 登记状态：见tp_public_dict的385 |
| status | varchar(4) | Y |  | 成交单状态：见tp_public_dict的342 |
| remark | varchar(256) | Y |  | 备注 |
| operator | varchar(40) | Y |  | 操作人员 |
| operate_time | varchar(20) | Y |  | 操作时间 |
| operate_date | varchar(8) | Y |  | 操作日期 |
| confirm_valid_time | varchar(8) | Y |  | 确认时间有效期 |
| notional_principal | numeric(24,6) | Y |  | 名义本金 |
| reg_summit | varchar(1) | N | √ | 登记提交方：见tp_public_dict的464 |
| trade_init_mode | varchar(1) | Y |  |  |

---

## 279. dimple.tc_home_option_unmatch　(60 字段)
> 表含义：境内期权询价成交待确认表　|　估算行数：**351**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| unmatch_no | varchar(24) | Y |  | 待确认成交单号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| institution_id | varchar(10) | Y |  | 登记提交机构 |
| apply_date | varchar(8) | Y |  | 登记日期 |
| otc_reg_confirm_time | varchar(21) | Y |  | 登记时间 |
| offline_match_date | varchar(18) | Y |  | 线下成交日期 |
| match_no | varchar(24) | Y |  | 成交单号 |
| inst_id | varchar(8) | Y |  | 询价合约代码 |
| order_no | varchar(24) | Y |  | 报单编号 |
| source | varchar(1) | Y |  | 本方渠道代码 |
| member_id | varchar(6) | Y |  | 本方会员代码 |
| seat_id | varchar(6) | Y |  | 本方交易席位代码 |
| client_id | varchar(10) | Y |  | 本方客户代码 |
| client_abbr | varchar(20) | Y |  | 本方客户简称 |
| client_eabbr | varchar(20) | Y |  | 本方客户英文简称 |
| broker_id | varchar(10) | Y |  | 本方经济机构代码 |
| trader_id | varchar(40) | Y |  | 本方交易员代码 |
| role | varchar(6) | Y |  | 本方席位角色 |
| partner_source | varchar(1) | Y |  | 对手方渠道代码 |
| partner_member_id | varchar(6) | Y |  | 对手方会员代码 |
| partner_seat_id | varchar(6) | Y |  | 对手方交易席位代码 |
| partner_client_id | varchar(10) | Y |  | 对手方客户代码 |
| partner_client_abbr | varchar(30) | Y |  | 对手方客户简称 |
| partner_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| partner_broker_id | varchar(10) | Y |  | 对手方经济机构代码 |
| partner_trader_id | varchar(40) | Y |  | 对手方交易员代码 |
| partner_role | varchar(6) | Y |  | 对手方席位角色 |
| public_offer_flag | varchar(1) | Y |  | 是否公开报价成交 |
| trade_or_registe | varchar(1) | Y |  | 交易/登记 |
| member_confirm_state | varchar(1) | Y |  | 会员确认状态，见tp_public_dict的378 |
| client_confirm_state | varchar(1) | Y |  | 客户确认状态，见tp_public_dict的379 |
| sge_confirm_state | varchar(1) | Y |  | 交易所确认状态，见tp_public_dict的380 |
| registe_state | varchar(1) | Y |  | 登记状态，见tp_public_dict的385 |
| transfer_fail_info | varchar(20) | Y |  | 登记失败原因 |
| otc_trade_type | varchar(2) | Y |  | 询价交易类型 |
| exe_type | varchar(1) | Y |  | 行权方式 |
| option_type | varchar(1) | Y |  | 期权类型 328 |
| trade_volume | float8 | Y |  | 数量 |
| otc_trade_weight | numeric(18,6) | Y |  | 重量 |
| price | numeric(24,8) | Y |  | 行权价 |
| exe_date | varchar(8) | Y |  | 行权日 |
| otc_exercise_time | varchar(8) | Y |  | 行权截止时间 |
| settle_accounts_date | varchar(8) | Y |  | 结算日 |
| option_money | numeric(24,8) | Y |  | 权利金 |
| option_paydate | varchar(8) | Y |  | 权利金支付日 |
| settle_accounts_type | varchar(1) | Y |  | 结算方式 |
| ref_price_type | varchar(1) | Y |  | 现金结算期权参考价格类型 |
| warehouse_id | varchar(4) | Y |  | 指定仓库 |
| otc_remark | varchar(256) | Y |  | 信用型询价附加条款 |
| ref_price_updown | numeric(12,6) | Y |  | 参考价格调整项 |
| notional_principal | numeric(24,6) | Y |  | 名义本金 |
| period | varchar(10) | Y |  | 期限 |
| trader_no | varchar(40) | Y |  | 发起方交易员 |
| trade_purpose | varchar(3) | Y |  | 交易目的 |
| seq_no | float8 | N | √ | 本地流水号 |
| bs_flag | varchar(3) | Y |  | 发起方交易方向 |
| confirm_valid_time | varchar(8) | Y |  | 确认时间有效期 |
| registe_time | varchar(20) | Y |  | 登记时间 |
| reg_summit | varchar(1) | Y |  | 登记提交方：见tp_public_dict的464 |

---

## 280. dimple.tc_hz_account　(23 字段)
> 表含义：杭州银行账务管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| batch_no | varchar(40) | N | √ | 批次号 |
| seq_no | varchar(40) | N | √ | 记账流水号 |
| business_type | varchar(40) | Y |  | 业务类型 |
| sub_type | varchar(40) | Y |  | 子类型 |
| buy_flag | varchar(40) | N | √ | 借贷收付:见tp_public_dict的276,301 |
| subject | varchar(40) | Y |  | 科目 |
| name | varchar(40) | Y |  | 名称 |
| account | varchar(20) | Y |  | 账号 |
| account_name | varchar(40) | Y |  | 账户名称 |
| branches | varchar(10) | Y |  | 网点号 |
| currency | varchar(40) | Y |  | 币种 |
| amt | numeric(38,8) | Y |  | 发生额 |
| remark | varchar(100) | Y |  | 摘要 |
| send_status | varchar(10) | Y |  | 发送状态 |
| status | varchar(10) | Y |  | 处理状态:见tp_public_dict的311 |
| fail_reason | varchar(40) | Y |  | 失败原因 |
| main_no | varchar(40) | Y |  | 主机流水号 |
| main_date | varchar(8) | Y |  | 核心日期 |
| create_time | varchar(8) | Y |  | 生成时间 |
| sysno | varchar(40) | Y |  | 系统编号 |
| uuid | varchar(40) | Y |  | 唯一识别码 |
| del_flag | varchar(3) | Y |  | 是否冲销标志 |

---

## 281. dimple.tc_hz_account_bond　(11 字段)
> 表含义：杭州银行-账务国债买卖表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(18,2) | Y |  | 成交量 |
| turnover | numeric(18,2) | Y |  | 成交额 |
| nominal_amt | numeric(18,2) | Y |  | 券面金额 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3 交割 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |

---

## 282. dimple.tc_hz_account_future　(10 字段)
> 表含义：杭州银行-账务贵金属期货业务　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |

---

## 283. dimple.tc_hz_remain_cost_check　(7 字段)
> 表含义：杭州银行-账户余额核对表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| subject | varchar(20) | Y |  | 对账项目 |
| account | varchar(50) | Y |  | 内部账号 |
| remain_cost | numeric(18,2) | Y |  | 主机账户余额 |
| sys_cost | numeric(18,2) | Y |  | 预期余额 |
| result | varchar(20) | Y |  | 对账结果 |

---

## 284. dimple.tc_hz_risk_recalc_future　(9 字段)
> 表含义：杭州日终重估业务-国债　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 285. dimple.tc_hz_subject　(8 字段)
> 表含义：杭州银行账务科目表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sys_no | varchar(40) | N | √ | 系统编号 |
| subject_id | varchar(20) | Y |  | 科目代号 |
| subject_name | varchar(50) | Y |  | 科目名称 |
| account | varchar(50) | Y |  | 内部资金账户 |
| account_name | varchar(50) | Y |  | 账户名称 |
| org | varchar(20) | Y |  | 网点号 |
| remarks | varchar(255) | Y |  | 备注 |
| exch_code | varchar(2) | Y |  | 交易所代码 |

---

## 286. dimple.tc_import_files_config　(3 字段)
> 表含义：导入文件方式配置　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 席位号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| link_type | varchar(2) | N | √ | 连接方式:见tp_public_dict的352;1-直连;2-间连CTP;上期所、中金所使用，金交所默认1-直连 |

---

## 287. dimple.tc_import_files_list　(7 字段)
> 表含义：导入文件清单列表　|　估算行数：**86**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| link_type | varchar(2) | N | √ | 连接方式:见tp_public_dict的352;1-直连;2-间连CTP;上期所、中金所使用，金交所默认1-直连 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| file_no | float8 | N | √ | 文件编号 |
| file_name | varchar(60) | N |  | 文件名 |
| file_remark | varchar(200) | N |  | 文件名备注 |
| if_sge_main | varchar(2) | Y |  | 是否金交所主板清算文件:见tp_public_dict的027 |
| if_sge_intl | varchar(2) | Y |  | 是否金交所国际版清算文件:见tp_public_dict的027 |

---

## 288. dimple.tc_import_files_list_ex　(7 字段)
> 表含义：导入(外部)文件清单列表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| bank_abb | varchar(20) | N | √ | 银行简称(见TP_PARA) |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(20) | N |  | 会员号 |
| file_no | varchar(20) | N | √ | 文件编号 |
| file_funno | varchar(20) | Y |  | 调用文件功能号 |
| file_name | varchar(60) | Y |  | 文件名 |
| file_remark | varchar(200) | Y |  | 文件名备注 |

---

## 289. dimple.tc_import_files_status　(10 字段)
> 表含义：导入文件清单状态表　|　估算行数：**423,446**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 席位号 |
| file_no | float8 | N | √ | 文件编号 |
| file_name | varchar(60) | N |  | 文件名 |
| file_remark | varchar(200) | N |  | 文件名备注 |
| download_status | varchar(4) | N |  | 下载状态：见tp_public_dict的335 |
| import_status | varchar(4) | N |  | 导入状态：见tp_public_dict的335 |
| reason | varchar(200) | Y |  | 失败原因 |
| records | numeric(5,0) | Y |  | 数据条数 |

---

## 290. dimple.tc_import_files_status_ex　(12 字段)
> 表含义：导入(外部)文件清单状态表　|　估算行数：**68**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| bank_abb | varchar(20) | N | √ | 银行简称(见TP_PARA) |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| file_no | varchar(20) | N | √ | 文件编号 |
| file_funno | varchar(20) | Y |  | 调用文件功能号 |
| file_name | varchar(60) | N |  | 文件名 |
| file_remark | varchar(200) | N |  | 文件名备注 |
| download_status | varchar(4) | N |  | 下载状态：见tp_public_dict的335 |
| import_status | varchar(4) | N |  | 导入状态：见tp_public_dict的335 |
| reason | varchar(256) | Y |  | 失败原因 |
| records | numeric(5,0) | Y |  | 数据条数 |

---

## 291. dimple.tc_inq_opt_match_manage_jour　(9 字段)
> 表含义：询价期权等级分配表　|　估算行数：**795**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| manage_date | varchar(8) | N | √ | 分配日期 |
| input_date | varchar(8) | N | √ | 导入日期 |
| inq_match_no | varchar(20) | N | √ | 询价系统成交编号 |
| match_no | varchar(20) | Y |  | 主系统成交编号 |
| bs_flag | varchar(3) | N | √ | 本方交易方向 |
| trader_no | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 292. dimple.tc_inquire_exchange　(5 字段)
> 表含义：询价市场状态信息　|　估算行数：**504**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| inquire_status | varchar(1) | Y |  | 询价市场状态:见tp_public_dict的384 |
| exch_status | varchar(1) | Y |  | 交易所状态:见tp_public_dict的398 |
| last_trade_date | varchar(8) | Y |  | 上一交易日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| next_trade_date | varchar(8) | Y |  | 下一交易日期 |

---

## 293. dimple.tc_inquire_fee　(14 字段)
> 表含义：询价手续费率表　|　估算行数：**10,800**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约 |
| source_id | varchar(3) | N | √ | 来源：见tp_public_dict的249 |
| match_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的253 |
| period_abbr | varchar(20) | N | √ | 期限名称 |
| period_name | varchar(50) | Y |  | 期限全称 |
| period_low | numeric(10,0) | N |  | 期限下限 |
| period_up | numeric(10,0) | N |  | 期限上限 |
| delivery_type | varchar(3) | N | √ | 交割方式：见tp_public_dict的051 |
| buy_rate | numeric(22,6) | N |  | 买手续费率 |
| sell_rate | numeric(22,6) | N |  | 卖手续费率 |
| fee_type | varchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| if_exch_clearfund | varchar(4) | N | √ | 是否交易所清算资金：见tp_public_dict的027 |
| remark | varchar(150) | Y |  | 备注 |

---

## 294. dimple.tc_inquire_fee_list　(5 字段)
> 表含义：询价手续费率零级表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| period_abbr | varchar(20) | N | √ | 期限名称 |
| period_name | varchar(50) | Y |  | 期限全称 |
| period_low | numeric(10,0) | N |  | 期限下限 |
| period_up | numeric(10,0) | N |  | 期限上限 |
| remark | varchar(150) | Y |  | 备注 |

---

## 295. dimple.tc_inquire_gate_status　(7 字段)
> 表含义：询价报盘状态表　|　估算行数：**914**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 席位号 |
| access_id | varchar(30) | N | √ | 接入单元 |
| trader_no | varchar(30) | N | √ | 交易员号 |
| status | varchar(2) | Y |  | 状态:见tp_public_dict的120 |
| tick | varchar(20) | Y |  | 心跳时钟 |
| localsvrno | varchar(10) | Y |  | 服务号 |

---

## 296. dimple.tc_inquire_match_detail　(13 字段)
> 表含义：询价成交表　|　估算行数：**5,328**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N | √ | 导入日期 |
| trade_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(30) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| bs_flag | varchar(3) | N | √ | 买卖方向 |
| price | numeric(24,6) | Y |  | 成交价格 |
| qty | numeric(20,3) | Y |  | 成交数量 |
| match_type | varchar(3) | Y |  | 类型：1普通 |
| delivery_type | varchar(3) | Y |  | 交割方式;见public_dict的051 |
| calc_price_type | varchar(3) | Y |  | 参考价格类型：1开盘价;2收盘价;3结算价;4基准价(上午);5基准价(下午);6固定值;7基准价夜市;9其他价格 |
| calc_price_date | varchar(8) | Y |  | 参考价格日期 |
| calc_price | numeric(24,6) | Y |  | 参考价格 |

---

## 297. dimple.tc_inquire_period_date　(4 字段)
> 表含义：询价交易日与期限对应表　|　估算行数：**24,545**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_type | varchar(3) | N | √ | 询价交易类型：见tp_public_dict的376 |
| period | varchar(10) | N | √ | 期限：见tp_public_dict的344 |
| due_date | varchar(8) | Y |  | 期限对应日期 |

---

## 298. dimple.tc_inquire_swift　(51 字段)
> 表含义：境外询价成交swift报文　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| fn_flag | varchar(3) | N | √ | 近远端标志 |
| match_no | varchar(20) | N |  | 成交单号 |
| seq_no | float8 | N |  | 流水号 |
| bs_flag | varchar(3) | N |  | 买卖方向 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| check_status | varchar(3) | N |  | 复核状态见tp_public_dict的282 |
| check_oper | varchar(40) | N |  | 操作员 |
| send_status | varchar(3) | N |  | 发送状态见tp_public_dict的294 |
| send_msg | varchar(255) | Y |  | 发送失败原因 |
| tag_15a | varchar(1) | Y |  | 空域 |
| tag_20 | varchar(16) | Y |  | 交易流水号 |
| tag_21 | varchar(16) | Y |  | 默认值与交易流水号一样 |
| tag_22a | varchar(9) | Y |  | 通用参考信息a |
| tag_22b | varchar(21) | Y |  | 通用参考信息b |
| tag_94a | varchar(4) | Y |  | 经营范围 |
| tag_82a | varchar(220) | Y |  | A/B/D+内容本行SWIFT号 |
| tag_87a | varchar(220) | Y |  | 交易对手SWIFT号 |
| tag_83a | varchar(220) | Y |  | 客户信息 |
| tag_30 | varchar(6) | Y |  | 合约日期 |
| tag_26c | varchar(43) | Y |  | 商品识别信息 |
| tag_26h | varchar(16) | Y |  | 交易对手信息 |
| tag_33g | varchar(33) | Y |  | 成交单价 |
| tag_71c | varchar(220) | Y |  | 调整详情 |
| tag_77h | varchar(21) | Y |  | 协议版本 |
| tag_77d | varchar(220) | Y |  | 条款和条件 |
| tag_14c | varchar(4) | Y |  | 年的定义 |
| tag_72 | varchar(220) | Y |  | 发送方、接收方附加信息 |
| tag_15b_b | varchar(1) | Y |  | swift报文B区域标志域 |
| tag_32f_b | varchar(20) | Y |  | 买数量 |
| tag_86a_b | varchar(220) | Y |  | 本行黄金中转行BIC码和账号 |
| tag_87a_b | varchar(220) | Y |  | 本行黄金代理行账号和BIC码 |
| tag_34p_b | varchar(25) | Y |  | 成交额 |
| tag_53a_b | varchar(220) | Y |  | 本行美金代理行账号和BIC码 |
| tag_56a_b | varchar(220) | Y |  | 交易对手方的美金中转行BIC和账号 |
| tag_57a_b | varchar(220) | Y |  | 交易对手行的美金代理行BIC码和账号 |
| tag_15b_c | varchar(1) | Y |  | swift报文C区域标志域 |
| tag_32f_c | varchar(20) | Y |  | 卖数量 |
| tag_86a_c | varchar(220) | Y |  | 本行黄金中转行BIC码和账号 |
| tag_87a_c | varchar(220) | Y |  | 本行黄金代理行账号和BIC码 |
| tag_34r_c | varchar(25) | Y |  | 报酬 |
| tag_56a_c | varchar(220) | Y |  | 本行美金中转行账号和BIC码 |
| tag_57a_c | varchar(220) | Y |  | 本行美金代理行账号和BIC码 |
| operator | varchar(40) | Y |  | 操作员 |
| op_date | varchar(8) | N | √ | 新增日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_type | varchar(3) | Y |  | 操作类型 |
| sender | varchar(11) | Y |  | 发送方swift号 |
| receiver | varchar(11) | Y |  | 接收方swift号 |
| jour_no | float8 | N | √ | 系统流水号 |
| mod_date | varchar(8) | Y |  | 操作日期 |

---

## 299. dimple.tc_interest　(9 字段)
> 表含义：日利息计提表　|　估算行数：**862**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 系统流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| delay_no | varchar(30) | Y |  | 展期编号 |
| trade_type | varchar(3) | Y |  | 交易类型:见tp_public_dict的298 |
| trade_date | varchar(8) | Y |  | 交易日 |
| interest | numeric(24,6) | Y |  | 利息 |
| lend_flag | varchar(3) | Y |  | 拆借方向:见tp_public_dict的221 拆入和拆出 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 300. dimple.tc_invest_plan_detail　(40 字段)
> 表含义：投资计划明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| invest_plan_id | varchar(20) | N | √ | 投资计划编号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| trade_purpose | varchar(10) | N |  | 交易目的代码 |
| contract_id1 | varchar(20) | N |  | 合约代码1 |
| contract_id2 | varchar(20) | N |  | 合约代码2, 0表示无合约 |
| trade_direction | varchar(3) | N |  | 交易方向 dict-484 |
| low_limit | numeric(24,8) | Y |  | 最低价格 最低价差 |
| high_limit | numeric(24,8) | Y |  | 最高价格 最高价差 |
| invest_amount | numeric(30,8) | N |  | 投资额度（元） |
| check_status | varchar(3) | N |  | 审核状态 dict-480 |
| term | varchar(10) | Y |  | 期限 |
| upload_approval_file_id | varchar(20) | Y |  | 上传审批单文件id |
| upload_invest_file_id | varchar(20) | Y |  | 上传投资计划导入文件id |
| upload_invest_risk_file_id | varchar(20) | Y |  | 上传投资计划风控文件id |
| risk_invest_ratio | numeric(10,4) | Y |  | 风控指标-投资比例(%) |
| risk_major_invest_ratio | numeric(10,4) | Y |  | 风控指标-大类资产投资比例(%) |
| risk_compre_solvency_ratio | numeric(10,4) | Y |  | 风控指标-综合偿付能力充足率(%) |
| risk_core_solvency_ratio | numeric(10,4) | Y |  | 风控指标-核心偿付能力充足率(%) |
| input_user | varchar(50) | Y |  | 录入人员 |
| input_date | varchar(8) | Y |  | 录入日期 |
| input_time | varchar(8) | Y |  | 录入时间 |
| check_user | varchar(50) | Y |  | 审批人员 |
| check_date | varchar(8) | Y |  | 审批日期 |
| check_time | varchar(8) | Y |  | 审批时间 |
| risk_invest_ratio_show | varchar(10) | Y |  |  |
| risk_major_invest_ratio_show | varchar(10) | Y |  |  |
| risk_compre_solvency_ratio_show | varchar(10) | Y |  |  |
| risk_core_solvency_ratio_show | varchar(10) | Y |  |  |
| risk_spot_amount | numeric(30,8) | Y |  | 当前黄金现货合约总规模（元） |
| risk_trade_party_lease_stop | numeric(30,8) | Y |  | 单一交易对手方租借禁止线额度（元） |
| risk_swap_far_net_ratio | numeric(10,4) | Y |  | 掉期远端空头净敞口占黄金现货比例(%) |
| risk_swap_near_duration_ratio | numeric(10,4) | Y |  | 掉期近端存续规模占总资产比例(%) |
| risk_swap_far_duration_ratio | numeric(10,4) | Y |  | 掉期远端存续规模占总资产比例(%) |
| risk_spot_amount_show | varchar(10) | Y |  |  |
| risk_trade_party_lease_stop_show | varchar(10) | Y |  |  |
| risk_swap_far_net_ratio_show | varchar(10) | Y |  |  |
| risk_swap_near_duration_ratio_show | varchar(10) | Y |  |  |
| risk_swap_far_duration_ratio_show | varchar(10) | Y |  |  |
| risk_cal_amount | numeric(30,8) | Y |  | 风控计算额度 |

---

## 301. dimple.tc_invest_plan_risk_param　(15 字段)
> 表含义：公司级风控参数设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| param_id | varchar(20) | N | √ | 风控参数设置id uuid |
| use_year | numeric(4,0) | N |  | 使用年份 |
| use_month | numeric(2,0) | N |  | 使用月份 |
| param_type | varchar(2) | N |  | 参数名称 dict-483 |
| param_value | numeric(28,8) | N |  | 参数值（元） |
| op_user | varchar(50) | Y |  | 操作人员 |
| op_date | varchar(8) | N |  | 操作日期 |
| op_time | varchar(8) | N |  | 操作时间 |
| create_user | varchar(50) | Y |  | 创建人员 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_user | varchar(50) | Y |  | 更新人员 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |
| remark | varchar(1000) | Y |  | 备注 |

---

## 302. dimple.tc_invest_plan_risk_threshold　(8 字段)
> 表含义：公司级风控阈值设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| indicator_type | varchar(3) | N | √ | 风控指标类型 dict-482 |
| indicator_value | numeric(5,0) | N |  | 禁止线(%) |
| op_user | varchar(50) | Y |  | 操作人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| remark | varchar(1000) | Y |  | 备注 |
| alarm_line_1 | numeric(5,0) | N |  | 预警线1(%) |
| alarm_line_2 | numeric(5,0) | N |  | 预警线2(%) |

---

## 303. dimple.tc_invest_plan_risk_total　(32 字段)
> 表含义：投资计划风控审核合计数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| invest_amount | numeric(30,8) | N |  | 投资额度（元） |
| upload_approval_file_id | varchar(20) | Y |  | 上传审批单文件id |
| upload_invest_file_id | varchar(20) | Y |  | 上传投资计划导入文件id |
| upload_invest_risk_file_id | varchar(20) | N | √ | 上传投资计划风控文件id |
| risk_invest_ratio | numeric(10,4) | Y |  | 风控指标-投资比例(%) |
| risk_major_invest_ratio | numeric(10,4) | Y |  | 风控指标-大类资产投资比例(%) |
| risk_compre_solvency_ratio | numeric(10,4) | Y |  | 风控指标-综合偿付能力充足率(%) |
| risk_core_solvency_ratio | numeric(10,4) | Y |  | 风控指标-核心偿付能力充足率(%) |
| check_status | varchar(3) | N |  | 风控审核状态 |
| risk_invest_ratio_show | varchar(10) | Y |  |  |
| risk_major_invest_ratio_show | varchar(10) | Y |  |  |
| risk_compre_solvency_ratio_show | varchar(10) | Y |  |  |
| risk_core_solvency_ratio_show | varchar(10) | Y |  |  |
| risk_spot_amount | numeric(30,8) | Y |  | 当前黄金现货合约总规模（元） |
| risk_trade_party_lease_stop | numeric(30,8) | Y |  | 单一交易对手方租借禁止线额度（元） |
| risk_swap_far_net_ratio | numeric(10,4) | Y |  | 掉期远端空头净敞口占黄金现货比例(%) |
| risk_swap_near_duration_ratio | numeric(10,4) | Y |  | 掉期近端存续规模占总资产比例(%) |
| risk_swap_far_duration_ratio | numeric(10,4) | Y |  | 掉期远端存续规模占总资产比例(%) |
| risk_spot_amount_show | varchar(10) | Y |  |  |
| risk_trade_party_lease_stop_show | varchar(10) | Y |  |  |
| risk_swap_far_net_ratio_show | varchar(10) | Y |  |  |
| risk_swap_near_duration_ratio_show | varchar(10) | Y |  |  |
| risk_swap_far_duration_ratio_show | varchar(10) | Y |  |  |
| if_send_eoa | bpchar(1) | Y |  | 是否发送EOA |
| if_renew | bpchar(1) | Y |  | 是否重传 |
| renew_reason | varchar(400) | Y |  | 重传原因 |
| risk_cal_amount | numeric(30,8) | Y |  | 风控计算额度 |
| risk_check_opinion | varchar(500) | Y |  | 风控审核意见 |
| risk_check_user | varchar(50) | Y |  | 风控审核人 |
| trade_check_opinion | varchar(500) | Y |  | 交易复核意见 |
| trade_check_user | varchar(50) | Y |  | 交易复核人 |

---

## 304. dimple.tc_jh_storage_clear　(4 字段)
> 表含义：交行库存特殊表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| dt_qty | numeric(16,6) | Y |  | hjdt库存量 |
| lend_qty | numeric(16,6) | Y |  | 境外拆借库存量 |

---

## 305. dimple.tc_kondor_purpose　(4 字段)
> 表含义：kondor folder与交易目的对应表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | numeric(10,0) | N | √ | 序号 |
| folder | varchar(24) | Y |  | 交易级别 |
| pcode | varchar(3) | Y |  | 交易目的 |
| if_default | varchar(3) | Y |  | 是否默认 |

---

## 306. dimple.tc_large_amount_match　(22 字段)
> 表含义：大宗交易成交表　|　估算行数：**14**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| apply_date | varchar(8) | N | √ | 申报日期 |
| trader_no | varchar(16) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| party_member_id | varchar(8) | Y |  | 对手方席位号 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | Y |  | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| price | numeric(20,8) | Y |  | 成交价格 |
| remark | varchar(254) | Y |  | 备注 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| apply_status | varchar(3) | Y |  | 申报状态：见tp_public_dict的403  |
| match_no | varchar(20) | Y |  | SGE成交单号 |

---

## 307. dimple.tc_large_amount_match_jour　(23 字段)
> 表含义：大宗交易成交流水表　|　估算行数：**65**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| match_seq_no | float8 | N | √ | 大宗交易成交表流水号 |
| apply_date | varchar(8) | N | √ | 申报日期 |
| trader_no | varchar(16) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| party_member_id | varchar(8) | Y |  | 对手方席位号 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | Y |  | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| price | numeric(20,8) | Y |  | 成交价格 |
| remark | varchar(254) | Y |  | 备注 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| apply_status | varchar(3) | Y |  | 申报状态：见tp_public_dict的403  |
| match_no | varchar(20) | Y |  | SGE成交单号 |

---

## 308. dimple.tc_largeside_contract_group　(8 字段)
> 表含义：大边保证金合约(组)表　|　估算行数：**43,260**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| exch_code | varchar(2) | N | √ | 交易所代码:见tp_public_dict的217 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| group_no | numeric(10,0) | N | √ | 组合代码 |
| group_name | varchar(30) | Y |  | 组合名称 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |

---

## 309. dimple.tc_largeside_flag　(11 字段)
> 表含义：大边合约组方向场上表　|　估算行数：**8**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| exch_code | varchar(2) | N | √ | 交易所:见tp_public_dict的217 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| group_no | numeric(10,0) | N | √ | 组合代码 |
| largeside_flag | bpchar(1) | Y |  | 大边方向:见tp_public_dict的002 |
| sum_buy_margin | numeric(18,2) | Y |  | 买持仓保证金汇总 |
| sum_sell_margin | numeric(18,2) | Y |  | 卖持仓保证金汇总 |
| sum_buy_frozen_margin | numeric(18,2) | Y |  | 买委托冻结保证金汇总 |
| sum_sell_frozen_margin | numeric(18,2) | Y |  | 卖委托冻结保证金汇总 |
| discount_amount | numeric(18,2) | Y |  | 保证金优惠总金额 |

---

## 310. dimple.tc_largeside_flag_clear　(9 字段)
> 表含义：大边合约组方向结算表　|　估算行数：**6,821**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| exch_code | varchar(2) | N | √ | 交易所:见tp_public_dict的217 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| group_no | numeric(10,0) | N | √ | 组合代码 |
| largeside_flag | bpchar(1) | Y |  | 大边方向:见tp_public_dict的002 |
| sum_buy_margin | numeric(18,2) | Y |  | 买保证金汇总 |
| sum_sell_margin | numeric(18,2) | Y |  | 卖保证金汇总 |
| discount_amount | numeric(18,2) | Y |  | 保证金优惠总金额 |

---

## 311. dimple.tc_largeside_member_config　(2 字段)
> 表含义：金交所大边保证金席位配置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| if_largeside | varchar(1) | N |  | 是否按大边规则计算保证金:见Tp_public_dict的027 |

---

## 312. dimple.tc_last_purpose_cost_clear　(6 字段)
> 表含义：现货上日余量成本表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | Y |  | 席位 |
| contract_id | varchar(20) | N |  | 合约 |
| remain_qty | numeric(25,8) | Y |  | 库存余量(手) |
| remain_cost | numeric(25,8) | Y |  | 库存成本 |
| purpose_code | varchar(3) | N |  | 投组 |

---

## 313. dimple.tc_lend_contract_relation　(2 字段)
> 表含义：金交所拆借合约、交割品种对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| lend_contract_id | varchar(20) | N | √ | 拆借合约 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |

---

## 314. dimple.tc_lend_interest_clear　(21 字段)
> 表含义：导入表-拆借利息表　|　估算行数：**790**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| interestclearno | varchar(20) | Y |  | 主系统利息清算单编号 |
| lendregno | varchar(20) | Y |  | 询价拆借登记单编号 |
| regno | varchar(20) | N |  | 主系统拆借登记单编号 |
| memberid1 | varchar(8) | Y |  | 本方会员代码 |
| mabbr1 | varchar(20) | Y |  | 本方会员简称 |
| clientid1 | varchar(12) | Y |  | 本方客户代码 |
| cabbr1 | varchar(20) | Y |  | 本方客户简称 |
| memberid2 | varchar(8) | Y |  | 对手方会员代码 |
| mabbr2 | varchar(20) | Y |  | 对手方会员简称 |
| clientid2 | varchar(12) | Y |  | 对手方客户代码 |
| cabbr2 | varchar(20) | Y |  | 对手方客户简称 |
| interest | numeric(24,6) | Y |  | 利息金额\本方收到资金金额 |
| flag | varchar(4) | Y |  | 本方利息支付方向 |
| paydate | varchar(8) | N |  | 付息日期 |
| actualpaydate | varchar(8) | N |  | 实际付息日期 |
| clearingresult | varchar(4) | Y |  | 清算结果：见tp_public_dict的355 |
| impdate | varchar(8) | Y |  | 导入日期 |
| imptime | varchar(8) | Y |  | 导入时间 |
| lend_flag | varchar(4) | Y |  | 本方方向：见tp_public_dict的221中拆入和拆出 |
| contract_id | varchar(20) | Y |  | 合约代码 |

---

## 315. dimple.tc_lending_counterparty　(13 字段)
> 表含义：拆借交易对手方管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(20) | N | √ | 交易所 |
| client_id | varchar(10) | Y |  | 对手方客户号 |
| client_name | varchar(40) | N |  | 对手方简称 |
| client_code | varchar(20) | N | √ | 对手方代码 |
| client_full_name | varchar(20) | Y |  | 对手方全称 |
| contact_person | varchar(16) | Y |  | 联系人 |
| contact_phone | varchar(15) | Y |  | 联系电话 |
| money_account | varchar(20) | Y |  | 资金划拨账号 |
| state | varchar(3) | N |  | 状态 见tp_public_dict:245 |
| create_date | timestamp | N |  | 创建日期 |
| creater_id | varchar(30) | N |  | 创建者 |
| modify_date | timestamp | N |  | 修改日期 |
| modifier_id | varchar(30) | N |  | 修改者 |

---

## 316. dimple.tc_lending_detail　(12 字段)
> 表含义：实时拆借明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 系统日期 |
| match_local_no | numeric(10,0) | N | √ | 本地申报单号 |
| seq_no | numeric(10,0) | N | √ | 序号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种 |
| storage_flag | varchar(4) | N |  | 仓库 见tp_public_dict:245 |
| delivery_num | numeric(16,3) | N |  | 数量 |
| delivery_price | numeric(24,6) | N |  | 定盘价 |
| delivery_rate | numeric(16,2) | N |  | 协议利率 |
| create_date | timestamp | N |  | 创建日期 |
| creater_id | varchar(30) | N |  | 创建者 |
| modify_date | timestamp | N |  | 修改日期 |
| modifier_id | varchar(30) | N |  | 修改者 |

---

## 317. dimple.tc_lending_match　(21 字段)
> 表含义：实时拆借成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(3) | N | √ | 交易所 |
| trade_date | varchar(8) | N | √ | 系统日期 |
| match_date | varchar(8) | N |  | 交易日 |
| effect_date | varchar(8) | N |  | 申报日期 |
| match_local_no | numeric(10,0) | N | √ | 本地申报单号 |
| match_no | varchar(20) | Y |  | 租借登记申报编号 |
| apply_flag | varchar(3) | Y |  | 申报方 见tp_public_dict:242 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| lender_id | varchar(10) | Y |  | 拆借客户号 |
| agreement_sn | varchar(20) | N |  | 租借合约编号 |
| expire_date | varchar(8) | N |  | 租借到期日 |
| trader_no | varchar(16) | N |  | 交易员 |
| status | varchar(3) | N |  | 申报状态 |
| remark | varchar(100) | Y |  | 备注 见tp_public_dict:243 |
| create_date | timestamp | N |  | 创建日期 |
| creater_id | varchar(30) | N |  | 创建者 |
| modify_date | timestamp | N |  | 修改日期 |
| modifier_id | varchar(30) | N |  | 修改者 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| cost_price | numeric(24,6) | Y |  | 成本价 |

---

## 318. dimple.tc_lending_storage_tot　(10 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种 |
| init_storage | numeric(16,6) | Y |  | 期初库存量（千克） |
| final_storage | numeric(16,6) | Y |  | 期末库存量（千克） |
| lend_in_storage | numeric(16,6) | Y |  | 拆入量（千克） |
| lend_out_storage | numeric(16,6) | Y |  | 拆出量（千克） |
| mod_storage | numeric(16,6) | Y |  | 修改量（千克） |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 319. dimple.tc_lendmatch_swift　(81 字段)
> 表含义：境外拆借swift报文　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| seq_no | float8 | N |  | 成交区域流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| operator | varchar(40) | Y |  | 操作员 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| tag94a_a | varchar(4) | Y |  | A区经营范围 |
| tag22b_a | varchar(4) | Y |  | A区事件类型 |
| tag21n_a | varchar(16) | Y |  | A区代理方的交易编号 |
| tag82a_a | varchar(20) | Y |  | A区本行SWIFT号 |
| tag87a_a | varchar(20) | Y |  | A区交易对手SWIFT号 |
| tag83a_a | varchar(220) | Y |  | A区基金机构方 |
| tag26c_a | varchar(43) | Y |  | A区商品标识 |
| tag77d_a | varchar(220) | Y |  | A区条款和条件 |
| tag15b_b | varchar(1) | Y |  | B区标志域 |
| tag17r_b | varchar(1) | Y |  | B区本行的拆借方向 |
| tag30t_b | varchar(8) | Y |  | B区交易日期 |
| tag30v_b | varchar(8) | Y |  | B区起息日 |
| tag30p_b | varchar(8) | Y |  | B区到期日期 |
| tag32a_b | varchar(18) | Y |  | B区货币/本金、数量 |
| tag30x_b | varchar(8) | Y |  | B区应付利息日 |
| tag34a_b | varchar(18) | Y |  | B区币种和利息 |
| tag37g_b | varchar(12) | Y |  | B区利率 |
| tag14d_b | varchar(7) | Y |  | B区计息天数 |
| tag30f_b | varchar(8) | Y |  | B区最近付息日 |
| tag38j_b | varchar(4) | Y |  | B区天数 |
| tag15c_c | varchar(1) | Y |  | C区标志域 |
| tag53a_c | varchar(220) | Y |  | C区投递代理机构信息 |
| tag86a_c | varchar(220) | Y |  | C区中介机构信息2 |
| tag56a_c | varchar(220) | Y |  | C区中介机构信息1 |
| tag57a_c | varchar(220) | Y |  | C区收货代理机构信息 |
| tag58a_c | varchar(220) | Y |  | C区收益机构 |
| tag15d_d | varchar(1) | Y |  | D区标志域 |
| tag53a_d | varchar(220) | Y |  | D区投递代理机构信息 |
| tag86a_d | varchar(220) | Y |  | D区中介机构信息2 |
| tag56a_d | varchar(220) | Y |  | D区本行的黄金中转行账号+swift码 |
| tag57a_d | varchar(220) | Y |  | D区本行的黄金代理行账号+swift码 |
| tag58a_d | varchar(220) | Y |  | D区收益机构 |
| tag15e_e | varchar(1) | Y |  | E区标志域 |
| tag53a_e | varchar(220) | Y |  | E区投递代理机构信息 |
| tag86a_e | varchar(220) | Y |  | E区中介机构信息2 |
| tag56a_e | varchar(220) | Y |  | E区交易对手的美金中转行账号+swift码 |
| tag57a_e | varchar(220) | Y |  | E区交易对手的美金代理行账号+swift码 |
| tag58a_e | varchar(220) | Y |  | E区收益机构 |
| tag15f_f | varchar(1) | Y |  | F区标志域 |
| tag53a_f | varchar(220) | Y |  | F区投递代理机构信息 |
| tag86a_f | varchar(220) | Y |  | F区中介机构信息2 |
| tag56a_f | varchar(220) | Y |  | F区本行的美金中转行账号+swfit码 |
| tag57a_f | varchar(220) | Y |  | F区本行的美金代理行账号+swift码 |
| tag58a_f | varchar(220) | Y |  | F区收益机构 |
| tag15g_g | varchar(1) | Y |  | G区标志域 |
| tag37l_g | varchar(12) | Y |  | G区税率 |
| tag33a_g | varchar(18) | Y |  | G区货币/利息、金额 |
| tag36_g | varchar(12) | Y |  | G区汇率 |
| tag33ao_g | varchar(15) | Y |  | G区货币/税收金额 |
| tag15h_h | varchar(1) | Y |  | H区标志域 |
| tag29a_h | varchar(150) | Y |  | H区联系信息 |
| tag24d_h | varchar(40) | Y |  | H区合约处理方法 |
| tag84a_h | varchar(220) | Y |  | H区机构A处理部门 |
| tag85a_h | varchar(220) | Y |  | H区机构B处理部门 |
| tag88a_h | varchar(220) | Y |  | H区代理人信息 |
| tag71f_h | varchar(18) | Y |  | H区代理人佣金 |
| tag26h_h | varchar(16) | Y |  | H区交易对手参考信息 |
| tag21g_h | varchar(16) | Y |  | H区代理人参考信息 |
| tag22z_h | varchar(6) | Y |  | H区产品标识 |
| tag72_h | varchar(220) | Y |  | H区发送方到接收方信息 |
| op_date | varchar(8) | N |  | 新增日期 |
| tag15a_a | varchar(1) | Y |  | A区标志域 |
| tag20_a | varchar(16) | Y |  | A区发送方参考号码 |
| tag21_a | varchar(16) | Y |  | A区对方相关参考信息 |
| tag22a_a | varchar(4) | Y |  | A区操作类型 |
| op_type | varchar(3) | Y |  | 操作类型 |
| jour_no | float8 | N |  | 系统流水号 |
| send_status | varchar(3) | N |  | 发送状态见tp_public_dict的294 |
| send_msg | varchar(255) | Y |  | 发送失败原因 |
| tag32a2_b | varchar(15) | Y |  | B区数量 |
| tag32a1_b | varchar(15) | Y |  | B区本金 |
| sender | varchar(11) | Y |  | 发送方swift号 |
| receiver | varchar(11) | Y |  | 接收方swift号 |
| mod_date | varchar(8) | Y |  | 操作日期 |

---

## 320. dimple.tc_manual_offset_order_match　(18 字段)
> 表含义：平盘手工补录表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 录入日期 |
| offset_type | varchar(2) | N |  | 平盘类型：见tp_public_dict的405 |
| paris_currency | varchar(8) | N |  | 货币对 |
| offset_mode | varchar(2) | N |  | 平盘模式：见tp_public_dict的034 |
| offset_strategy | varchar(2) | Y |  | 平盘策略: 见tp_public_dict的406，可为空，数据字典等需求 |
| offset_channel | varchar(50) | Y |  | 平盘方: 标注外资行,可为空 |
| member_id | varchar(8) | Y |  | 平盘席位号:美元平盘不填 |
| client_id | varchar(16) | Y |  | 平盘客户号:美元平盘不填 |
| manual_no | varchar(64) | N |  | 补录单号:等同于接口返回的订单号 |
| offset_flag | varchar(2) | N |  | 平盘方向: 见tp_public_dict的002 |
| offset_qty1 | numeric(24,8) | Y |  | 平盘重量(克)：美元平盘不填 |
| offset_qty2 | numeric(24,8) | Y |  | 平盘重量(盎司)：美元平盘不填 |
| offset_amt1 | numeric(24,8) | Y |  | 平盘金额(元)：贵金属平盘不填 |
| offset_amt2 | numeric(24,8) | Y |  | 平盘金额(美元) |
| trader_no | varchar(16) | Y |  | 操作员 |
| op_time | varchar(12) | Y |  | 时间 |
| manual_status | varchar(2) | Y |  | 补录状态: 见tp_public_dict的407;此处仅2,X |
| remark | varchar(250) | Y |  | 备注 |

---

## 321. dimple.tc_market_trader_purpose　(7 字段)
> 表含义：市场默认交易员交易目的表:249版本用万能参数表替代，此表废弃　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| market_type | varchar(3) | N | √ | 市场:见tp_public_dict的001 |
| trader_no | varchar(30) | N |  | 交易员编码 |
| tpcode | varchar(3) | N |  | 交易目的字段 |
| create_date | timestamp | Y |  | 创建日期 |
| create_id | varchar(30) | Y |  | 创建人 |
| modify_date | timestamp | Y |  | 修改日期 |
| modify_id | varchar(30) | Y |  | 修改人 |

---

## 322. dimple.tc_match_allocate_batch_tmp　(20 字段)
> 表含义：交易员成交未分配批量分配整理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| due_date | varchar(20) | Y |  | 到期日：保证金询价使用 |
| trader_no | varchar(16) | Y |  | 原交易员 |
| qty | numeric(12,0) | Y |  | 总数量（手） |
| nqty | numeric(12,0) | Y |  | 已分配数量（手） |
| noqty | numeric(12,0) | Y |  | 未分配数量（手）：总数量-已分配数量 |
| price | numeric(20,8) | Y |  | 价格 |
| match_time | varchar(12) | Y |  | 成交时间 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| remark | varchar(200) | Y |  | 分配流水表中交易目的简称 |
| opcode | varchar(3) | N |  | 原成交临时表交易目的代码 |
| match_type | bpchar(1) | Y |  | 成交类型:见tp_public_dict237 |
| oremark | varchar(200) | Y |  | 原成交临时表交易目的简称 |
| delivery_type | varchar(3) | Y |  | 交割方式;见public_dict的051 |

---

## 323. dimple.tc_mc_avg_clear　(6 字段)
> 表含义：移动平均最终表　|　估算行数：**25,217**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| group_no | varchar(10) | N | √ | 组号 |
| remain_price | numeric(20,8) | Y |  | 当笔均价 |
| remain_qty | numeric(16,6) | Y |  | 当笔数量 |
| remain_amt | numeric(24,6) | Y |  | 当笔成本 |
| profit | numeric(24,6) | Y |  | 盈亏 |

---

## 324. dimple.tc_mc_avg_detail　(18 字段)
> 表含义：移动平均计算明细表　|　估算行数：**1,240**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| group_no | varchar(10) | N | √ | 组号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | numeric(10,0) | N | √ | 序号 |
| rank_no | numeric(10,0) | N | √ | 排序位置 |
| posi_flag | varchar(3) | Y |  | 持仓方向:0：无方向；1：买（正向） 3：卖（反向） |
| io_flag | varchar(3) | Y |  | 增减标志：见dict 315 |
| last_avg_price | numeric(20,8) | Y |  | 上笔均价 |
| last_qty | numeric(16,6) | Y |  | 上笔数量 |
| last_amt | numeric(24,6) | Y |  | 上笔成本 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(16,6) | Y |  | 平仓量:单位手 |
| amt | numeric(24,6) | Y |  | 金额 |
| cost_amt | numeric(24,6) | Y |  | 成本金额 |
| remain_avg_price | numeric(20,8) | Y |  | 当笔均价 |
| remain_qty | numeric(16,6) | Y |  | 当笔数量 |
| remain_amt | numeric(24,6) | Y |  | 当笔成本 |
| profit | numeric(24,6) | Y |  | 盈亏 |

---

## 325. dimple.tc_mc_day_avg_clear　(6 字段)
> 表含义：每日移动平均计算明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 清算日期 |
| group_no | varchar(10) | N |  | 组号 |
| remain_price | numeric(20,8) | Y |  | 当日均价 |
| remain_qty | numeric(16,6) | Y |  | 当日数量 |
| remain_amt | numeric(24,6) | Y |  | 当日成本 |
| profit | numeric(24,6) | N |  | 盈亏 |

---

## 326. dimple.tc_mc_day_avg_detail　(14 字段)
> 表含义：每日移动平均计算明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 清算日期 |
| group_no | varchar(10) | N |  | 组号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| seq_no | numeric(10,0) | N |  | 序号 |
| last_avg_price | numeric(20,8) | Y |  | 昨日均价 |
| last_avg_qty | numeric(16,6) | Y |  | 昨日数量 |
| last_avg_amt | numeric(24,6) | Y |  | 昨日成本 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(16,6) | N |  | 平仓量:单位手 |
| amt | numeric(24,6) | Y |  | 金额 |
| remain_price | numeric(20,8) | Y |  | 当日均价 |
| remain_qty | numeric(16,6) | Y |  | 当日数量 |
| remain_amt | numeric(24,6) | Y |  | 当日成本 |
| profit | numeric(24,6) | N |  | 盈亏 |

---

## 327. dimple.tc_mc_fifo_clear　(10 字段)
> 表含义：FIFO计算统计表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| group_no | varchar(10) | N | √ | 分组号 |
| buy_qty | numeric(16,6) | Y |  | 买持仓量 |
| buy_avg_price | numeric(20,8) | Y |  | 买持仓均价 |
| buy_amt | numeric(24,6) | Y |  | 买持仓金额 |
| sell_qty | numeric(16,6) | Y |  | 买持仓量 |
| sell_avg_price | numeric(20,8) | Y |  | 买持仓均价 |
| sell_amt | numeric(24,6) | Y |  | 买持仓金额 |
| buy_profit | numeric(24,6) | Y |  | 买平盈亏 |
| sell_profit | numeric(24,6) | Y |  | 卖平盈亏 |

---

## 328. dimple.tc_mc_fifo_hold_detail　(7 字段)
> 表含义：计算层表-先进先出明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| group_no | varchar(10) | N | √ | 组号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | numeric(10,0) | N | √ | 当日序号 |
| price | numeric(20,8) | Y |  | 价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| qty | numeric(16,6) | N |  | 量:单位手 |

---

## 329. dimple.tc_mc_fifo_offset_detail　(14 字段)
> 表含义：计算用先进先出平仓明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| group_no | varchar(10) | N | √ | 组号 |
| offset_trade_date | varchar(8) | N | √ | 平仓交易日期 |
| open_trade_date | varchar(8) | N | √ | 开仓交易日期 |
| offset_seq_no | numeric(10,0) | N | √ | 平仓序号 |
| open_seq_no | numeric(10,0) | N | √ | 开仓序号 |
| offset_price | numeric(20,8) | Y |  | 价格 |
| open_price | numeric(20,8) | Y |  | 价格 |
| offset_amt | numeric(24,6) | Y |  | 金额 |
| open_amt | numeric(24,6) | Y |  | 金额 |
| offset_qty | numeric(16,6) | N |  | 平仓量 |
| open_qty | numeric(16,6) | Y |  | 开仓量 |
| remain_qty | numeric(16,6) | N |  | 剩余量 |
| profit | numeric(24,6) | N |  | 盈亏 |

---

## 330. dimple.tc_mc_group　(15 字段)
> 表含义：现金先出分组表　|　估算行数：**99**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| group_no | varchar(10) | N | √ | 组号 |
| gen_date | varchar(8) | Y |  | 生成日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(16) | Y |  | 交易员 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| account_type | varchar(3) | Y |  | 账务处理类型：见Dict 313 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| calc_type | varchar(3) | Y |  | 计算类型：见Dict 314 |
| contract_id | varchar(20) | Y |  | 合约号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| delivery_variety_id | varchar(3) | Y |  | 交割品 |
| posi_flag | varchar(3) | Y |  | 持仓方向:0：无方向；1：买（正向） 3：卖（反向） |
| cost_type | varchar(10) | Y |  | 成本中心：见dict 316 |
| cfg_seq_no | float8 | Y |  | 配置序列号 |

---

## 331. dimple.tc_mc_group_config　(15 字段)
> 表含义：组设置　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| config_code | varchar(20) | N | √ | 银行配置: 见para的ACCOUNT_CTL_TYPE |
| seq_no | float8 | N | √ | 配置序号 |
| if_member | varchar(3) | Y |  | 是否关心会员：见 dict 027 |
| if_client | varchar(3) | Y |  | 是否关心客户：见 dict 027 |
| if_user | varchar(3) | Y |  | 是否关心用户：见 dict 027 |
| if_sh_flag | varchar(3) | Y |  | 是否关心投机套保：见 dict 027 |
| if_account_type | varchar(3) | Y |  | 是否关心账务类型：见 dict 027 |
| if_arbi_contract | varchar(3) | Y |  | 是否关心套利合约：见 dict 027 |
| if_deli_variety | varchar(3) | Y |  | 是否关心交割品种：见 dict 027 |
| if_posi_flag | varchar(3) | Y |  | 是否关心持仓方向：见 dict 027 |
| if_cost_type | varchar(3) | Y |  | 是否关心成本中心：见 dict 027 |
| if_contract | varchar(3) | Y |  | 是否关心合约：见 dict 027 |
| if_purpose | varchar(3) | Y |  | 是否关心交易目的：见 dict 027 |
| calc_type | varchar(3) | Y |  | 计算类型:见 dict 314 |
| remark | varchar(250) | Y |  | 备注 |

---

## 332. dimple.tc_mc_match　(25 字段)
> 表含义：计算用成交表　|　估算行数：**1,052,235**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| seq_no | numeric(10,0) | N | √ | 编号 |
| match_date | varchar(8) | Y |  | 成交日期 |
| match_time | varchar(8) | Y |  | 成交时间 |
| match_no | varchar(20) | Y |  | 成交号 |
| trade_type | varchar(3) | Y |  | 交易类型：见dict 001 |
| match_type | varchar(3) | Y |  | 成交类型:1-成交;2-交割;3#中立仓交割;4-库存 |
| contract_id | varchar(20) | Y |  | 合约号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| delivery_variety_id | varchar(3) | Y |  | 交割品 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(16) | Y |  | 交易员 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| io_flag | varchar(3) | Y |  | 增减标志：见dict 315 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| qty | numeric(16,6) | Y |  | 数量:单位手 |
| price | numeric(20,8) | Y |  | 价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| cancel_flag | varchar(3) | Y |  | 冲销标志:见dict 27 |
| posi_flag | varchar(3) | Y |  | 持仓方向:0：无方向；1：买（正向） 3：卖（反向） |
| cost_type | varchar(10) | Y |  | 成本中心：见dict 316 |
| account_type | varchar(3) | Y |  | 账务类型:见Dict 313 |
| delivery_type | varchar(3) | Y |  | 交割方式:见Dict 051 |

---

## 333. dimple.tc_mc_match_manage_jour　(13 字段)
> 表含义：计算用成交分配流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| jour_no | numeric(10,0) | N | √ | 分配流水号 |
| seq_no | numeric(10,0) | Y |  | 编号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(16) | Y |  | 交易员 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| account_type | varchar(3) | Y |  | 计算类型:见Dict 313 |
| cost_type | varchar(10) | Y |  | 成本中心：见dict 316 |
| creater | varchar(16) | N |  | 分配人 |
| create_date | varchar(8) | N |  | 分配日期 |
| create_time | varchar(8) | N |  | 分配时间 |

---

## 334. dimple.tc_mc_match_posi　(4 字段)
> 表含义：计算用成交持仓属性表　|　估算行数：**1,042,552**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| seq_no | numeric(10,0) | N | √ | 编号 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| inq_deli_price | numeric(20,8) | Y |  | 询价交割结算价 |

---

## 335. dimple.tc_mc_match_storage　(8 字段)
> 表含义：计算用成交库存属性表　|　估算行数：**7,014**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| seq_no | numeric(10,0) | N | √ | 编号 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号 |
| deli_contract_id | varchar(20) | Y |  | 交割合约号 |
| trans_type | varchar(3) | Y |  | 库存变化类型:见dict 221 |
| storage_no | varchar(4) | Y |  | 仓库代码：见dict 244 |
| paper_amt | numeric(24,6) | Y |  | 原发票金额 |
| stock_source | varchar(3) | Y |  | 出入库性质,见tp_public_dict的236 |

---

## 336. dimple.tc_member_posi　(29 字段)
> 表含义：导入会员持仓文件表　|　估算行数：**3,732**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(30) | N |  | 合约号 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开成交量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开成交量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平成交量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平成交量 |
| buy_total_qty | numeric(12,0) | Y |  | 今日买成交量合计 |
| sell_total_qty | numeric(12,0) | Y |  | 今日卖成交量合计 |
| buy_turnover | numeric(19,2) | Y |  | 今日买成交额 |
| sell_turnover | numeric(19,2) | Y |  | 今日卖成交额 |
| t_buy_qty | numeric(12,0) | Y |  | 投机买持仓量 |
| b_buy_qty | numeric(12,0) | Y |  | 保值买持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量合计 |
| t_sell_qty | numeric(12,0) | Y |  | 投机卖持仓量 |
| b_sell_qty | numeric(12,0) | Y |  | 保值卖持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量合计 |
| margin | numeric(19,2) | Y |  | 交易保证金 |
| profitloss | numeric(19,2) | Y |  | 当日盈亏 |
| due_fee | numeric(19,2) | Y |  | 应收手续费 |
| actual_fee | numeric(19,2) | Y |  | 实收手续费 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| derate_fee | numeric(19,2) | Y |  | 减免手续费 |
| buy_open_turnover | numeric(19,2) | Y |  | 买开成交额：上期所 |
| sell_open_turnover | numeric(19,2) | Y |  | 卖开成交额：上期所 |
| buy_offset_turnover | numeric(19,2) | Y |  | 买平成交额：上期所 |
| sell_offset_turnover | numeric(19,2) | Y |  | 卖平成交额：上期所 |

---

## 337. dimple.tc_member_tot　(9 字段)
> 表含义：会员统计表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| today_match_qty | numeric(12,0) | Y |  | 当日成交量 |
| today_match_amt | numeric(24,6) | Y |  | 当日成交额 |
| month_match_qty | numeric(12,0) | Y |  | 月累计成交量 |
| month_match_amt | numeric(24,6) | Y |  | 月累计成交额 |
| year_match_qty | numeric(12,0) | Y |  | 年累计成交量 |
| year_match_amt | numeric(24,6) | Y |  | 年累计成交额 |

---

## 338. dimple.tc_message_jour　(8 字段)
> 表含义：短信发送日志表　|　估算行数：**959**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | float8 | N | √ | 流水号 |
| trade_date | varchar(8) | N | √ | 发送日期 |
| trade_time | varchar(8) | Y |  | 发送时间 |
| message_type | varchar(2) | Y |  | 短信类型:见tp_public_dict的400 |
| message_content | varchar(255) | Y |  | 短信内容 |
| receiver_name | varchar(50) | Y |  | 短信接收人 |
| phone_number | varchar(11) | Y |  | 手机号 |
| if_success | varchar(2) | Y |  | 是否发送成功：见tp_public_dict的027 |

---

## 339. dimple.tc_message_reveiver_manage　(3 字段)
> 表含义：短信人员管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| message_type | varchar(2) | N | √ | 短信类型:见tp_public_dict的400 |
| receiver_name | varchar(50) | N |  | 短信接收人 |
| phone_number | varchar(11) | N | √ | 手机号 |

---

## 340. dimple.tc_metal_offset_posi_clear　(25 字段)
> 表含义：贵金属平盘头寸结算表　|　估算行数：**8,864**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | N | √ | 客户代码 |
| paris_currency | varchar(8) | N | √ | 货币对 |
| last_buy_qty1 | numeric(24,8) | Y |  | 上一日平盘买头寸:克 |
| last_sell_qty1 | numeric(24,8) | Y |  | 上一日平盘卖头寸:克 |
| last_buy_qty2 | numeric(24,8) | Y |  | 上一日平盘买头寸:盎司 |
| last_sell_qty2 | numeric(24,8) | Y |  | 上一日平盘卖头寸:盎司 |
| last_money_in | numeric(24,8) | Y |  | 上一日平盘卖出收入头寸：美元 |
| last_money_out | numeric(24,8) | Y |  | 上一日平盘买入支出头寸：美元 |
| offset_buy_qty1 | numeric(24,8) | Y |  | 平盘买头寸:克 |
| offset_sell_qty1 | numeric(24,8) | Y |  | 平盘卖头寸:克 |
| net_offset_qty1 | numeric(24,8) | Y |  | 平盘轧差头寸:克 |
| t_offset_buy_qty1 | numeric(24,8) | Y |  | 今日平盘买量:克 |
| t_offset_sell_qty1 | numeric(24,8) | Y |  | 今日平盘卖量:克 |
| offset_buy_qty2 | numeric(24,8) | Y |  | 平盘买头寸:盎司 |
| offset_sell_qty2 | numeric(24,8) | Y |  | 平盘卖头寸:盎司 |
| net_offset_qty2 | numeric(24,8) | Y |  | 平盘轧差头寸:盎司 |
| t_offset_buy_qty2 | numeric(24,8) | Y |  | 今日平盘买量:盎司 |
| t_offset_sell_qty2 | numeric(24,8) | Y |  | 今日平盘卖量:盎司 |
| money_in | numeric(24,8) | Y |  | 平盘卖出收入头寸：美元 |
| money_out | numeric(24,8) | Y |  | 平盘买入支出头寸：美元 |
| net_money | numeric(24,8) | Y |  | 平盘轧差头寸：美元；公式=上一日平盘卖出收入头寸+今日平盘卖出收入金额-上一日平盘买入支出头寸-今日平盘买入支出金额 |
| t_money_in | numeric(24,8) | Y |  | 今日平盘卖出收入金额：美元 |
| t_money_out | numeric(24,8) | Y |  | 今日平盘买入支出金额：美元 |

---

## 341. dimple.tc_mid_ftr_fee　(16 字段)
> 表含义：期货手续费率中间表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| variety_id | varchar(4) | Y |  | 品种代码 |
| contract_id | varchar(20) | N |  | 合约代码:$表示所有合约 |
| clear_account_no | varchar(14) | N |  | 结算子帐号:$表示所有结算帐号 |
| client_id | varchar(16) | N |  | 客户号:$表示所有客户 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| open_fee | numeric(18,2) | N |  | 开仓结算手续费 |
| offset_fee | numeric(18,2) | N |  | 平仓结算手续费 |
| t_open_fee | numeric(18,2) | N |  | 开仓交易手续费 |
| t_offset_fee | numeric(18,2) | N |  | 平仓交易手续费 |
| short_open_fee | numeric(18,2) | N |  | 短线开仓手续费 |
| short_offset_fee | numeric(18,2) | N |  | 短线平仓手续费 |
| op_type | bpchar(1) | N |  | 操作类型:参考常量表。－》见tp_public_dict的091。 |
| status | bpchar(1) | N |  | 状态:参考常数表。－》见tp_public_dict的094。 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 342. dimple.tc_mid_maintenance　(9 字段)
> 表含义：结算准备金最低余额中间表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| clear_account_no | varchar(14) | N |  | 结算子帐号:$表示所有结算帐号 |
| account_type | varchar(4) | N |  | 帐号类型:见tp_public_dict的038 |
| call_low_bal | numeric(18,2) | Y |  | 追保下限 |
| rule_low_bal | numeric(18,2) | Y |  | 强平下限 |
| op_type | bpchar(1) | N |  | 操作类型:参考常量表。－》见tp_public_dict的091。 |
| status | bpchar(1) | N |  | 状态:参考常数表。－》见tp_public_dict的094。 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 343. dimple.tc_mid_posi_margin_rate　(17 字段)
> 表含义：持仓量保证金率中间表:存储关于持仓量的保证金率信息的中间表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码:$表示所有合约 |
| clear_account_no | varchar(14) | N | √ | 结算子帐号:$表示所有结算帐号 |
| posi_min | numeric(12,0) | N | √ | 持仓量下限 |
| posi_max | numeric(12,0) | N | √ | 持仓量上限:为999999999999表示上限为无限大 |
| spec_buy_rate | numeric(10,6) | N |  | 投机买率 |
| spec_sell_rate | numeric(10,6) | N |  | 投机卖率 |
| hedge_buy_rate | numeric(10,6) | N |  | 套保买率 |
| hedge_sell_rate | numeric(10,6) | N |  | 套保卖率 |
| margin_type | bpchar(1) | N |  | 保证金类型:预留，用于确定保证金率是比率值还是固定值。参考常量表。－》见tp_public_dict的092。 |
| op_type | bpchar(1) | N |  | 操作类型:参考常量表。－》见tp_public_dict的091。 |
| status | bpchar(1) | N |  | 状态:参考常数表。－》见tp_public_dict的094。 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| recheck_date | varchar(8) | Y |  | 审核日期:对于品种合约保证金管理，该项即操作日期;对于特殊结算帐号保证金管理，该项即审核日期 |
| recheck_oper | varchar(30) | Y |  | 审核员:对于品种合约保证金管理，该项即操作员;对于特殊结算帐号保证金管理，该项即审核操作的操作员 |

---

## 344. dimple.tc_mid_rpt_day_report　(18 字段)
> 表含义：中台损益报表　|　估算行数：**225,023**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| market_type | varchar(3) | N | √ | 市场类型 |
| convert_rate | numeric(20,8) | Y |  | 汇率 |
| last_buy_num | numeric(16,6) | Y |  | 昨持买量 |
| last_sell_num | numeric(16,6) | Y |  | 昨持卖量 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_num | numeric(16,6) | Y |  | 持买量 |
| buy_amt | numeric(24,6) | Y |  | 买持成本 |
| sell_num | numeric(16,6) | Y |  | 持卖量 |
| sell_amt | numeric(24,6) | Y |  | 卖持成本 |
| variety_id | varchar(4) | Y |  | 品种号 |
| day_profit | numeric(24,6) | Y |  | 日盈亏 |
| month_profit | numeric(24,6) | Y |  | 月盈亏 |
| year_profit | numeric(24,6) | Y |  | 年盈亏 |

---

## 345. dimple.tc_money_application　(16 字段)
> 表含义：出金申请表　|　估算行数：**110**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| local_seq_no | numeric(10,0) | N | √ | 本地流水号 |
| exch_seq_no | varchar(32) | Y |  | 交易所流水号 |
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| amt | numeric(24,6) | Y |  | 金额 |
| capitaltranstype | varchar(1) | Y |  | 保证金交易业务类型:见tp_public_dict的373 |
| todotxseqno | varchar(8) | Y |  | 发电流水序号 |
| todotxdate | timestamp | Y |  | 发电记账日期 |
| sentflag | varchar(2) | Y |  | 已发电标志:见tp_public_dict的374 |
| returnflag | varchar(4) | Y |  | 回执标志 |
| settlebankid | varchar(4) | Y |  | 结算行号 |
| status | varchar(3) | Y |  | 状态：见tp_public_dict的372 |
| abstract | varchar(256) | Y |  | 备注 |
| op_time | varchar(8) | Y |  | 时间 |
| op_user | varchar(30) | Y |  | 操作员 |

---

## 346. dimple.tc_money_detail　(31 字段)
> 表含义：交易编码资金明细表　|　估算行数：**6,942**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| currency | varchar(2) | N | √ | 币种 |
| delivery_margin | numeric(19,2) | Y |  | 交割保证金 |
| offset_profitloss | numeric(19,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(19,2) | Y |  | 持仓盈亏 |
| buy_premium | numeric(19,2) | Y |  | 权利金支出 |
| sell_premium | numeric(19,2) | Y |  | 权利金收入 |
| trade_fee | numeric(19,2) | Y |  | 交易手续费 |
| clear_fee | numeric(19,2) | Y |  | 结算手续费 |
| delivery_fee | numeric(19,2) | Y |  | 交割手续费 |
| move_posi_fee | numeric(19,2) | Y |  | 移仓手续费 |
| ret_fee | numeric(19,2) | Y |  | 返还手续费 |
| free_trade_fee | numeric(19,2) | Y |  | 减免交易手续费 |
| margin | numeric(19,2) | Y |  | 交易保证金 |
| mort_amt | numeric(19,2) | Y |  | 质押金额 |
| reserve | numeric(24,6) | Y |  | 利息 |
| other_money | numeric(19,2) | Y |  | 其他资金 |
| force_amt | numeric(19,2) | Y |  | 强平金额 |
| money_in | numeric(19,2) | Y |  | 当日入金 |
| money_out | numeric(19,2) | Y |  | 当日出金 |
| buy_amount | numeric(19,2) | Y |  | 买货款 |
| sell_amount | numeric(19,2) | Y |  | 卖货款 |
| frozen_profitloss | numeric(19,2) | Y |  | 盈亏冻结 |
| frozen_amount | numeric(19,2) | Y |  | 货款冻结 |
| ag_frozen_amount | numeric(19,2) | Y |  | 白银货款冻结 |
| manual_frozen_amount | numeric(19,2) | Y |  | 手工货款冻结 |
| law_last_forzen_amt | numeric(19,2) | Y |  | 上日司法冻结金额 |
| law_forzen_amt | numeric(19,2) | Y |  | 当日司法冻结金额 |

---

## 347. dimple.tc_money_type　(8 字段)
> 表含义：其他资金类型表:包括交定金,退定金,仓储费,质押手续费,转货款,其他划款，违约金，奖励等　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| money_type | varchar(20) | N | √ | 其他资金类型 |
| money_name | varchar(40) | N |  | 其他资金名称 |
| if_variety | bpchar(1) | N |  | 是否有品种属性:其他资金录入时使用，若为是，则其他资金录入时需要填入品种 |
| if_time | bpchar(1) | N |  | 是否有时间属性:其他资金录入时使用，若为是，则其他资金录入时需要填入时间 |
| direction | varchar(2) | Y |  | 资金划拨方向:见tp_public_dict的124 |
| status | bpchar(1) | N |  | 状态:见tp_public_dict的125 |
| if_fixed | bpchar(1) | N |  | 是否固化 |
| money_sort | bpchar(1) | N |  | 资金类别:见tp_public_dict的174 |

---

## 348. dimple.tc_mort_detail　(14 字段)
> 表含义：质押品明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| bill_no | varchar(30) | N | √ | 对应合同号 |
| bond_code | varchar(20) | N | √ | 债券代码 |
| bond_abbr | varchar(30) | Y |  | 债券简称 |
| bond_amt | numeric(20,2) | Y |  | 债券面额（万元） |
| mort_bond_amt | numeric(20,2) | Y |  | 质押券价值（元） |
| mort_bond_price | numeric(20,6) | Y |  | 质押券价格（元/百元） |
| mort_rate | numeric(20,6) | Y |  | 质押率 |
| trade_type | varchar(30) | Y |  | 交易类型 |
| record_status | varchar(30) | Y |  | 记录状态 |
| create_date | varchar(8) | Y |  | 生成日期 |
| cancel_date | varchar(8) | Y |  | 取消日期 |
| update_time | varchar(20) | Y |  | 更新时间 |
| trust_org | varchar(100) | Y |  | 托管机构 |
| mort_jour | varchar(40) | Y |  | 质押流水号 |

---

## 349. dimple.tc_mort_info　(21 字段)
> 表含义：质押信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| mort_jour | varchar(20) | N | √ | 质押流水号 |
| out_abbr | varchar(30) | Y |  | 出押方简称 |
| out_bond_no | varchar(20) | Y |  | 出押方债券账号 |
| in_abbr | varchar(30) | Y |  | 受押方简称 |
| in_bond_no | varchar(20) | Y |  | 受押方债券账号 |
| bus_type | varchar(30) | Y |  | 业务类别 |
| exposure_amt | numeric(20,2) | Y |  | 敞口金额（元） |
| real_exposure_amt | numeric(20,2) | Y |  | 实际敞口金额（元） |
| mort_amt | numeric(20,2) | Y |  | 质押券价值（元） |
| exposure_role | varchar(30) | Y |  | 敞口角色 |
| due_date | varchar(8) | Y |  | 到期日 |
| bind_flag | varchar(1) | Y |  | 是否绑定 |
| status | varchar(30) | Y |  | 状态 |
| operator | varchar(40) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| checker_id | varchar(30) | Y |  | 复核员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| seq_no | float8 | Y |  | 系统流水号 |
| bill_no | varchar(30) | Y |  | 合同号 |

---

## 350. dimple.tc_mort_value　(11 字段)
> 表含义：质押价值表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| mort_amt_no | varchar(20) | N | √ | 质押价值流水号 |
| bond_code | varchar(20) | Y |  | 债券代码 |
| mort_amt | numeric(20,2) | Y |  | 质押价值（元） |
| effect_date | varchar(8) | Y |  | 生效日期 |
| operator | varchar(40) | Y |  | 操作人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| checker_id | varchar(30) | Y |  | 复核员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(30) | Y |  | 复核状态 |

---

## 351. dimple.tc_nb_account_ag　(9 字段)
> 表含义：宁波银行-白银远期业务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖 |
| qty | numeric(18,2) | Y |  | 成交量(克) |
| price | numeric(20,8) | Y |  | 成交价 |
| turnover | numeric(18,2) | Y |  | 成交金额 |
| clear_price | numeric(20,8) | Y |  | 收盘价 |
| profit | numeric(18,2) | Y |  | 盈亏 |

---

## 352. dimple.tc_nb_account_defer　(9 字段)
> 表含义：宁波银行-账务递延买卖表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |

---

## 353. dimple.tc_nb_account_future　(9 字段)
> 表含义：宁波银行-账务债券期货业务　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |

---

## 354. dimple.tc_nb_account_lend　(5 字段)
> 表含义：宁波银行-黄金租赁业务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| trans_type | varchar(2) | Y |  | 库存变化类型 |
| delivery_variety_id | varchar(3) | Y |  | 交割品 |
| lend_qty | numeric(16,3) | Y |  | 租借量（克） |
| sheet_no | varchar(20) | Y |  | 租借登记编号 |

---

## 355. dimple.tc_nb_account_manage　(7 字段)
> 表含义：宁波银行-账务管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 序号 |
| total_count | numeric(20,0) | Y |  | 总记录数 |
| send_count | numeric(20,0) | Y |  | 发送记录数 |
| status | varchar(3) | Y |  | 状态:1未生成;2 已生成未发送;3发送中;4发送成功;5发送失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 356. dimple.tc_nb_account_priceing　(9 字段)
> 表含义：宁波银行-定价金业务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖 |
| qty | numeric(18,2) | Y |  | 成交量(克) |
| price | numeric(20,8) | Y |  | 成交价 |
| turnover | numeric(18,2) | Y |  | 成交金额 |
| clear_price | numeric(20,8) | Y |  | 收盘价 |
| profit | numeric(18,2) | Y |  | 盈亏 |

---

## 357. dimple.tc_nb_account_shfe　(9 字段)
> 表含义：宁波银行-上期所标准仓单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(3) | Y |  | 交易所代码 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| variety_id | varchar(8) | Y |  | 品种名称 |
| amt | numeric(18,2) | Y |  | 金额 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| avg_carry | numeric(18,2) | Y |  | 成交额 |
| contract_id | varchar(20) | Y |  | 合约号 |
| io_type | varchar(3) | Y |  | 性质：1-交易所调拨、2-出库 |

---

## 358. dimple.tc_nb_accounting　(13 字段)
> 表含义：宁波银行-账务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| seq_no | varchar(30) | Y |  | 流水号 |
| currency | varchar(10) | Y |  | 币种 |
| borrow_account | varchar(50) | Y |  | 借方账户 |
| borrow_type | varchar(20) | Y |  | 借方科目 |
| lend_account | varchar(50) | Y |  | 贷方账户 |
| lend_type | varchar(20) | Y |  | 贷方科目 |
| amt | varchar(40) | Y |  | 发生额 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| bus_type | varchar(30) | Y |  | 业务大类 |
| system_event | varchar(50) | Y |  | 事件 |
| description | varchar(100) | Y |  | 描述 |
| remark | varchar(500) | Y |  | 备注 |

---

## 359. dimple.tc_nb_accout_spot　(19 字段)
> 表含义：黄金现货账务中间表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 结算日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 库存量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| avg_carry | numeric(18,2) | Y |  | 加权平均成本 |
| trans_type | varchar(3) | Y |  | 库存变化类型 |
| last_remain_qty | numeric(18,2) | Y |  | 前剩余库存 |
| remain_qty | numeric(18,2) | Y |  | 剩余库存 |
| price | numeric(24,6) | Y |  | 成交价 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| trade_type | varchar(3) | Y |  | 市场类型 |
| variety_id | varchar(4) | Y |  | 品种 |
| last_weighted_price | numeric(20,8) | Y |  | 前加权平均价 |
| remain_cost | numeric(24,6) | Y |  | 成本 |
| last_remain_cost | numeric(24,6) | Y |  | 前成本 |
| realized_profitloss | numeric(24,6) | Y |  | 盈亏 |

---

## 360. dimple.tc_nb_bond_manage　(11 字段)
> 表含义：宁波银行-债券管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | varchar(20) | Y |  | 流水号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| trader_no | varchar(30) | Y |  | 席位号 |
| bs_flag | varchar(3) | Y |  | 买卖方向 |
| bond_id | varchar(10) | Y |  | 债券代码 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| amount | numeric(18,2) | Y |  | 金额 |
| value_date | varchar(8) | Y |  | 起息日 |
| settle_date | varchar(8) | Y |  | 到期日 |

---

## 361. dimple.tc_nb_bond_match　(14 字段)
> 表含义：宁波银行-债券成交单表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | varchar(20) | N | √ | 流水号 |
| exch_code | varchar(10) | N | √ | 交易所代码 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| trader_no | varchar(16) | Y |  | 席位号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| bond_id | varchar(10) | N | √ | 债券代码 |
| price | numeric(20,8) | Y |  | 成交价格 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| amout | numeric(18,2) | Y |  | 金额 |
| value_date | varchar(8) | Y |  | 起息日 |
| settle_date | varchar(8) | Y |  | 到期日 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |

---

## 362. dimple.tc_nb_clear_price　(8 字段)
> 表含义：宁波银行QUOT结算价表　|　估算行数：**15,271**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(10) | N | √ | 交易日期 |
| exch_code | varchar(10) | N |  | 交易所代码 |
| contract_id | varchar(40) | N | √ | 合约 |
| delivery_month | varchar(10) | N | √ | 交割月 |
| clear_price | numeric(20,8) | N |  | 结算价 |
| status | varchar(3) | Y |  | 状态:0未发送；1 成功；2失败 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 363. dimple.tc_nb_fee_detail　(17 字段)
> 表含义：宁波银行-费用明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| fee | numeric(18,2) | Y |  | 手续费 |
| storage_fee | numeric(18,2) | Y |  | 仓储费 |
| trans_fee | numeric(18,2) | Y |  | 运保费 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| overdue_fee | numeric(18,2) | Y |  | 超期费 |
| zyredist_fee | numeric(18,2) | Y |  | 质押登记费 |
| lendregist_fee | numeric(18,2) | Y |  | 租赁登记费 |
| break_fee | numeric(18,2) | Y |  | 违约金 |
| delay_fee | numeric(18,2) | Y |  | 滞纳金 |
| fine | numeric(18,2) | Y |  | 罚款 |
| interest | numeric(18,2) | Y |  | 利息 |
| w_premium | numeric(18,2) | Y |  | 重量溢短 |
| amount | numeric(18,2) | Y |  | 费用合计 |
| ohter_fee | numeric(18,2) | Y |  | 其他费用 |
| ag_premium | numeric(18,2) | Y |  | 白银差价款 |

---

## 364. dimple.tc_nb_his_account_ag　(9 字段)
> 表含义：宁波银行-白银远期业务历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖 |
| qty | numeric(18,2) | Y |  | 成交量(克) |
| price | numeric(20,8) | Y |  | 成交价 |
| turnover | numeric(18,2) | Y |  | 成交金额 |
| clear_price | numeric(20,8) | Y |  | 收盘价 |
| profit | numeric(18,2) | Y |  | 盈亏 |

---

## 365. dimple.tc_nb_his_account_defer　(9 字段)
> 表含义：宁波银行-账务递延买卖表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |

---

## 366. dimple.tc_nb_his_account_future　(9 字段)
> 表含义：宁波银行-账务债券期货业务　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |

---

## 367. dimple.tc_nb_his_account_lend　(5 字段)
> 表含义：宁波银行-黄金租赁业务历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| trans_type | varchar(2) | Y |  | 库存变化类型 |
| delivery_variety_id | varchar(3) | Y |  | 交割品 |
| lend_qty | numeric(16,3) | Y |  | 租借量（克） |
| sheet_no | varchar(20) | Y |  | 租借登记编号 |

---

## 368. dimple.tc_nb_his_account_priceing　(9 字段)
> 表含义：宁波银行-定价金业务历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖 |
| qty | numeric(18,2) | Y |  | 成交量(克) |
| price | numeric(20,8) | Y |  | 成交价 |
| turnover | numeric(18,2) | Y |  | 成交金额 |
| clear_price | numeric(20,8) | Y |  | 收盘价 |
| profit | numeric(18,2) | Y |  | 盈亏 |

---

## 369. dimple.tc_nb_his_account_shfe　(9 字段)
> 表含义：宁波银行-上期所标准仓单历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(3) | Y |  | 交易所代码 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| variety_id | varchar(8) | Y |  | 品种名称 |
| amt | numeric(18,2) | Y |  | 金额 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| avg_carry | numeric(18,2) | Y |  | 成交额 |
| contract_id | varchar(20) | Y |  | 合约号 |
| io_type | varchar(3) | Y |  | 性质：1-交易所调拨、2-出库 |

---

## 370. dimple.tc_nb_his_accounting　(14 字段)
> 表含义：宁波银行-账务历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| batch_no | float8 | Y |  | 批次号 |
| seq_no | varchar(30) | Y |  | 流水号 |
| currency | varchar(10) | Y |  | 币种 |
| borrow_account | varchar(50) | Y |  | 借方账户 |
| borrow_type | varchar(20) | Y |  | 借方科目 |
| lend_account | varchar(50) | Y |  | 贷方账户 |
| lend_type | varchar(20) | Y |  | 贷方科目 |
| amt | varchar(40) | Y |  | 发生额 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| bus_type | varchar(30) | Y |  | 业务大类 |
| system_event | varchar(50) | Y |  | 事件 |
| description | varchar(100) | Y |  | 描述 |
| remark | varchar(500) | Y |  | 备注 |

---

## 371. dimple.tc_nb_his_accout_spot　(8 字段)
> 表含义：黄金现货账务中间表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 结算日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 库存量（克） |
| turnover | numeric(18,2) | Y |  | 加权平均价 |
| avg_carry | numeric(18,2) | Y |  | 收盘价 |
| trans_type | varchar(3) | Y |  | 库存变化类型 |

---

## 372. dimple.tc_nb_lend_match　(13 字段)
> 表含义：宁波银行-黄金租赁表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| apply_flag | varchar(3) | N |  | 申报方 |
| delivery_variety_id | varchar(3) | N |  | 交割品 |
| effect_date | varchar(8) | Y |  | 申报日期 |
| expire_date | varchar(8) | Y |  | 租借到期日 |
| delivery_rate | numeric(16,2) | Y |  | 利率 |
| delivery_num | numeric(16,2) | Y |  | 金额 |
| lender_name | varchar(10) | Y |  | 交易对手方简称 |
| trader_no | varchar(16) | Y |  | 交易员 |
| seq_no | numeric(10,0) | Y |  | 租借物明细流水 |
| agreement_sn | varchar(20) | N |  | 租借合约编号 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |

---

## 373. dimple.tc_nb_match　(20 字段)
> 表含义：宁波银行-spot、future成交单表　|　估算行数：**53**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交单 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(10) | N | √ | 交易所代码 |
| contract_id | varchar(20) | N | √ | 合约 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| eo_flag | varchar(3) | Y |  | 开平标志 |
| price | numeric(20,8) | Y |  | 成交价格 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| amout | numeric(18,2) | Y |  | 金额 |
| trader_no | varchar(16) | N | √ | 席位号 |
| match_type | varchar(3) | N | √ | 成交类型：1 spot;2 future |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| status | varchar(6) | Y |  | 状态：0未发送；1 成功；2失败 |
| remark | varchar(500) | Y |  | 备注 |
| valuedata | varchar(16) | Y |  | 到期日:1、上海金、白银现货即期T+2日,现货、递延交割库存流水都是当前交易日 |
| member_id | varchar(8) | N | √ | 会员号/席位号 |
| eo_flagdetail | varchar(3) | Y |  | 开平明细:见tp_public_dict的003 |
| sh_flag | varchar(3) | Y |  | 投保标志 |
| summit_no | varchar(20) | Y |  | 推送编号 |
| trade_time | varchar(8) | Y |  | 交易时间 |

---

## 374. dimple.tc_nb_match_group　(11 字段)
> 表含义：宁波银行summit推送批次表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| summit_no | varchar(20) | N | √ | 推送编号 |
| summit_date | varchar(8) | Y |  | 推送日期 |
| summit_time | varchar(8) | Y |  | 推送时间 |
| trader_no | varchar(16) | Y |  | 席位号 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| bs_flag | varchar(3) | Y |  | 买卖标签 |
| eo_flag | varchar(3) | Y |  | 开平标志 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| amount | numeric(18,2) | Y |  | 数额 |
| remark | varchar(500) | Y |  | 备注 |

---

## 375. dimple.tc_nb_money　(9 字段)
> 表含义：宁波银行-日终资金信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(10) | N |  | 交易日期 |
| member_id | varchar(10) | N |  | 会员号 |
| exch_code | varchar(4) | N |  | 交易所 |
| margin | numeric(18,2) | Y |  | 当日占用保证金 |
| frozen_margin | numeric(18,2) | Y |  | 冻结保证金 |
| remain | numeric(18,2) | Y |  | 当日结算准备金余额 |
| status | varchar(3) | Y |  | 状态:0未发送；1 成功；2失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 376. dimple.tc_nb_moneydetail　(8 字段)
> 表含义：宁波银行-日终资金明细信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(10) | N |  | 交易日期 |
| member_id | varchar(10) | N |  | 会员号 |
| exch_code | varchar(4) | N |  | 交易所 |
| fee_type | varchar(22) | N |  | 费用类型 |
| amount | numeric(18,2) | Y |  | 金额 |
| status | varchar(3) | Y |  | 状态:0未发送；1 成功；2失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |

---

## 377. dimple.tc_nb_rfqo_match　(61 字段)
> 表含义：宁波银行RFQO推送表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| summit_status | varchar(8) | Y |  | 推送状态:0未发送；1 成功；2失败 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| summit_remark | varchar(500) | Y |  | 备注 |
| match_no | varchar(24) | Y |  | 成交单编号 |
| apply_date | varchar(8) | Y |  | 自然日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| otc_reg_confirm_time | varchar(21) | Y |  | 登记时间 |
| offline_match_date | varchar(8) | Y |  | 线下成交日期 |
| member_id | varchar(6) | Y |  | 本方会员号 |
| seat_id | varchar(6) | Y |  | 本方席位号 |
| client_id | varchar(12) | Y |  | 本方客户号 |
| client_abbr | varchar(20) | Y |  | 本方客户简称 |
| client_eabbr | varchar(20) | Y |  | 本方客户英文简称 |
| broker_id | varchar(10) | Y |  | 本方经纪机构代码 |
| otc_broker_user_id | varchar(20) | Y |  | 本方经纪机构用户 |
| role | varchar(6) | Y |  | 本方席位角色 |
| partner_member_id | varchar(6) | Y |  | 对手方会员号 |
| partner_seat_id | varchar(6) | Y |  | 对手方席位号 |
| partner_trader_id | varchar(10) | Y |  | 对手方交易员代码 |
| partner_client_id | varchar(12) | Y |  | 对手方客户号 |
| partner_client_abbr | varchar(20) | Y |  | 对手方客户简称 |
| partner_client_eabbr | varchar(20) | Y |  | 对手方客户英文简称 |
| partner_broker_id | varchar(10) | Y |  | 对手方经纪机构代码 |
| partner_otc_broker_user_id | varchar(20) | Y |  | 对手方经纪机构用户 |
| partner_source | varchar(1) | Y |  | 对手方渠道代码 |
| partner_role | varchar(6) | Y |  | 对手方席位角色1-maker，2-taker |
| inst_id | varchar(8) | Y |  | 合约代码 |
| trade_or_registe | varchar(1) | Y |  | 交易/登记:1-交易，2-登记 |
| exe_type | varchar(1) | Y |  | 行权方式 |
| option_type | varchar(1) | Y |  | 期权类型 |
| inst_unit | numeric(12,6) | Y |  | 交易单位数量 |
| trade_volume | float8 | Y |  | 数量 |
| otc_std_weight | numeric(18,6) | Y |  | 发生标准重量 |
| period | varchar(10) | Y |  | 期限 |
| price_unit | varchar(1) | Y |  | 权利金和行权价报价单位 |
| price | numeric(24,8) | Y |  | 行权价 |
| exe_date | varchar(8) | Y |  | 行权日 |
| otc_exercise_time | varchar(8) | Y |  | 行权截止时间 |
| actual_exercise_date | varchar(8) | Y |  | 实际行权日 |
| contract_period | varchar(2) | Y |  | 实物交割标的合约期限 |
| settle_accounts_date | varchar(8) | Y |  | 结算日 |
| actual_interest_date | varchar(8) | Y |  | 实际结算日 |
| option_money | numeric(24,8) | Y |  | 权利金 |
| option_paydate | varchar(8) | Y |  | 权利金支付日 |
| actual_option_paydate | varchar(8) | Y |  | 实际权利金支付日 |
| settle_accounts_type | varchar(1) | Y |  | 结算方式 |
| ref_price_type | varchar(8) | Y |  | 现金结算期权参考价格类型 |
| ref_price_updown | numeric(12,6) | Y |  | 现金结算期权参考价格调整项 |
| warehouse_id | varchar(4) | Y |  | 指定仓库 |
| otc_remark | varchar(256) | Y |  | 信用型询价附加条款 |
| trader_no | varchar(10) | Y |  | 发起方交易员 |
| institution_id | varchar(10) | Y |  | 发起方交易席位 |
| trade_type | varchar(3) | Y |  | 交易类型 |
| bs_flag | varchar(3) | Y |  | 发起方交易方向:1-买，2-卖 |
| weight | numeric(18,6) | Y |  | 重量 |
| registe_state | varchar(1) | Y |  | 登记状态8-SGE确认成功 |
| remark | varchar(256) | Y |  | 备注 |
| notional_principal | numeric(24,6) | Y |  | 名义本金 |
| reg_summit | varchar(1) | Y |  | 登记提交方:1-本方，2-对手方 |
| trade_init_mode | varchar(1) | Y |  | 报价类型 |

---

## 378. dimple.tc_nb_rfqsfs_match　(61 字段)
> 表含义：宁波银行RFQSFS推送表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| summit_status | varchar(8) | Y |  | 推送状态:0未发送；1 成功；2失败 |
| return_status | varchar(6) | Y |  | 返回状态：pgshine返回状态 |
| summit_remark | varchar(500) | Y |  | 备注 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| match_no | varchar(20) | Y |  | 成交单号 |
| match_type | varchar(3) | Y |  | 业务类型:0-即期 1-远期 2-掉期 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| member_id | varchar(8) | Y |  | 会员席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | Y |  | 买卖标志:1-买，3-卖 |
| currency_buy | varchar(8) | Y |  | 买入币种，若为掉期，为近端币种 |
| num_buy | numeric(24,6) | Y |  | 买入量，若为掉期，为近端买入量 |
| currency_sell | varchar(8) | Y |  | 卖出币种，若为掉期，为近端卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量，若为掉期，为近端卖出量 |
| price | numeric(20,8) | Y |  | 成交价格，若为掉期，为近端成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日，若为掉期，为近端起息日 |
| reference_type | varchar(3) | Y |  | 参考价类型，若为掉期，为近端参考价类型 |
| reference_date | varchar(8) | Y |  | 参考价日期，若为掉期，为近端参考价日期 |
| reference_price | numeric(20,8) | Y |  | 参考价格，若为掉期，为近端参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项，若为掉期，为近端参考价格调整项 |
| currency_buy_farleg | varchar(8) | Y |  | 掉期远端币种 |
| num_buy_farleg | numeric(24,6) | Y |  | 掉期远端买入量 |
| currency_sell_farleg | varchar(8) | Y |  | 掉期远端卖出币种 |
| num_sell_farleg | numeric(24,6) | Y |  | 掉期远端卖出量 |
| price_farleg | numeric(20,8) | Y |  | 掉期远端成交价格 |
| due_date_farleg | varchar(8) | Y |  | 掉期远端起息日 |
| reference_type_farleg | varchar(3) | Y |  | 掉期远端参考价类型 |
| reference_date_farleg | varchar(8) | Y |  | 掉期远端参考价日期 |
| reference_price_farleg | numeric(20,8) | Y |  | 掉期远端参考价格 |
| reference_adjust_farleg | numeric(20,8) | Y |  | 掉期远端参考价格调整项 |
| delivery_type | varchar(3) | Y |  | 交割方式 |
| sys_inquire_status | varchar(3) | Y |  | 系统询价状态:8-SGE确认成功 |
| inquire_type | varchar(3) | Y |  | 询价类型 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| role | varchar(4) | Y |  | 本方角色，1-maker，2-taker |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| party_role | varchar(4) | Y |  | 对手方角色，1-maker，2-taker |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| trade_reg | varchar(4) | Y |  | 交易/登记：1-交易，2-登记 |
| related_match_no | varchar(20) | Y |  | 相关成交单号 |
| period | varchar(10) | Y |  | 期限 |
| price_unit | varchar(4) | Y |  | 报价单位 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金:0-否，1-是 |
| storage_no | varchar(4) | Y |  | 指定仓库代码,白银合约时字段有值 |
| trade_volume | numeric(16,0) | Y |  | 交易手数 |
| refprice_info | varchar(50) | Y |  | 其他参考价格说明 |
| remark | varchar(254) | Y |  | 附加条款 |
| party_member_id | varchar(8) | Y |  | 对手方席位号 |
| mmb_id | varchar(8) | Y |  | 本方会员号 |
| party_mmb_id | varchar(8) | Y |  | 对手方会员号 |
| client_broker | varchar(20) | Y |  | 本方经纪机构用户 |
| party_client_broker | varchar(20) | Y |  | 对手方经纪机构用户 |
| unit | numeric(12,6) | Y |  | 交易单位 |
| member_type | varchar(1) | Y |  | 本方会员类型 |
| party_member_type | varchar(1) | Y |  | 对手方会员类型 |
| exch_trader_no | varchar(15) | Y |  | 交易所本方交易员代码 |
| weight | numeric(24,6) | Y |  | 重量 |
| trade_time | varchar(8) | Y |  | 交易时间 |

---

## 379. dimple.tc_nb_risk_recalc_bond　(9 字段)
> 表含义：宁波日终重估业务-国债　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(18,2) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(18,2) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 380. dimple.tc_nb_risk_recalc_defer　(9 字段)
> 表含义：宁波日终重估业务-递延　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 381. dimple.tc_nb_risk_recalc_future　(9 字段)
> 表含义：宁波日终重估业务-国债　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 382. dimple.tc_nb_risk_recalc_shfe　(8 字段)
> 表含义：宁波日终重估业务-上期所仓单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| variety_id | varchar(8) | Y |  | 品种代码 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| turnover | numeric(20,8) | Y |  | 成本 |
| qty | numeric(12,0) | Y |  | 数量（克） |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 383. dimple.tc_nb_risk_recalc_spot　(6 字段)
> 表含义：宁波日终重估业务-现货　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(12,0) | Y |  | 库存量（克） |
| avg_price | numeric(20,8) | Y |  | 加权平均价 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 384. dimple.tc_nb_roledetail　(8 字段)
> 表含义：宁波银行-日终本方角色信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 询价成交单号 |
| role | varchar(8) | Y |  | 本方角色：1 Maker;2 Taker |
| status | varchar(3) | Y |  | 状态:0未发送；1 成功；2失败 |
| return_status | varchar(6) | Y |  | 返回状态 |
| remark | varchar(500) | Y |  | 备注 |
| trade_date | varchar(10) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |

---

## 385. dimple.tc_not_perf_client_posi_clear　(17 字段)
> 表含义：客户非优惠组合持仓结算表　|　估算行数：**30,414**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号:各腿的合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见t_public_code的004 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| exch_buy_margin | numeric(18,2) | Y |  | 交易所买保证金 |
| exch_sell_margin | numeric(18,2) | Y |  | 交易所卖保证金 |
| buy_margin | numeric(18,2) | Y |  | 买保证金：考虑大边 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金：考虑大边 |
| ftr_clear_price | numeric(18,2) | Y |  | 期货结算价 |
| opt_clear_price | numeric(18,2) | Y |  | 期权结算价 |
| group_no | numeric(10,0) | Y |  | 组合代码 |
| largeside_flag | bpchar(1) | Y |  | 大边方向:见tp_public_dict的002 |
| discount_amount | numeric(18,2) | Y |  | 保证金优惠金额 |

---

## 386. dimple.tc_offset_profitloss　(15 字段)
> 表含义：期货平仓盈亏表:日终结算产生，利用此表计算平仓盈亏。
 如果平仓日期＝开仓日期：
  卖平：盯市平仓盈亏＝（平仓价－开仓价）×平仓手数×每手数量
  买平：盯市平仓盈亏＝（开仓价－平仓价）×平仓手数×每手数量
 如果平仓日期 小于 开仓日期：
  卖平：盯市平仓盈亏＝（平仓价－昨结算价）×平仓手数×每手数量
  买平：盯市平仓盈亏＝（昨结算价－平仓价）×平仓手数×每手数量　|　估算行数：**186,721**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| offset_type | varchar(2) | Y |  | 平仓类型:见tp_public_dict的179 |
| match_no | varchar(20) | Y |  | 成交号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |

---

## 387. dimple.tc_offset_profitloss_purpose　(15 字段)
> 表含义：交易目的期货平仓盈亏表:日终结算产生，利用此表计算平仓盈亏。
 如果平仓日期＝开仓日期：
  卖平：盯市平仓盈亏＝（平仓价－开仓价）×平仓手数×每手数量
  买平：盯市平仓盈亏＝（开仓价－平仓价）×平仓手数×每手数量
 如果平仓日期 小于 开仓日期：
  卖平：盯市平仓盈亏＝（平仓价－昨结算价）×平仓手数×每手数量
  买平：盯市平仓盈亏＝（昨结算价－平仓价）×平仓手数×每手数量　|　估算行数：**75,198**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| offset_type | varchar(2) | Y |  | 平仓类型:见tp_public_dict的179 |
| match_no | varchar(20) | Y |  | 成交号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 388. dimple.tc_offset_profitloss_trader　(16 字段)
> 表含义：交易员期货平仓盈亏表:日终结算产生，利用此表计算平仓盈亏。
 如果平仓日期＝开仓日期：
  卖平：盯市平仓盈亏＝（平仓价－开仓价）×平仓手数×每手数量
  买平：盯市平仓盈亏＝（开仓价－平仓价）×平仓手数×每手数量
 如果平仓日期 小于 开仓日期：
  卖平：盯市平仓盈亏＝（平仓价－昨结算价）×平仓手数×每手数量
  买平：盯市平仓盈亏＝（昨结算价－平仓价）×平仓手数×每手数量　|　估算行数：**510,906**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| offset_type | varchar(2) | Y |  | 平仓类型:见tp_public_dict的179 |
| match_no | varchar(20) | Y |  | 成交号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 389. dimple.tc_opt_client_posi_clear　(23 字段)
> 表含义：期权结算持仓表:日终结算时计算，也是次日持仓初始数据的来源。　|　估算行数：**8,626**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(30) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量＋非持仓变动变动引起的量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:即今日买开仓权利金支出:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:即今日卖开仓权利金收入:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:即今日买平仓权利金支出:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:即今日卖平仓权利金收入:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| premium_out | numeric(19,2) | Y |  | 权利金支出 |
| premium_in | numeric(19,2) | Y |  | 权利金收入 |
| sell_margin | numeric(19,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 390. dimple.tc_opt_offset_profitloss　(11 字段)
> 表含义：期权平仓表　|　估算行数：**78**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| match_no | varchar(20) | Y |  | 平仓成交号 |

---

## 391. dimple.tc_opt_offset_purpose　(12 字段)
> 表含义：交易目的期权平仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| match_no | varchar(20) | Y |  | 平仓成交号 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 392. dimple.tc_opt_offset_trader　(13 字段)
> 表含义：交易员期权平仓表　|　估算行数：**78**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| match_no | varchar(20) | Y |  | 平仓成交号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 393. dimple.tc_opt_posi_detail　(11 字段)
> 表含义：期权结算持仓明细表　|　估算行数：**32,609**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(30) | N | √ | 合约号 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 394. dimple.tc_opt_posi_detail_purpose　(12 字段)
> 表含义：交易目的期权结算持仓明细表　|　估算行数：**18,285**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 395. dimple.tc_opt_posi_detail_trader　(13 字段)
> 表含义：交易员期权结算持仓明细表　|　估算行数：**17,736**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 396. dimple.tc_opt_purpose_posi_clear　(24 字段)
> 表含义：交易目的期权结算持仓表:日终结算时计算，也是次日持仓初始数据的来源。　|　估算行数：**2,589**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量＋非持仓变动变动引起的量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| premium_out | numeric(19,2) | Y |  | 权利金支出 |
| premium_in | numeric(19,2) | Y |  | 权利金收入 |
| sell_margin | numeric(19,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 397. dimple.tc_opt_trader_posi_clear　(25 字段)
> 表含义：交易员期权结算持仓表:日终结算时计算，也是次日持仓初始数据的来源。　|　估算行数：**2,140**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量＋非持仓变动变动引起的量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| premium_out | numeric(19,2) | Y |  | 权利金支出 |
| premium_in | numeric(19,2) | Y |  | 权利金收入 |
| sell_margin | numeric(19,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 398. dimple.tc_order_command_detail　(19 字段)
> 表含义：交易指令集明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| invest_plan_id | varchar(20) | N | √ | 投资计划编号 |
| order_command_id | varchar(20) | Y |  | 交易指令集编号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| trade_purpose | varchar(10) | N |  | 交易目的代码 |
| contract_id1 | varchar(20) | N |  | 合约代码1 |
| contract_id2 | varchar(20) | N |  | 合约代码2, 0表示无合约 |
| trade_direction | varchar(3) | N |  | 交易方向 dict-484 |
| low_limit | numeric(24,8) | Y |  | 最低价格 最低价差 |
| high_limit | numeric(24,8) | Y |  | 最高价格 最高价差 |
| invest_amount | numeric(30,8) | N |  | 投资额度（元） |
| check_status | varchar(3) | N |  | 复核状态 dict-481 |
| term | varchar(10) | Y |  | 期限 |
| gen_user | varchar(50) | Y |  | 指令生成人员 |
| gen_date | varchar(8) | Y |  | 指令生成日期 |
| gen_time | varchar(8) | Y |  | 指令生成时间 |
| check_user | varchar(50) | Y |  | 指令复核人员 |
| check_date | varchar(8) | Y |  | 指令复核日期 |
| check_time | varchar(8) | Y |  | 指令复核时间 |

---

## 399. dimple.tc_order_command_total　(16 字段)
> 表含义：交易指令集汇总交易额度表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| strategy_no | varchar(8) | N | √ | 投资策略编号 |
| member_id | varchar(8) | N |  | 席位代码 |
| trade_purpose | varchar(10) | N |  | 交易目的代码 |
| contract_id1 | varchar(20) | N |  | 合约代码1 |
| contract_id2 | varchar(20) | N |  | 合约代码2, 0表示无合约 |
| trade_direction | varchar(3) | N |  | 交易方向 dict-484 |
| low_limit | numeric(24,8) | Y |  | 最低价格 最低价差 |
| high_limit | numeric(24,8) | Y |  | 最高价格 最高价差 |
| invest_amount_total | numeric(30,8) | N |  | 当日总投资额度（元） |
| invest_amount_used | numeric(30,8) | Y |  | 占用投资额度（元） |
| invest_amount_frozen | numeric(30,8) | Y |  | 冻结投资额度（元） |
| term | varchar(10) | Y |  | 期限 |
| gen_date | varchar(8) | Y |  | 额度生成日期 |
| gen_time | varchar(8) | Y |  | 额度生成时间 |
| status | varchar(1) | Y |  | 上场状态，见tp_public_dict的510 |

---

## 400. dimple.tc_order_machine_failover　(8 字段)
> 表含义：报盘机双活机制维护表　|　估算行数：**24**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 席位号 |
| record_timestamp | timestamp | Y |  | 记录的时间戳 |
| max_trader_count | numeric(12,0) | N |  | 最大允许接入交易员数 |
| ip_address | varchar(64) | Y |  | ip地址 |
| trader_no | varchar(10) | N | √ | 交易员编号 |
| order_machine_type | varchar(4) | N | √ | 报盘机种类(金交所竞价--01，金交所仓储--02，金交所信用询价--03，金交所保证金询价--04，金交所定价--05，上期所竞价--06，上期所行情--07，Etf--08，金交所国际报盘--09)，同步写种类(synwrite--99) |
| machine_id | varchar(64) | N |  | 报盘机设备号 |
| remarks | varchar(128) | Y |  | 备注信息 |

---

## 401. dimple.tc_order_manage_jour　(6 字段)
> 表含义：成交目的管理流水表(主要存放强减记录的流水)　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| order_no | varchar(20) | N | √ | 委托号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| contract_id | varchar(20) | N | √ | 合约 |
| rule_flag | bpchar(1) | N | √ | 是否强减 |
| order_sort | varchar(2) | N |  | 定单类别:见tp_public_dict的005 |

---

## 402. dimple.tc_origin_match　(20 字段)
> 表含义：原始成交表　|　估算行数：**712,583**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N | √ | 撮合号 |
| bs_flag | varchar(20) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| member_name | varchar(80) | Y |  | 会员名称 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(30) | Y |  | 合约号 |
| qty | numeric(12,0) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 价格 |
| turnover | numeric(19,2) | Y |  | 成交额 |
| match_time | varchar(12) | Y |  | 成交时间 |
| eo_flag | varchar(20) | Y |  | 开平标志 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| sh_flag | varchar(20) | N |  | 投保标志:见tp_public_dict的004 |
| operator_id | varchar(20) | Y |  | 操作员 |
| checker_id | varchar(20) | Y |  | 复核员 |
| if_checked | varchar(3) | Y |  | 复核标志 |
| bus_type | varchar(2) | Y |  | 业务类型:见tp_public_dict的358 |

---

## 403. dimple.tc_origin_money　(75 字段)
> 表含义：原始资金表　|　估算行数：**3,163**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| clear_account_no | varchar(14) | N | √ | 结算子帐号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| currency | varchar(2) | N | √ | 币种 |
| last_remain | numeric(19,2) | Y |  | 上期所：上日实有货币资金余额；金交所：上日结算准备金余额 |
| recv_money | numeric(19,2) | Y |  | 当日收入资金 |
| profitloss | numeric(19,2) | Y |  | 当日盈亏 |
| pay_money | numeric(19,2) | Y |  | 当日付出资金 |
| fee | numeric(19,2) | Y |  | 手续费 |
| trade_fee | numeric(19,2) | Y |  | 交易手续费 |
| clear_fee | numeric(19,2) | Y |  | 结算手续费 |
| delivery_fee | numeric(19,2) | Y |  | 交割手续费 |
| move_posi_fee | numeric(19,2) | Y |  | 移仓手续费 |
| deposit | numeric(19,2) | Y |  | 当日实有货币资金余额：上期所、金交所 |
| margin | numeric(19,2) | Y |  | 交易保证金：货币加额度 |
| remain | numeric(19,2) | Y |  | 结算准备金；金交所：当日结算准备金余额 |
| money_in | numeric(19,2) | Y |  | 申报划入金额 |
| money_out | numeric(19,2) | Y |  | 申报划出金额 |
| prepare_margin | numeric(19,2) | Y |  | 开仓准备金 |
| pay_fee | numeric(19,2) | Y |  | 支付手续费 |
| deposit_chg | numeric(19,2) | Y |  | 实有货币资金变动 |
| margin_chg | numeric(19,2) | Y |  | 交易保证金变动 |
| remain_chg | numeric(19,2) | Y |  | 结算准备金变动 |
| if_cmp | varchar(2) | Y |  | 币种 |
| right_valid | numeric(19,2) | Y |  | 权利凭证实际可用金额 |
| right_used | numeric(19,2) | Y |  | 权利凭证实际占用 |
| spec_margin | numeric(19,2) | Y |  | 投机头寸保证金 |
| hedge_margin | numeric(19,2) | Y |  | 保值头寸保证金 |
| delivery_margin | numeric(19,2) | Y |  | 交割头寸保证金 |
| free_trade_fee | numeric(19,2) | Y |  | 减免交易手续费 |
| mate_money | numeric(19,2) | Y |  | 最大配比金额 |
| right_off_money | numeric(19,2) | Y |  | 权利凭证折后金额 |
| buy_amount | numeric(19,2) | Y |  | 买货款 |
| sell_amount | numeric(19,2) | Y |  | 卖货款 |
| call_margin | numeric(19,2) | Y |  | 追加保证金 |
| other_money | numeric(19,2) | Y |  | 其他费用 |
| reserve | numeric(19,2) | Y |  | 利息 |
| last_balance | numeric(19,2) | Y |  | 上日结算准备金余额 |
| last_frozen_margin | numeric(19,2) | Y |  | 上日占用保证金 |
| last_base_margin | numeric(19,2) | Y |  | 上日基础保证金 |
| forzen_margin | numeric(19,2) | Y |  | 当日占用保证金 |
| base_margin | numeric(19,2) | Y |  | 当日基础保证金 |
| frozen_profitloss | numeric(19,2) | Y |  | 当日远期盈亏冻结 |
| pt_frozen_amount | numeric(19,2) | Y |  | 当日铂金冻结金额 |
| ag_frozen_amount | numeric(19,2) | Y |  | 当日白银冻结金额 |
| manual_frozen_amount | numeric(19,2) | Y |  | 当日手工冻结金额 |
| last_frozen_profitloss | numeric(19,2) | Y |  | 上日盈亏冻结 |
| last_frozen_amount | numeric(19,2) | Y |  | 上日货款冻结 |
| last_delivery_margin | numeric(19,2) | Y |  | 上日交割保证金 |
| trade_margin | numeric(19,2) | Y |  | 交易保证金 |
| trade_posi_margin | numeric(19,2) | Y |  | 交易持仓保证金 |
| trade_deli_margin | numeric(19,2) | Y |  | 交易交割保证金 |
| last_trights | numeric(19,2) | Y |  | 上日总权益 |
| total_rights | numeric(19,2) | Y |  | 总权益 |
| last_deposit | numeric(19,2) | Y |  | 上日实有货币资金：金交所 |
| setoff_out_limit | numeric(19,2) | Y |  | 充抵出金限制金额：金交所 |
| last_setoff_quota | numeric(19,2) | Y |  | 上日实际充抵额度：金交所 |
| setoff_quota | numeric(19,2) | Y |  | 当日实际充抵额度：金交所 |
| last_setoff_usedquota | numeric(19,2) | Y |  | 上日已用充抵额度：金交所 |
| setoff_usedquota | numeric(19,2) | Y |  | 当日已用充抵额度：金交所 |
| setoff_avaliablequota | numeric(19,2) | Y |  | 当日剩余充抵额度：金交所 |
| last_cash_occupied | numeric(19,2) | Y |  | 上日货币交易保证金占用：金交所 |
| cash_occupied | numeric(19,2) | Y |  | 当日货币交易保证金占用：金交所 |
| last_quota_occupied | numeric(19,2) | Y |  | 上日额度交易保证金占用：金交所 |
| quota_occupied | numeric(19,2) | Y |  | 当日额度交易保证金占用：金交所 |
| last_cash_balance | numeric(19,2) | Y |  | 上日货币交易可报价余额：金交所 |
| cash_balance | numeric(19,2) | Y |  | 当日货币交易可报价余额：金交所 |
| last_quota_balance | numeric(19,2) | Y |  | 上日额度交易可报价余额：金交所 |
| quota_balance | numeric(19,2) | Y |  | 当日额度交易可报价余额：金交所 |
| available | numeric(19,2) | Y |  | 当日可提资金：金交所 |
| last_available | numeric(19,2) | Y |  | 上日可提资金：金交所 |
| opt_total_amt | numeric(19,2) | Y |  | 当日总期权权利金：上期所 |
| law_last_forzen_amt | numeric(19,2) | Y |  | 上日司法冻结金额 |
| law_forzen_amt | numeric(19,2) | Y |  | 当日司法冻结金额 |

---

## 404. dimple.tc_origin_posi　(19 字段)
> 表含义：原始持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_turnover | numeric(18,2) | Y |  | 今日买成交额 |
| sell_turnover | numeric(18,2) | Y |  | 今日卖成交额 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| margin | numeric(18,2) | Y |  | 交易保证金 |
| profitloss | numeric(18,2) | Y |  | 当日盈亏 |
| fee | numeric(18,2) | Y |  | 手续费 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| sh_flag | varchar(20) | N |  | 投保标志:见tp_public_dict的004 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |

---

## 405. dimple.tc_other_fee　(8 字段)
> 表含义：其他费率表　|　估算行数：**69**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| fee_type | bpchar(1) | N | √ | 手续费类型:见tp_public_dict的092 |
| fee_kind | varchar(8) | N | √ | 费率类型:见tp_public_dict的354 |
| fee_rate | numeric(22,6) | N |  | 费率 |

---

## 406. dimple.tc_other_fee_list　(6 字段)
> 表含义：其他费率表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| fee_type | bpchar(1) | N | √ | 手续费类型:见tp_public_dict的092 |
| fee_kind | varchar(8) | N | √ | 费率类型:见tp_public_dict的354 |
| fee_rate | numeric(22,6) | N |  | 费率 |

---

## 407. dimple.tc_overdue_fee_rate　(12 字段)
> 表含义：超期费率表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | varchar(12) | N | √ | 序号 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| day_count | float8 | Y |  | 天数 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| day_min | float8 | Y |  | 最小持仓天数 |
| day_max | float8 | Y |  | 最大持仓天数 |
| create_date | varchar(8) | Y |  | 新增日期 |
| creater | varchar(40) | Y |  | 新增人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| updater | varchar(40) | Y |  | 更新人 |

---

## 408. dimple.tc_oversea_contract　(5 字段)
> 表含义：境外合约表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| ot_contract_id | varchar(20) | N | √ | 合约号 |
| ot_contract_name | varchar(50) | Y |  | 合约名称 |
| trade_type | varchar(3) | Y |  | 市场：6-平盘货币对 ；5-境外纸黄金（对应public_dict中001中的5） |
| exch_code | varchar(3) | Y |  | 交易所代码 |
| variety_id | varchar(4) | Y |  | 品种代码 |

---

## 409. dimple.tc_overseas_inq　(25 字段)
> 表含义：中行境外数据导入表　|　估算行数：**463**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| import_date | varchar(8) | Y |  | 导入日期 |
| import_time | varchar(8) | Y |  | 导入时间 |
| member_id | varchar(8) | Y |  | 席位号 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| cfets_match_no | varchar(30) | N | √ | 外汇交易成交单号 |
| trader_no | varchar(40) | Y |  | 本方交易员 |
| role | varchar(40) | Y |  | 角色 见tp_public_dict的340 |
| party_org | varchar(40) | Y |  | 对手方机构 |
| match_type | varchar(3) | N |  | 见tp_public_dict的253 |
| currency | varchar(20) | Y |  | 货币对 AUX/CNY AUY/CNY |
| contract_id | varchar(20) | Y |  | 合约 Au99.95 Au99.99 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| near_period | varchar(10) | Y |  | 近端期限 |
| near_due_date | varchar(8) | Y |  | 近端到期日 |
| near_num_buy | numeric(24,6) | Y |  | 近端交割重量 |
| near_amount | varchar(40) | Y |  | 近端对应货币交易量 |
| far_period | varchar(10) | Y |  | 远端期限 |
| far_due_date | varchar(8) | Y |  | 远端到期日 |
| far_num_buy | numeric(24,6) | Y |  | 远端交割重量 |
| far_amount | varchar(40) | Y |  | 远端对应货币交易量 |
| initiator | varchar(20) | Y |  | 发起方中文名称 |
| quoteputor | varchar(20) | Y |  | 报价方中文名称 |
| deal_status | varchar(3) | N |  | 是否生效 027 |
| common_date | varchar(8) | N | √ | 当前日期，用于将上一日数据滚到第二日 |
| operator | varchar(80) | Y |  | 操作员 |

---

## 410. dimple.tc_pay_date　(8 字段)
> 表含义：付息日表　|　估算行数：**2,690**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 系统流水号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| delay_no | varchar(30) | Y |  | 展期编号 |
| trade_type | varchar(3) | Y |  | 交易类型:见tp_public_dict的298 |
| pay_date | varchar(8) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 付息日对应的总利息 |
| lend_flag | varchar(3) | Y |  | 拆借方向:见tp_public_dict的221中拆入和拆出 |
| last_pay_date | varchar(8) | Y |  | 上一付息日 |

---

## 411. dimple.tc_pf_billing_subject　(6 字段)
> 表含义：浦发银行-会计科目对应表　|　估算行数：**27**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| subject_id | float8 | Y |  | 科目ｉｄ |
| buy_flag | varchar(4) | Y |  | 借贷/收付 |
| subject | varchar(4) | Y |  | 科目 |
| name | varchar(2000) | Y |  | 名称 |
| client_id | varchar(30) | Y |  | 账号 |
| remark | varchar(2000) | Y |  | 摘要 |

---

## 412. dimple.tc_pf_dk_agent_detail　(16 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(10) | N |  |  |
| book_date | varchar(10) | N |  |  |
| leg_reg_no | varchar(20) | N | √ |  |
| apply_origin | varchar(1) | N |  |  |
| lend_in_seatno | varchar(10) | N |  |  |
| lend_out_seatno | varchar(10) | N |  |  |
| lend_contractno | varchar(20) | Y |  |  |
| due_date | varchar(8) | Y |  |  |
| early_termi_flag | varchar(10) | Y |  |  |
| lend_var | varchar(50) | N |  |  |
| lend_weight | varchar(50) | N |  |  |
| lend_price | varchar(50) | N |  |  |
| lend_amount | varchar(50) | N |  |  |
| backup_list1 | varchar(256) | Y |  |  |
| backup_list2 | varchar(256) | Y |  |  |
| backup_list3 | varchar(256) | Y |  |  |

---

## 413. dimple.tc_pf_exch_fee_dispatch　(14 字段)
> 表含义：浦发银行：交易所费用分摊表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| exch_abbr | varchar(40) | Y |  | 交易所简称 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| money_type | varchar(3) | N | √ | 费用类型:见tp_public_dict的233(只上期所费用类型) |
| amt | numeric(18,2) | N |  | 费用金额 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 414. dimple.tc_pf_tmp_agent_lend_file　(15 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(10) | N |  |  |
| trade_date | varchar(10) | N |  |  |
| leg_reg_no | varchar(20) | N |  |  |
| apply_origin | varchar(1) | N |  |  |
| lend_in_seatno | varchar(10) | N |  |  |
| lend_out_seatno | varchar(10) | N |  |  |
| lend_contractno | varchar(20) | Y |  |  |
| due_date | varchar(8) | N |  |  |
| weight_unit | varchar(8) | N |  |  |
| lend_list1 | varchar(250) | N |  |  |
| early_termi_flag | varchar(10) | Y |  |  |
| early_termi_list | varchar(250) | Y |  |  |
| backup_list1 | varchar(250) | Y |  |  |
| backup_list2 | varchar(250) | Y |  |  |
| backup_list3 | varchar(250) | Y |  |  |

---

## 415. dimple.tc_pingan_account　(25 字段)
> 表含义：平安账务文件表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| seq_no | varchar(30) | Y |  | 流水号 |
| group_no | varchar(30) | Y |  | 组号 |
| trade_logno | varchar(30) | Y |  | 交易流水号 |
| currency | varchar(10) | Y |  | 币种 |
| direction | varchar(2) | Y |  | 借贷方向：D借，C贷 |
| org | varchar(20) | Y |  | 机构代码 |
| account | varchar(50) | Y |  | 账号 |
| subject | varchar(20) | Y |  | 科目 |
| amt | numeric(24,6) | Y |  | 发生额 |
| remark | varchar(255) | Y |  | 备注 |
| isrecal | varchar(2) | Y |  | 是否为日终估值账务：0否；1是 |
| accounting_no | varchar(9) | Y |  | ICS产生的传票号 |
| account_date | varchar(9) | Y |  | 会计日期 |
| trans_status | varchar(2) | Y |  | 发送状态：0未发送；1 成功；2失败 |
| trans_result | varchar(20) | Y |  | 发送返回代码 |
| trans_msg | varchar(100) | Y |  | 发送返回信息 |
| check_status | varchar(2) | Y |  | 对账状态：0未对账；1已对账 |
| check_result | varchar(20) | Y |  | 对账返回代码 |
| check_msg | varchar(100) | Y |  | 对账返回信息 |
| exg_seq_no | varchar(40) | Y |  | 结售汇流水号 |
| del_flag | varchar(3) | Y |  | 冲销标志：N普通 R冲销 |
| biz_logno | varchar(30) | Y |  | 业务流水号 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 416. dimple.tc_pingan_account_bond　(13 字段)
> 表含义：平安银行-账务国债买卖表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(18,2) | Y |  | 成交量 |
| turnover | numeric(18,2) | Y |  | 成交额 |
| nominal_amt | numeric(18,2) | Y |  | 券面金额 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 417. dimple.tc_pingan_account_defer　(12 字段)
> 表含义：平安银行-账务递延买卖表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量 |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 418. dimple.tc_pingan_account_future　(12 字段)
> 表含义：平安银行-账务贵金属期货业务　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(18,2) | Y |  | 成交量（克） |
| turnover | numeric(18,2) | Y |  | 成交额 |
| open_turnover | numeric(18,2) | Y |  | 建仓成本 |
| eo_flag | varchar(3) | Y |  | 开平标志: 1 开仓；2 平仓；3交易所强平 |
| open_match_no | varchar(20) | Y |  | 开仓成交号 |
| off_match_no | varchar(20) | Y |  | 平仓成交号 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 419. dimple.tc_pingan_file_status　(3 字段)
> 表含义：文件生成状态表(平安银行专用)　|　估算行数：**22**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(9) | N | √ | 交易日期 |
| file_name | varchar(60) | N | √ | 文件名 |
| status | varchar(3) | Y |  | 生成状态:0-失败,1-成功 |

---

## 420. dimple.tc_pingan_portfolio_relation　(6 字段)
> 表含义：平安银行：Portfolio与交易员、交易目的关系　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 席位号 |
| trader_no | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| portfolio | varchar(20) | Y |  | 投组 |
| dealer_role | varchar(50) | Y |  | 交易员UM号 |
| tran_type | varchar(20) | Y |  | 交易类型 |

---

## 421. dimple.tc_pingan_recalc_spot　(7 字段)
> 表含义：平安日终重估业务-现货　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(10) | Y |  | 交易所代码 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(12,2) | Y |  | 当日库存量（克） |
| price | numeric(20,8) | Y |  | 当日收盘价 |
| cost_amt | numeric(18,2) | Y |  | 当日公允价值 |
| profit | numeric(18,2) | Y |  | 重估损益 |

---

## 422. dimple.tc_pingan_send_futures_order　(32 字段)
> 表含义：期货委托单供数表　|　估算行数：**5,503**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(9) | N | √ | 交易日期 |
| exch_code | varchar(3) | N |  | 交易所 |
| purpose_code | varchar(4) | N |  | 交易目的 |
| order_no | varchar(21) | N |  | 委托单编号 |
| buysell | varchar(4) | Y |  | 买卖方向 |
| futurelabel | varchar(20) | Y |  | 期货/递延产品名称 |
| maturitylabel | varchar(20) | Y |  | 到期类别 |
| quotationlabel | varchar(29) | Y |  | 单位 |
| quantity | varchar(30) | Y |  | 手数 |
| location | varchar(20) | Y |  | 交割账户 |
| price | varchar(20) | Y |  | 成交价格 |
| strategysource | varchar(10) | Y |  | 多空头 |
| trade_usage | varchar(10) | Y |  | 交易类别 |
| tradeglobalid | varchar(20) | N | √ | 外部交易号 |
| ourportfolio | varchar(35) | Y |  | 投组 |
| theirname | varchar(35) | Y |  | 交易对手名称 |
| match_date | varchar(8) | Y |  | 成交日期 |
| sourcemodule | varchar(22) | Y |  | 上游系统 |
| settlementmethod | varchar(22) | Y |  | 清算方式 |
| tradeoperatetype | varchar(1) | Y |  | 交易操作类型 |
| eventdate | varchar(8) | Y |  | 事件日期 |
| trader | varchar(50) | Y |  | 交易员 |
| sourcecomments | varchar(90) | Y |  | 备注 |
| ori_ctp | varchar(20) | Y |  | 原始交易对手 |
| product_cate | varchar(20) | Y |  | 黄金进口方式 |
| ori_cnt_code | varchar(20) | Y |  | 原始交易合约代码 |
| product_type | varchar(20) | Y |  | 交易类型 |
| count_p | varchar(20) | Y |  | 对公原始交易对手BECIF号 |
| agg_size | varchar(21) | Y |  | 归集数目 |
| status | varchar(3) | Y |  | 状态 |
| send_occasion | varchar(3) | N | √ | 供数时机:1-盘中,2-盘后 |
| is_repeat_send | varchar(3) | Y |  | 是否重复发送:见tp_public_dict的027 |

---

## 423. dimple.tc_pingan_send_spot_order　(40 字段)
> 表含义：现货委托单供数表　|　估算行数：**536**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(9) | N | √ | 交易日期 |
| exch_code | varchar(3) | N |  | 交易所 |
| purpose_code | varchar(4) | N |  | 交易目的 |
| order_no | varchar(21) | N |  | 委托单编号 |
| instrument | varchar(20) | Y |  | 产品 |
| currency | varchar(3) | Y |  | 货币 |
| unit | varchar(25) | Y |  | 单位 |
| buysell | varchar(4) | Y |  | 买卖方向 |
| nominal | varchar(20) | Y |  | 本金 |
| price | varchar(20) | Y |  | 成交价格 |
| location | varchar(20) | Y |  | 交割账户 |
| quality | varchar(20) | Y |  | 成色 |
| settlementmode | varchar(20) | Y |  | 交割方式 |
| settlementdate | varchar(8) | Y |  | 交割日期 |
| delivery_index | varchar(50) | Y |  | 交割组合 |
| archivingseries | varchar(50) | Y |  | 交割价格参考 |
| deliverydate | varchar(8) | Y |  | 到期日 |
| trade_usage | varchar(10) | Y |  | 交易类别 |
| archivingrefdate | varchar(8) | Y |  | 交割价格参考日期 |
| tradeglobalid | varchar(20) | N | √ | 外部交易号 |
| ourportfolio | varchar(35) | Y |  | 投组 |
| theirname | varchar(35) | Y |  | 交易对手名称 |
| tradedate | varchar(8) | Y |  | 成交日期 |
| match_date | varchar(8) | Y |  |  |
| sourcemodule | varchar(22) | Y |  | 上游系统 |
| settlementmethod | varchar(22) | Y |  | 清算方式 |
| tradeoperatetype | varchar(1) | Y |  | 交易操作类型 |
| eventdate | varchar(8) | Y |  | 事件日期 |
| trader | varchar(50) | Y |  | 交易员 |
| sourcecomments | varchar(90) | Y |  | 备注 |
| ori_ctp | varchar(20) | Y |  | 原始交易对手 |
| product_cate | varchar(20) | Y |  | 黄金进口方式 |
| ori_cnt_code | varchar(20) | Y |  | 原始交易合约代码 |
| product_type | varchar(20) | Y |  | 交易类型 |
| count_p | varchar(20) | Y |  | 对公原始交易对手BECIF号 |
| agg_size | varchar(21) | Y |  | 归集数目 |
| sn | varchar(20) | Y |  | 请求流水号 |
| status | varchar(3) | Y |  | 状态 |
| send_occasion | varchar(3) | N | √ | 供数时机:1-盘中,2-盘后 |
| is_repeat_send | varchar(3) | Y |  | 是否重复发送:见tp_public_dict的027 |

---

## 424. dimple.tc_pingan_subject　(12 字段)
> 表含义：平安账务科目表　|　估算行数：**375**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| subject_id | varchar(20) | Y |  | 科目代号 |
| subject | varchar(20) | Y |  | 科目 |
| subject_name | varchar(75) | Y |  | 名称 |
| currency | varchar(10) | Y |  | 币种 |
| account | varchar(50) | Y |  | 内部资金账户 |
| org | varchar(20) | Y |  | 机构代码 |
| calc_content | varchar(100) | Y |  | 核算内容 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| fee_code | varchar(20) | Y |  | 费用代码 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| bank_name | varchar(40) | Y |  |  |
| bank_branch | varchar(40) | Y |  |  |

---

## 425. dimple.tc_pingan_valueadded_tax　(15 字段)
> 表含义：平安银行：增值税发票流水补录信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | varchar(40) | N | √ | 业务流水号 |
| becif_no | varchar(50) | Y |  | 客户编码:BECIF号 |
| origin_date | varchar(8) | Y |  | 原交易日期 |
| origin_no | varchar(40) | Y |  | 原业务流水号 |
| usage_no | varchar(2) | Y |  | 用途编码:见tp_public_dict的364 |
| attn_no | varchar(32) | Y |  | 经办人编码 |
| attn_name | varchar(200) | Y |  | 经办人名称 |
| ods_date | varchar(8) | Y |  | 供数日期 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 426. dimple.tc_pingan_valueadded_tax_sub　(16 字段)
> 表含义：平安银行：增值税发票流水补录票据子表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | varchar(40) | N | √ | 业务流水号 |
| vat_type | varchar(4) | Y |  | 增值税票据类型:见tp_public_dict的365 |
| bill_no | varchar(16) | Y |  | 票据代码 |
| bill_no_2 | varchar(32) | Y |  | 票据号码 |
| bill_amt | numeric(18,2) | Y |  | 票据金额 |
| bill_tax | numeric(18,2) | Y |  | 票据税额 |
| pritax_total | numeric(18,2) | Y |  | 价税合计 |
| amt_used | numeric(18,2) | Y |  | 交易流水占用票据金额 |
| ods_date | varchar(8) | Y |  | 供数日期 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 427. dimple.tc_pledge_orgin　(8 字段)
> 表含义：质押表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | Y |  | 导入日期 |
| op_time | varchar(8) | Y |  | 导入时间 |
| approve_date | varchar(8) | Y |  | 处质日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| seq_no | varchar(10) | Y |  | 流水号 |
| trade_type | varchar(3) | Y |  | 交易类型 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(16,4) | Y |  | 重量 |

---

## 428. dimple.tc_posi_day_report　(11 字段)
> 表含义：持有量日报表　|　估算行数：**57,849**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| month_no | varchar(8) | N | √ | 月份 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_qty | numeric(15,3) | Y |  | 多头数量:kg |
| buy_amt | numeric(24,6) | Y |  | 多头金额 |
| buy_margin | numeric(18,2) | Y |  | 多头保证金 |
| sell_qty | numeric(15,3) | Y |  | 空头数量:kg |
| sell_amt | numeric(24,6) | Y |  | 空头金额 |
| sell_margin | numeric(18,2) | Y |  | 空头保证金 |

---

## 429. dimple.tc_posi_month_report　(10 字段)
> 表含义：持有量月报表　|　估算行数：**3,797**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| month_no | varchar(8) | N | √ | 月份 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_qty | numeric(15,3) | Y |  | 多头数量:kg |
| buy_amt | numeric(24,6) | Y |  | 多头金额 |
| buy_margin | numeric(18,2) | Y |  | 多头保证金 |
| sell_qty | numeric(15,3) | Y |  | 空头数量:kg |
| sell_amt | numeric(24,6) | Y |  | 空头金额 |
| sell_margin | numeric(18,2) | Y |  | 空头保证金 |

---

## 430. dimple.tc_price_deviation_parameter　(11 字段)
> 表含义：合规参数设置--价格偏离参数管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| price_limit | numeric(6,4) | Y |  | 价格偏离限制值 |
| price_alarm | numeric(6,4) | Y |  | 价格偏离预警值 |
| input_user | varchar(50) | Y |  | 录入人员 |
| input_date | varchar(8) | Y |  | 录入日期 |
| input_time | varchar(8) | Y |  | 录入时间 |
| update_user | varchar(50) | Y |  | 修改人员 |
| update_date | varchar(8) | Y |  | 修改日期 |
| update_time | varchar(8) | Y |  | 修改时间 |

---

## 431. dimple.tc_priceing_session_config　(3 字段)
> 表含义：定盘价与场次对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| session_id | numeric(6,0) | N | √ | 场次编号 |
| price_type | varchar(3) | N | √ | 价格类型:见tp_public_dict的288；只配置定价类型早盘、晚盘、夜市 |

---

## 432. dimple.tc_profit_rate　(14 字段)
> 表含义：自营交易员收益率表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| currency | varchar(3) | N | √ | 币种 |
| amt_fee | numeric(24,6) | Y |  | 手续费 |
| margin | numeric(18,2) | Y |  | 收益 |
| used_money | numeric(18,2) | Y |  | 占用资金 |
| day_account | numeric(12,0) | Y |  | 天数 |
| avg_maigin | numeric(18,2) | Y |  | 日均收益率 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| storage_cost_tot | numeric(24,6) | Y |  | 累计库存成本 |
| rpl_tot | numeric(18,2) | Y |  | 累计实现盈亏 |
| unrpl_tot | numeric(18,2) | Y |  | 累计未实现盈亏 |

---

## 433. dimple.tc_purpose_config　(9 字段)
> 表含义：交易目的表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| pcode | varchar(3) | N | √ | 类型编号 |
| pname | varchar(40) | Y |  | 类型名称 |
| fcode | varchar(3) | Y |  | 父类型编码 |
| status | varchar(3) | Y |  | 类型状态 |
| remark | varchar(200) | Y |  | 类型描述 |
| create_date | timestamp | Y |  | 创建日期 |
| create_id | varchar(30) | Y |  | 创建人 |
| modify_date | timestamp | Y |  | 修改日期 |
| modify_id | varchar(30) | Y |  | 修改人 |

---

## 434. dimple.tc_purpose_cost_dayavg_clear　(23 字段)
> 表含义：品种每日平均成本结算表 品种内容包含现货、境外黄金、期货、黄金T+D　|　估算行数：**553**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| buy_qty | numeric(25,8) | Y |  | 当日买入量（千克） |
| buy_amt | numeric(24,6) | Y |  | 当日买入金额 |
| sell_qty | numeric(25,8) | Y |  | 当日卖出量（千克） |
| sell_amt | numeric(24,6) | Y |  | 当日卖出金额 |
| sell_cost | numeric(24,6) | Y |  | 当日卖出成本 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量（千克） |
| remain_cost | numeric(24,6) | Y |  | 剩余成本（元） |
| realized_profitloss | numeric(18,2) | Y |  | 实现盈亏 |
| au_buy_qty | numeric(25,8) | Y |  | 黄金仓单多头交收量合计（克） |
| au_buy_amt | numeric(24,6) | Y |  | 黄金仓单多头交收金额合计（元） |
| au_sell_qty | numeric(25,8) | Y |  | 黄金仓单空头交收量合计（克） |
| au_sell_amt | numeric(24,6) | Y |  | 黄金仓单空头交收金额合计（元） |
| au_sell_cost | numeric(24,6) | Y |  | 黄金仓单空头交收总成本（元） |
| au_realized_prof | numeric(18,2) | Y |  | 黄金仓单空头交收损益（元） |
| au_remain_qty | numeric(25,8) | Y |  | 黄金仓单空头交收剩余库存（克） |
| au_remain_cost | numeric(24,6) | Y |  | 黄金仓单空头交收剩余成本（元） |
| trade_type | varchar(3) | Y |  | 交易类型:见tp_public_dict的266 |

---

## 435. dimple.tc_purpose_delivery_posi　(21 字段)
> 表含义：交易目的交割持仓表:期货交割持仓表:记录期转现，滚动交割，一次性交割的平仓量和相应资金.日终结算产生　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| match_date | varchar(8) | N |  | 配对日 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| delivery_way | varchar(2) | N |  | 交割方式:见tp_public_dict的051 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| ahead_buy_qty | numeric(12,0) | Y |  | 提前买交割量 |
| ahead_sell_qty | numeric(12,0) | Y |  | 提前卖交割量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_margin | numeric(18,2) | Y |  | 买保证金:仅对滚动交割和一次性交割有效；指买方转货款；此字段仅用来查询。 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金:仅对滚动交割和一次性交割有效；指卖方转交割保证金；此字段仅用来查询。 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| wrap_price | numeric(20,8) | Y |  | 包装物价格 |
| delivery_fee | numeric(18,2) | Y |  | 交割手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| clear_account_no | varchar(14) | Y |  | 结算帐号 |
| delivery_date | varchar(8) | Y |  | 交割日 |

---

## 436. dimple.tc_purpose_storage_clear　(13 字段)
> 表含义：交易目的结算库存表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| etf_frozen_storage | numeric(16,6) | Y |  | 认申赎冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 437. dimple.tc_quote_alarm_note　(7 字段)
> 表含义：报价风控信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 席位代码：根据业务规则，部分风控指标类型不填 |
| contract_id | varchar(20) | N |  | 合约 |
| risk_type | varchar(10) | N |  | 风控指标类型：见tp_public_dict的409 |
| seq_no | float8 | N | √ | 序列号 |
| risk_time | varchar(8) | Y |  | 预警时间 |
| risk_info | varchar(255) | Y |  | 预警信息 |

---

## 438. dimple.tc_quote_risk_config　(14 字段)
> 表含义：报价风控参数设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | Y |  | 席位代码：根据业务规则，部分风控指标类型不填 |
| client_id | varchar(16) | Y |  | 客户代码：根据业务规则，部分风控指标类型不填 |
| contract_id | varchar(20) | N |  | 合约 |
| risk_type | varchar(10) | N |  | 风控指标类型：见tp_public_dict的409 |
| numbers_limit | numeric(5,0) | Y |  | 次数参数 |
| duration_limit | numeric(5,0) | Y |  | 时长参数：秒 |
| qty_limit | numeric(4,0) | Y |  | 重量参数：克 |
| amt_limit | numeric(12,2) | Y |  | 金额参数：元 |
| if_valid | varchar(2) | N |  | 是否启用：见tp_public_dict的027 |
| remark | varchar(100) | Y |  | 指标说明 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |

---

## 439. dimple.tc_quote_risk_config_jour　(16 字段)
> 表含义：报价风控参数设置流水表　|　估算行数：**1,042**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| change_date | varchar(8) | N | √ | 变更日期 |
| seq_no | numeric(5,0) | N | √ | 序号 |
| member_id | varchar(8) | Y |  | 席位代码：根据业务规则，部分风控指标类型不填 |
| client_id | varchar(16) | Y |  | 客户代码：根据业务规则，部分风控指标类型不填 |
| contract_id | varchar(20) | N |  | 合约 |
| risk_type | varchar(10) | N |  | 指标类型：见tp_public_dict的xxx |
| numbers_limit | numeric(5,0) | Y |  | 次数参数 |
| duration_limit | numeric(5,0) | Y |  | 时长参数：秒 |
| qty_limit | numeric(4,0) | Y |  | 重量参数：克 |
| amt_limit | numeric(12,2) | Y |  | 金额参数：元 |
| if_valid | varchar(2) | N |  | 是否启用：见tp_public_dict的027 |
| remark | varchar(100) | Y |  | 指标说明 |
| operator | varchar(30) | Y |  | 录入人员 |
| op_date | varchar(8) | Y |  | 操作日期:原记录中的op_date |
| op_time | varchar(8) | Y |  | 录入时间 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |

---

## 440. dimple.tc_real_money　(11 字段)
> 表含义：场上查询资金表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| invest_id | varchar(14) | N |  | 投资者号 |
| invest_abbr | varchar(14) | N |  | 投资者简称 |
| clear_account_no | varchar(14) | N |  | 结算子帐号 |
| currency | varchar(10) | N |  | 币种 |
| last_remain | numeric(18,2) | Y |  | 昨日结算准备金余额 |
| today_out | numeric(18,2) | Y |  | 本日资金出入 |
| change_remain | numeric(18,2) | Y |  | 交易保证金变动 |
| offset_profit | numeric(18,2) | Y |  | 平仓盈亏 |
| used_money | numeric(18,2) | Y |  | 定单占用资金 |
| using_money | numeric(18,2) | Y |  | 可用资金 |
| out_money | numeric(18,2) | Y |  | 可出资金 |

---

## 441. dimple.tc_recalc_price　(5 字段)
> 表含义：另类盈亏计算价格表　|　估算行数：**1,517,262**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 清算日期 |
| price_type | varchar(3) | N | √ | 价格类型:见tp_public_dict的288 |
| contract_id | varchar(20) | N | √ | 合约 |
| calc_price | numeric(20,8) | Y |  | 计算价格 |
| last_calc_price | numeric(20,8) | Y |  | 上日计算价格 |

---

## 442. dimple.tc_receiver_manage　(10 字段)
> 表含义：收件人管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| receiver_type | varchar(3) | N |  | 收件人类型 dict-486 |
| receiver | varchar(200) | Y |  | 收件人 |
| notice | varchar(3) | N |  | 通知事项 dict-485 |
| email_address | varchar(255) | Y |  | 收件人email地址 |
| email_title | varchar(510) | Y |  | 邮件标题 |
| data_status | varchar(3) | N |  | 收件人配置状态 dict-487,0-已生效,1-已删除 |
| op_user | varchar(50) | Y |  | 操作人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| remark | varchar(1000) | Y |  | 备注 |

---

## 443. dimple.tc_req_process_d410_pack_jour　(14 字段)
> 表含义：黄金远期价格曲线报价流水表　|　估算行数：**417**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | bpchar(8) | N |  | 交易日 |
| seq_no | numeric(20,0) | N |  | 上场序号 |
| trader_id | varchar(64) | N |  | 交易员 |
| member_id | varchar(64) | N |  | 交易席位 |
| variety_id | varchar(64) | N |  | 品种ID |
| bs_flag | bpchar(1) | N |  | 买卖方向 |
| price_on | numeric(24,10) | N |  | O/N价格 |
| price_1w | numeric(24,10) | N |  | 1W价格 |
| price_2w | numeric(24,10) | N |  | 2W价格 |
| price_1m | numeric(24,10) | N |  | 1M价格 |
| price_3m | numeric(24,10) | N |  | 3M价格 |
| price_6m | numeric(24,10) | N |  | 6M价格 |
| price_9m | numeric(24,10) | N |  | 9M价格 |
| price_1y | numeric(24,10) | N |  | 1Y价格 |

---

## 444. dimple.tc_req_process_d550_pack_jour　(14 字段)
> 表含义：白银远期价格曲线报价流水表　|　估算行数：**150**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | bpchar(8) | N |  | 交易日 |
| seq_no | numeric(20,0) | N |  | 上场序号 |
| trader_id | varchar(64) | N |  | 交易员 |
| member_id | varchar(64) | N |  | 交易席位 |
| variety_id | varchar(64) | N |  | 品种ID |
| bs_flag | bpchar(1) | N |  | 买卖方向 |
| price_on | numeric(24,10) | N |  | O/N价格 |
| price_1w | numeric(24,10) | N |  | 1W价格 |
| price_2w | numeric(24,10) | N |  | 2W价格 |
| price_1m | numeric(24,10) | N |  | 1M价格 |
| price_3m | numeric(24,10) | N |  | 3M价格 |
| price_6m | numeric(24,10) | N |  | 6M价格 |
| price_9m | numeric(24,10) | N |  | 9M价格 |
| price_1y | numeric(24,10) | N |  | 1Y价格 |

---

## 445. dimple.tc_req_process_d610_pack_jour　(12 字段)
> 表含义：期权波动率曲线报价流水表　|　估算行数：**1,284**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | bpchar(8) | N |  | 交易日 |
| seq_no | numeric(20,0) | N |  | 上场序号 |
| trader_id | varchar(64) | N |  | 交易员 |
| member_id | varchar(64) | N |  | 交易席位 |
| variety_id | varchar(64) | N |  | 品种ID |
| bs_flag | bpchar(1) | N |  | 买卖方向 |
| period | varchar(64) | N |  | 期限 |
| vol_atmf | numeric(24,10) | N |  | ATMF波动率 |
| vol_25d_call | numeric(24,10) | N |  | 25D看涨期权波动率 |
| vol_25d_put | numeric(24,10) | N |  | 25D看跌期权波动率 |
| vol_10d_call | numeric(24,10) | N |  | 10D看涨期权波动率 |
| vol_10d_put | numeric(24,10) | N |  | 10D看跌期权波动率 |

---

## 446. dimple.tc_ret_ilease_match　(34 字段)
> 表含义：境内租赁归还成交　|　估算行数：**18**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| agreement_sn | varchar(30) | N |  | 金交所租借登记编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：Y本方还金/Z本方收金 见tp_public_dict的221 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| return_no | varchar(30) | Y |  | 金交所还金登记号 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| ret_seq_no | float8 | N | √ | 归还流水号 |
| if_send_exch | varchar(3) | Y |  | 是否发送交易所：1是/0否 见tp_public_dict的027 |
| local_no | varchar(16) | Y |  | 本地申报单编号 |
| apply_sheet_no | varchar(20) | Y |  | 租借还金申报编号 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |
| interest_lease | varchar(32) | Y |  | 租借利息 |
| apply_date | varchar(8) | Y |  | 申报自然日期 |
| rsp_code | varchar(20) | Y |  | 响应代码 |
| rsp_msg | varchar(100) | Y |  | 响应消息 |

---

## 447. dimple.tc_ret_lease_detail　(6 字段)
> 表含义：境内租赁物归还明细表　|　估算行数：**131**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| ret_seq_no | float8 | N | √ | 归还记录归还流水号 |
| seq_no | float8 | N |  | 租赁记录系统流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| variety_id | varchar(3) | N | √ | 交易品种 |
| storage_no | varchar(4) | N | √ | 仓库代码 |
| qty | numeric(16,6) | Y |  | 归还重量 |

---

## 448. dimple.tc_ret_lease_match　(35 字段)
> 表含义：境内租赁归还成交　|　估算行数：**85**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| agreement_sn | varchar(30) | N |  | 金交所租借登记编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：Y本方还金/Z本方收金 见tp_public_dict的221 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| return_no | varchar(30) | Y |  | 金交所还金登记号 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| ret_seq_no | float8 | N | √ | 归还流水号 |
| if_send_exch | varchar(3) | Y |  | 是否发送交易所：1是/0否 见tp_public_dict的027 |
| local_no | varchar(16) | Y |  | 本地申报单编号 |
| apply_sheet_no | varchar(20) | Y |  | 租借还金申报编号 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |
| interest_lease | varchar(32) | Y |  | 租借利息 |
| apply_date | varchar(8) | Y |  | 申报自然日期 |
| rsp_code | varchar(20) | Y |  | 响应代码 |
| rsp_msg | varchar(100) | Y |  | 响应消息 |
| strategy_no | varchar(4) | Y |  | 投资策略 |

---

## 449. dimple.tc_ret_lease_match_jour　(35 字段)
> 表含义：境内租赁归还成交流水　|　估算行数：**326**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | Y |  | 合同号 |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记编号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：Y本方还金/Z本方收金 见tp_public_dict的221 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 系统租赁状态：见tp_public_dict的375 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| return_no | varchar(30) | Y |  | 金交所还金登记号 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| ret_seq_no | float8 | Y |  | 归还流水号 |
| if_send_exch | varchar(3) | Y |  | 是否发送交易所：1是/0否 见tp_public_dict的027 |
| local_no | varchar(16) | Y |  | 本地申报单编号 |
| apply_sheet_no | varchar(20) | Y |  | 租借还金申报编号 |
| party_member_id | varchar(8) | Y |  | 交易对手方席位号 |
| party_client_id | varchar(16) | Y |  | 交易对手方客户号 |
| interest_lease | varchar(32) | Y |  | 租借利息（上送交易所代收） |
| apply_date | varchar(8) | Y |  | 申报自然日期 |
| rsp_code | varchar(20) | Y |  | 响应代码 |
| rsp_msg | varchar(100) | Y |  | 响应消息 |
| strategy_no | varchar(4) | Y |  | 投资策略 |

---

## 450. dimple.tc_ret_lend_match　(30 字段)
> 表含义：境内归还成交　|　估算行数：**869**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| bill_no | varchar(30) | N | √ | 合同号 |
| return_no | varchar(30) | Y |  | 金交所还金登记编号 |
| agreement_sn | varchar(30) | N |  | 金交所租借登记号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：见tp_public_dict的221.还入和还出 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| sheet_no | varchar(20) | Y |  | 主系统黄金过户单编号 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| ret_seq_no | float8 | N | √ | 归还流水号 |
| delivery_rate_tot | varchar(8) | Y |  | 利率（总部） |
| isimported | varchar(3) | Y |  | 是否导入 |

---

## 451. dimple.tc_ret_lend_match_jour　(28 字段)
> 表含义：境内归还成交流水　|　估算行数：**2,244**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 系统编号 |
| return_no | varchar(30) | Y |  | 金交所还金登记编号 |
| bill_no | varchar(30) | Y |  | 合同号(租赁) |
| agreement_sn | varchar(30) | Y |  | 金交所租借登记号 |
| branches | varchar(10) | Y |  | 经营单位 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| return_flag | varchar(3) | Y |  | 归还方向：见tp_public_dict的221.还入和还出 |
| trader | varchar(40) | Y |  | 交易员 |
| tradedate | varchar(8) | Y |  | 交易日 |
| operator | varchar(40) | Y |  | 录入员 |
| op_date | varchar(8) | Y |  | 录入日期 |
| op_time | varchar(8) | Y |  | 录入时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| sheet_no | varchar(20) | Y |  | 主系统黄金过户单编号 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| precalc_status | varchar(4) | Y |  | 试算功能状态：见tp_public_dict的367 |
| precalc_reasons | varchar(100) | Y |  | 试算结果原因 |
| ret_seq_no | float8 | Y |  | 归还流水号 |

---

## 452. dimple.tc_rfq_adjust_posi_detail　(14 字段)
> 表含义：保证金询价调仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 调仓成交单编号 |
| bs_flag | varchar(1) | N | √ | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | N |  | 成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| trader_no | varchar(16) | N | √ | 交易员代码 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 453. dimple.tc_rfq_his_adjust_posi_detail　(14 字段)
> 表含义：保证金询价历史调仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 调仓成交单编号 |
| bs_flag | varchar(1) | N | √ | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | N | √ | 成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| trader_no | varchar(16) | N | √ | 交易员代码 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 454. dimple.tc_rfq_his_breach　(10 字段)
> 表含义：保证金询价历史违约申报表(会员)　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| trader_no | varchar(16) | Y |  | 交易员 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| due_date | varchar(8) | N | √ | 到期日 |
| breach_qty | numeric(12,0) | Y |  | 违约申报量 |
| status | varchar(2) | Y |  | 申报状态:见tp_public_dict的440 |
| apply_time | varchar(12) | Y |  | 申报时间 |
| long_posi | numeric(12,0) | Y |  | 多头持仓数量 |

---

## 455. dimple.tc_rfq_his_breach_jour　(11 字段)
> 表含义：保证金询价历史违约申报表(操作员)　|　估算行数：**84**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N |  | 合约代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| due_date | varchar(8) | N |  | 到期日 |
| breach_qty | numeric(12,0) | Y |  | 违约申报量 |
| status | varchar(2) | Y |  | 申报状态:见tp_public_dict的440 |
| apply_time | varchar(12) | Y |  | 申报时间 |
| long_posi | numeric(12,0) | Y |  | 多头持仓数量 |
| local_no | varchar(20) | N | √ | 本地报单编号 |

---

## 456. dimple.tc_rfq_his_match　(27 字段)
> 表含义：保证金询价历史成交表　|　估算行数：**2,242**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交编号 |
| bs_flag | varchar(1) | N | √ | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | N | √ | 成交日期 |
| offline_date | varchar(8) | Y |  | 线下成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| period | varchar(8) | Y |  | 期限名 |
| trade_reg | varchar(1) | Y |  | 交易登记：见tp_public_dict的341 |
| trade_type | varchar(1) | Y |  | 交易类型：见tp_public_dict的253 |
| match_type | varchar(1) | Y |  | 成交类型：见tp_public_dict的436 |
| fn_flag | varchar(1) | Y |  | 近远端：见tp_public_dict的250 |
| related_swap_no | varchar(20) | Y |  | 关联掉期编号 |
| due_date_type | varchar(1) | Y |  | 到期日类型：见tp_public_dict的437 |
| force_flag | varchar(1) | Y |  | 强平标志：见tp_public_dict的027 |
| order_no | varchar(20) | Y |  | 报单编号 |
| broker_no | varchar(10) | Y |  | 经纪机构代码 |
| channel_no | varchar(8) | Y |  | 交易来源渠道 |
| local_order_no | varchar(20) | Y |  | 本地报单编号 |
| trader_no | varchar(16) | N | √ | 交易员代码 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 457. dimple.tc_rfq_his_para　(9 字段)
> 表含义：保证金询价历史参数表　|　估算行数：**66,269**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| seat_type | varchar(1) | Y |  | 席位性质:见tp_public_dict的332 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| uniltr_margin_rate | numeric(16,6) | Y |  | 单边保证金率：元/手 |
| swap_margin_rate | numeric(16,6) | Y |  | 掉期保证金率：元/手 |
| delivery_margin_rate | numeric(16,6) | Y |  | 交割保证金率：元/手 |
| breach_rate | numeric(16,6) | Y |  | 违约金率：元/手 |
| if_update_byimp | varchar(2) | Y |  | 是否根据清算文件导入时自动更新：tp_public_dict的027 目前仅更新单边保证金率和掉期保证金率 |

---

## 458. dimple.tc_rfq_his_unchmatch　(35 字段)
> 表含义：保证金询价历史待确认成交单表　|　估算行数：**2,841**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| trader_no | varchar(16) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trade_type | varchar(2) | Y |  | 交易类型:见tp_public_dict的253 |
| member_id | varchar(8) | Y |  | 本方席位代码 |
| client_id | varchar(16) | Y |  | 本方客户代码 |
| broker_id | varchar(10) | Y |  | 本方经纪机构 |
| party_member_id | varchar(8) | Y |  | 对方席位代码 |
| party_client_id | varchar(16) | Y |  | 对方客户代码 |
| party_broker_id | varchar(10) | Y |  | 对方经纪机构 |
| party_trader_no | varchar(16) | Y |  | 对方交易员 |
| match_date | varchar(8) | Y |  | 成交日期 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| contract_no | varchar(10) | Y |  | 合约编号 |
| bs_flag | varchar(2) | N | √ | 买卖方向:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| weight | numeric(12,6) | Y |  | 重量 |
| price | numeric(12,6) | Y |  | 价格 |
| due_date | varchar(8) | Y |  | 到期日 |
| ternor_name | varchar(8) | Y |  | 期限 |
| add_clause | varchar(200) | Y |  | 附加条款 |
| far_due_date | varchar(8) | Y |  | 远端到期日 |
| far_ternor_name | varchar(8) | Y |  | 远期期限 |
| far_price | numeric(12,6) | Y |  | 远端价格 |
| local_no | varchar(20) | Y |  | 本地待确认成交单编号 |
| apply_date | varchar(8) | Y |  | 申报日期 |
| apply_time | varchar(20) | Y |  | 申报时间 |
| unchmatch_no | varchar(20) | N | √ | 待确认成交单编号 |
| force_order_flag | varchar(2) | Y |  | 是否强平:见tp_public_dict的027 |
| match_type | varchar(2) | Y |  | 成交类型:见tp_public_dict的436 |
| client_confirm_state | varchar(2) | Y |  | 客户确认状态:见tp_public_dict的443 |
| member_confirm_state | varchar(2) | Y |  | 会员确认状态:见tp_public_dict的442 |
| sge_confirm_state | varchar(2) | Y |  | 交易所确认状态:见tp_public_dict的380 |
| confirm_state | varchar(2) | Y |  | 确认状态:见tp_public_dict的441 |
| reg_submit | varchar(2) | Y |  | 登记提交方:见tp_public_dict的439 |

---

## 459. dimple.tc_rfq_margin_posi_clear　(11 字段)
> 表含义：席位保证金询价保证金表　|　估算行数：**1,066**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| swap_qty | numeric(12,0) | Y |  | 掉期持仓量 |
| uniltr_qty | numeric(12,0) | Y |  | 单边持仓量 |
| swap_margin | numeric(18,2) | Y |  | 掉期保证金 |
| uniltr_margin | numeric(18,2) | Y |  | 单边保证金 |
| margin | numeric(18,2) | Y |  | 持仓保证金=掉期保证金+单边保证金 |

---

## 460. dimple.tc_rfq_match　(27 字段)
> 表含义：保证金询价成交表　|　估算行数：**2**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交编号 |
| bs_flag | varchar(1) | N | √ | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | Y |  | 成交日期 |
| offline_date | varchar(8) | Y |  | 线下成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| period | varchar(8) | Y |  | 期限名 |
| trade_reg | varchar(1) | Y |  | 交易登记：见tp_public_dict的341 |
| trade_type | varchar(1) | Y |  | 交易类型：见tp_public_dict的253 |
| match_type | varchar(1) | Y |  | 成交类型：见tp_public_dict的436 |
| fn_flag | varchar(1) | Y |  | 近远端：见tp_public_dict的250 |
| related_swap_no | varchar(20) | Y |  | 关联掉期编号 |
| due_date_type | varchar(1) | Y |  | 到期日类型：见tp_public_dict的437 |
| force_flag | varchar(1) | Y |  | 强平标志：见tp_public_dict的027 |
| order_no | varchar(20) | Y |  | 报单编号 |
| broker_no | varchar(10) | Y |  | 经纪机构代码 |
| channel_no | varchar(8) | Y |  | 交易来源渠道 |
| local_order_no | varchar(20) | Y |  | 本地报单编号 |
| trader_no | varchar(16) | N | √ | 交易员代码 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 461. dimple.tc_rfq_mid_match　(27 字段)
> 表含义：保证金询价成交中间表：不含调仓单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交编号 |
| bs_flag | varchar(1) | N | √ | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | Y |  | 成交日期 |
| offline_date | varchar(8) | Y |  | 线下成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| period | varchar(8) | Y |  | 期限名 |
| trade_reg | varchar(1) | Y |  | 交易登记：见tp_public_dict的341 |
| trade_type | varchar(1) | Y |  | 交易类型：见tp_public_dict的253 |
| match_type | varchar(1) | Y |  | 成交类型：见tp_public_dict的436 |
| fn_flag | varchar(1) | Y |  | 近远端：见tp_public_dict的250 |
| related_swap_no | varchar(20) | Y |  | 关联掉期编号 |
| due_date_type | varchar(1) | Y |  | 到期日类型：见tp_public_dict的437 |
| force_flag | varchar(1) | Y |  | 强平标志：见tp_public_dict的027 |
| order_no | varchar(20) | Y |  | 报单编号 |
| broker_no | varchar(10) | Y |  | 经纪机构代码 |
| channel_no | varchar(8) | Y |  | 交易来源渠道 |
| local_order_no | varchar(20) | Y |  | 本地报单编号 |
| trader_no | varchar(16) | N | √ | 交易员代码 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 462. dimple.tc_rfq_no_match　(28 字段)
> 表含义：保证金询价成交差异表：场上同步和清算文件差异　|　估算行数：**1,678**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 成交编号 |
| bs_flag | varchar(1) | N |  | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | Y |  | 成交日期 |
| offline_date | varchar(8) | Y |  | 线下成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| period | varchar(8) | Y |  | 期限名 |
| trade_reg | varchar(1) | Y |  | 交易登记：见tp_public_dict的341 |
| trade_type | varchar(1) | Y |  | 交易类型：见tp_public_dict的253 |
| match_type | varchar(1) | Y |  | 成交类型：见tp_public_dict的436 |
| fn_flag | varchar(1) | Y |  | 近远端：见tp_public_dict的250 |
| related_swap_no | varchar(20) | Y |  | 关联掉期编号 |
| due_date_type | varchar(1) | Y |  | 到期日类型：见tp_public_dict的437 |
| force_flag | varchar(1) | Y |  | 强平标志：见tp_public_dict的027 |
| order_no | varchar(20) | Y |  | 报单编号 |
| broker_no | varchar(10) | Y |  | 经纪机构代码 |
| channel_no | varchar(8) | Y |  | 交易来源渠道 |
| local_order_no | varchar(20) | Y |  | 本地报单编号 |
| trader_no | varchar(16) | Y |  | 交易员代码 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| nomatch_type | varchar(1) | Y |  | 对账差异类型：见tp_public_dict的438 |

---

## 463. dimple.tc_rfq_para　(8 字段)
> 表含义：保证金询价参数表　|　估算行数：**72**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 席位代码 |
| seat_type | varchar(1) | Y |  | 席位性质:见tp_public_dict的332 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| uniltr_margin_rate | numeric(16,6) | Y |  | 单边保证金率：元/手 |
| swap_margin_rate | numeric(16,6) | Y |  | 掉期保证金率：元/手 |
| delivery_margin_rate | numeric(16,6) | Y |  | 交割保证金率：元/手 |
| breach_rate | numeric(16,6) | Y |  | 违约金率：元/手 |
| if_update_byimp | varchar(2) | Y |  | 是否根据清算文件导入时自动更新：tp_public_dict的027 目前仅更新单边保证金率和掉期保证金率 增加交割保证金率 |

---

## 464. dimple.tc_risk_config　(4 字段)
> 表含义：风控参数设置　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| para_code | varchar(20) | N | √ | 参数编码 |
| para_abbr | varchar(50) | Y |  | 参数名称 |
| para_value | varchar(20) | Y |  | 参数值 |
| para_desc | varchar(254) | Y |  | 参数备注 |

---

## 465. dimple.tc_risk_control　(4 字段)
> 表含义：风险预警表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| risk_type | varchar(3) | N | √ | 预警类型：见dict 317 |
| risk_info | varchar(254) | Y |  | 预警信息 |
| risk_value | numeric(24,6) | Y |  | 当前预警值 |
| if_alarm | varchar(3) | Y |  | 是否预警 |

---

## 466. dimple.tc_rpl_day_report　(12 字段)
> 表含义：损益日报表　|　估算行数：**1,412**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| month_no | varchar(8) | N | √ | 月份 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| spot_rpl | numeric(18,2) | Y |  | 现货货款轧差 |
| defer_rpl | numeric(18,2) | Y |  | 延期平仓盈亏 |
| ftr_rpl | numeric(18,2) | Y |  | 期货平仓盈亏 |
| trade_fee | numeric(18,2) | Y |  | 手续费 |
| storage_fee | numeric(18,2) | Y |  | 仓储费 |
| trans_fee | numeric(18,2) | Y |  | 运保费 |
| other_fee | numeric(18,2) | Y |  | 其它费用 |

---

## 467. dimple.tc_rpl_month_report　(11 字段)
> 表含义：损益月报表　|　估算行数：**102**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| month_no | varchar(8) | N | √ | 月份 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| spot_rpl | numeric(18,2) | Y |  | 现货货款轧差 |
| defer_rpl | numeric(18,2) | Y |  | 延期平仓盈亏 |
| ftr_rpl | numeric(18,2) | Y |  | 期货平仓盈亏 |
| trade_fee | numeric(18,2) | Y |  | 手续费 |
| storage_fee | numeric(18,2) | Y |  | 仓储费 |
| trans_fee | numeric(18,2) | Y |  | 运保费 |
| other_fee | numeric(18,2) | Y |  | 其它费用 |

---

## 468. dimple.tc_rpt_client_act_clear　(15 字段)
> 表含义：账务类型统计报表　|　估算行数：**91**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| account_type | varchar(3) | N | √ | 账务处理类型：见Dict 313 |
| contract_id | varchar(20) | N | √ | 合约号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品 |
| buy_avg_price | numeric(20,8) | Y |  | 当笔均价 |
| buy_qty | numeric(16,6) | Y |  | 当笔数量 |
| buy_amt | numeric(24,6) | Y |  | 当笔成本 |
| sell_avg_price | numeric(20,8) | Y |  | 当笔均价 |
| sell_qty | numeric(16,6) | Y |  | 当笔数量 |
| sell_amt | numeric(24,6) | Y |  | 当笔成本 |
| real_profit | numeric(24,6) | Y |  | 实现盈亏 |
| float_profit | numeric(24,6) | Y |  | 浮动盈亏 |

---

## 469. dimple.tc_rpt_client_cost_clear　(16 字段)
> 表含义：成本中心统计报表　|　估算行数：**91**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| cost_type | varchar(10) | N | √ | 成本中心：见dict 316 |
| account_type | varchar(3) | N | √ | 账务处理类型：见Dict 313 |
| contract_id | varchar(20) | N | √ | 合约号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品 |
| buy_avg_price | numeric(20,8) | Y |  | 当笔均价 |
| buy_qty | numeric(16,6) | Y |  | 当笔数量 |
| buy_amt | numeric(24,6) | Y |  | 当笔成本 |
| sell_avg_price | numeric(20,8) | Y |  | 当笔均价 |
| sell_qty | numeric(16,6) | Y |  | 当笔数量 |
| sell_amt | numeric(24,6) | Y |  | 当笔成本 |
| real_profit | numeric(24,6) | Y |  | 实现盈亏 |
| float_profit | numeric(24,6) | Y |  | 浮动盈亏 |

---

## 470. dimple.tc_rule_alarm_note　(8 字段)
> 表含义：合规管理报警信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| alarm_date | varchar(8) | N |  | 报警日期 |
| seq_no | float8 | N | √ | 流水号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| alarm_type | bpchar(1) | N | √ | 报警类型:见tp_public_dict的232 |
| alarm_time | varchar(8) | N |  | 报警时间 |
| exch_code | varchar(30) | N |  | 交易所代码 |
| alarm_note | varchar(254) | Y |  | 报警信息 |

---

## 471. dimple.tc_rule_cancel_control　(7 字段)
> 表含义：合规参数设置--撤单管理　|　估算行数：**17**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| cancel_times | numeric(10,0) | Y |  | 撤单次数 |
| alarm_times | numeric(10,0) | Y |  | 预警阀值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作人员 |

---

## 472. dimple.tc_rule_large_cancel_control　(8 字段)
> 表含义：合规参数设置--大额撤单管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| cancel_times | numeric(10,0) | Y |  | 撤单次数 |
| alarm_times | numeric(10,0) | Y |  | 预警阀值 |
| alarm_qty_times | numeric(10,0) | Y |  | 撤单手数阀值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作人员 |

---

## 473. dimple.tc_rule_selfmatch_control　(6 字段)
> 表含义：合规参数设置--自成交管理　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| alarm_type | varchar(3) | N | √ | 预警类型:见Dict 319 |
| selfmatch_times | numeric(10,0) | Y |  | 自成交次数 |
| alarm_times | numeric(10,0) | Y |  | 预警阀值 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_user | varchar(30) | Y |  | 操作用户 |

---

## 474. dimple.tc_setoff_apply_detail　(23 字段)
> 表含义：充抵申请明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| import_date | varchar(8) | Y |  | 导入日期 |
| apply_no | varchar(16) | Y |  | 充抵申请单编号 |
| apply_date | varchar(8) | Y |  | 充抵申请日期 |
| apply_time | varchar(8) | Y |  | 充抵申请时间 |
| member_id | varchar(8) | Y |  | 申请会员代码 |
| client_id | varchar(16) | Y |  | 申请客户代码 |
| setoff_variety_id | varchar(10) | Y |  | 充抵申请物代码 |
| setoff_variety_abbr | varchar(30) | Y |  | 充抵申请物简称 |
| setoff_variety_type | varchar(1) | Y |  | 充抵申请物类型代码 |
| apply_qty | numeric(16,2) | Y |  | 充抵申请物数量 |
| effective_qty | numeric(16,2) | Y |  | 充抵申请物有效数量 |
| apply_deli_qty | numeric(16,2) | Y |  | 充抵申请物转交割数量 |
| breach_qty | numeric(16,2) | Y |  | 违约处置数量 |
| due_qty | numeric(16,2) | Y |  | 充抵到期数量 |
| due_date | varchar(8) | Y |  | 充抵到期日 |
| real_due_date | varchar(8) | Y |  | 实际充抵到期日 |
| submit_date | varchar(9) | Y |  | 提交日期 |
| status | varchar(4) | Y |  | 状态:见tp_public_dict的333 |
| fee_date | varchar(8) | Y |  | 计费日期 |
| fee_rate | numeric(10,6) | Y |  | 充抵手续费率 |
| fee | numeric(18,2) | Y |  | 充抵手续费 |
| setoff_value | numeric(18,2) | Y |  | 充抵申请物估价金额 |
| setoff_discount_value | numeric(18,2) | Y |  | 充抵申请物折后金额 |

---

## 475. dimple.tc_sge_acc_current　(14 字段)
> 表含义：上金所往来账消息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| local_seq_no | numeric(10,0) | N | √ | 本地流水号 |
| exch_seq_no | varchar(32) | Y |  | 交易所流水号 |
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| amt | numeric(24,6) | Y |  | 金额 |
| capitaltranstype | varchar(1) | Y |  | 保证金交易业务类型:见tp_public_dict的373 |
| todotxseqno | varchar(8) | Y |  | 发电流水序号 |
| todotxdate | varchar(8) | Y |  | 发电记账日期 |
| sentflag | varchar(2) | Y |  | 已发电标志:见tp_public_dict的374 |
| returnflag | varchar(4) | Y |  | 回执标志 |
| settlebankid | varchar(4) | Y |  | 结算行号 |
| accountdate | varchar(8) | Y |  | 记账日期 |
| abstract | varchar(256) | Y |  | 备注 |

---

## 476. dimple.tc_sge_agio_detail　(4 字段)
> 表含义：客户升贴水明细表:3代　|　估算行数：**144**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| agio_type | varchar(4) | N | √ | 升贴水类型：见tp_public_dict的336 |
| agio_value | numeric(20,2) | Y |  | 金额 |

---

## 477. dimple.tc_sge_cash_delivery_mode　(3 字段)
> 表含义：延期现金合约交割方式　|　估算行数：**1,794**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| contract_id | varchar(10) | N | √ | 合约代码 |
| delivery_style | varchar(1) | Y |  | 交割方式,见tp_public_dict的430 |

---

## 478. dimple.tc_sge_client_fee_detail　(16 字段)
> 表含义：SGE客户费用明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| trade_fee | numeric(18,2) | Y |  | 交易所手续费 |
| delivery_fee | numeric(18,2) | Y |  | 交割手续费 |
| storage_fee | numeric(18,2) | Y |  | 仓储费 |
| trans_fee | numeric(18,2) | Y |  | 运保费 |
| overdue_fee | numeric(18,2) | Y |  | 超期费 |
| mort_fee | numeric(18,2) | Y |  | 质押登记费 |
| lease_fee | numeric(18,2) | Y |  | 租借登记费 |
| breach_fee | numeric(18,2) | Y |  | 违约费 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| profit | numeric(18,2) | Y |  | 盈亏 |
| amount_total | numeric(18,2) | Y |  | 总金额 |
| diff_fee | numeric(18,2) | Y |  | 溢短费 |
| aigo_fee | numeric(18,2) | Y |  | 升贴水 |

---

## 479. dimple.tc_sge_client_quote_posi　(9 字段)
> 表含义：导入表:客户报价持仓数据文件　|　估算行数：**141**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | N |  | 客户代码 |
| contract_no | numeric(8,0) | N |  | 合约编号 |
| contract_id | varchar(20) | N |  | 合约代码 |
| buy_qty | numeric(18,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(18,0) | Y |  | 空头持仓量 |
| t_buy_qty | numeric(18,0) | Y |  | 今日买入量 |
| t_sell_qty | numeric(18,0) | Y |  | 今日卖出量 |

---

## 480. dimple.tc_sge_client_storage　(24 字段)
> 表含义：SGE客户库存表　|　估算行数：**9,099**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| buy_qty | numeric(16,6) | Y |  | 当日买入 |
| sell_qty | numeric(16,6) | Y |  | 当日卖出 |
| deposit_qty | numeric(16,6) | Y |  | 当日存入 |
| real_deposit_qty | numeric(16,6) | Y |  | 当日存入实重 |
| diff_storage_in | numeric(16,6) | Y |  | 入库溢短总量 |
| unclear_diff_storage_in | numeric(16,6) | Y |  | 未清算入库溢短 |
| draw_qty | numeric(16,6) | Y |  | 当日提出 |
| real_draw_qty | numeric(16,6) | Y |  | 当日提出实重 |
| diff_storage_out | numeric(16,6) | Y |  | 出库溢短总量 |
| lend_qty | numeric(16,6) | Y |  | 当日借出 |
| borrow_qty | numeric(16,6) | Y |  | 当日借入 |
| shfitout_qty | numeric(16,6) | Y |  | 当日转出 |
| shiftin_qty | numeric(16,6) | Y |  | 当日转入 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 481. dimple.tc_sge_client_storage_jour　(17 字段)
> 表含义：SGE客户库存流水表　|　估算行数：**14,017**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号 |
| sheet_no | varchar(20) | Y |  | 单据编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| total_store | numeric(18,6) | Y |  | 实际发生重量 |
| remain_store | numeric(18,6) | Y |  | 库存余量 |
| trans_type | varchar(2) | N |  | 库存变化类型:见tp_public_dict的221 |
| op_date | varchar(8) | Y |  | 实际发生日期 |
| op_time | varchar(8) | Y |  | 实际发生时间 |
| std_store | numeric(18,6) | Y |  | 发生标准重量 |
| account_type | varchar(2) | Y |  | 帐号类型:见tp_public_code的038 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| pickup_sheet_no | varchar(16) | Y |  | 提货申请单编号 |
| storage_flag | varchar(4) | Y |  | 仓库号,见tp_public_dict的244 |
| input_date | varchar(8) | Y |  | 入库日期 |

---

## 482. dimple.tc_sge_defer_cash_delivery　(10 字段)
> 表含义：延期现金交割表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_date | varchar(8) | N | √ | 交割日期 |
| delivery_no | varchar(20) | N | √ | 交割序号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(6) | N | √ | 会员代码 |
| client_id | varchar(10) | N |  | 客户代码 |
| contract_id | varchar(20) | N |  | 合约代码 |
| bs_flag | varchar(1) | N | √ | 多空方向:1-多;0-空 |
| delivery_price | numeric(12,6) | Y |  | 交割价格 |
| delivery_qty | numeric(12,0) | Y |  | 交割数量 |
| delivery_amt | numeric(18,2) | Y |  | 交割金额 |

---

## 483. dimple.tc_sge_defer_delivery_match　(12 字段)
> 表含义：SGE客户递延交割成交表　|　估算行数：**1,114**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| match_time | varchar(8) | Y |  | 成交时间 |
| trader_no | varchar(15) | Y |  | 席位号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| middle_flag | bpchar(1) | Y |  | 是否为中立仓: 0否,1是 |

---

## 484. dimple.tc_sge_delivery_jour　(13 字段)
> 表含义：交割单表：3代　|　估算行数：**5,399**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_no | varchar(20) | N | √ | 交割序号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志：见TP_PUBLIC_DICT的002 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| price | numeric(20,6) | Y |  | 交割价格 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| delivery_variety_id | varchar(3) | N |  | 交割品种号 |
| std_qty | numeric(12,0) | Y |  | 标准数量：竞价即期、延期白银为标重；其它都是手数，询价白银为手数 |
| std_amount | numeric(20,2) | Y |  | 标准金额 |
| real_qty | numeric(16,6) | Y |  | 实际交割重量：对于黄金、铂金品种，该字段为标准重量；对于白银品种，该字段为实际重量 |
| real_amount | numeric(18,2) | Y |  | 实际交割金额 |
| warehouse_id | bpchar(4) | Y |  | 意向仓库号 |

---

## 485. dimple.tc_sge_etf_client　(17 字段)
> 表含义：ETF交易所账户表　|　估算行数：**63**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| op_date | varchar(8) | Y |  | 请求日期 |
| op_time | varchar(8) | Y |  | 请求时间 |
| seq_no | varchar(20) | Y |  | 本地编号 |
| exch_seq_no | varchar(20) | Y |  | ETF账户备案流水 |
| client_name | varchar(80) | Y |  | 投资人名称 |
| client_type | varchar(4) | Y |  | 投资人类型:见public_dict274 |
| paper_type | varchar(4) | Y |  | 投资人证件类型:见public_dict275 |
| paper_no | varchar(30) | Y |  | 投资人证件号码 |
| client_code | varchar(50) | Y |  | 法人组织机构代码 |
| client_id | varchar(20) | Y |  | 投资人黄金账号 |
| member_id | varchar(8) | Y |  | 会员代码 |
| member_name | varchar(80) | Y |  | 黄金账号指定会员名称 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| trade_type | varchar(4) | Y |  | 业务类型:见public_dict272 |
| confirm_type | varchar(4) | Y |  | 确认标志:见public_dict270 |

---

## 486. dimple.tc_sge_etf_fee　(5 字段)
> 表含义：ETF费用表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| effect_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| trade_fee | numeric(18,2) | Y |  | 认申赎费 |
| cash_balance | numeric(18,2) | Y |  | 实际现金差额 |

---

## 487. dimple.tc_sge_etf_fee_detail　(6 字段)
> 表含义：ETF费用明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| effect_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| trade_fee | numeric(18,2) | Y |  | 认申赎费 |
| cash_balance | numeric(18,2) | Y |  | 实际现金差额 |

---

## 488. dimple.tc_sge_etf_match　(24 字段)
> 表含义：ETF交易所认申赎明细　|　估算行数：**341**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| client_id | varchar(16) | Y |  | 投资人黄金账号 |
| member_id | varchar(8) | Y |  | 会员代码 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| qty_1 | numeric(20,6) | Y |  | 重量1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| qty_2 | numeric(20,6) | Y |  | 重量2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| qty_3 | numeric(20,6) | Y |  | 重量3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| qty_4 | numeric(20,6) | Y |  | 重量4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| qty_5 | numeric(20,6) | Y |  | 重量5 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| local_seq_no | varchar(20) | Y |  | 本地编号 |
| status | varchar(4) | Y |  | 状态:见public_dict269 |
| trade_type | varchar(4) | Y |  | 交易类型:见public_dict268 |

---

## 489. dimple.tc_sge_fee_detail　(4 字段)
> 表含义：SGE客户费用明细表:3代　|　估算行数：**8,714**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| fee_type | varchar(4) | N | √ | 费用类型：见tp_public_dict的233 |
| fee_value | numeric(20,2) | Y |  | 费用合计 |

---

## 490. dimple.tc_sge_fee_rate　(9 字段)
> 表含义：SGE手续费率表　|　估算行数：**150,218**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| seat_type | varchar(3) | Y |  | 席位性质: 1 主板,2国际版;只金交所使用;见tp_public_dict的332 |
| exch_code | varchar(2) | N |  | 交易所 |
| contract_id | varchar(20) | N |  | 合约代码 |
| eo_flag | varchar(3) | Y |  | 开平标志：见tp_public_dict的351 |
| app_type | varchar(3) | Y |  | 定价成交申报类型：见tp_public_dict330; |
| fee_type | varchar(3) | N |  | 手续费类型：见tp_public_dict的092 |
| fee_rate | numeric(16,6) | N |  | 手续费率 |

---

## 491. dimple.tc_sge_foward_curve_info　(6 字段)
> 表含义：远期价格曲线：来自金交所场外询价业务平台接口　|　估算行数：**3,538**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| local_seq_no | numeric(10,0) | N |  | 序号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| contract_id | varchar(20) | N |  | 合约代码 |
| period | varchar(10) | N |  | 远端期限名称：O/N,1W,2W,3W,1M,2M,3M,4M,5M,6M,9M,1Y,Broken等标准期限和其他非标准期限 |
| announce_date | varchar(8) | N |  | 发布日期 |
| price | numeric(22,10) | N |  | 曲线价格:元/克;元/千克 |

---

## 492. dimple.tc_sge_foward_curve_quote　(11 字段)
> 表含义：远期价格曲线报价记录表　|　估算行数：**10,308**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(20) | N | √ | 本方席位号 |
| trader_no | varchar(40) | N |  | 本方交易员号 |
| bid_state | varchar(1) | Y |  | 报单状态;见tp_public_dict的458 |
| quote_time | varchar(22) | N | √ | 报价时间 |
| contract_id | varchar(40) | N | √ | 合约代码 |
| period | varchar(10) | N | √ | 期限：见tp_public_dict的344 |
| bs_flag | varchar(3) | N | √ | 买卖方向：见tp_public_dict的002 |
| price | numeric(20,8) | Y |  | 曲线价格 |
| urgent_number | numeric(10,0) | N | √ | 报价次数 |
| if_sync_exch | varchar(1) | Y |  | 是否已同步交易所;见tp_public_dict的027 |
| order_no | varchar(20) | Y |  | 报价编号 |

---

## 493. dimple.tc_sge_home_inquire_match　(61 字段)
> 表含义：金交所：境内询价成交导入表　|　估算行数：**8,110**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N |  | 导入日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N | √ | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| trade_party_name | varchar(40) | Y |  | 交易对手方简称 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy | varchar(8) | Y |  | 买入币种 |
| num_buy | numeric(24,6) | Y |  | 买入量 |
| currency_sell | varchar(8) | Y |  | 卖出币种 |
| num_sell | numeric(24,6) | Y |  | 卖出量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253只包含即期和远期 |
| reference_type | varchar(3) | Y |  | 参考价类型：见tp_public_dict的288 |
| reference_date | varchar(8) | Y |  | 参考价日期 |
| reference_price | numeric(20,8) | Y |  | 参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| insert_date | varchar(8) | Y |  | 操作日期 |
| update_date | varchar(8) | Y |  | 更新日期 |
| agreement_sn | varchar(30) | Y |  | 系统登记单编号 |
| inquire_type | varchar(3) | Y |  | 询价类型：见Dict的325 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码：见tp_public_dict的382 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(10) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码：见tp_public_dict的382 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| related_match_no | varchar(20) | Y |  | 相关成交单号:用来记录行权的期权成交单号，或为未来其他业务备用 |
| period | varchar(10) | Y |  | 期限：见tp_public_dict的344 |
| price_unit | varchar(4) | Y |  | 报价单位：见tp_public_dict的357 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| status | varchar(4) | Y |  | 成交单状态：见tp_public_dict的342 |
| clear_status | varchar(4) | Y |  | 清算信息：见tp_public_dict的355 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| storage_no | varchar(4) | Y |  | 指定仓库代码,白银合约时字段有值 |
| trade_volume | numeric(16,0) | Y |  | 交易手数 |
| refprice_info | varchar(50) | Y |  | 其他参考价格说明 |
| remark | varchar(254) | Y |  | 附加条款 |
| party_member_id | varchar(40) | Y |  | 对手方席位号 |
| act_due_date | varchar(8) | Y |  | 实际到期日 |
| mmb_id | varchar(8) | Y |  | 本方会员号 |
| party_mmb_id | varchar(8) | Y |  | 对手方会员号 |
| client_broker | varchar(20) | Y |  | 本方经纪机构用户 |
| party_client_broker | varchar(20) | Y |  | 对手方经纪机构用户 |
| unit | numeric(12,6) | Y |  | 交易单位 |
| exch_trader_no | varchar(15) | Y |  | 交易所本方交易员代码 |

---

## 494. dimple.tc_sge_home_lend_clear　(14 字段)
> 表含义：导入表-拆借过户清算单数据文件　|　估算行数：**2,692**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| sheet_no | varchar(30) | N | √ | 询价拆借过户单编号 |
| agreement_sn | varchar(30) | N | √ | 成交单编号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| lend_flag | varchar(4) | N | √ | 本方方向（原交易方向）：见tp_public_dict的221 拆入、拆出 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| variety_id | varchar(20) | N | √ | 过户品种 |
| bor | varchar(4) | N | √ | 借金/还金:见tp_public_dict的356 |
| qty | numeric(10,0) | Y |  | 数量(手） |
| weight | numeric(12,6) | Y |  | 重量（千克） |
| real_weight | numeric(12,6) | Y |  | 本方收到实物重量（千克）：本方收货，数值为正；本方交货，数值为负 |
| storage_no | varchar(4) | Y |  | 仓库代码 |
| clear_status | varchar(4) | Y |  | 清算信息：成功、失败:见tp_public_dict的355 |

---

## 495. dimple.tc_sge_home_lend_match　(51 字段)
> 表含义：金交所：境内拆借成交导入表　|　估算行数：**1,747**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N |  | 新增记录日期 |
| agreement_sn | varchar(30) | N | √ | 金交所租借登记号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| trade_party_name | varchar(30) | Y |  | 交易对手方简称 |
| variety_id | varchar(3) | Y |  | 交易品种(实际存放合约号信息) |
| clear_price | numeric(20,8) | Y |  | 初始结算价 |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| reg_date | varchar(8) | Y |  | 起息日 |
| due_date | varchar(8) | Y |  | 到期日 |
| days | numeric(8,0) | Y |  | 天数 |
| delivery_rate | numeric(12,8) | Y |  | 利率 |
| interest_base | varchar(3) | Y |  | 计息基准：见tp_public_dict的285 |
| pay_date | varchar(255) | Y |  | 付息日 |
| interest | numeric(24,6) | Y |  | 利息 |
| remain_days | numeric(8,0) | Y |  | 剩余天数 |
| tradedate | varchar(8) | N | √ | 交易日 |
| insert_date | varchar(8) | Y |  | 操作日期 |
| update_date | varchar(8) | Y |  | 更新日期 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算利息 |
| source_id | varchar(3) | Y |  | 来源:1会服,2拆借平台 |
| sheet_no | varchar(20) | Y |  | 主系统黄金过户单编号 |
| is_delay | varchar(3) | Y |  | 是否展期:0原记录1展期 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(30) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| party_client_id | varchar(10) | Y |  | 对手方客户代码 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| trade_reg | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| qty | numeric(10,0) | Y |  | 数量：手 |
| interest_base_unit | varchar(4) | Y |  | 计息基准价单位：元/克、元/千克 |
| period | varchar(10) | Y |  | 期限 |
| lend_status | varchar(4) | Y |  | 借金状态：见tp_public_dict的345 |
| ret_type | varchar(4) | Y |  | 还金类型：见tp_public_dict的346 |
| ret_status | varchar(4) | Y |  | 还金状态：见tp_public_dict的347 |
| pay_status | varchar(4) | Y |  | 付息状态：见tp_public_dict的348 |
| ret_deli_variety_id | varchar(15) | Y |  | 还金交割品种 |
| agreement_sn_pre | varchar(30) | Y |  | 前接成交单编号 |
| agreement_sn_next | varchar(30) | Y |  | 后续成交单编号 |
| status | varchar(4) | Y |  | 状态：见tp_public_dict的342 |
| fail_reason | varchar(20) | Y |  | 登记失败原因：见tp_public_dict的389 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |

---

## 496. dimple.tc_sge_inq_opt_his_match　(69 字段)
> 表含义：历史询价期权成交单变更数据文件　|　估算行数：**3,494**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| inq_match_no | varchar(20) | Y |  | 询价系统成交编号/3代成交单编号 |
| match_no | varchar(20) | Y |  | 主系统成交编号/3代报价单编号 |
| contract_id | varchar(20) | Y |  | 期权合约代码 |
| opt_contract_id | varchar(20) | Y |  | 行权合约代码 |
| member_id | varchar(8) | Y |  | 本方会员席位代码 |
| member_abbr | varchar(40) | Y |  | 本方会员席位简称 |
| client_id | varchar(16) | Y |  | 本方客户代码 |
| client_abbr | varchar(40) | Y |  | 本方客户简称 |
| party_member_id | varchar(8) | Y |  | 对手方会员席位代码 |
| party_member_abbr | varchar(40) | Y |  | 对手方会员席位简称 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_client_abbr | varchar(40) | Y |  | 对手方客户简称 |
| trader_no | varchar(15) | Y |  | 本方交易员代码 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| bs_flag | varchar(3) | Y |  | 本方交易方向：见tp_public_dict的002 |
| match_date | varchar(8) | Y |  | 询价成交日期/3代交易日期 |
| match_time | varchar(8) | Y |  | 询价成交时间/3代交易时间 |
| eo_flag | varchar(3) | Y |  | 开平仓标志：3代之后此字段废弃 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| opt_trade_type | varchar(3) | Y |  | 期权交易类型：见tp_public_dict的328 |
| exec_type | varchar(3) | Y |  | 行权方式：见tp_public_dict的324 |
| exec_price | numeric(11,3) | Y |  | 行权价格 |
| exec_date | varchar(8) | Y |  | 行权日 |
| exec_deadline | varchar(8) | Y |  | 行权截止时间 |
| exec_clear_date | varchar(8) | Y |  | 结算日期 |
| opt_amt | numeric(24,6) | Y |  | 期权权利金 |
| opt_total_amt | numeric(24,6) | Y |  | 期权权利金总金额 |
| opt_pay_date | varchar(8) | Y |  | 期权权利金支付日期 |
| delivery_type | varchar(3) | Y |  | 到期结算交割方式/3代结算方式 |
| reference_type | varchar(3) | Y |  | 现金交割参考价格类型/3代现金结算期权参考价格类型：见tp_public_dict的288 |
| reference_price | numeric(11,3) | Y |  | 现金交割参考价格：3代之后此字段废弃 |
| reference_adjust | numeric(11,3) | Y |  | 现金调整项/3代现金结算期权参考价格调整项 |
| reference_date | varchar(8) | Y |  | 现金交割参考价格日期：3代之后此字段废弃 |
| reg_fee_type | varchar(3) | Y |  | 本方登记费率类型：3代之后此字段废弃 |
| reg_fee_rate | numeric(20,2) | Y |  | 本方登记费率：3代之后此字段废弃 |
| reg_fee | numeric(20,2) | Y |  | 本方登记费：3代之后此字段废弃 |
| natural_date | varchar(8) | Y |  | 自然日期：3代 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| match_type | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| weight | numeric(12,6) | Y |  | 重量（千克） |
| period | varchar(10) | Y |  | 期限 |
| price_unit | varchar(4) | Y |  | 权利金和行权价报价单位：见tp_public_dict的357 |
| pay_status | varchar(4) | Y |  | 权利金支付状态：见tp_public_dict的348 |
| clear_status | varchar(4) | Y |  | 权利金清算信息：见tp_public_dict的355 |
| exec_match_no | varchar(20) | Y |  | 行权交易成交单号 |
| status | varchar(4) | Y |  | 状态：见tp_public_dict的342 |
| exec_status | varchar(4) | Y |  | 行权状态：见tp_public_dict的350 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| act_exec_date | varchar(8) | Y |  | 实际行权日 |
| act_clear_date | varchar(8) | Y |  | 实际结算日期 |
| unit | numeric(10,0) | Y |  | 交易单位 |
| act_pay_date | varchar(8) | Y |  | 实际权利金支付日 |
| offset_opt_amt | numeric(20,2) | Y |  | 平仓权利金 |
| offset_pay_status | varchar(4) | Y |  | 平仓权利金支付状态：见tp_public_dict的348 |
| offset_clear_status | varchar(4) | Y |  | 平仓权利金清算信息：见tp_public_dict的355 |
| offset_pay_date | varchar(8) | Y |  | 平仓权利金支付日 |
| act_offset_pay_date | varchar(8) | Y |  | 实际平仓权利金支付日 |
| offset_fee_status | varchar(4) | Y |  | 平仓收费状态：见tp_public_dict的343 |
| offset_fee_date | varchar(8) | Y |  | 平仓收费日期 |
| storage_no | varchar(4) | Y |  | 指定仓库代码 |
| offset_opt_total_amt | numeric(24,6) | Y |  | 期权平仓权利金总金额 |

---

## 497. dimple.tc_sge_inq_opt_match_clear　(25 字段)
> 表含义：询价期权权利金清算结果　|　估算行数：**2,099**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| clear_no | varchar(20) | Y |  | 主系统清算登记号 |
| inq_match_no | varchar(20) | Y |  | 询价系统成交编号 |
| member_id | varchar(8) | Y |  | 本方会员代码 |
| member_abbr | varchar(40) | Y |  | 本方会员简称 |
| client_id | varchar(16) | Y |  | 本方客户代码 |
| client_abbr | varchar(40) | Y |  | 本方客户简称 |
| party_member_id | varchar(8) | Y |  | 对手方会员代码 |
| party_member_abbr | varchar(40) | Y |  | 对手方会员简称 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_client_abbr | varchar(40) | Y |  | 对手方客户简称 |
| contract_id | varchar(20) | Y |  | 期权合约代码 |
| opt_contract_id | varchar(20) | Y |  | 行权合约代码 |
| eo_flag | varchar(3) | Y |  | 开平仓标志 |
| opt_total_amt | numeric(20,2) | Y |  | 期权权利金总金额 |
| pay_flag | varchar(3) | Y |  | 本方期权权利金支付方向（收付）：见tp_public_dict的326 |
| opt_pay_date | varchar(8) | Y |  | 期权权利金支付日期 |
| opt_act_pay_date | varchar(8) | Y |  | 期权权利金实际支付日期 |
| status | varchar(3) | Y |  | 清算结果：见tp_public_dict的327 |
| clear_date | varchar(8) | Y |  | 日期:生成清算单的日期 |
| bs_flag | varchar(4) | Y |  | 本方方向：见tp_public_dict的002 |
| opt_amt | numeric(12,6) | Y |  | 权利金：元/克、元/千克 |
| qty | numeric(10,0) | Y |  | 数量：手 |
| weight | numeric(12,6) | Y |  | 重量（千克） |
| if_breach_apply | varchar(4) | Y |  | 是否违约申报：见tp_public_dict的027 |

---

## 498. dimple.tc_sge_inq_opt_match_detail　(69 字段)
> 表含义：询价期权成交单数据文件　|　估算行数：**2,030**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| inq_match_no | varchar(20) | Y |  | 询价系统成交编号/3代成交单编号 |
| match_no | varchar(20) | Y |  | 主系统成交编号/3代报价单编号 |
| contract_id | varchar(20) | Y |  | 期权合约代码 |
| opt_contract_id | varchar(20) | Y |  | 行权合约代码 |
| member_id | varchar(8) | Y |  | 本方会员席位代码 |
| member_abbr | varchar(40) | Y |  | 本方会员席位简称 |
| client_id | varchar(16) | Y |  | 本方客户代码 |
| client_abbr | varchar(40) | Y |  | 本方客户简称 |
| party_member_id | varchar(8) | Y |  | 对手方会员席位代码 |
| party_member_abbr | varchar(40) | Y |  | 对手方会员席位简称 |
| party_client_id | varchar(16) | Y |  | 对手方客户代码 |
| party_client_abbr | varchar(40) | Y |  | 对手方客户简称 |
| trader_no | varchar(15) | Y |  | 本方交易员代码 |
| party_trader_no | varchar(15) | Y |  | 对手方交易员代码 |
| bs_flag | varchar(3) | Y |  | 本方交易方向：b 买;s 卖 |
| match_date | varchar(8) | Y |  | 询价成交日期/3代交易日期 |
| match_time | varchar(8) | Y |  | 询价成交时间/3代交易时间 |
| eo_flag | varchar(3) | Y |  | 开平仓标志：3代之后此字段废弃 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| opt_trade_type | varchar(3) | Y |  | 期权交易类型：见tp_public_dict的328 |
| exec_type | varchar(3) | Y |  | 行权方式：见tp_public_dict的324 |
| exec_price | numeric(11,3) | Y |  | 行权价格 |
| exec_date | varchar(8) | Y |  | 行权日 |
| exec_deadline | varchar(8) | Y |  | 行权截止时间 |
| exec_clear_date | varchar(8) | Y |  | 结算日期 |
| opt_amt | numeric(24,6) | Y |  | 期权权利金 |
| opt_total_amt | numeric(24,6) | Y |  | 期权权利金总金额 |
| opt_pay_date | varchar(8) | Y |  | 期权权利金支付日期 |
| delivery_type | varchar(3) | Y |  | 到期结算交割方式/3代结算方式 |
| reference_type | varchar(3) | Y |  | 现金交割参考价格类型/3代现金结算期权参考价格类型：见tp_public_dict的445 |
| reference_price | numeric(11,3) | Y |  | 现金交割参考价格：3代之后此字段废弃 |
| reference_adjust | numeric(11,3) | Y |  | 现金调整项/3代现金结算期权参考价格调整项 |
| reference_date | varchar(8) | Y |  | 现金交割参考价格日期：3代之后此字段废弃 |
| reg_fee_type | varchar(3) | Y |  | 本方登记费率类型：3代之后此字段废弃 |
| reg_fee_rate | numeric(20,2) | Y |  | 本方登记费率：3代之后此字段废弃 |
| reg_fee | numeric(20,2) | Y |  | 本方登记费：3代之后此字段废弃 |
| natural_date | varchar(8) | Y |  | 自然日期：3代 |
| his_update_date | varchar(8) | Y |  | 成交单历史状态记录时间 |
| role | varchar(4) | Y |  | 本方角色：见tp_public_dict的340 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| channel_no | varchar(4) | Y |  | 本方渠道代码 |
| party_role | varchar(4) | Y |  | 对手方角色：见tp_public_dict的340 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| party_channel_no | varchar(4) | Y |  | 对手方渠道代码 |
| match_type | varchar(4) | Y |  | 交易/登记：见tp_public_dict的341 |
| weight | numeric(12,6) | Y |  | 重量（千克） |
| period | varchar(10) | Y |  | 期限 |
| price_unit | varchar(4) | Y |  | 权利金和行权价报价单位：见tp_public_dict的357 |
| pay_status | varchar(4) | Y |  | 权利金支付状态：见tp_public_dict的348 |
| clear_status | varchar(4) | Y |  | 权利金清算信息：见tp_public_dict的355 |
| exec_match_no | varchar(20) | Y |  | 行权交易成交单号 |
| status | varchar(4) | Y |  | 状态：见tp_public_dict的342 |
| exec_status | varchar(4) | Y |  | 行权状态：见tp_public_dict的350 |
| fee_status | varchar(4) | Y |  | 收费状态：见tp_public_dict的343 |
| fee_date | varchar(8) | Y |  | 收费日期：清算收费成功后填写当日日期 |
| act_exec_date | varchar(8) | Y |  | 实际行权日 |
| act_clear_date | varchar(8) | Y |  | 实际结算日期 |
| unit | numeric(10,0) | Y |  | 交易单位 |
| act_pay_date | varchar(8) | Y |  | 实际权利金支付日 |
| offset_opt_amt | numeric(20,2) | Y |  | 平仓权利金 |
| offset_pay_status | varchar(4) | Y |  | 平仓权利金支付状态：见tp_public_dict的348 |
| offset_clear_status | varchar(4) | Y |  | 平仓权利金清算信息：见tp_public_dict的355 |
| offset_pay_date | varchar(8) | Y |  | 平仓权利金支付日 |
| act_offset_pay_date | varchar(8) | Y |  | 实际平仓权利金支付日 |
| offset_fee_status | varchar(4) | Y |  | 平仓收费状态：见tp_public_dict的343 |
| offset_fee_date | varchar(8) | Y |  | 平仓收费日期 |
| storage_no | varchar(4) | Y |  | 指定仓库代码 |
| offset_opt_total_amt | numeric(24,6) | Y |  | 期权平仓权利金总金额 |

---

## 499. dimple.tc_sge_inquire_fee_detail　(9 字段)
> 表含义：询价成交手续费明细：3代　|　估算行数：**10,541**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户代码 |
| fee_date | varchar(8) | Y |  | 收费日期 |
| bus_type | varchar(2) | Y |  | 业务类型：见tp_public_dict的337;1-询价即远掉2-询价期权3-询价拆借 |
| match_no | varchar(20) | Y |  | 成交单编号 |
| eo_flag | varchar(1) | Y |  | 开平标志:见tp_public_dict的003,业务类型为2-询价期权时有用 |
| fee_type | varchar(2) | Y |  | 手续费类型:见tp_public_dict的092 |
| fee_rate | numeric(20,6) | Y |  | 手续费率 |
| fee | numeric(20,2) | Y |  | 手续费 |

---

## 500. dimple.tc_sge_inquire_match　(27 字段)
> 表含义：金交所询价表　|　估算行数：**5,099**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| match_no | varchar(30) | Y |  | 询价即远掉到期清算单编号 |
| bs_flag | varchar(3) | Y |  | 买卖方向 |
| client_id | varchar(10) | Y |  | 客户号 |
| client_type | varchar(3) | Y |  | 客户类型：0自营;1代理 |
| member_id | varchar(8) | Y |  | 会员号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_date | varchar(8) | Y |  | 成交日期 |
| match_time | varchar(8) | Y |  | 成交时间 |
| price | numeric(24,6) | Y |  | 成交价格 |
| qty | numeric(20,3) | Y |  | 成交数量 |
| order_no | varchar(30) | Y |  | 系统报单号 |
| local_order_no | varchar(30) | Y |  | 报单本地委托号 |
| match_type | varchar(3) | Y |  | 类型：1普通 |
| delivery_type | varchar(3) | Y |  | 交割方式：1实物交割;2现金交割 |
| calc_price_type | varchar(3) | Y |  | 参考价格类型：见tp_public_dict的288 |
| calc_price_date | varchar(8) | Y |  | 参考价格日期 |
| calc_price | numeric(24,6) | Y |  | 参考价格 |
| trade_type | varchar(3) | Y |  | 交易类别:0普通1行权 |
| inquire_no | varchar(20) | Y |  | 成交号 |
| fn_flag | varchar(4) | Y |  | 近/远端：见tp_public_dict的250 |
| weight | numeric(24,6) | Y |  | 重量（千克） |
| receive_money | numeric(24,6) | Y |  | 本方收到资金金额(元)：元；本方收到，数值为正；本方支出，数值为负。 |
| receive_weight | numeric(24,6) | Y |  | 本方收到实物重量(千克)：元；本方收到，数值为正；本方支出，数值为负。 |
| if_breach_apply | varchar(4) | Y |  | 是否违约申报：见tp_public_dict的338 |
| clear_status | varchar(4) | Y |  | 清算信息：见tp_public_dict的355 |
| storage_no | varchar(4) | Y |  | 指定仓库代码,白银合约时字段有值 |

---

## 501. dimple.tc_sge_intl_client_money　(25 字段)
> 表含义：金交所国际版-客户资金数据文件　|　估算行数：**329**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| client_id | varchar(16) | N | √ | 客户代码 |
| member_id | varchar(8) | N | √ | 席位代码 |
| remain | numeric(18,2) | Y |  | 当日余额：元 |
| available | numeric(18,2) | Y |  | 当日可提：元 |
| money_out | numeric(18,2) | Y |  | 当日出金：元 |
| money_in | numeric(18,2) | Y |  | 当日入金：元 |
| buy_amount | numeric(18,2) | Y |  | 成交买入金额：元 |
| sell_amount | numeric(18,2) | Y |  | 成交卖岀金额：元 |
| exch_margin | numeric(18,2) | Y |  | 成交交易所保证金：元 |
| member_margin | numeric(18,2) | Y |  | 成交会员保证金：元 |
| delivery_margin | numeric(18,2) | Y |  | 当日交割保证金：元 |
| exch_trade_fee | numeric(18,2) | Y |  | 成交交易所交易费用：元 |
| member_trade_fee | numeric(18,2) | Y |  | 成交会员交易费用：元 |
| other_fee | numeric(18,2) | Y |  | 其他费用：元 |
| break_amt_out | numeric(18,2) | Y |  | 支付违约金：元 |
| break_amt_in | numeric(18,2) | Y |  | 收到违约金：元 |
| profit | numeric(18,2) | Y |  | 盯市盈余：元 |
| frozen_amt | numeric(18,2) | Y |  | 当日冻结资金：元 |
| interest_accumu | numeric(18,2) | Y |  | 利息积数：元 |
| penalty_int_accumu | numeric(18,2) | Y |  | 罚息积数：元 |
| interest | numeric(18,2) | Y |  | 当日入账利息：元 |
| interest_tax | numeric(18,2) | Y |  | 当日入账利息税：元 |
| manual_frozen_amt | numeric(18,2) | Y |  | 当日手工冻结资金：元 |
| penalty_interest | numeric(18,2) | Y |  | 当日入账罚息：元 |

---

## 502. dimple.tc_sge_intl_client_offset　(9 字段)
> 表含义：金交所国际版-客户额度资金数据文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| client_id | varchar(16) | N | √ | 客户代码 |
| member_id | varchar(8) | N | √ | 席位代码 |
| total_offset_quota | numeric(18,2) | Y |  | 当日总充抵额度：元 |
| avail_offset_quota | numeric(18,2) | Y |  | 当日总剩余充抵额度：元 |
| used_quota_exch | numeric(18,2) | Y |  | 当日交易所已用充抵额度：元 |
| used_quota_member | numeric(18,2) | Y |  | 当日会员已用充抵额度：元 |
| avail_quota_exch | numeric(18,2) | Y |  | 当日交易所剩余额度：元 |
| risk_tolerate_limit | numeric(18,2) | Y |  | 风险容忍限额：元 |

---

## 503. dimple.tc_sge_intl_interest_flow　(7 字段)
> 表含义：金交所国际版-结息流水数据文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| seq_no | varchar(18) | N |  | 流水号 |
| client_id | varchar(16) | N |  | 客户代码 |
| member_id | varchar(8) | N |  | 席位代码 |
| interest | numeric(18,2) | Y |  | 当日入账利息：元 |
| interest_tax | numeric(18,2) | Y |  | 当日入账利息税：元 |
| interest_penalty | numeric(18,2) | Y |  | 入账罚息：元；入账利息不包含入账罚息。入账利息、入账罚息分别单独计算 |

---

## 504. dimple.tc_sge_intl_member_money　(9 字段)
> 表含义：金交所国际版-席位资金数据文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| owned_money | numeric(18,2) | Y |  | 自有资金：元，包括自营席位的出入金和对客户收取的手续费 |
| fee_in | numeric(18,2) | Y |  | 当日手续费收入：元 |
| interest | numeric(18,2) | Y |  | 当日入账利息：元 |
| interest_tax | numeric(18,2) | Y |  | 当日入账利息税：元 |
| money_out | numeric(18,2) | Y |  | 当日会员出金：元 |
| money_in | numeric(18,2) | Y |  | 当日会员入金：元 |
| frozen_amt | numeric(18,2) | Y |  | 当日冻结资金 |

---

## 505. dimple.tc_sge_intl_money_io　(12 字段)
> 表含义：金交所国际版-出入金流水数据文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| trade_seq_no | varchar(18) | Y |  | 交易流水号 |
| client_id | varchar(16) | Y |  | 客户代码 |
| member_id | varchar(8) | Y |  | 席位代码 |
| bank_no | varchar(4) | Y |  | 存管行号 |
| bus_type | varchar(2) | Y |  | 业务类型：1-银行转账，5-手工出入金，6-手工调账，7-冻结解冻 |
| bus_flag | varchar(2) | Y |  | 存取方向：1-存入，2-取出 |
| amt | numeric(18,2) | Y |  | 发生金额：元 |
| if_send | varchar(2) | Y |  | 是否发送：见tp_public_dict的027 |
| if_booked | varchar(2) | Y |  | 是否入账：见tp_public_dict的027 |
| bank_seq_no | varchar(30) | Y |  | 银行流水号 |
| bank_date | varchar(8) | Y |  | 银行日期 |

---

## 506. dimple.tc_sge_largeside_instgroup　(6 字段)
> 表含义：金交所：单向大边合约组合数据文件　|　估算行数：**15,398**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| group_no | numeric(10,0) | Y |  | 组合代码 |
| group_name | varchar(30) | Y |  | 组合名称 |
| contract_id | varchar(20) | Y |  | 合约代码 |

---

## 507. dimple.tc_sge_lease_baserate_avg　(12 字段)
> 表含义：租借基准利率和均值　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 序号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| natural_date | varchar(8) | Y |  | 自然日期 |
| variety_id | varchar(1) | Y |  | 品种 |
| period | varchar(2) | Y |  | 期限:见tp_public_dict的353 |
| rate | numeric(20,6) | Y |  | 利率 |
| rise_fall | numeric(20,6) | Y |  | 涨跌 |
| avg_5 | numeric(20,6) | Y |  | 5日均值 |
| avg_10 | numeric(20,6) | Y |  | 10日均值 |
| avg_20 | numeric(20,6) | Y |  | 20日均值 |
| system_date | varchar(8) | Y |  | 发布日期 |
| system_time | varchar(8) | Y |  | 发布时间 |

---

## 508. dimple.tc_sge_lend_fee　(5 字段)
> 表含义：金交所拆借费用合计表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| got_trade_fee | numeric(30,6) | Y |  | 拆借手续费 |
| got_interest | numeric(30,6) | Y |  | 拆借利息 |

---

## 509. dimple.tc_sge_lend_fee_detail　(6 字段)
> 表含义：金交所拆借费用明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 导入日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| got_trade_fee | numeric(30,6) | Y |  | 拆借手续费 |
| got_interest | numeric(30,6) | Y |  | 拆借利息 |

---

## 510. dimple.tc_sge_margin_rate　(8 字段)
> 表含义：SGE交易所保证金率表　|　估算行数：**85,876**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| exch_code | varchar(2) | N |  | 交易所 |
| contract_id | varchar(20) | N |  | 合约代码 |
| margin_type | varchar(3) | N |  | 保证金类型：见tp_public_dict的092 |
| bs_flag | varchar(3) | Y |  | 多空方向：见TP_PUBLIC_DICT的002 |
| margin_rate | numeric(16,6) | N |  | 保证金率 |
| seat_type | varchar(1) | Y |  | 席位性质: 1 主板,2国际版;只金交所使用;见tp_public_dict的332 |

---

## 511. dimple.tc_sge_nonetrade_fee　(3 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| effect_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员代码 |
| nonetrade_trans_fee | numeric(24,6) | Y |  | 非交易过户费 |

---

## 512. dimple.tc_sge_nonetrade_fee_detail　(4 字段)
> 表含义：非交易过户费用明细数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| effect_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| nonetrade_trans_fee | numeric(24,6) | Y |  | 非交易过户费 |

---

## 513. dimple.tc_sge_opt_fee_detail　(4 字段)
> 表含义：期权权利金费用明细数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| opt_fee_amt | numeric(20,2) | Y |  | 权利金金额 |

---

## 514. dimple.tc_sge_opt_fee_total　(3 字段)
> 表含义：期权权利金费用合计　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| opt_fee_amt | numeric(20,2) | Y |  | 权利金金额 |

---

## 515. dimple.tc_sge_opt_imp_vol_curve_quote　(12 字段)
> 表含义：期权隐含波动率曲线报价记录表　|　估算行数：**2,500**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(20) | N | √ | 本方席位号 |
| trader_no | varchar(40) | N |  | 本方交易员号 |
| bid_state | varchar(1) | Y |  | 报单状态;见tp_public_dict的458 |
| quote_time | varchar(22) | N | √ | 报价时间 |
| contract_id | varchar(40) | N | √ | 合约代码 |
| period | varchar(10) | N | √ | 期限：见tp_public_dict的344 |
| bs_flag | varchar(3) | N | √ | 买卖方向：见tp_public_dict的002 |
| urgent_number | numeric(10,0) | N | √ | 报价次数 |
| if_sync_exch | varchar(1) | Y |  | 是否已同步交易所;见tp_public_dict的027 |
| option_delta | numeric(17,8) | Y |  | 波动率，单位% |
| bid_target | varchar(10) | N | √ | 报价标的：见tp_public_dict的457 |
| order_no | varchar(20) | Y |  | 报价编号 |

---

## 516. dimple.tc_sge_origin_breach　(10 字段)
> 表含义：原始违约单　|　估算行数：**422**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| delivery_no | varchar(20) | N | √ | 交割序号 |
| bs_flag | bpchar(1) | N | √ | 买卖方向,见tp_public_dict的002 |
| client_id | varchar(16) | N |  | 客户代码 |
| member_id | varchar(8) | N | √ | 会员代码 |
| contract_id | varchar(20) | N |  | 合约代码 |
| qty | numeric(18,0) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 价格 |
| breach_direct | bpchar(1) | N | √ | 违约方向:见tp_public_dict的220 |
| effect_date | varchar(8) | N | √ | 违约日期 |

---

## 517. dimple.tc_sge_origin_invoicedata　(4 字段)
> 表含义：原始发票相关数据　|　估算行数：**672**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| delivery_no | varchar(20) | N | √ | 交割单号 |
| delivery_no_type | bpchar(1) | N |  | 交割单类型,见tp_public_dict的231 |

---

## 518. dimple.tc_sge_origin_silver_premium　(5 字段)
> 表含义：原始白银品牌升贴水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| trade_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| premium | numeric(18,2) | N |  | 品牌升贴水 |

---

## 519. dimple.tc_sge_predelivery_jour　(12 字段)
> 表含义：预交割单表　|　估算行数：**2,488**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| predelivery_no | varchar(20) | N | √ | 预交割单号 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| apply_date | varchar(8) | Y |  | 申报日期 |
| bs_flag | bpchar(1) | N |  | 买卖标志：见TP_PUBLIC_DICT的002 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(20,6) | Y |  | 数量：3代交割重量(kg) |
| amount | numeric(18,2) | Y |  | 金额 |
| qty_s | numeric(12,0) | Y |  | 交割手数 |

---

## 520. dimple.tc_sge_priceing_delivery　(11 字段)
> 表含义：定价交割单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_no | varchar(20) | Y |  | 交割编号 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| bs_flag | varchar(3) | Y |  | 买卖方向 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 交割价格 |
| delivery_variety_id | varchar(8) | Y |  | 交割品种 |
| qty | numeric(12,0) | Y |  | 交割数量 |
| storage_qty | numeric(16,6) | Y |  | 交割重量 |
| amt | numeric(24,6) | Y |  | 交割金额 |

---

## 521. dimple.tc_sge_priceing_match　(12 字段)
> 表含义：定价成交单　|　估算行数：**948**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | Y |  | 成交编号 |
| bs_flag | varchar(3) | Y |  | 买卖方向 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| match_date | varchar(8) | Y |  | 成交日期 |
| match_time | varchar(8) | Y |  | 成交时间 |
| match_round | numeric(6,0) | Y |  | 成交轮次 |
| match_session | varchar(3) | Y |  | 成交场次 |
| app_type | varchar(3) | Y |  | 申报类型 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |

---

## 522. dimple.tc_sge_priceing_quot　(18 字段)
> 表含义：定价定盘价　|　估算行数：**32,935**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | Y |  | 合约号 |
| contract_name | varchar(18) | Y |  | 合约名称 |
| session_id | varchar(10) | Y |  | 场次编号 |
| session_name | varchar(60) | Y |  | 场次名称 |
| reference_price | numeric(20,8) | Y |  | 参考价 |
| report_time | varchar(8) | Y |  | 参考价报入时间 |
| traded_lots | numeric(12,0) | Y |  | 成交手数 |
| traded_volume | numeric(16,6) | Y |  | 成交重量 |
| buy_lots | numeric(12,0) | Y |  | 买成交手数 |
| buy_volume | numeric(16,6) | Y |  | 买成交重量 |
| sell_lots | numeric(12,0) | Y |  | 卖成交手数 |
| sell_volume | numeric(16,6) | Y |  | 卖成交重量 |
| fix_price | numeric(20,8) | Y |  | 定盘价 |
| if_settleprice | varchar(3) | Y |  | 是否是结算价 |
| month_avg_price | numeric(20,8) | Y |  | 月均价 |
| month_volume | numeric(16,6) | Y |  | 月成交量 |
| year_avg_price | numeric(20,8) | Y |  | 年均价 |
| quot_date | varchar(8) | Y |  | 行情日期 |

---

## 523. dimple.tc_sge_quote_client_settle　(9 字段)
> 表含义：导入表:报价市场客户结算清单数据文件　|　估算行数：**181**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | N |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| fee | numeric(20,2) | Y |  | 手续费：单位元；当收费模式为1-对报价商收费时：对于报价商，为报价商手续费，对于非报价商，为0；当模式为2-对点价客户收费时，均为报价交易手续费 |
| profit | numeric(20,2) | Y |  | 交易盈亏：单位元 |
| margin | numeric(20,2) | Y |  | 保证金：单位元 |
| interest | numeric(20,2) | Y |  | 仓息：单位元 |

---

## 524. dimple.tc_sge_quote_fee_mode　(3 字段)
> 表含义：导入表:报价市场手续费收取模式数据文件　|　估算行数：**2,517**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| fee_mode | varchar(3) | Y |  | 收费模式:1-对报价商收费，2-对点价客户收费 |

---

## 525. dimple.tc_sge_quote_interest_rate　(7 字段)
> 表含义：导入表:报价仓息费率数据文件　|　估算行数：**14,256**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| direction | varchar(1) | Y |  | 多空方向:见tp_public_dict的128 |
| interval_days | numeric(10,0) | Y |  | 间隔天数：单位天 |
| fee_rate | numeric(16,6) | Y |  | 费率 |

---

## 526. dimple.tc_sge_quote_match　(12 字段)
> 表含义：导入表:报价保证金交易成交单数据文件　|　估算行数：**7,567**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| match_no | varchar(20) | N |  | 报价成交编号 |
| bs_flag | varchar(3) | N |  | 买卖方向:见tp_public_dict的002 |
| client_id | varchar(16) | Y |  | 客户代码 |
| member_id | varchar(8) | N |  | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编码 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| price | numeric(20,8) | Y |  | 价格：目前铂金和钯金相关合约单位是元/克 |
| qty | numeric(12,0) | Y |  | 数量：手 |
| order_no | varchar(20) | Y |  | 报价报单号 |
| local_order_no | varchar(20) | Y |  | 报价本地报单号 |

---

## 527. dimple.tc_sge_quote_net_posi　(7 字段)
> 表含义：导入表:报价市场报价商头寸轧差数据文件　|　估算行数：**66**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | N |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| bs_flag | varchar(3) | N |  | 买卖方向:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 成交量：单位手 |

---

## 528. dimple.tc_sge_quoter_fee_rate　(7 字段)
> 表含义：导入表:报价市场报价商手续费率数据文件　|　估算行数：**390**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| seat_type | varchar(3) | Y |  | 席位性质:见tp_public_dict的332 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| unit | varchar(3) | Y |  | 点数单位:1-分/克，2-分/千克 |
| dealer_fee_rate | numeric(18,0) | Y |  | 报价商手续费点数 |
| agent_fee_rate | numeric(18,0) | Y |  | 报价代理佣金点数 |

---

## 529. dimple.tc_sge_reclear_money_detail　(7 字段)
> 表含义：二次清算费用明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户编码 |
| weight_diff | numeric(18,2) | Y |  | 重量溢短 |
| variety_agio | numeric(18,2) | Y |  | 品种升贴水 |
| item_agio | numeric(18,2) | Y |  | 条块升贴水 |
| sum_agio | numeric(18,2) | Y |  | 升贴水合计 |

---

## 530. dimple.tc_sge_reclear_money_total　(6 字段)
> 表含义：二次清算费用合计　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 会员号 |
| weight_diff | numeric(18,2) | Y |  | 重量溢短 |
| variety_agio | numeric(18,2) | Y |  | 品种升贴水 |
| item_agio | numeric(18,2) | Y |  | 条块升贴水 |
| sum_agio | numeric(18,2) | Y |  | 升贴水合计 |

---

## 531. dimple.tc_sge_rfq_adjust_posi_detail　(12 字段)
> 表含义：保证金询价交易调仓单数据文件　|　估算行数：**21**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 调仓成交单编号 |
| bs_flag | varchar(1) | N |  | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | N |  | 成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |

---

## 532. dimple.tc_sge_rfq_due_settle　(16 字段)
> 表含义：保证金询价到期清算单数据文件　|　估算行数：**311**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_no | varchar(20) | N |  | 到期清算单编号 |
| trade_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| due_date | varchar(8) | Y |  | 到期日 |
| bs_flag | varchar(1) | N |  | 买卖方向：public_dict的002 |
| price | numeric(20,8) | Y |  | 交割价格 |
| qty | numeric(12,0) | Y |  | 交割数量 |
| weight | numeric(20,8) | Y |  | 交割重量：千克 |
| amt | numeric(18,2) | Y |  | 交割金额：元 |
| real_qty | numeric(12,0) | Y |  | 实际交割数量 |
| real_weight | numeric(20,8) | Y |  | 实际交割重量：千克 |
| real_amt | numeric(18,2) | Y |  | 实际交割金额：元 |
| if_breach_apply | varchar(1) | Y |  | 是否违约申报：见tp_public_dict的027 |
| breach_qty | numeric(12,0) | Y |  | 违约申报数量 |

---

## 533. dimple.tc_sge_rfq_margin_rate　(6 字段)
> 表含义：保证金询价席位保证金率数据文件　|　估算行数：**1,599**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| seat_type | varchar(1) | Y |  | 席位性质:见tp_public_dict的332 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| uniltr_margin_rate | numeric(16,6) | Y |  | 单边保证金率：元/手 |
| swap_margin_rate | numeric(16,6) | Y |  | 掉期保证金率：元/手 |

---

## 534. dimple.tc_sge_rfq_match　(26 字段)
> 表含义：保证金询价交易成交单数据文件　|　估算行数：**2,485**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 成交编号 |
| bs_flag | varchar(1) | N |  | 买卖方向：public_dict的002 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| trade_date | varchar(8) | Y |  | 成交日期 |
| offline_date | varchar(8) | Y |  | 线下成交日期 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 成交价格：黄金-元/克 |
| qty | numeric(12,0) | Y |  | 成交数量：手 |
| match_weight | numeric(16,6) | Y |  | 成交重量：千克 |
| due_date | varchar(8) | Y |  | 到期日 |
| period | varchar(8) | Y |  | 期限名 |
| trade_reg | varchar(1) | Y |  | 交易登记：见tp_public_dict的341 |
| trade_type | varchar(1) | Y |  | 交易类型：见tp_public_dict的253 |
| match_type | varchar(1) | Y |  | 成交类型：见tp_public_dict的436 |
| fn_flag | varchar(1) | Y |  | 近远端：见tp_public_dict的250 |
| related_swap_no | varchar(20) | Y |  | 关联掉期编号 |
| due_date_type | varchar(1) | Y |  | 到期日类型：见tp_public_dict的437 |
| force_flag | varchar(1) | Y |  | 强平标志：见tp_public_dict的027 |
| order_no | varchar(20) | Y |  | 报单编号 |
| sge_trader_no | varchar(10) | Y |  | 交易员代码 |
| broker_no | varchar(10) | Y |  | 经纪机构代码 |
| channel_no | varchar(8) | Y |  | 交易来源渠道 |
| local_order_no | varchar(20) | Y |  | 本地报单编号 |

---

## 535. dimple.tc_sge_rfq_posi　(8 字段)
> 表含义：席位保证金询价持仓数据文件　|　估算行数：**2,430**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| due_date | varchar(8) | Y |  | 到期日 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| net_qty | numeric(12,0) | Y |  | 净持仓 |

---

## 536. dimple.tc_sge_rfq_settle_price　(5 字段)
> 表含义：保证金询价结算价数据文件　|　估算行数：**468,778**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N |  | 合约代码 |
| due_date | varchar(8) | N |  | 到期日 |
| clear_price | numeric(20,8) | Y |  | 结算价：黄金-元/克 |

---

## 537. dimple.tc_sge_rfq_trade_fee_detail　(6 字段)
> 表含义：保证金询价手续费明细单数据文件　|　估算行数：**2,607**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N |  | 成交编号 |
| bs_flag | varchar(1) | N |  | 买卖方向：public_dict的002 |
| trade_fee | numeric(18,2) | Y |  | 手续费：元 |
| fee_rate | numeric(18,6) | Y |  | 手续费率：元/手 |
| trade_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 席位代码 |

---

## 538. dimple.tc_sge_setoff_apply_detail　(23 字段)
> 表含义：SGE充抵申请明细表　|　估算行数：**54**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| import_date | varchar(8) | Y |  | 导入日期 |
| apply_no | varchar(20) | Y |  | 充抵申请单编号 |
| apply_date | varchar(8) | Y |  | 充抵申请日期 |
| apply_time | varchar(8) | Y |  | 充抵申请时间 |
| member_id | varchar(8) | Y |  | 申请会员代码 |
| client_id | varchar(16) | Y |  | 申请客户代码 |
| setoff_variety_id | varchar(10) | Y |  | 充抵申请物代码 |
| setoff_variety_abbr | varchar(30) | Y |  | 充抵申请物简称 |
| setoff_variety_type | varchar(1) | Y |  | 充抵申请物类型代码 |
| apply_qty | numeric(16,2) | Y |  | 充抵申请物数量 |
| effective_qty | numeric(16,2) | Y |  | 充抵申请物有效数量 |
| apply_deli_qty | numeric(16,2) | Y |  | 充抵申请物转交割数量 |
| breach_qty | numeric(16,2) | Y |  | 违约处置数量 |
| due_qty | numeric(16,2) | Y |  | 充抵到期数量 |
| due_date | varchar(8) | Y |  | 充抵到期日 |
| real_due_date | varchar(8) | Y |  | 实际充抵到期日 |
| submit_date | varchar(9) | Y |  | 提交日期 |
| status | varchar(4) | Y |  | 状态:见tp_public_dict的333 |
| fee_date | varchar(8) | Y |  | 计费日期 |
| fee_rate | numeric(10,6) | Y |  | 充抵手续费率 |
| fee | numeric(18,2) | Y |  | 充抵手续费 |
| setoff_value | numeric(18,2) | Y |  | 充抵申请物估价金额 |
| setoff_discount_value | numeric(18,2) | Y |  | 充抵申请物折后金额 |

---

## 539. dimple.tc_sge_setoff_fee_detail　(4 字段)
> 表含义：充抵费用明细数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| effect_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户编号 |
| setoff_fee | numeric(20,2) | Y |  | 充抵手续费 |

---

## 540. dimple.tc_sge_shfe_storage_jour　(4 字段)
> 表含义：交易所库存流水业务对应表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date1 | varchar(8) | N |  | 交易日期1 |
| exch_seq_no1 | varchar(10) | N |  | 交易所库存流水1 |
| trade_date2 | varchar(8) | N |  | 交易日期2 |
| exch_seq_no2 | varchar(10) | N |  | 交易所库存流水2 |

---

## 541. dimple.tc_sge_silver_delivery_jour　(13 字段)
> 表含义：白银交割单表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_no | varchar(16) | N | √ | 交割单号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志：见TP_PUBLIC_DICT的002 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| price | numeric(20,8) | Y |  | 交割交割 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| delivery_variety_id | varchar(3) | N |  | 交割品种号 |
| std_qty | numeric(10,0) | Y |  | 标准数量 |
| std_amount | numeric(18,2) | Y |  | 标准金额 |
| real_qty | numeric(16,6) | Y |  | 实际数量 |
| real_amount | numeric(18,2) | Y |  | 实际金额 |
| warehouse_id | bpchar(4) | Y |  | 意向仓库号 |

---

## 542. dimple.tc_sge_storage_orgin　(16 字段)
> 表含义：金交所库存流水原始表　|　估算行数：**3,397**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 交易日期_Dimple |
| trade_date | varchar(8) | Y |  | 交易日期_Sge |
| seq_no | float8 | Y |  | 流水号 |
| sheet_no | varchar(20) | Y |  | 单据编号 |
| client_id | varchar(20) | Y |  | 客户号 |
| member_id | varchar(8) | Y |  | 会员号 |
| account_type | varchar(3) | Y |  | 客户类型 |
| trans_type | varchar(3) | Y |  | 库存变化类型:见tp_public_dict的221 |
| delivery_variety_id | varchar(4) | Y |  | 交割品种代码 |
| storage_flag | varchar(8) | Y |  | 仓库代码 |
| std_qty | numeric(20,6) | Y |  | 发生标准重量 |
| ture_qty | numeric(20,6) | Y |  | 发生实际重量 |
| remain_qty | numeric(20,6) | Y |  | 剩余重量 |
| trans_date | varchar(8) | Y |  | 发生日期 |
| trans_time | varchar(8) | Y |  | 发生时间 |
| ins_dt | varchar(20) | Y |  | 记录日期 |

---

## 543. dimple.tc_sge_swap_fee　(4 字段)
> 表含义：库存互换费用合计　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| effect_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员代码 |
| swap_fee | numeric(24,6) | Y |  | 库存互换费 |
| swap_trans_fee | numeric(24,6) | Y |  | 库存互换过户费 |

---

## 544. dimple.tc_sge_swap_fee_detail　(5 字段)
> 表含义：库存互换费用明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| effect_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 会员代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| swap_fee | numeric(24,6) | Y |  | 库存互换费 |
| swap_trans_fee | numeric(24,6) | Y |  | 库存互换过户费 |

---

## 545. dimple.tc_sh_com_future_save　(28 字段)
> 表含义：上海银行Com Future供数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| trade_type | varchar(40) | Y |  | 数据所属交易类型 |
| type | varchar(10) | Y |  | 业务类型 |
| buysell | varchar(4) | Y |  | 买卖方向 |
| futurelabel | varchar(20) | Y |  | FUTURELABEL |
| maturitylabel | varchar(10) | Y |  | MATURITYLABEL |
| quotationlabel | varchar(29) | Y |  | QUOTATIONLABEL |
| quantity | numeric(24,8) | Y |  | 成交量 |
| price | numeric(24,8) | Y |  | 成交价 |
| strategy | varchar(10) | Y |  | 买卖方向和开平标志 |
| usage | varchar(50) | Y |  | 金交所席位 |
| tradeglobalid | varchar(20) | N | √ | 流水号 |
| ourportfolio | varchar(35) | Y |  | 投组 |
| theirname | varchar(35) | Y |  | 交易对手方 |
| tradedate | varchar(8) | Y |  | 交易日期 |
| sourcemodule | varchar(22) | Y |  | 来源模块 |
| settlementmethod | varchar(22) | Y |  | 结算方式 |
| udfcharacterlabels | varchar(50) | Y |  | UDF字符标签 |
| udfcharactervalues | varchar(200) | Y |  | UDF字符值 |
| udfnumericlabels | varchar(20) | Y |  | UDF数值标签 |
| udfnumericvalues | varchar(20) | Y |  | UDF数值值 |
| udfdatelabels | varchar(20) | Y |  | UDF日期标签 |
| udfdatevalues | varchar(20) | Y |  | UDF日期值 |
| trader | varchar(22) | Y |  | 交易员姓名 |
| purpose | varchar(10) | Y |  | 目的 |
| isoversea | varchar(1) | Y |  | 是否为境外产品 |
| cuser | varchar(10) | Y |  | 用户 |
| cgroup | varchar(10) | Y |  | 组 |

---

## 546. dimple.tc_sh_com_spot_fwd_save　(39 字段)
> 表含义：上海银行Com Spot Fwd供数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| trade_type | varchar(40) | Y |  | 数据所属交易类型 |
| type | varchar(10) | Y |  | 业务类型 |
| instrument | varchar(20) | Y |  | 合约 |
| currency | varchar(3) | Y |  | 近端买入币种 |
| unit | varchar(25) | Y |  | 单位 |
| buysell | varchar(4) | Y |  | 买卖方向 |
| nominal | numeric(24,8) | Y |  | 近端买入量 |
| price | numeric(21,8) | Y |  | 成交价 |
| price2 | numeric(21,8) | Y |  | 成交价2 |
| location | varchar(20) | Y |  | LOCATION |
| quality | varchar(20) | Y |  | 质量 |
| settlementmode | varchar(20) | Y |  | 交割方式 |
| settlementdate | varchar(8) | Y |  | 现金交割日期 |
| cindex | varchar(50) | Y |  | INDEX |
| archivingseries | varchar(50) | Y |  | 近端参考价格类型 |
| archivingseries2 | varchar(50) | Y |  | 远端参考价格类型 |
| archivingrefdate | varchar(8) | Y |  | 交割价格参考日期 |
| archivingrefdate2 | varchar(8) | Y |  | 交割价格参考日期2 |
| deliverydate | varchar(8) | Y |  | 近端到期交割日 |
| deliverydate2 | varchar(8) | Y |  | 远端到期交割日 |
| usage | varchar(50) | Y |  | 金交所席位 |
| tradeglobalid | varchar(40) | N | √ | 流水号 |
| ourportfolio | varchar(35) | Y |  | 投组 |
| theirname | varchar(35) | Y |  | 交易对手方 |
| tradedate | varchar(8) | Y |  | 交易日期 |
| sourcemodule | varchar(22) | Y |  | 来源模块 |
| settlementmethod | varchar(22) | Y |  | 结算方式 |
| udfcharacterlabels | varchar(50) | Y |  | UDF字符标签 |
| udfcharactervalues | varchar(200) | Y |  | UDF字符值 |
| udfnumericlabels | varchar(20) | Y |  | UDF数值标签 |
| udfnumericvalues | varchar(20) | Y |  | UDF数值值 |
| udfdatelabels | varchar(20) | Y |  | UDF日期标签 |
| udfdatevalues | varchar(20) | Y |  | UDF日期值 |
| trader | varchar(22) | Y |  | 交易员姓名 |
| purpose | varchar(10) | Y |  | 目的 |
| isoversea | varchar(1) | Y |  | 是否为境外产品 |
| cuser | varchar(10) | Y |  | 用户 |
| cgroup | varchar(10) | Y |  | 组 |

---

## 547. dimple.tc_sh_crmsdata　(14 字段)
> 表含义：CRMS数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_date | varchar(8) | N |  | 交易日期 |
| bill_no | varchar(30) | Y |  | 信贷出帐号 |
| currency | varchar(3) | Y |  | 币种 |
| subject | varchar(80) | Y |  | 科目 |
| remain_qty | numeric(16,6) | Y |  | 黄金余额(克) |
| branches | varchar(20) | Y |  | 网点号 |
| reg_date | varchar(8) | Y |  | 起始日期 |
| due_date | varchar(8) | Y |  | 到期日期 |
| account | varchar(30) | Y |  | 账号 |
| account_name | varchar(60) | Y |  | 账户名称 |
| create_date | varchar(8) | Y |  | 生成日期 (自然日) |
| status | varchar(3) | Y |  | 处理状态 见tp_public_dict的277 ； 0未发送  1 发送成功 2发送失败 |
| sysno | varchar(40) | N |  | 系统编号 |
| member_id | varchar(8) | Y |  | 会员号 |

---

## 548. dimple.tc_sh_delivery_save　(29 字段)
> 表含义：上海银行Delivery供数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| trade_type | varchar(40) | Y |  | 数据所属交易类型 |
| type | varchar(10) | Y |  | 业务类型 |
| buysell | varchar(4) | Y |  | 买卖方向 |
| futurelabel | varchar(20) | Y |  | FUTURELABEL |
| maturitylabel | varchar(10) | Y |  | MATURITYLABEL |
| quotationlabel | varchar(29) | Y |  | QUOTATIONLABEL |
| quantity | numeric(24,8) | Y |  | 成交量 |
| price | numeric(24,8) | Y |  | 成交价格 |
| strategy | varchar(10) | Y |  | 买卖方向和开平标志 |
| usage | varchar(10) | Y |  | 金交所席位 |
| instrument | varchar(20) | Y |  | INSTRUMENT |
| tradeglobalid | varchar(20) | N | √ | 流水号 |
| ourportfolio | varchar(35) | Y |  | 投组 |
| theirname | varchar(35) | Y |  | 交易对手方 |
| tradedate | varchar(8) | Y |  | 交易日期 |
| sourcemodule | varchar(22) | Y |  | 来源模块 |
| settlementmethod | varchar(22) | Y |  | 结算方式 |
| udfcharacterlabels | varchar(50) | Y |  | UDF字符标签 |
| udfcharactervalues | varchar(200) | Y |  | UDF字符值 |
| udfnumericlabels | varchar(20) | Y |  | UDF数值标签 |
| udfnumericvalues | varchar(20) | Y |  | UDF数值值 |
| udfdatelabels | varchar(20) | Y |  | UDF日期标签 |
| udfdatevalues | varchar(20) | Y |  | UDF日期值 |
| trader | varchar(22) | Y |  | 交易员姓名 |
| purpose | varchar(10) | Y |  | 目的 |
| isoversea | varchar(1) | Y |  | 是否为境外产品 |
| cuser | varchar(10) | Y |  | 用户 |
| cgroup | varchar(10) | Y |  | 组 |

---

## 549. dimple.tc_sh_foreign_inq_strategy　(5 字段)
> 表含义：境外交易策略信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| strategy_no | varchar(100) | N | √ | 交易策略序号 |
| strategy_id | varchar(255) | N | √ | 交易策略代码 |
| state | varchar(3) | Y |  | 状态 474 |
| isdefault | varchar(3) | Y |  | 是否默认 |
| op_date | varchar(9) | Y |  | 操作日期 |

---

## 550. dimple.tc_sh_loan_deposit_save　(33 字段)
> 表含义：上海银行Loan Deposit供数表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| trade_type | varchar(40) | Y |  | 数据所属交易类型 |
| type | varchar(20) | Y |  | 业务类型 |
| optionfamily | varchar(35) | Y |  | OPTIONFAMILY |
| lnbrnature | varchar(15) | Y |  | LNBRNATURE |
| paymentccy | varchar(3) | Y |  | 付款货币 |
| lendorborrow | varchar(15) | Y |  | 拆借方向 |
| nominalamount | numeric(21,8) | Y |  | 重量 |
| startdate | varchar(8) | Y |  | 起息日 |
| maturitydate | varchar(8) | Y |  | 到期日 |
| unitprice | numeric(21,8) | Y |  | 单位成交价格 |
| rate | numeric(21,8) | Y |  | 利率 |
| generator | varchar(35) | Y |  | 付息方式 |
| generatorrateconvension | varchar(35) | Y |  | 计息基准 |
| usage | varchar(50) | Y |  | 金交所席位 |
| rolldate | varchar(8) | Y |  | 首次付息日 |
| tradeglobalid | varchar(40) | N | √ | 流水号 |
| ourportfolio | varchar(35) | Y |  | 投组 |
| theirname | varchar(35) | Y |  | 交易对手方 |
| tradedate | varchar(8) | Y |  | 交易日期 |
| sourcemodule | varchar(22) | Y |  | 来源模块 |
| settlementmethod | varchar(22) | Y |  | 结算方式 |
| udfcharacterlabels | varchar(50) | Y |  | UDF字符标签 |
| udfcharactervalues | varchar(200) | Y |  | UDF字符值 |
| udfnumericlabels | varchar(20) | Y |  | UDF数值标签 |
| udfnumericvalues | varchar(20) | Y |  | UDF数值值 |
| udfdatelabels | varchar(20) | Y |  | UDF日期标签 |
| udfdatevalues | varchar(20) | Y |  | UDF日期值 |
| trader | varchar(22) | Y |  | 交易员姓名 |
| purpose | varchar(10) | Y |  | 目的 |
| isoversea | varchar(1) | Y |  | 是否为境外产品 |
| cuser | varchar(10) | Y |  | 用户 |
| cgroup | varchar(10) | Y |  | 组 |

---

## 551. dimple.tc_sh_trade_strategy　(9 字段)
> 表含义：交易与交易策略关联关系表　|　估算行数：**102**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| trader_no | varchar(40) | N | √ | 交易员 |
| sheet_no | varchar(20) | N | √ | 业务单据号：上期所、上金所竞价业务，业务单据号为“本地委托单编号”；境外贵金属询价业务，业务单据号为“成交单编号”；USD/CNY业务，业务单据号为“成交单编号” |
| trade_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的001 |
| contract_id | varchar(20) | N | √ | 合约代码：上期所期货、上金所递延竞价交易，使用标准合约代码；境外贵金属询价业务，合约代码为XAU/USD、XAG/USD、Phy-Gold |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| strategy_id | varchar(255) | Y |  | 交易策略代码：由量化系统直接传入，dimple只做数据转存不做处理 |
| note | varchar(20) | Y |  | 备注：由量化系统直接传入，dimple只做数据转存不做处理 |

---

## 552. dimple.tc_sh_trade_strategy_jour　(9 字段)
> 表含义：交易与交易策略关联关系历史表　|　估算行数：**452**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| trader_no | varchar(40) | N | √ | 交易员 |
| sheet_no | varchar(20) | N | √ | 业务单据号：上期所、上金所竞价业务，业务单据号为“本地委托单编号”；境外贵金属询价业务，业务单据号为“成交单编号”；USD/CNY业务，业务单据号为“成交单编号” |
| trade_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的001 |
| contract_id | varchar(20) | N | √ | 合约代码：上期所期货、上金所递延竞价交易，使用标准合约代码；境外贵金属询价业务，合约代码为XAU/USD、XAG/USD、Phy-Gold |
| fn_flag | varchar(3) | N | √ | 远近端：见tp_public_dict的250 |
| strategy_id | varchar(255) | Y |  | 交易策略代码：由量化系统直接传入，dimple只做数据转存不做处理 |
| note | varchar(20) | Y |  | 备注：由量化系统直接传入，dimple只做数据转存不做处理 |

---

## 553. dimple.tc_shbank_send_jour　(13 字段)
> 表含义：上海银行T24接口发送流水　|　估算行数：**76**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_date | varchar(8) | N | √ | 日期 |
| batch_no | varchar(40) | Y |  | 批次号 |
| local_seq_no | varchar(18) | N | √ | 本地流水号 |
| uuid | varchar(40) | N | √ | 唯一识别码UUID |
| glblsrlno | varchar(30) | Y |  | 全局流水号:交易日期(8位：YYYYMMDD)+应用编号(3位)+子应用编号(3位) +集群编号(2位) +流水序号(右对齐12位,不足补0) |
| cnsmrsysid | varchar(8) | Y |  | 消费方系统标识,固定GTM |
| cnltxncd | varchar(8) | Y |  | 渠道交易码字 |
| sumflag | varchar(3) | Y |  | 是否外围合并记账:是-“Y”,否-空 |
| resultcode | varchar(20) | Y |  | 操作返回码 |
| resultmsg | varchar(200) | Y |  | 操作返回信息 |
| main_no | varchar(40) | Y |  | 主机流水号 |
| command_type | varchar(40) | Y |  | 操作指令 |
| remark | varchar(255) | Y |  | 摘要 |

---

## 554. dimple.tc_shfe_client_storage_jour　(24 字段)
> 表含义：SHFE客户库存流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| trans_type | varchar(2) | Y |  | 库存变化类型:见tp_public_dict的221 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(16,4) | Y |  | 数量:kg |
| amt | numeric(24,6) | Y |  | 原发票金额 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |
| real_alloy | varchar(8) | Y |  | 实际成色 |
| stock_source | bpchar(1) | Y |  | 出入库性质,见tp_public_dict的236 |
| trader_no | varchar(30) | Y |  | 交易员 |
| contract_id | varchar(20) | Y |  | 合约号 |
| variety_type | varchar(3) | Y |  | 品种类型:1:AU；2:AG |
| trade_type | varchar(3) | Y |  | 交易类型:见tp_public_dict的266 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| client_account_no | varchar(20) | Y |  | 客户帐号 |
| org | varchar(6) | Y |  | 帐务机构号 |
| bus_code | varchar(6) | Y |  | 业务代号 |
| if_reverse_entry | varchar(3) | Y |  | 是否红冲：1是/0否 见tp_public_dict的027 |
| client_id_dk | varchar(16) | Y |  | 代客客户号 |
| accounts_type | varchar(20) | Y |  | 投机套保:1-投机,3-保值 见tp_public_dict的004 |

---

## 555. dimple.tc_shfe_contract_para　(108 字段)
> 表含义：上期所合约结算参数　|　估算行数：**969,643**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| product_id | varchar(8) | Y |  | 产品代码 |
| udly_contract_id | varchar(30) | Y |  | 合约标的物 |
| unit | numeric(5,0) | Y |  | 合约数量乘数 |
| op_trade_type | varchar(1) | Y |  | 期权类型 |
| clear_price | numeric(12,2) | Y |  | 结算价 |
| bspec_long_margin_r | numeric(17,8) | Y |  | 代理投机多头保证金率 |
| bspec_short_margin_r | numeric(17,8) | Y |  | 代理投机空头保证金率 |
| bhedge_long_margin_r | numeric(17,8) | Y |  | 代理套保多头保证金率 |
| bhedge_short_margin_r | numeric(17,8) | Y |  | 代理套保空头保证金率 |
| hspec_long_margin_r | numeric(17,8) | Y |  | 自营投机多头保证金率 |
| hspec_short_margin_r | numeric(17,8) | Y |  | 自营投机空头保证金率 |
| hhedge_long_margin_r | numeric(17,8) | Y |  | 自营套保多头保证金率 |
| hhedge_short_margin_r | numeric(17,8) | Y |  | 自营套保空头保证金率 |
| mspec_long_margin_r | numeric(17,8) | Y |  | 做市商投机多头保证金率 |
| mspec_short_margin_r | numeric(17,8) | Y |  | 做市商投机空头保证金率 |
| mhedge_long_margin_r | numeric(17,8) | Y |  | 做市商套保多头保证金率 |
| mhedge_short_margin_r | numeric(17,8) | Y |  | 做市商套保空头保证金率 |
| bspec_long_dmargin_r | numeric(17,8) | Y |  | 代理投机多头交割保证金率 |
| bspec_short_dmargin_r | numeric(17,8) | Y |  | 代理投机空头交割保证金率 |
| bhedge_long_dmargin_r | numeric(17,8) | Y |  | 代理套保多头交割保证金率 |
| bhedge_short_dmargin_r | numeric(17,8) | Y |  | 代理套保多头交割保证金率 |
| hspec_long_dmargin_r | numeric(17,8) | Y |  | 自营投机多头交割保证金率 |
| hspec_short_dmargin_r | numeric(17,8) | Y |  | 自营投机空头交割保证金率 |
| hhedge_long_dmargin_r | numeric(17,8) | Y |  | 自营套保多头交割保证金率 |
| hhedge_short_dmargin_r | numeric(17,8) | Y |  | 自营套保空头交割保证金率 |
| mspec_long_dmargin_r | numeric(17,8) | Y |  | 做市商投机多头交割保证金率 |
| mspec_short_dmargin_r | numeric(17,8) | Y |  | 做市商投机空头交割保证金率 |
| mhedge_long_dmargin_r | numeric(17,8) | Y |  | 做市商套保多头交割保证金率 |
| mhedge_short_dmargin_r | numeric(17,8) | Y |  | 做市商套保空头交割保证金率 |
| vat_invoice_margin_rate | numeric(17,8) | Y |  | 增值税发票保证金率 |
| bspec_long_fee_r | numeric(17,8) | Y |  | 代理投机多头交易手续费率 |
| bspec_long_fee_u | numeric(12,2) | Y |  | 代理投机多头交易手续费单价 |
| bspec_short_fee_r | numeric(17,8) | Y |  | 代理投机空头交易手续费率 |
| bspec_short_fee_u | numeric(12,2) | Y |  | 代理投机空头交易手续费单价 |
| bhedge_long_fee_r | numeric(17,8) | Y |  | 代理套保多头交易手续费率 |
| bhedge_long_fee_u | numeric(12,2) | Y |  | 代理套保多头交易手续费单价 |
| bhedge_short_fee_r | numeric(17,8) | Y |  | 代理套保空头交易手续费率 |
| bhedge_short_fee_u | numeric(12,2) | Y |  | 代理套保空头交易手续费单价 |
| hspec_long_fee_r | numeric(17,8) | Y |  | 自营投机多头交易手续费率 |
| hspec_long_fee_u | numeric(12,2) | Y |  | 自营投机多头交易手续费单价 |
| hspec_short_fee_r | numeric(17,8) | Y |  | 自营投机空头交易手续费率 |
| hspec_short_fee_u | numeric(12,2) | Y |  | 自营投机空头交易手续费单价 |
| hhedge_long_fee_r | numeric(17,8) | Y |  | 自营套保多头交易手续费率 |
| hhedge_long_fee_u | numeric(12,2) | Y |  | 自营套保多头交易手续费单价 |
| hhedge_short_fee_r | numeric(17,8) | Y |  | 自营套保空头交易手续费率 |
| hhedge_short_fee_u | numeric(12,2) | Y |  | 自营套保空头交易手续费单价 |
| mspec_long_fee_r | numeric(17,8) | Y |  | 做市商投机多头交易手续费率 |
| mspec_long_fee_u | numeric(12,2) | Y |  | 做市商投机多头交易手续费单价 |
| mspec_short_fee_r | numeric(17,8) | Y |  | 做市商投机空头交易手续费率 |
| mspec_short_fee_u | numeric(12,2) | Y |  | 做市商投机空头交易手续费单价 |
| mhedge_long_fee_r | numeric(17,8) | Y |  | 做市商套保多头交易手续费率 |
| mhedge_long_fee_u | numeric(12,2) | Y |  | 做市商套保多头交易手续费单价 |
| mhedge_short_fee_r | numeric(17,8) | Y |  | 做市商套保空头交易手续费率 |
| mhedge_short_fee_u | numeric(12,2) | Y |  | 做市商套保空头交易手续费单价 |
| bspec_long_cfee_r | numeric(17,8) | Y |  | 代理投机多头平今手续费率 |
| bspec_long_cfee_u | numeric(12,2) | Y |  | 代理投机多头平今手续费单价 |
| bspec_short_cfee_r | numeric(17,8) | Y |  | 代理投机空头平今手续费率 |
| bspec_short_cfee_u | numeric(12,2) | Y |  | 代理投机空头平今手续费单价 |
| bhedge_long_cfee_r | numeric(17,8) | Y |  | 代理套保多头平今手续费率 |
| bhedge_long_cfee_u | numeric(12,2) | Y |  | 代理套保多头平今手续费单价 |
| bhedge_short_cfee_r | numeric(17,8) | Y |  | 代理套保空头平今手续费率 |
| bhedge_short_cfee_u | numeric(12,2) | Y |  | 代理套保空头平今手续费单价 |
| hspec_long_cfee_r | numeric(17,8) | Y |  | 自营投机多头平今手续费率 |
| hspec_long_cfee_u | numeric(12,2) | Y |  | 自营投机多头平今手续费单价 |
| hspec_short_cfee_r | numeric(17,8) | Y |  | 自营投机空头平今手续费率 |
| hspec_short_cfee_u | numeric(12,2) | Y |  | 自营投机空头平今手续费单价 |
| hhedge_long_cfee_r | numeric(17,8) | Y |  | 自营套保多头平今手续费率 |
| hhedge_long_cfee_u | numeric(12,2) | Y |  | 自营套保多头平今手续费单价 |
| hhedge_short_cfee_r | numeric(17,8) | Y |  | 自营套保空头平今手续费率 |
| hhedge_short_cfee_u | numeric(12,2) | Y |  | 自营套保空头平今手续费单价 |
| mspec_long_cfee_r | numeric(17,8) | Y |  | 做市商投机多头平今手续费率 |
| mspec_long_cfee_u | numeric(12,2) | Y |  | 做市商投机多头平今手续费单价 |
| mspec_short_cfee_r | numeric(17,8) | Y |  | 做市商投机空头平今手续费率 |
| mspec_short_cfee_u | numeric(12,2) | Y |  | 做市商投机空头平今手续费单价 |
| mhedge_long_cfee_r | numeric(17,8) | Y |  | 做市商套保多头平今手续费率 |
| mhedge_long_cfee_u | numeric(12,2) | Y |  | 做市商套保多头平今手续费单价 |
| mhedge_short_cfee_r | numeric(17,8) | Y |  | 做市商套保空头平今手续费率 |
| mhedge_short_cfee_u | numeric(12,2) | Y |  | 做市商套保空头平今手续费单价 |
| bspec_delivery_fee_r | numeric(17,8) | Y |  | 代理投机交割手续费率 |
| bspec_delivery_fee_u | numeric(12,2) | Y |  | 代理投机交割手续费单价 |
| bhedge_delivery_fee_r | numeric(17,8) | Y |  | 代理套保交割手续费率 |
| bhedge_delivery_fee_u | numeric(12,2) | Y |  | 代理套保交割手续费单价 |
| hspec_delivery_fee_r | numeric(17,8) | Y |  | 自营投机交割手续费率 |
| hspec_delivery_fee_u | numeric(12,2) | Y |  | 自营投机交割手续费单价 |
| hhedge_delivery_fee_r | numeric(17,8) | Y |  | 自营套保交割手续费率 |
| hhedge_delivery_fee_u | numeric(12,2) | Y |  | 自营套保交割手续费单价 |
| mspec_delivery_fee_r | numeric(17,8) | Y |  | 做市商投机交割手续费率 |
| mspec_delivery_fee_u | numeric(12,2) | Y |  | 做市商投机交割手续费单价 |
| mhedge_delivery_fee_r | numeric(17,8) | Y |  | 做市商套保交割手续费率 |
| mhedge_delivery_fee_u | numeric(12,2) | Y |  | 做市商套保交割手续费单价 |
| bspec_ss_fee_r | numeric(17,8) | Y |  | 代理投机执行手续费率 |
| bspec_ss_fee_u | numeric(12,2) | Y |  | 代理投机执行手续费单价 |
| bhedge_ss_fee_r | numeric(17,8) | Y |  | 代理套保执行手续费率 |
| bhedge_ss_fee_u | numeric(12,2) | Y |  | 代理套保执行手续费单价 |
| hspec_ss_fee_r | numeric(17,8) | Y |  | 自营投机执行手续费率 |
| hspec_ss_fee_u | numeric(12,2) | Y |  | 自营投机执行手续费单价 |
| hhedge_ss_fee_r | numeric(17,8) | Y |  | 自营套保执行手续费率 |
| hhedge_ss_fee_u | numeric(12,2) | Y |  | 自营套保执行手续费单价 |
| mspec_ss_fee_r | numeric(17,8) | Y |  | 做市商投机执行手续费率 |
| mspec_ss_fee_u | numeric(12,2) | Y |  | 做市商投机执行手续费单价 |
| mhedge_ss_fee_r | numeric(17,8) | Y |  | 做市商套保执行手续费率 |
| mhedge_ss_fee_u | numeric(12,2) | Y |  | 做市商套保执行手续费单价 |
| delta | numeric(17,8) | Y |  | 虚实度 |
| volatitiy | numeric(17,8) | Y |  | 隐含波动率 |
| at_the_money | varchar(1) | Y |  | 是否平值期权:见tp_public_dict的027 |
| min_margin | numeric(19,2) | Y |  | 最小保证金 |

---

## 556. dimple.tc_shfe_doc_of_title_detail　(6 字段)
> 表含义：上期所：权利凭证明细栏 20190101开始废弃　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 导入日期 |
| doc_name | varchar(50) | Y |  | 权利凭证名称 |
| discount_price | varchar(50) | Y |  | 折后价 |
| qty | varchar(50) | Y |  | 数量 |
| discount_amt | varchar(50) | Y |  | 折后金额 |
| duty_status | varchar(50) | Y |  | 完税状态 |

---

## 557. dimple.tc_shfe_fund　(5 字段)
> 表含义：浦发银行-上期货款台账表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| delivery_contract_id | varchar(60) | Y |  | 合约号 |
| amount | numeric(38,2) | Y |  | 金额 |
| operator | varchar(30) | Y |  | 更新用户 |
| update_date | timestamp | Y |  | 更新日期 |

---

## 558. dimple.tc_shfe_manual_fund　(13 字段)
> 表含义：浦发银行-上期手工台账表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq | float8 | N | √ | 流水号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| trade_type | varchar(4) | Y |  | 业务类型 |
| amount | numeric(38,2) | Y |  | 金额 |
| status | varchar(2) | Y |  | 状态 |
| create_user | varchar(30) | Y |  | 录入人 |
| create_date | timestamp | Y |  | 录入时间 |
| create_chk_user | varchar(30) | Y |  | 录入复核人 |
| create_chk_date | timestamp | Y |  | 录入复核时间 |
| delete_user | varchar(30) | Y |  | 删除人 |
| delete_date | timestamp | Y |  | 删除时间 |
| delete_chk_user | varchar(30) | Y |  | 删除复核人 |
| delete_chk_date | timestamp | Y |  | 删除复核时间 |

---

## 559. dimple.tc_shfe_money_io_detail　(9 字段)
> 表含义：上期所:出入金明细　|　估算行数：**137**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 导入日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| sheet_no | varchar(50) | Y |  | 单据号 |
| money_type | varchar(50) | Y |  | 资金类型名称 |
| amt | varchar(50) | Y |  | 金额 |
| io_type | varchar(50) | Y |  | 资金划账方式:内部转帐;银行转帐 |
| input_date | varchar(8) | Y |  | 录入日期 |
| effect_date | varchar(8) | Y |  | 到帐日期 |
| currency | varchar(3) | Y |  | 币种代码:见tp_public_dict的036 |

---

## 560. dimple.tc_shfe_mortgage_detail　(15 字段)
> 表含义：上期所：抵押品明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 导入日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户编码 |
| mortgage_id | varchar(8) | Y |  | 抵押品代码 |
| mort_name | varchar(50) | Y |  | 抵押品名称 |
| mort_unit | varchar(10) | Y |  | 抵押品单位 |
| collateral_type | varchar(1) | Y |  | 抵押品类型:见tp_public_dict的411 |
| duty_status | varchar(1) | Y |  | 保税/完税状态:见tp_public_dict的412 |
| due_date | varchar(8) | Y |  | 到期日期 |
| mort_type | varchar(1) | Y |  | 抵押类型:见tp_public_dict的413 |
| amount | numeric(10,0) | Y |  | 数量 |
| mortgage_amt | numeric(19,2) | Y |  | 充抵金额 |
| deduction_amt | numeric(19,2) | Y |  | 折后金额 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| posi_direct | varchar(1) | Y |  | 持仓方向:见tp_public_dict的414 |

---

## 561. dimple.tc_shfe_notrading_posi_chg　(17 字段)
> 表含义：非交易持仓变动明细　|　估算行数：**42,303**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户编码 |
| seq_no | numeric(20,0) | Y |  | 持仓变动明细序号 |
| posi_chg_type | varchar(1) | Y |  | 持仓变动类型:见tp_public_dict的431 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| posi_direct | varchar(1) | Y |  | 持仓方向:见tp_public_dict的414 |
| sh_flag | varchar(1) | Y |  | 投机套保标志:见tp_public_dict的004;1-非套保3-套保 |
| volume | numeric(10,0) | Y |  | 持仓变动数量：正数表示持仓增加，负数表示持仓减少 |
| price | numeric(12,2) | Y |  | 价格 |
| delivery_type | varchar(1) | Y |  | 交割方式:见tp_public_dict的051;0-现金交割，4-实物交割 |
| match_no | varchar(12) | Y |  | 成交编号：持仓变动类型为期权执行、期权自对冲、期货自对冲、强减时字段不为空，且与成交文件中成交编号不重复，其他持仓变动类型时该字段为空 |
| eo_flag | varchar(1) | Y |  | 开平标志：见tp_public_dict的003;不区分平今、平昨;1-开仓,2-平仓 |
| amount | numeric(19,2) | Y |  | 期货成交金额 |
| exec_price | numeric(19,2) | Y |  | 行权价 |
| trade_time | varchar(8) | Y |  | 成交时间:统一填写15:00:00 |
| open_match_no | varchar(12) | Y |  | 原开仓成交编号 |

---

## 562. dimple.tc_shfe_notrading_posi_chg_tmp　(17 字段)
> 表含义：非交易持仓变动明细临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户编码 |
| seq_no | numeric(20,0) | Y |  | 持仓变动明细序号 |
| posi_chg_type | varchar(1) | Y |  | 持仓变动类型:见tp_public_dict的431 |
| contract_id | varchar(30) | Y |  | 合约代码 |
| posi_direct | varchar(1) | Y |  | 买卖方向:见tp_public_dict的002 |
| sh_flag | varchar(1) | Y |  | 投机套保标志:见tp_public_dict的004;1-非套保3-套保 |
| volume | numeric(10,0) | Y |  | 持仓变动数量：正数表示持仓增加，负数表示持仓减少 |
| price | numeric(12,2) | Y |  | 价格 |
| delivery_type | varchar(1) | Y |  | 交割方式:见tp_public_dict的051;0-现金交割，4-实物交割 |
| match_no | varchar(12) | Y |  | 成交编号：持仓变动类型为期权执行、期权自对冲、期货自对冲、强减时字段不为空，且与成交文件中成交编号不重复，其他持仓变动类型时该字段为空 |
| eo_flag | varchar(1) | Y |  | 开平标志：见tp_public_dict的003;不区分平今、平昨;1-开仓,2-平仓 |
| amount | numeric(19,2) | Y |  | 期货成交金额 |
| exec_price | numeric(19,2) | Y |  | 行权价 |
| trade_time | varchar(8) | Y |  | 成交时间:统一填写15:00:00 |
| open_match_no | varchar(12) | Y |  | 原开仓成交编号 |

---

## 563. dimple.tc_short_tot　(12 字段)
> 表含义：短线汇总表:据期货和期权的短线明细汇总得到.　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| short_qty | numeric(12,0) | Y |  | 短线量 |
| short_turnover | numeric(18,2) | Y |  | 短线成交额 |
| short_profitloss | numeric(18,2) | Y |  | 短线盈亏 |
| short_fee | numeric(18,2) | Y |  | 短线手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费 |
| exch_short_fee | numeric(18,2) | Y |  | 交易所短线手续费 |
| exch_ret_fee | numeric(18,2) | Y |  | 交易所返还手续费 |
| sh_flag | varchar(1) | N | √ | 投保标志:见tp_public_dict的004 |

---

## 564. dimple.tc_sl　(16 字段)
> 表含义：止损点表　|　估算行数：**8**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| market_type | bpchar(1) | N | √ | 市场:见tp_public_dict的001 |
| sl_day | numeric(22,6) | Y |  | 日止损限额 |
| sl_month | numeric(22,6) | Y |  | 月止损限额 |
| sl_year | numeric(22,6) | Y |  | 年止损限额 |
| sl_operator | varchar(30) | Y |  | 操作员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 565. dimple.tc_sl_check　(21 字段)
> 表含义：止损点复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| seq_no | float8 | N | √ | 序列号 |
| trade_date | varchar(8) | N |  | 日期 |
| user_id | varchar(30) | N |  | 交易员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| sl_day | numeric(22,6) | Y |  | 日止损限额 |
| sl_month | numeric(22,6) | Y |  | 月止损限额 |
| sl_year | numeric(22,6) | Y |  | 年止损限额 |
| operator | varchar(30) | Y |  | 操作员 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| status | varchar(3) | Y |  | 状态:见dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型:见dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 566. dimple.tc_sl_clear　(17 字段)
> 表含义：止损点结算表　|　估算行数：**11,138**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| market_type | bpchar(1) | N | √ | 市场:见tp_public_dict的001 |
| sl_day | numeric(22,6) | Y |  | 日止损限额 |
| sl_month | numeric(22,6) | Y |  | 月止损限额 |
| sl_year | numeric(22,6) | Y |  | 年止损限额 |
| operator | varchar(30) | Y |  | 操作员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 567. dimple.tc_sl_jour　(15 字段)
> 表含义：止损流水表　|　估算行数：**125**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| seq_no | float8 | N | √ | 序列号 |
| user_id | varchar(30) | N |  | 交易员 |
| variety_id | varchar(4) | N |  | 品种 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| sl_day | numeric(22,6) | Y |  | 日止损 |
| sl_month | numeric(22,6) | Y |  | 月止损 |
| sl_year | numeric(22,6) | Y |  | 年止损 |
| oper_type | varchar(3) | Y |  | 操作类型:见dict的265 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| create_id | varchar(30) | Y |  | 创建人 |

---

## 568. dimple.tc_spmm_business_parameter　(9 字段)
> 表含义：上期所组合保证金业务参数表　|　估算行数：**14,559**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(3) | Y |  | 交易所 |
| minmgrate | numeric(17,8) | N |  | 最小保证金比例 |
| oucommpref | numeric(17,8) | N |  | 跨品种优惠系数 |
| incommpref | numeric(17,8) | N |  | 跨期优惠系数 |
| opriskrate | numeric(17,8) | N |  | 期权纯粹价格风险比例 |
| comb_comgrp | varchar(30) | N |  | 商品群:见tp_public_dict的476 |
| spmmcateid | varchar(1) | N |  | 组保客户分类代码:见tp_public_dict的478 |
| import_date | varchar(9) | N |  | 导入日期 |
| trader_no | varchar(16) | N |  | 席位号 |

---

## 569. dimple.tc_spmm_client_type　(5 字段)
> 表含义：上期所组合保证金客户分类表　|　估算行数：**610**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(3) | Y |  | 交易所 |
| client_id | varchar(10) | N | √ | 客户编码 |
| spmmcateid | varchar(1) | N | √ | 组保客户分类代码:见tp_public_dict的478 |
| import_date | varchar(9) | N | √ | 导入日期 |
| trader_no | varchar(16) | N | √ | 席位号 |

---

## 570. dimple.tc_spmm_contract_parameter　(7 字段)
> 表含义：上期所组合保证金合约参数表　|　估算行数：**897,354**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(3) | Y |  | 交易所 |
| instr_id | varchar(30) | N |  | 合约代码 |
| margin_calc | varchar(1) | N |  | 保证金算法:见tp_public_dict的479 |
| comb_commid | varchar(8) | N |  | 商品组:见tp_public_dict的477 |
| comb_comgrp | varchar(30) | N |  | 商品群:见tp_public_dict的476 |
| import_date | varchar(9) | N |  | 导入日期 |
| trader_no | varchar(16) | N |  | 席位号 |

---

## 571. dimple.tc_spmm_details　(11 字段)
> 表含义：上期所组合保证金明细表　|　估算行数：**597**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(3) | Y |  | 交易所 |
| duemgprf | numeric(19,2) | N |  | 参与优惠应收保证金 |
| duemgnoprf | numeric(19,2) | N |  | 不参与优惠应收保证金 |
| margin | numeric(19,2) | N |  | 实收保证金 |
| inmargpref | numeric(19,2) | N |  | 跨期优惠保证金 |
| comb_comgrp | varchar(30) | N |  | 商品群:见tp_public_dict的476 |
| client_id | varchar(10) | N |  | 客户编码 |
| oumargpref | numeric(19,2) | N |  | 跨品种优惠保证金 |
| minmargin | numeric(19,2) | N |  | 最小保证金 |
| import_date | varchar(9) | N |  | 导入日期 |
| trader_no | varchar(16) | N |  | 席位号 |

---

## 572. dimple.tc_spot_day_report　(28 字段)
> 表含义：现货交易日报表　|　估算行数：**1,952**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| month_no | varchar(8) | N | √ | 月份 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_spot_qty | numeric(15,3) | Y |  | 现货买入量 |
| buy_spot_amt | numeric(24,6) | Y |  | 现货买入金额 |
| sell_spot_qty | numeric(15,3) | Y |  | 现货卖出量 |
| sell_spot_amt | numeric(24,6) | Y |  | 现货卖出金额 |
| buy_defer_qty | numeric(15,3) | Y |  | 非即期买入量 |
| buy_defer_amt | numeric(24,6) | Y |  | 非即期买入金额 |
| sell_defer_qty | numeric(15,3) | Y |  | 非即期卖出量 |
| sell_defer_amt | numeric(24,6) | Y |  | 非即期卖出金额 |
| buy_inquire_qty | numeric(15,3) | Y |  | 询价买入量 |
| buy_inquire_amt | numeric(24,6) | Y |  | 询价买入金额 |
| sell_inquire_qty | numeric(15,3) | Y |  | 询价卖出量 |
| sell_inquire_amt | numeric(24,6) | Y |  | 询价卖出金额 |
| lend_in_qty | numeric(15,3) | Y |  | 拆入量 |
| lend_in_amt | numeric(24,6) | Y |  | 拆入金额 |
| lend_out_qty | numeric(15,3) | Y |  | 拆出量 |
| lend_out_amt | numeric(24,6) | Y |  | 拆出金额 |
| storage_in_qty | numeric(15,3) | Y |  | 现货入库量 |
| storage_in_amt | numeric(24,6) | Y |  | 现货入库金额 |
| storage_out_qty | numeric(15,3) | Y |  | 现货出库量 |
| storage_out_amt | numeric(24,6) | Y |  | 现货出库金额 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| day_qty | numeric(15,3) | Y |  | 当日变化量 |
| day_amt | numeric(24,6) | Y |  | 当日变化金额 |

---

## 573. dimple.tc_spot_month_report　(29 字段)
> 表含义：现货交易月报表　|　估算行数：**2,900**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| month_no | varchar(8) | N | √ | 月份 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| init_qty | numeric(15,3) | Y |  | 期初量 |
| init_amt | numeric(24,6) | Y |  | 期初金额 |
| buy_spot_qty | numeric(15,3) | Y |  | 现货买入量 |
| buy_spot_amt | numeric(24,6) | Y |  | 现货买入金额 |
| sell_spot_qty | numeric(15,3) | Y |  | 现货卖出量 |
| sell_spot_amt | numeric(24,6) | Y |  | 现货卖出金额 |
| buy_defer_qty | numeric(15,3) | Y |  | 非即期买入量 |
| buy_defer_amt | numeric(24,6) | Y |  | 非即期买入金额 |
| sell_defer_qty | numeric(15,3) | Y |  | 非即期卖出量 |
| sell_defer_amt | numeric(24,6) | Y |  | 非即期卖出金额 |
| buy_inquire_qty | numeric(15,3) | Y |  | 询价买入量 |
| buy_inquire_amt | numeric(24,6) | Y |  | 询价买入金额 |
| sell_inquire_qty | numeric(15,3) | Y |  | 询价卖出量 |
| sell_inquire_amt | numeric(24,6) | Y |  | 询价卖出金额 |
| lend_in_qty | numeric(15,3) | Y |  | 拆入量 |
| lend_in_amt | numeric(24,6) | Y |  | 拆入金额 |
| lend_out_qty | numeric(15,3) | Y |  | 拆出量 |
| lend_out_amt | numeric(24,6) | Y |  | 拆出金额 |
| storage_in_qty | numeric(15,3) | Y |  | 现货入库量 |
| storage_in_amt | numeric(24,6) | Y |  | 现货入库金额 |
| storage_out_qty | numeric(15,3) | Y |  | 现货出库量 |
| storage_out_amt | numeric(24,6) | Y |  | 现货出库金额 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| remain_qty | numeric(15,3) | Y |  | 期末量 |
| remain_amt | numeric(24,6) | Y |  | 期末金额 |

---

## 574. dimple.tc_srcb_abnormal_account　(12 字段)
> 表含义：上海农商行历史帐务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | numeric(10,0) | Y |  | 凭证组号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| member_id | varchar(8) | Y |  | 席位代码 |
| voucher_no | varchar(12) | Y |  | 凭证号 |
| account_sysno | varchar(30) | Y |  | 账号/科目系统编号 |
| buy_flag | varchar(4) | Y |  | 借贷标识：见tp_public_dict 276 |
| currency | varchar(3) | Y |  | 币种:默认CNY |
| amount | numeric(24,6) | Y |  | 金额 |
| remark | varchar(100) | Y |  | 摘要 |
| reason | varchar(100) | Y |  | 原因:默认借贷不平 |
| create_time | varchar(8) | Y |  | 生成时间 |
| processing_status | varchar(3) | Y |  | 处理状态:0-未处理、1-已处理，初始状态为"未处理",见tp_public_dict 390 |

---

## 575. dimple.tc_srcb_account　(13 字段)
> 表含义：上海农商行帐务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | numeric(10,0) | Y |  | 凭证组号 |
| id | varchar(3) | Y |  | 物理ID |
| trade_date | varchar(8) | Y |  | 交易日期 |
| member_id | varchar(8) | Y |  | 席位代码 |
| voucher_no | varchar(12) | Y |  | 凭证号 |
| account_sysno | varchar(30) | Y |  | 账号/科目系统编号 |
| buy_flag | varchar(4) | Y |  | 借贷标识：见tp_public_dict 276 |
| currency | varchar(3) | Y |  | 币种:默认CNY |
| amount | numeric(24,6) | Y |  | 金额 |
| remark | varchar(100) | Y |  | 摘要 |
| sub_type | varchar(3) | Y |  | 业务类型 |
| note | varchar(100) | Y |  | 备注 |
| status | varchar(3) | Y |  | 记账状态：见tp_public_dict 304 |

---

## 576. dimple.tc_srcb_account_no　(9 字段)
> 表含义：农商银行帐号配置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| account_sysno | varchar(30) | N | √ | 账号/科目系统编号 |
| account | varchar(20) | Y |  | 账号 |
| account_name | varchar(200) | Y |  | 账号名称 |
| subject_id | varchar(20) | Y |  | 科目 |
| subject_name | varchar(200) | Y |  | 科目名称 |
| account_sign | varchar(6) | Y |  | 账户标识：见TP_PUBLIC_DICT392 |
| account_type | varchar(6) | Y |  | 账户类型：见TP_PUBLIC_DICT的393 |
| cue_code | varchar(6) | Y |  | 提示码 |
| transition_sysno | varchar(20) | Y |  | 过渡账户系统编号 |

---

## 577. dimple.tc_srcb_account_record　(11 字段)
> 表含义：会计核算规则表　|　估算行数：**160**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | varchar(3) | N | √ | 物理主键 |
| seq_no | numeric(10,0) | Y |  | 凭证组号 |
| member_id | varchar(8) | N | √ | 席位号 |
| sub_type | varchar(3) | Y |  | 业务类型 |
| buy_flag | varchar(4) | Y |  | 借贷标识：见tp_public_dict 276 |
| account_sysno | varchar(30) | Y |  | 账号/科目系统编号 |
| source_id | varchar(3) | Y |  | 数据来源ID |
| content | varchar(60) | Y |  | 记账金额对应字段 |
| note | varchar(100) | Y |  | 备注 |
| constraint_condition | varchar(100) | Y |  | 约束条件 |
| if_account | varchar(3) | Y |  | 是否出帐：见tp_public_dict 027 |

---

## 578. dimple.tc_srcb_account_type　(4 字段)
> 表含义：农商银行业务类型　|　估算行数：**39**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| market_type | varchar(3) | N | √ | 业务类型 |
| market_name | varchar(40) | Y |  | 业务类型名称 |
| sub_type | varchar(3) | N | √ | 子类型 |
| sub_name | varchar(60) | Y |  | 子类型名称 |

---

## 579. dimple.tc_srcb_accumugold_vaexp_clear　(11 字段)
> 表含义：上海农商行：积存金敞口额度表　|　估算行数：**2,847**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(12) | N | √ | 会员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| day_used_exposure | numeric(25,9) | Y |  | 当日积存金已占敞口 :克 |
| sum_used_exposure | numeric(25,9) | Y |  | 积存金敞口余量 :克 |
| exposure_ratio | numeric(25,9) | Y |  | 敞口系数 |
| sum_exposure | numeric(25,9) | Y |  | 积存金敞口 :克 |
| day_offset_qty | numeric(25,9) | Y |  | 当日平盘量 :克 |
| sum_offset_qty | numeric(25,9) | Y |  | 累计平盘量 :克 |
| day_noffset_qty | numeric(25,9) | Y |  | 当日待平盘量 :克 |
| net_exposure | numeric(25,9) | Y |  | 席位净敞口 :克 |

---

## 580. dimple.tc_srcb_basicinfo_tot　(8 字段)
> 表含义：贵金属业务基本情况统计表　|　估算行数：**96**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| yearmonth | varchar(6) | N | √ | 年月 |
| tot_name | varchar(50) | N | √ | 统计项 |
| trade_num | varchar(90) | Y |  | 交易笔数本期 |
| trade_weight | numeric(24,6) | Y |  | 交易量本期（千克） |
| weight_year | numeric(24,6) | Y |  | 交易量本年累计 |
| trade_amt | numeric(24,6) | Y |  | 交易金额本期 |
| amt_year | numeric(24,6) | Y |  | 交易金额本年累计 |
| month_notdue_amt | numeric(24,6) | Y |  | 业务余额本期 |

---

## 581. dimple.tc_srcb_datasource　(2 字段)
> 表含义：农商银行帐务数据来源表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| source_id | varchar(3) | Y |  | 数据来源ID |
| source | varchar(60) | Y |  | 数据来源 |

---

## 582. dimple.tc_srcb_inquire_value　(9 字段)
> 表含义：上海农商行贵金属业务库存估值表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| contract_id | varchar(20) | N | √ | 合约名称 |
| bs_flag | varchar(3) | N | √ | 买卖方向 1-买入，3-卖出 |
| match_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的253 |
| member_id | varchar(8) | N | √ | 会员号,默认 $ |
| qty | numeric(20,0) | Y |  | 交易数量 |
| amt | numeric(20,8) | Y |  | 交易总金额 |
| last_value | numeric(20,8) | Y |  | 估值上日公允价值变动 |
| value_amt | numeric(20,8) | Y |  | 估值当日公允价值变动损益 |

---

## 583. dimple.tc_srcb_metal_vaexp_clear　(8 字段)
> 表含义：上海农商行：贵金属敞口统计表　|　估算行数：**38,342**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| source_name | varchar(50) | N | √ | 来源名称 |
| member_id | varchar(12) | N | √ | 会员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| metal_id | varchar(100) | N | √ | 贵金属代码 |
| direction | varchar(3) | N | √ | 多空方向:多，空，- |
| exposure | numeric(22,6) | Y |  | 本期末敞口（克） |
| exposure_amt | numeric(22,6) | Y |  | 本期末金额（元） |

---

## 584. dimple.tc_srcb_storage_value　(22 字段)
> 表含义：上海农商行贵金属业务库存估值表　|　估算行数：**1,100**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 日期 |
| contract_id | varchar(20) | Y |  | 合约名称 |
| member_id | varchar(8) | Y |  | 会员号 |
| clear_price | numeric(20,8) | Y |  | 当日市价 |
| last_clear_price | numeric(20,8) | Y |  | 前日市价 |
| qty | numeric(20,0) | Y |  | 库存数量 |
| avg_price | numeric(20,8) | Y |  | 库存平均成本 |
| cost | numeric(20,8) | Y |  | 库存总成本 |
| value_profitloss | numeric(20,8) | Y |  | 估值损益 |
| value_profitloss_chg | numeric(20,8) | Y |  | 库存估值损益变动额 |
| last_bear_amt | numeric(20,8) | Y |  | 额度负债上日估值 |
| bear_amt | numeric(20,8) | Y |  | 额度负债当日估值 |
| fw_bs_flag | varchar(3) | Y |  | 远期买卖方向 |
| fw_qty | numeric(20,0) | Y |  | 远期估值交易数量 |
| fw_amt | numeric(20,8) | Y |  | 远期估值交易总金额 |
| fw_last_value | numeric(20,8) | Y |  | 远期估值上日公允价值变动 |
| fw_value | numeric(20,8) | Y |  | 远期估值当日公允价值变动损益 |
| sw_bs_flag | varchar(3) | Y |  | 掉期买卖方向 |
| sw_qty | numeric(20,0) | Y |  | 掉期估值交易数量 |
| sw_amt | numeric(20,8) | Y |  | 掉期估值交易总金额 |
| sw_last_value | numeric(20,8) | Y |  | 掉期估值上日公允价值变动 |
| sw_value | numeric(20,8) | Y |  | 掉期估值当日公允价值变动损益 |

---

## 585. dimple.tc_srcb_storage_value_calc　(19 字段)
> 表含义：上海农商行贵金属业务库存估值表　|　估算行数：**97**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| contract_id | varchar(20) | N | √ | 合约名称 |
| member_id | varchar(8) | N | √ | 会员号,默认 $ |
| clear_price | numeric(20,8) | Y |  | 当日市价 |
| last_clear_price | numeric(20,8) | Y |  | 上日市价 |
| qty | numeric(20,0) | Y |  | 库存数量 |
| avg_price | numeric(20,8) | Y |  | 库存平均成本 |
| cost_amt | numeric(20,8) | Y |  | 库存总成本 |
| storage_value | numeric(20,8) | Y |  | 当日剩余库存估值 |
| bear_value | numeric(20,8) | Y |  | 当日额度负债估值 |
| value_chg | numeric(20,8) | Y |  | 估值变动额 |
| value_profitloss | numeric(20,8) | Y |  | 估值损益 |
| value_profitloss_chg | numeric(20,8) | Y |  | 当日估值损益变动额 |
| bear_value_chg | numeric(20,8) | Y |  | 额度负债估值变动 |
| bear_value_profitloss | numeric(20,8) | Y |  | 卖空估值损益 |
| last_storage_value | numeric(20,8) | Y |  | 上日库存估值余额 |
| last_bear_value | numeric(20,8) | Y |  | 上日负债估值余额 |
| last_value_profitloss | numeric(20,8) | Y |  | 上日估值损益 |
| last_bear_value_profitloss | numeric(20,8) | Y |  | 上日卖空估值损益 |

---

## 586. dimple.tc_srcb_subject_record　(6 字段)
> 表含义：会计分录帐号表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| id | varchar(3) | N | √ | 物理主键 |
| member_id | varchar(8) | Y |  | 席位代码 |
| account_sysno | varchar(30) | Y |  | 账号/科目系统编号 |
| source_id | varchar(3) | Y |  | 数据来源ID |
| content | varchar(60) | Y |  | 对应字段 |
| note | varchar(2000) | Y |  | 说明 |

---

## 587. dimple.tc_srcb_sumclear　(27 字段)
> 表含义：上海农商行贵金属业务清算汇总表　|　估算行数：**185**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| contract_id | varchar(20) | N | √ | 合约名称 |
| account_type | varchar(3) | N | √ | 交易目的 |
| member_id | varchar(8) | N | √ | 会员号 |
| buy_avg_price | numeric(20,8) | Y |  | 买入均价 |
| buy_qty | numeric(12,0) | Y |  | 买入量 |
| buy_amt | numeric(20,8) | Y |  | 买入支付金额 |
| sell_avg_price | numeric(20,8) | Y |  | 卖出均价 |
| sell_qty | numeric(12,0) | Y |  | 卖出量 |
| sell_amt | numeric(20,8) | Y |  | 卖出收到金额 |
| sell_cost_amt | numeric(20,8) | Y |  | 当日卖出扣减成本 |
| bear_qty | numeric(12,0) | Y |  | 空头总量 |
| bear_amt | numeric(20,8) | Y |  | 空头金额 |
| offset_qty | numeric(12,0) | Y |  | 冲减量 |
| offset_amt | numeric(20,8) | Y |  | 冲减应付金额 |
| offset_cost | numeric(20,8) | Y |  | 冲减成本 |
| bear_remain_qty | numeric(12,0) | Y |  | 空头剩余量 |
| bear_remain_amt | numeric(20,8) | Y |  | 剩余空头金额 |
| bear_offset_profit | numeric(20,8) | Y |  | 冲减空头损益 |
| self_profit | numeric(20,8) | Y |  | 自营损益 |
| profit | numeric(20,8) | Y |  | 总损益 |
| last_remain_qty | numeric(12,0) | Y |  | 上日库存量 |
| last_avg_price | numeric(20,8) | Y |  | 上日平均成本 |
| last_remain_cost | numeric(20,8) | Y |  | 上日库存总成本 |
| remain_qty | numeric(12,0) | Y |  | 当日库存量 |
| avg_price | numeric(20,8) | Y |  | 当日库存平均成本 |
| remain_cost | numeric(20,8) | Y |  | 当日库存总成本 |

---

## 588. dimple.tc_srcb_transition　(5 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| transition_sysno | varchar(20) | N | √ | 过渡账户系统编号 |
| transition_account | varchar(20) | Y |  | 过渡账户 |
| account_sign | varchar(6) | Y |  | 账户标志：见TP_PUBLIC_DICT392 |
| account_type | varchar(6) | Y |  | 提示码 |
| cue_code | varchar(6) | Y |  |  |

---

## 589. dimple.tc_staff_post_change　(24 字段)
> 表含义：4A异动消息记录表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| msg_id | varchar(64) | N |  | 消息id |
| uniq_key | varchar(128) | N | √ | 业务唯一键 |
| type | varchar(2) | N |  | 消息类型：1-离岗；2-调岗 |
| user_id | varchar(64) | N | √ | 异动人员UM账号 |
| trader_no | varchar(64) | N | √ | 本地用户 |
| create_date | varchar(30) | Y |  | 新增时间 |
| domain_account | varchar(64) | Y |  | 域账号 |
| gender | varchar(8) | Y |  | 性别 |
| display_name | varchar(128) | Y |  | 中文名 |
| manager | varchar(64) | Y |  | 直属上级领导UM号 |
| mobile | varchar(32) | Y |  | 电话 |
| email | varchar(128) | Y |  | 邮箱 |
| org | varchar(64) | Y |  | 部门编码 |
| origin_dept | varchar(64) | Y |  | 原部门编码 |
| origin_display_name | varchar(128) | Y |  | 原部门名称 |
| origin_org_type | varchar(32) | Y |  | 原部门分类 |
| origin_owner | varchar(64) | Y |  | 原部门负责人UM号 |
| origin_parent_code | varchar(64) | Y |  | 原部门上级部门编号 |
| dest_dept | varchar(64) | Y |  | 目标部门编码 |
| dest_display_name | varchar(128) | Y |  | 目标部门名称 |
| dest_org_type | varchar(32) | Y |  | 目标部门分类 |
| dest_owner | varchar(64) | Y |  | 目标部门负责人UM号 |
| dest_parent_code | varchar(64) | Y |  | 目标部门上级部门编号 |
| deal_status | varchar(2) | Y |  | 处理状态：0-未处理；1-处理完成；2-处理失败；3-无需处理 |

---

## 590. dimple.tc_summit_future_match　(20 字段)
> 表含义：期货盘后表　|　估算行数：**160,965**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 清算日期 |
| seq_no | float8 | N |  | 发送批次号 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| match_no | varchar(30) | Y |  | 成交号 |
| variety_id | varchar(9) | Y |  | 品种号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| eo_flag | varchar(3) | Y |  | 开平标志  |
| sh_flag | varchar(3) | Y |  | 投机套保标志  |
| deli_month | varchar(8) | Y |  | 交割月 |
| deli_date | varchar(8) | Y |  | 交割月 |
| price | numeric(24,6) | Y |  | 价格 |
| qty | numeric(20,3) | Y |  | 数量 |
| purpose_code | varchar(4) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| trader_no | varchar(16) | Y |  | 交易员 |
| exch_code | varchar(3) | Y |  | 交易所 |
| contract_id | varchar(20) | Y |  | 合约号 |
| datadim | varchar(3) | Y |  | 数据维度:1-明细,2-汇总 |
| strategy_trader_no | varchar(15) | Y |  | 策略交易员 |

---

## 591. dimple.tc_summit_match　(6 字段)
> 表含义：SUMMIT实时成交已发送数据表　|　估算行数：**916**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | Y |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| trader_no | varchar(16) | N |  | 席位号 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 592. dimple.tc_summit_member_relation　(2 字段)
> 表含义：SUMMIT会员对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| st_member_id | varchar(8) | Y |  | 对应会员号：summit使用 |

---

## 593. dimple.tc_summit_member_send　(4 字段)
> 表含义：多会员SUMMIT接口发送表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| summitdata | bpchar(2) | N | √ | 是否发送该会员的summit接口数据,0-不发送,1-发送 |
| customdata | bpchar(2) | N | √ | 是否发送该会员的其它接口数据,如浦发IMA接口,0-不发送,1-发送 |
| remark | varchar(100) | Y |  | 备注 |

---

## 594. dimple.tc_summit_spot_match　(17 字段)
> 表含义：现货盘后表　|　估算行数：**7,394**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 清算日期 |
| seq_no | float8 | N |  | 发送批次号 |
| match_no | varchar(30) | Y |  | 成交号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| price | numeric(24,6) | Y |  | 价格 |
| qty | numeric(20,6) | Y |  | 数量 |
| purpose_code | varchar(4) | Y |  | 交易目的 |
| order_type | varchar(3) | Y |  | 订单类型 |
| eo_flag | varchar(3) | Y |  | 开平标志  |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| trader_no | varchar(16) | Y |  | 交易员 |
| exch_code | varchar(3) | Y |  | 交易所 |
| sh_flag | varchar(8) | Y |  | 投机套保标志   |
| trade_time | varchar(10) | Y |  | 成交时间 |
| datadim | varchar(3) | Y |  | 数据维度:1-明细,2-汇总 |

---

## 595. dimple.tc_summit_storage　(2 字段)
> 表含义：客户库存流水发送表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_seq_no | varchar(10) | N |  | 交易所流水号 |
| effect_date | varchar(8) | N |  | 生效日期 |

---

## 596. dimple.tc_swap_deli_match　(16 字段)
> 表含义：上期商品互换交割数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| clear_date | varchar(8) | Y |  | 日期 |
| bs_flag | varchar(1) | Y |  | 买卖 |
| match_no | varchar(20) | Y |  | 交割编号 |
| variety | varchar(80) | Y |  | 品种 |
| variety_name | varchar(80) | Y |  | 品种名称 |
| contract_id | varchar(80) | Y |  | 协议标的 |
| due_date | varchar(8) | Y |  | 到期日 |
| settle_due_price | varchar(40) | Y |  | 到期结算价 |
| match_date | varchar(8) | Y |  | 成交日期 |
| deal_number | varchar(20) | Y |  | 成交编号 |
| last_clearprice | numeric(19,2) | Y |  | 昨日结算价 |
| price | numeric(19,2) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 交割量 |
| profit | numeric(19,2) | Y |  | 到期盈亏 |

---

## 597. dimple.tc_swap_import_status　(4 字段)
> 表含义：商品互换导入状态表　|　估算行数：**336**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 日期 |
| file_no | numeric(10,0) | Y |  | 文件编号 |
| import_times | varchar(8) | Y |  | 导入时间 |
| status | varchar(1) | Y |  | 状态 |

---

## 598. dimple.tc_swap_match_detail　(18 字段)
> 表含义：上期商品互换成交明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 席位号 |
| client_id | varchar(16) | Y |  | 客户号 |
| match_no | varchar(20) | Y |  | 成交编号 |
| match_time | varchar(8) | Y |  | 成交时间 |
| variety | varchar(80) | Y |  | 品种 |
| variety_name | varchar(80) | Y |  | 品种名称 |
| contract_id | varchar(80) | Y |  | 协议标的 |
| due_date | varchar(8) | Y |  | 到期日 |
| settle_due_price | varchar(40) | Y |  | 到期结算价 |
| bs_flag | varchar(1) | Y |  | 买卖 |
| price | numeric(19,2) | Y |  | 成交价 |
| qty | numeric(12,0) | Y |  | 成交量 |
| amt | numeric(12,0) | Y |  | 成交额 |
| fee | numeric(19,2) | Y |  | 手续费 |
| settle_fee | numeric(19,2) | Y |  | 结算费 |
| listing_date | varchar(8) | Y |  | 挂牌日期 |
| listing_no | varchar(20) | Y |  | 挂牌编号 |

---

## 599. dimple.tc_swap_settle_captial　(5 字段)
> 表含义：结算准备金明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 日期 |
| member_id | varchar(8) | Y |  | 席位号 |
| subject | varchar(80) | Y |  | 资金科目名称 |
| chg_type | varchar(10) | Y |  | 变动类型 |
| amt | numeric(19,2) | Y |  | 金额 |

---

## 600. dimple.tc_swap_settle_qry　(14 字段)
> 表含义：当日结算准备金查询　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| member_id | varchar(8) | Y |  | 席位号 |
| last_remain | numeric(19,2) | Y |  | 上日货币资金余额 |
| money_in | numeric(19,2) | Y |  | 当日入金 |
| float_profit | numeric(19,2) | Y |  | 当日盈亏 |
| due_profit | numeric(19,2) | Y |  | 到期盈亏 |
| money_out | numeric(19,2) | Y |  | 当日出金 |
| fee | numeric(19,2) | Y |  | 交易手续费 |
| settle_fee | numeric(19,2) | Y |  | 结算费 |
| interest | numeric(19,2) | Y |  | 利息 |
| other_in | numeric(19,2) | Y |  | 其它收入 |
| other_out | numeric(19,2) | Y |  | 其它支出 |
| balance | numeric(19,2) | Y |  | 当日货币资金余额 |
| remain | numeric(19,2) | Y |  | 结算准备金 |

---

## 601. dimple.tc_swift_info　(16 字段)
> 表含义：交易对手方SWIFT信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| counterparty_swift_no | varchar(20) | N | √ | 对方SWIFT号 |
| usd_interbank | varchar(40) | Y |  | 美金中转行账号 |
| usd_interbank_account | varchar(20) | Y |  | 美金中转行SWIFT号 |
| usd_agency | varchar(40) | Y |  | 美金代理行账号 |
| usd_agency_account | varchar(20) | Y |  | 美金代理行SWIFT号 |
| au_interbank | varchar(40) | Y |  | 黄金中转行账号 |
| au_interbank_account | varchar(20) | Y |  | 黄金中转行SWIFT号 |
| au_agency | varchar(40) | Y |  | 黄金代理行账号 |
| au_agency_account | varchar(20) | Y |  | 黄金代理行SWIFT号 |
| ag_interbank | varchar(40) | Y |  | 白银中转行账号 |
| ag_interbank_account | varchar(20) | Y |  | 白银中转行SWIFT账号 |
| ag_agency | varchar(40) | Y |  | 白银代理行账号 |
| ag_agency_account | varchar(20) | Y |  | 白银代理行SWIFT号 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 602. dimple.tc_swift_self　(11 字段)
> 表含义：上海银行本身swift账号　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| swift_no | varchar(20) | Y |  | 本行swift号 |
| usd_interbank | varchar(40) | Y |  | 美金中转行账号 |
| usd_interbank_account | varchar(20) | Y |  | 美金中转行SWIFT号 |
| usd_agency | varchar(40) | Y |  | 美金代理行账号 |
| usd_agency_account | varchar(20) | Y |  | 美金代理行SWIFT号 |
| au_interbank | varchar(40) | Y |  | 黄金中转行账号 |
| au_interbank_account | varchar(20) | Y |  | 黄金中转行SWIFT号 |
| au_agency | varchar(40) | Y |  | 黄金代理行账号 |
| au_agency_account | varchar(20) | Y |  | 黄金代理行SWIFT号 |
| ag_agency | varchar(40) | Y |  | 白银中转行账号 |
| ag_agency_account | varchar(20) | Y |  | 白银中转行SWIFT账号 |

---

## 603. dimple.tc_syscfee_breach_fee_detail　(12 字段)
> 表含义：违约费表　|　估算行数：**301**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| delivery_no | varchar(20) | N | √ | 交割序号 |
| bs_flag | bpchar(1) | N | √ | 买卖方向,见tp_public_dict的002 |
| client_id | varchar(16) | N |  | 客户代码 |
| member_id | varchar(8) | N | √ | 会员代码 |
| contract_id | varchar(20) | N |  | 合约代码 |
| qty | numeric(18,0) | Y |  | 数量:单位手 |
| price | numeric(20,8) | Y |  | 价格 |
| breach_direct | bpchar(1) | N | √ | 违约方向:见tp_public_dict的220 |
| effect_date | varchar(8) | N | √ | 违约日期 |
| fee_rate | numeric(22,6) | N |  | 违约费率 |
| fee | numeric(22,6) | N |  | 违约费 |

---

## 604. dimple.tc_syscfee_extra_charge_detail　(15 字段)
> 表含义：交割附加费表：白银用标准重量计算费用　|　估算行数：**700**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| delivery_no | varchar(20) | N | √ | 交割单号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志：见TP_PUBLIC_DICT的002 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| contract_id | varchar(20) | N |  | 合约号 |
| price | numeric(20,8) | Y |  | 交割交割 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| delivery_variety_id | varchar(3) | N |  | 交割品种号 |
| std_qty | numeric(10,0) | Y |  | 标准交割重量 |
| std_amount | numeric(18,2) | Y |  | 标准金额 |
| fee_kind | varchar(8) | N | √ | 费率类型:见tp_public_dict的354 |
| fee_rate | numeric(22,6) | N |  | 费率 |
| fee | numeric(22,6) | N |  | 费用 |

---

## 605. dimple.tc_syscfee_inquire_fee_detail　(22 字段)
> 表含义：询价手续费明细表　|　估算行数：**3,512**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_no | varchar(20) | N |  | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| seq_no | float8 | N | √ | 成交流水号 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| trader_no | varchar(40) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| qty | numeric(24,6) | Y |  | 成交量：单位kg |
| amt | numeric(24,6) | Y |  | 成交金额：单位元 |
| price | numeric(20,8) | Y |  | 成交价格 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| period | numeric(10,0) | Y |  | 期限 |
| period_abbr | varchar(20) | Y |  | 期限名称 |
| fee_rate | numeric(22,6) | Y |  | 手续费率 |
| fee | numeric(24,6) | Y |  | 手续费 |

---

## 606. dimple.tc_system_calc_fee_clear　(5 字段)
> 表含义：Dimple系统自计算费用表　|　估算行数：**3,071**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| exch_code | varchar(3) | N | √ | 交易所 |
| fee_type | varchar(3) | N | √ | 费用类型:见tp_public_dict的233 |
| fee_amt | numeric(24,6) | Y |  | 费用 |
| note | varchar(255) | Y |  | 备注 |

---

## 607. dimple.tc_system_cfee_clear_detail　(15 字段)
> 表含义：结算手续费明细　|　估算行数：**1,519,293**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| qty | numeric(20,8) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| clear_fee | numeric(24,6) | Y |  | 结算费 |

---

## 608. dimple.tc_system_cfee_clear_trader　(17 字段)
> 表含义：交易员结算手续费明细　|　估算行数：**1,022,889**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(16) | N | √ | 席位号 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| qty | numeric(20,8) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| clear_fee | numeric(24,6) | Y |  | 结算费 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 609. dimple.tc_system_cfee_defer_detail　(11 字段)
> 表含义：递延费明细　|　估算行数：**12,636**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓 |
| buy_qty | numeric(12,0) | Y |  | 买持仓 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| defer_fee | numeric(24,6) | Y |  | 递延费 |

---

## 610. dimple.tc_system_cfee_delivery_detail　(13 字段)
> 表含义：交割费明细　|　估算行数：**1,194**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| delivery_fee | numeric(24,6) | Y |  | 交割手续费 |

---

## 611. dimple.tc_system_cfee_delivery_trader　(15 字段)
> 表含义：交割费明细　|　估算行数：**1,091**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| trader_no | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约 |
| sh_flag | varchar(3) | N | √ | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| delivery_fee | numeric(24,6) | Y |  | 交割手续费 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 612. dimple.tc_system_cfee_overdue_detail　(14 字段)
> 表含义：超期费明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| overdue_fee | numeric(24,6) | Y |  | 超期费 |

---

## 613. dimple.tc_system_cfee_overdue_trader　(16 字段)
> 表含义：交易员超期费明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| overdue_fee | numeric(24,6) | Y |  | 超期费 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 614. dimple.tc_system_cfee_trade_detail　(17 字段)
> 表含义：系统计算手续费　|　估算行数：**1,723,085**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| qty | numeric(12,0) | Y |  | 数量 |
| short_qty | numeric(12,0) | Y |  | 短线数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| fee_rate_short | numeric(12,8) | Y |  | 短线手续费率 |
| trade_fee | numeric(24,6) | Y |  | 手续费 |

---

## 615. dimple.tc_system_cfee_trader_detail　(19 字段)
> 表含义：系统计算交易员手续费　|　估算行数：**1,225,237**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| match_no | varchar(20) | N | √ | 成交号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N | √ | 买卖标志:见tp_public_dict的002 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| qty | numeric(12,0) | Y |  | 数量 |
| short_qty | numeric(12,0) | Y |  | 短线数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| fee_rate_short | numeric(12,8) | Y |  | 短线手续费率 |
| trade_fee | numeric(24,6) | Y |  | 手续费 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 616. dimple.tc_system_short_fee_detail　(20 字段)
> 表含义：系统计算短线手续费　|　估算行数：**109,405**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N |  | 成交号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| qty | numeric(12,0) | Y |  | 数量 |
| short_qty | numeric(12,0) | Y |  | 短线数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_type | varchar(3) | Y |  | 手续费类型:见tp_public_dict的092 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| fee_rate_short | numeric(12,8) | Y |  | 短线手续费率 |
| trade_fee | numeric(24,6) | Y |  | 手续费 |
| short_fee | numeric(24,6) | Y |  | 短线手续费 |
| ret_fee | numeric(24,6) | Y |  | 返还手续费 |

---

## 617. dimple.tc_system_short_fee_trader　(22 字段)
> 表含义：系统计算交易员短线手续费　|　估算行数：**7,238**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 清算日期 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所 |
| match_no | varchar(20) | N |  | 成交号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| contract_id | varchar(20) | Y |  | 合约 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| eo_flag | varchar(3) | Y |  | 开平标志:见tp_public_dict的003 |
| qty | numeric(12,0) | Y |  | 数量 |
| short_qty | numeric(12,0) | Y |  | 短线数量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| amt | numeric(24,6) | Y |  | 金额 |
| fee_type | varchar(3) | Y |  | 手续费类型:见tp_public_dict的092 |
| fee_rate | numeric(12,8) | Y |  | 费率 |
| fee_rate_short | numeric(12,8) | Y |  | 短线手续费率 |
| trade_fee | numeric(24,6) | Y |  | 手续费 |
| short_fee | numeric(24,6) | Y |  | 短线手续费 |
| ret_fee | numeric(24,6) | Y |  | 返还手续费 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 618. dimple.tc_task_check　(11 字段)
> 表含义：任务检查配置表　|　估算行数：**2**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| bank_no | varchar(4) | N | √ | 银行代码: 参考interface.tp_para表的ACCOUNT_CTL_TYPE参数值，写入对应代码，上海银行代码为7 |
| task_id | varchar(10) | N | √ | 任务代码 |
| task_desc | varchar(255) | Y |  | 任务说明 |
| checked_time | varchar(4) | N | √ | 检查时机：1-结算前检查；2-日终对账后检查；3-交易初始化前检查； |
| customized | varchar(4) | N |  | 是否定制化任务: 0-否；1-是 |
| forced | varchar(4) | N |  | 是否允许强制通过: 0-否；1-是 |
| date_exec | varchar(8) | N | √ | 执行日期 |
| time_exec | varchar(22) | Y |  | 执行时间 |
| finished | varchar(4) | N |  | 执行完成标志: 0-未执行；1-执行完成；2-执行失败；3-强制跳过 |
| times | numeric(10,0) | N |  | 执行次数 |
| exec_desc | varchar(255) | Y |  | 执行说明 |

---

## 619. dimple.tc_trade_sync　(3 字段)
> 表含义：交易同步数据库状态表　|　估算行数：**1,581**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| sync_id | varchar(20) | N | √ | 同步源 |
| sync_status | bpchar(1) | N |  | 同步状态:见tp_public_code的180 |

---

## 620. dimple.tc_trader_buyout_detail_clear　(17 字段)
> 表含义：境外拆借买断明细表　|　估算行数：**24**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| buy_trade_date | varchar(8) | N | √ | 买断成交日期 |
| lend_trade_date | varchar(8) | N |  | 拆借成交日期 |
| match_no | varchar(30) | N | √ | 成交号 |
| seq_no | float8 | N | √ | 系统编号 |
| buy_no | varchar(30) | N | √ | 买断编号 |
| lend_flag | varchar(3) | N | √ | 拆借方向:public_dict的221只包含拆入和拆出 |
| trader_no | varchar(16) | N | √ | 交易员 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(20,8) | Y |  | 买断价格 |
| qty | numeric(16,6) | Y |  | 买断数量 |
| cost_price | numeric(20,8) | Y |  | 成本价 |
| purpose_code | varchar(4) | Y |  | 交易目的 |
| profit | numeric(24,6) | Y |  | 盈亏 |
| trade_type | varchar(3) | N | √ | 交易类型:见tp_public_dict的298 |

---

## 621. dimple.tc_trader_cancel　(16 字段)
> 表含义：交易员强撤记录表　|　估算行数：**98**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| order_no | varchar(20) | N | √ | 系统委托号 |
| user_id | varchar(30) | Y |  | 交易员号 |
| member_id | varchar(8) | Y |  | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| client_id | varchar(16) | Y |  | 客户号 |
| bs_flag | varchar(20) | N |  | 买卖标志 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 委托价格 |
| match_qty | numeric(12,0) | Y |  | 成交量 |
| order_qty | numeric(12,0) | N |  | 委托数量 |
| cancel_oper | varchar(30) | N |  | 撤单交易员号 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| offset_type | bpchar(1) | Y |  | 平仓类型:见tp_public_dict的179 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 622. dimple.tc_trader_cash_detail_clear　(18 字段)
> 表含义：现金交割明细表　|　估算行数：**1,659**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| trade_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(30) | N | √ | 成交号 |
| bs_flag | varchar(3) | N | √ | 买卖方向:public_dict的002 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(10) | Y |  | 客户号 |
| trader_no | varchar(16) | N | √ | 交易员 |
| delivery_variety_id | varchar(3) | Y |  | 品种号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| price | numeric(24,6) | Y |  | 成交价格 |
| qty | numeric(20,3) | Y |  | 成交数量 |
| match_type | varchar(3) | Y |  | 类型：1普通 |
| calc_price_type | varchar(3) | Y |  | 参考价格类型：1开盘价;2收盘价;3结算价;4基准价(上午);5基准价(下午);6固定值;7基准价夜市;9其他价格 |
| calc_price_date | varchar(8) | Y |  | 参考价格日期 |
| calc_price | numeric(24,6) | Y |  | 参考价格 |
| clear_price | numeric(24,6) | Y |  | 当日结算价 |
| purpose_code | varchar(4) | Y |  | 交易目的 |
| profit | numeric(30,6) | Y |  | 盈亏 |

---

## 623. dimple.tc_trader_conpor_clear　(16 字段)
> 表含义：交易员结算合约盈亏表　|　估算行数：**43,072**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 累计持仓盈亏 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 624. dimple.tc_trader_contract_profit　(15 字段)
> 表含义：交易员交易合约盈亏表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| last_price | numeric(20,8) | Y |  | 最新价 |
| op_time | varchar(8) | Y |  | 时间 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 625. dimple.tc_trader_cost　(10 字段)
> 表含义：交易员合约成本表 品种内容仅限于现货、境外黄金　|　估算行数：**8**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量：现货为手；境外黄金为 盎司 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：现货为元；境外黄金为 美元 |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 626. dimple.tc_trader_cost_clear　(10 字段)
> 表含义：交易员合约成本结算表 品种内容仅限于现货、境外黄金　|　估算行数：**37,255**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量：现货为手；境外黄金为 盎司 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：现货为元；境外黄金为 美元 |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 627. dimple.tc_trader_cost_detail　(20 字段)
> 表含义：交易员合约成本明细表 品种内容仅限于现货、境外黄金　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| seq_no | varchar(10) | N | √ | 流水号 |
| exch_seq_no | varchar(20) | N |  | 交易所流水号:现货买卖未成交号，现货出入库为交易所流水号，现货调拨为DB+调拨号，境外黄金为成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖标志:见tp_public_dict的002 |
| trans_type | varchar(2) | Y |  | 库存变化类型:见tp_public_dict的221 |
| price | numeric(20,8) | Y |  | 价格：现货为元/克；境外黄金为 美元/盎司 |
| qty | numeric(25,8) | Y |  | 数量：现货为手；境外黄金为 盎司 |
| amt | numeric(24,6) | Y |  | 成交金额：现货为元；境外黄金为 美元 |
| last_remain_qty | numeric(25,8) | Y |  | 上次剩余数量：现货为手；境外黄金为 盎司，卖空时为负 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量：现货为手；境外黄金为 盎司，卖空时为负 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：现货为元；境外黄金为 美元 |
| realized_profitloss | numeric(18,6) | Y |  | 实现盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| last_remain_cost | numeric(24,6) | Y |  | 上次剩余成本：现货为元；境外黄金为 美元 |
| last_weighted_price | numeric(20,8) | Y |  | 上次加权平均价：黄金为元/克，白银：元/千克 |

---

## 628. dimple.tc_trader_cost_detail_clear　(20 字段)
> 表含义：交易员合约成本明细结算表 品种内容仅限于现货、境外黄金　|　估算行数：**8,576**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| seq_no | varchar(10) | N | √ | 流水号 |
| exch_seq_no | varchar(20) | N |  | 交易所流水号:现货未交易所流水号，境外黄金为成交号 |
| bs_flag | bpchar(1) | Y |  | 买卖标志:见tp_public_dict的002 |
| trans_type | varchar(2) | Y |  | 库存变化类型:见tp_public_dict的221 |
| price | numeric(20,8) | Y |  | 价格：现货为元/克；境外黄金为 美元/盎司 |
| qty | numeric(25,8) | Y |  | 数量：现货为手；境外黄金为 盎司 |
| amt | numeric(24,6) | Y |  | 成交金额：现货为元；境外黄金为 美元 |
| last_remain_qty | numeric(25,8) | Y |  | 上次剩余数量：现货为手；境外黄金为 盎司，卖空时为负 |
| remain_qty | numeric(25,8) | Y |  | 剩余数量：现货为手；境外黄金为 盎司，卖空时为负 |
| weighted_price | numeric(20,8) | Y |  | 加权平均价：黄金为元/克，白银：元/千克 |
| remain_cost | numeric(24,6) | Y |  | 剩余成本：现货为元；境外黄金为 美元 |
| realized_profitloss | numeric(24,6) | Y |  | 实现盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| last_remain_cost | numeric(24,6) | Y |  | 上次剩余成本：现货为元；境外黄金为 美元 |
| last_weighted_price | numeric(20,8) | Y |  | 上次加权平均价：黄金为元/克，白银：元/千克 |

---

## 629. dimple.tc_trader_credit　(19 字段)
> 表含义：交易员信用额度表　|　估算行数：**146**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| currency | varchar(3) | N | √ | 币种:见tp_public_dict的435 |
| credit_tot | numeric(18,2) | Y |  | 信用额度 |
| credit_used | numeric(18,2) | Y |  | 已用信用额度 |
| credit_frozen | numeric(18,2) | Y |  | 冻结信用额度 |
| credit_remain | numeric(18,2) | Y |  | 剩余信用额度 |
| float_profitloss | numeric(18,2) | Y |  | 累计持仓盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 累计平仓盈亏 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| if_check | varchar(3) | N |  | 是否检查:见tp_public_dict的120 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 630. dimple.tc_trader_credit_check　(23 字段)
> 表含义：交易员信用额度复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| exch_code | varchar(2) | Y |  | 交易所 |
| member_id | varchar(8) | Y |  | 会员号 |
| user_id | varchar(30) | Y |  | 交易员号 |
| currency | varchar(3) | Y |  | 币种 |
| credit_tot | numeric(18,2) | Y |  | 信用额度 |
| credit_used | numeric(18,2) | Y |  | 已用信用额度 |
| credit_frozen | numeric(18,2) | Y |  | 冻结信用额度 |
| credit_remain | numeric(18,2) | Y |  | 剩余信用额度 |
| float_profitloss | numeric(18,2) | Y |  | 累计持仓盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 累计平仓盈亏 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| if_check | varchar(3) | N |  | 是否检查:见tp_public_dict的120 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 631. dimple.tc_trader_credit_clear　(21 字段)
> 表含义：交易员历史信用额度表　|　估算行数：**456,379**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| currency | varchar(3) | N | √ | 币种:见tp_public_dict的435 |
| credit_tot | numeric(18,2) | Y |  | 信用额度 |
| credit_used | numeric(18,2) | Y |  | 已用信用额度 |
| credit_frozen | numeric(18,2) | Y |  | 冻结信用额度 |
| credit_remain | numeric(18,2) | Y |  | 剩余信用额度 |
| operator | varchar(30) | Y |  | 操作员 |
| float_profitloss | numeric(18,2) | Y |  | 累计持仓盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 累计平仓盈亏 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| if_check | varchar(3) | N |  | 是否检查:见tp_public_dict的120 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 632. dimple.tc_trader_credit_jour　(11 字段)
> 表含义：交易员信用额度流水表　|　估算行数：**853**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| seq_no | float8 | N | √ | 流水号:ORACLE的seq |
| exch_code | varchar(2) | Y |  | 交易所 |
| member_id | varchar(8) | Y |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员号 |
| currency | varchar(3) | N |  | 币种 |
| change_credit | numeric(18,2) | Y |  | 变化额度 |
| op_type | varchar(2) | N |  | 信用额度流水操作类型:见tp_public_dict的068 |
| status | varchar(1) | Y |  | 流水状态:见tp_public_dict的209 |
| operator | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 633. dimple.tc_trader_delivery_posi　(22 字段)
> 表含义：交易员交割持仓表:期货交割持仓表:记录期转现，滚动交割，一次性交割的平仓量和相应资金.日终结算产生　|　估算行数：**1,462**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| match_date | varchar(8) | N |  | 配对日 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| delivery_way | varchar(2) | N |  | 交割方式:见tp_public_dict的051 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| ahead_buy_qty | numeric(12,0) | Y |  | 提前买交割量 |
| ahead_sell_qty | numeric(12,0) | Y |  | 提前卖交割量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_margin | numeric(18,2) | Y |  | 买保证金:仅对滚动交割和一次性交割有效；指买方转货款；此字段仅用来查询。 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金:仅对滚动交割和一次性交割有效；指卖方转交割保证金；此字段仅用来查询。 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| wrap_price | numeric(20,8) | Y |  | 包装物价格 |
| delivery_fee | numeric(18,2) | Y |  | 交割手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| clear_account_no | varchar(14) | Y |  | 结算帐号 |
| delivery_date | varchar(8) | Y |  | 交割日 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 634. dimple.tc_trader_forces　(17 字段)
> 表含义：交易员强平记录表　|　估算行数：**58**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| local_no | varchar(20) | N | √ | 本地委托号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| bs_flag | varchar(20) | N |  | 买卖标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| order_qty | numeric(12,0) | Y |  | 委托数量 |
| input_oper | varchar(30) | N |  | 录入人 |
| input_time | varchar(12) | Y |  | 录入时间 |
| rechk_oper | varchar(30) | Y |  | 复核人 |
| rechk_time | varchar(12) | Y |  | 复核时间 |
| force_offset_reason | varchar(2) | Y |  | 强平原因:见tp_public_dict的040 |
| status | bpchar(1) | N |  | 状态 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| offset_type | bpchar(1) | Y |  | 平仓类型:见tp_public_dict的179 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 635. dimple.tc_trader_id_rel　(3 字段)
> 表含义：交易员与交易员系统编号关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(30) | N |  | 操作员代码-对应系统内交易员 |
| purpose_code | varchar(3) | N |  | 交易目的代码 |
| trader_system_id | varchar(3) | N |  | 操作员系统编号-对应急速系统操作员编号,2位数字 |

---

## 636. dimple.tc_trader_integrate_posi　(11 字段)
> 表含义：交易员综合头寸表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| qty | numeric(18,6) | Y |  | 头寸数量：期货、现货为手；境外黄金为盎司 |
| cost_price | numeric(20,8) | Y |  | 最新成本价：期货、现货为元/克；境外黄金为 美元/盎司 |
| price | numeric(20,8) | Y |  | 最新价：期货、现货为元/克；境外黄金为 美元/盎司 |
| unrpl | numeric(19,6) | Y |  | 当日未实现盈亏：期货、现货为元；境外黄金为 美元 |
| rpl | numeric(19,6) | Y |  | 当日实现盈亏：期货、现货为元；境外黄金为 美元 |
| profitless | numeric(19,6) | Y |  | 总盈亏：期货、现货为元；境外黄金为 美元 |

---

## 637. dimple.tc_trader_integrate_posi_clear　(13 字段)
> 表含义：交易员综合头寸结算表　|　估算行数：**114,311**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| qty | numeric(25,8) | Y |  | 头寸数量：期货、现货为手；境外黄金为 盎司 |
| cost_price | numeric(26,8) | Y |  | 成本价：期货、现货为元/克；境外黄金为 美元/盎司 |
| clear_price | numeric(20,8) | Y |  | 结算价期货、现货为元/克；境外黄金为 美元/盎司 |
| unrpl | numeric(24,6) | Y |  | 当日未实现盈亏 |
| rpl | numeric(24,6) | Y |  | 当日实现盈亏 |
| profitloss | numeric(24,6) | Y |  | 年总盈亏 |
| month_profitloss | numeric(24,6) | Y |  | 月累计总盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 638. dimple.tc_trader_kondor_tot　(12 字段)
> 表含义：交易员kondor成交统计表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_qty | numeric(15,2) | Y |  | 当日买入(盎司) |
| sell_qty | numeric(15,2) | Y |  | 当日买出(盎司) |
| buy_amt_usa | numeric(24,6) | Y |  | 当日买金额(美元) |
| sell_amt_usa | numeric(24,6) | Y |  | 当日卖金额(美元) |
| month_amt_usa | numeric(24,6) | Y |  | 月成交额(美元)(卖-买) |
| year_amt_usa | numeric(24,6) | Y |  | 年成交额(美元)(卖-买) |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 639. dimple.tc_trader_posi_detail_shfe　(13 字段)
> 表含义：交易员级别：上期所合约最后交易日持仓明细表；目前仅供浙商银行summit使用　|　估算行数：**173,298**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 640. dimple.tc_trader_posi_move　(16 字段)
> 表含义：交易员持仓内部调转表　|　估算行数：**225**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | numeric(12,0) | N | √ | 调拨流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约 |
| bs_flag | varchar(3) | N |  | 买卖标志 |
| sh_flag | varchar(3) | N |  | 投保标志:见tp_public_dict的004 |
| qty | numeric(15,3) | N |  | 调拨数量 |
| price | numeric(20,8) | N |  | 调拨价格 |
| user_id_out | varchar(16) | N |  | 交易员调出方 |
| user_id_in | varchar(16) | N |  | 交易员调入方 |
| purpose_code_in | varchar(3) | N |  | 调入交易目的 |
| purpose_code_out | varchar(3) | N |  | 调出交易目的 |
| notes | varchar(254) | Y |  | 备注 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |

---

## 641. dimple.tc_trader_profit_recalc　(20 字段)
> 表含义：交易员买卖日盈亏　|　估算行数：**1,291,168**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 清算日期 |
| market_type | varchar(3) | Y |  | 市场类型:见tp_public_dict的001 |
| bus_type | varchar(3) | Y |  | 业务类型:见tp_public_dict的253 |
| trade_type | varchar(3) | Y |  | 交易类型:见tp_public_dict的253 只包含即期和远期 |
| curency | varchar(3) | Y |  | 币种:见tp_public_dict的036 |
| match_no | varchar(30) | Y |  | 成交号 |
| seq_no | varchar(20) | Y |  | 流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(16) | Y |  | 交易员 |
| contract_id | varchar(20) | N |  | 合约号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| qty | numeric(16,6) | N |  | 数量：黄金克；白银千克 |
| price | numeric(20,8) | Y |  | 成交价 |
| calc_price | numeric(20,8) | Y |  | 公允价 |
| last_calc_price | numeric(20,8) | Y |  | 上日公允价 |
| profit_type | varchar(3) | Y |  | 盈亏类型：1、买卖盈亏；2、浮动盈亏 |
| profit | numeric(24,6) | Y |  | 盈亏 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| convert_rate | numeric(20,8) | Y |  | 汇率 |

---

## 642. dimple.tc_trader_profit_tot　(7 字段)
> 表含义：交易员交易总额盈亏表　|　估算行数：**28**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| currency | varchar(3) | N | √ | 币种 |
| sum_float_profitloss | numeric(18,2) | Y |  | 累计持仓盈亏 |
| op_time | varchar(8) | Y |  | 时间 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 643. dimple.tc_trader_profit_tot_clear　(7 字段)
> 表含义：交易员结算总额盈亏表　|　估算行数：**16,112**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| currency | varchar(3) | N | √ | 币种 |
| sum_float_profitloss | numeric(18,2) | Y |  | 累计持仓盈亏 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 644. dimple.tc_trader_purpose　(9 字段)
> 表含义：交易员交易目的表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(30) | N | √ | 交易员编码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| tpcode | varchar(3) | N | √ | 交易目的字段 |
| if_default | varchar(3) | Y |  | 是否为默认值 |
| create_date | timestamp | Y |  | 创建日期 |
| create_id | varchar(30) | Y |  | 创建人 |
| modify_date | timestamp | Y |  | 修改日期 |
| modify_id | varchar(30) | Y |  | 修改人 |

---

## 645. dimple.tc_trader_rfq_deli_posi_clear　(12 字段)
> 表含义：交易员保证金询价交割持仓表　|　估算行数：**532**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| due_date | varchar(8) | N | √ | 到期日 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量：手 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量：手 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| amount | numeric(18,2) | Y |  | 交割货款 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| trader_no | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 646. dimple.tc_trader_rfq_mrg_posi_clear　(13 字段)
> 表含义：交易员保证金询价保证金表　|　估算行数：**668**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| swap_qty | numeric(12,0) | Y |  | 掉期持仓量 |
| uniltr_qty | numeric(12,0) | Y |  | 单边持仓量 |
| swap_margin | numeric(18,2) | Y |  | 掉期保证金 |
| uniltr_margin | numeric(18,2) | Y |  | 单边保证金 |
| margin | numeric(18,2) | Y |  | 持仓保证金=掉期保证金+单边保证金 |
| trader_no | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 647. dimple.tc_trader_rfq_posi_clear　(22 字段)
> 表含义：交易员保证金询价持仓表　|　估算行数：**1,073**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(30) | N | √ | 合约代码 |
| due_date | varchar(8) | N | √ | 到期日 |
| last_buy_qty | numeric(12,0) | Y |  | 上日多头持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日空头持仓量 |
| last_net_qty | numeric(12,0) | Y |  | 上日净持仓 |
| t_buy_qty | numeric(12,0) | Y |  | 当日买量 |
| t_sell_qty | numeric(12,0) | Y |  | 当日卖量 |
| t_buy_amt | numeric(18,2) | Y |  | 当日买金额 |
| t_sell_amt | numeric(18,2) | Y |  | 当日卖金额 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| net_qty | numeric(12,0) | Y |  | 净持仓 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| delivery_margin | numeric(18,2) | Y |  | 交割保证金：到期日=下一交易日 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| trader_no | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| buy_amt | numeric(18,2) | Y |  | 买额 |
| sell_amt | numeric(18,2) | Y |  | 卖额 |

---

## 648. dimple.tc_trader_rfq_posi_move　(16 字段)
> 表含义：交易员保证金询价持仓内部调转表　|　估算行数：**21**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | numeric(12,0) | N | √ | 调拨流水号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_no | numeric(8,0) | Y |  | 合约编号 |
| contract_id | varchar(20) | N |  | 合约 |
| due_date | varchar(8) | N |  | 到期日 |
| bs_flag | varchar(3) | N |  | 买卖标志 |
| qty | numeric(15,3) | N |  | 调拨数量 |
| price | numeric(20,8) | N |  | 调拨价格 |
| user_id_out | varchar(16) | N |  | 交易员调出方 |
| user_id_in | varchar(16) | N |  | 交易员调入方 |
| purpose_code_in | varchar(3) | N |  | 调入交易目的 |
| purpose_code_out | varchar(3) | N |  | 调出交易目的 |
| notes | varchar(254) | Y |  | 备注 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |

---

## 649. dimple.tc_trader_spot_clear　(11 字段)
> 表含义：交易员现货合约结算表　|　估算行数：**3,253**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| buy_qty | numeric(12,0) | Y |  | 当日买入 |
| sell_qty | numeric(12,0) | Y |  | 当日买出 |
| trade_fee | numeric(18,2) | Y |  | 手续费 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 650. dimple.tc_trader_storage　(15 字段)
> 表含义：交易员交易库存表　|　估算行数：**5**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| frozen_storage | numeric(16,6) | Y |  | 冻结库存 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| etf_frozen_storage | numeric(16,6) | Y |  | 认申赎冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 651. dimple.tc_trader_storage_clear　(14 字段)
> 表含义：交易员结算库存表　|　估算行数：**25,246**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| etf_frozen_storage | numeric(16,6) | Y |  | 认申赎冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 652. dimple.tc_trader_storage_jour　(20 字段)
> 表含义：交易员库存流水　|　估算行数：**13,892**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| exch_seq_no | varchar(10) | N | √ | 交易所流水号 |
| dispatch_no | float8 | N | √ | 分配流水号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| trans_type | varchar(2) | N |  | 库存变化类型:见tp_public_dict的221 |
| qty | numeric(15,3) | Y |  | 分配数量 |
| price | numeric(20,8) | Y |  | 价格 |
| status | bpchar(2) | N |  | 系统状态 |
| io_flag | bpchar(1) | N |  | 出入库标志:见tp_public_dict的230 |
| notes | varchar(254) | Y |  | 备注 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |
| contract_id | varchar(20) | Y |  | 合约号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| effect_date | varchar(8) | N |  | 生效日期 |
| isnote_flag | varchar(2) | Y |  | 是否备注 |

---

## 653. dimple.tc_trader_storage_move　(15 字段)
> 表含义：交易员库存内部调拨表　|　估算行数：**69**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 调拨流水号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| user_id_out | varchar(16) | N |  | 交易员调出方 |
| user_id_in | varchar(16) | N |  | 交易员调入方 |
| purpose_code_in | varchar(3) | N |  | 调入交易目的 |
| purpose_code_out | varchar(3) | N |  | 调出交易目的 |
| qty | numeric(15,3) | N |  | 调拨数量 |
| price | numeric(20,8) | Y |  | 调拨价格 |
| notes | varchar(254) | Y |  | 备注 |
| if_calc | varchar(3) | N |  | 是否用于拆借:见dict的027 |
| op_time | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作人 |

---

## 654. dimple.tc_trader_storage_tmp　(16 字段)
> 表含义：交易员库存临时表　|　估算行数：**5**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| source_flag | varchar(3) | Y |  | 来源:1 初始化 2 库存分配 3成交分配 4库存调拨 |
| total_storage | numeric(16,6) | Y |  | 库存总量 |
| frozen_storage | numeric(16,6) | Y |  | 冻结库存 |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| etf_frozen_storage | numeric(16,6) | Y |  | 认申赎冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 655. dimple.tc_trader_um　(5 字段)
> 表含义：交易员与UM对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(30) | N | √ | 交易员 |
| um_id | varchar(60) | N | √ | UM账号 |
| op_oper | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 656. dimple.tc_trader_vaexp_tmp　(9 字段)
> 表含义：交易员品种敞口额度临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | Y |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| frozen_exposure | numeric(22,6) | Y |  | 冻结敞口 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| buy_frozen_exposure | numeric(22,6) | Y |  | 买冻结敞口 |
| sell_frozen_exposure | numeric(22,6) | Y |  | 卖冻结敞口 |

---

## 657. dimple.tc_trading_order_clear　(9 字段)
> 表含义：交易目的级结算交易指令表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交单号 |
| client_id | varchar(16) | N |  | 客户号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| bs_flag | bpchar(1) | N | √ | 买卖方向 |
| trader_no | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(30) | N |  | 合约号 |
| member_id | varchar(8) | N | √ | 会员号 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| investment_strategy | varchar(4) | N | √ | 投资策略 |

---

## 658. dimple.tc_transtype_tdpps_config　(5 字段)
> 表含义：库存流水类型默认交易员交易目的配置:需要实施人员与客户定规则后提供零级数据;场上有效情况整理：配置全部有效，但是F-现货买入;G-现货卖出 不要配置进来,否则场上计算库存翻倍（因现货成交时根据成交计算库存变化）结算时有效情况整理：1. 下面7个库存流水配置了对结算不起作用M-大宗交易买入;N-大宗交易卖出;F-现货买入;G-现货卖出;H-处置质物;W-内部调转入;X-内部调转出;2.下面2个库存流水类型要注意，同对应的即远掉到期清算单的分配要一致0-询价卖出；L-询价买入;3.当tp_para参数中 LEND_MANAGER_TYPE=2-上海银行管理方式 时，以下8个库存流水类型配置了对结算不起作用B;C;Y;Z;21;22;23;24;4.以下ETF相关的8个库存流水类型配置了对结算不起作用11;12;13;14;15;16;17;18;5.其他库存流水类型配置了对结算起作用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| trans_type | varchar(2) | N | √ | 库存变化类型:见tp_public_dict的221 |
| trader_no | varchar(30) | N |  | 指定交易员 |
| tpcode | varchar(3) | N |  | 指定交易目的 |

---

## 659. dimple.tc_um_pwd　(2 字段)
> 表含义：中行员工号账号信息表　|　估算行数：**9**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| um_id | varchar(20) | N |  | Um账号 |
| pwd | varchar(256) | Y |  | Um密码 |

---

## 660. dimple.tc_usap_relationship　(6 字段)
> 表含义：USAP统一认证账号对应关系　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | Y |  | 操作员号 |
| usap_no | varchar(15) | Y |  | USAP账号 |
| sfz_id | varchar(18) | Y |  | 身份证号 |
| staff_id | numeric(24,0) | Y |  | 员工号 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |

---

## 661. dimple.tc_usd_offset_posi_clear　(23 字段)
> 表含义：美元平盘头寸结算表　|　估算行数：**1,279**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| currency | varchar(3) | N | √ | 货币：USD |
| last_m_money_in | numeric(24,8) | Y |  | 上一日贵金属平盘卖出收入头寸：美元 |
| last_m_money_out | numeric(24,8) | Y |  | 上一日贵金属平盘买入支出头寸：美元 |
| last_u_buy_amt1 | numeric(24,8) | Y |  | 上一日美元平盘买入头寸：美元 |
| last_u_sell_amt1 | numeric(24,8) | Y |  | 上一日美元平盘卖出头寸：美元 |
| last_u_buy_amt2 | numeric(24,8) | Y |  | 上一日美元平盘买入头寸：元;单位换算 |
| last_u_sell_amt2 | numeric(24,8) | Y |  | 上一日美元平盘卖出头寸：元;单位换算 |
| metal_money_in | numeric(24,8) | Y |  | 贵金属平盘卖出收入头寸：美元 |
| metal_money_out | numeric(24,8) | Y |  | 贵金属平盘买入支出头寸：美元 |
| metal_net_money | numeric(24,8) | Y |  | 贵金属平盘轧差头寸：美元；公式=今日贵金属平盘卖出收入金额+上一日贵金属平盘卖出收入头寸-今日贵金属平盘买入支出金额-上一日贵金属平盘买入支出头寸 |
| t_metal_money_in | numeric(24,8) | Y |  | 今日贵金属平盘卖出收入金额：美元 |
| t_metal_money_out | numeric(24,8) | Y |  | 今日贵金属平盘买入支出金额：美元 |
| usd_buy_amt1 | numeric(24,8) | Y |  | 美元平盘买入头寸：美元 |
| usd_sell_amt1 | numeric(24,8) | Y |  | 美元平盘卖出头寸：美元 |
| usd_net_amt1 | numeric(24,8) | Y |  | 美元平盘轧差头寸：美元 |
| t_usd_buy_amt1 | numeric(24,8) | Y |  | 今日美元平盘买入金额：美元 |
| t_usd_sell_amt1 | numeric(24,8) | Y |  | 今日美元平盘卖出金额：美元 |
| usd_buy_amt2 | numeric(24,8) | Y |  | 美元平盘买入头寸：元；为0或者有值；单位从美元换算成元 |
| usd_sell_amt2 | numeric(24,8) | Y |  | 美元平盘卖出头寸：元；为0或者有值；单位换算 |
| usd_net_amt2 | numeric(24,8) | Y |  | 美元平盘轧差头寸：元；单位换算 |
| t_usd_buy_amt2 | numeric(24,8) | Y |  | 今日美元平盘买入金额：元；单位换算 |
| t_usd_sell_amt2 | numeric(24,8) | Y |  | 今日美元平盘卖出金额：元；单位换算 |

---

## 662. dimple.tc_vaexp_clear　(17 字段)
> 表含义：结算品种敞口额度表　|　估算行数：**8,032,338**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| operator | varchar(30) | Y |  | 操作员 |
| market_type | bpchar(1) | N | √ | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| ifcheck | varchar(3) | Y |  | 是否检查敞敞口:见tp_public_dict的120 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 663. dimple.tc_variety_exposure　(18 字段)
> 表含义：品种敞口额度表　|　估算行数：**5,712**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| frozen_exposure | numeric(22,6) | Y |  | 冻结敞口额度 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| buy_frozen_exposure | numeric(22,6) | Y |  | 买冻结敞口 |
| sell_frozen_exposure | numeric(22,6) | Y |  | 卖冻结敞口 |
| market_type | bpchar(1) | N | √ | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| ifcheck | varchar(1) | Y |  | 是否设置检查 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 664. dimple.tc_variety_exposure_bak　(18 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N |  |  |
| user_id | varchar(30) | N |  |  |
| variety_id | varchar(4) | N |  |  |
| day_exposure | numeric(22,6) | Y |  |  |
| overnight_exposure | numeric(22,6) | Y |  |  |
| frozen_exposure | numeric(22,6) | Y |  |  |
| used_exposure | numeric(22,6) | Y |  |  |
| buy_frozen_exposure | numeric(22,6) | Y |  |  |
| sell_frozen_exposure | numeric(22,6) | Y |  |  |
| market_type | bpchar(1) | N |  |  |
| purpose_code | varchar(3) | N |  |  |
| ifcheck | varchar(1) | Y |  |  |
| create_id | varchar(30) | Y |  |  |
| create_date | varchar(8) | Y |  |  |
| create_time | varchar(8) | Y |  |  |
| update_id | varchar(30) | Y |  |  |
| update_date | varchar(8) | Y |  |  |
| update_time | varchar(8) | Y |  |  |

---

## 665. dimple.tc_variety_exposure_own　(11 字段)
> 表含义：品种敞口额度表:保存不考虑和交易目的树交易员树的数据　|　估算行数：**3,632,098**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| user_id | varchar(30) | N | √ | 交易员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| operator | varchar(30) | Y |  | 操作员 |
| market_type | bpchar(1) | N | √ | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| ifcheck | varchar(1) | Y |  | 是否设置检查:见tp_public_dict的120 |

---

## 666. dimple.tc_variety_tot　(18 字段)
> 表含义：品种统计表:结算后续处理产生.　|　估算行数：**292,055**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| trade_type | varchar(2) | N | √ | 交易类型:见tp_public_dict的001 |
| today_match_qty | numeric(12,0) | Y |  | 当日成交量 |
| today_match_amt | numeric(24,6) | Y |  | 当日成交额 |
| month_match_qty | numeric(12,0) | Y |  | 月累计成交量 |
| month_match_amt | numeric(24,6) | Y |  | 月累计成交额 |
| year_match_qty | numeric(12,0) | Y |  | 年累计成交量 |
| year_match_amt | numeric(24,6) | Y |  | 年累计成交额 |
| today_fee | numeric(18,2) | Y |  | 当日手续费 |
| month_fee | numeric(18,2) | Y |  | 月手续费 |
| year_fee | numeric(18,2) | Y |  | 年手续费 |
| max_match_qty | numeric(12,0) | Y |  | 最大成交量 |
| max_match_qty_date | varchar(8) | Y |  | 最大成交量发生日期 |
| min_match_qty | numeric(12,0) | Y |  | 最小成交量 |
| min_match_qty_date | varchar(8) | Y |  | 最小成交量发生日期 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 667. dimple.tc_vclient_posi_clear　(15 字段)
> 表含义：询价持仓表　|　估算行数：**26,240**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(10) | N | √ | 客户号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| bus_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的331 |
| last_buy_qty | numeric(16,6) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(16,6) | Y |  | 上日卖持仓量 |
| buy_reg_qty | numeric(16,6) | Y |  | 当日新增买持仓量 |
| sell_reg_qty | numeric(16,6) | Y |  | 当日新增卖持仓量 |
| buy_due_qty | numeric(16,6) | Y |  | 当日到期买持仓量 |
| sell_due_qty | numeric(16,6) | Y |  | 当日到期卖持仓量 |
| buy_qty | numeric(16,6) | Y |  | 买持仓量 |
| sell_qty | numeric(16,6) | Y |  | 卖持仓量 |
| day_profit | numeric(24,6) | Y |  | 日盈亏 |
| float_profit | numeric(24,6) | Y |  | 合约盈亏 |

---

## 668. dimple.tc_vclient_posi_detail_clear　(21 字段)
> 表含义：客户询价持仓明细表
用于对询价的成交未交割记录进行持仓虚拟动作　|　估算行数：**32,703**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 结算日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| due_date | varchar(8) | Y |  | 到期日期 |
| bus_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的331 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253 |
| delivery_type | varchar(3) | Y |  | 交割类型 |
| match_no | varchar(30) | N | √ | 成交号 |
| seq_no | numeric(20,0) | N | √ | 流水号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(16,6) | Y |  | 数量 |
| day_profit | numeric(24,6) | Y |  | 日盈亏 |
| float_profit | numeric(24,6) | Y |  | 合约盈亏 |
| calc_price | numeric(20,8) | Y |  | 公允价 |
| last_calc_price | numeric(20,8) | Y |  | 上日公允价 |
| fn_flag | varchar(3) | Y |  | 远近端：见tp_public_dict的250 |
| convert_rate | numeric(20,8) | Y |  | 汇率 |

---

## 669. dimple.tc_vtrader_posi_clear　(17 字段)
> 表含义：虚拟交易员持仓表　|　估算行数：**100,121**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 结算日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(16) | N | √ | 交易员 |
| contract_id | varchar(20) | N | √ | 合约号 |
| bus_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的331 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| last_buy_qty | numeric(16,6) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(16,6) | Y |  | 上日卖持仓量 |
| buy_reg_qty | numeric(16,6) | Y |  | 当日新增买持仓量 |
| sell_reg_qty | numeric(16,6) | Y |  | 当日新增卖持仓量 |
| buy_due_qty | numeric(16,6) | Y |  | 当日到期买持仓量 |
| sell_due_qty | numeric(16,6) | Y |  | 当日到期卖持仓量 |
| buy_qty | numeric(16,6) | Y |  | 买持仓量 |
| sell_qty | numeric(16,6) | Y |  | 卖持仓量 |
| day_profit | numeric(24,6) | Y |  | 日盈亏 |
| float_profit | numeric(24,6) | Y |  | 合约盈亏 |

---

## 670. dimple.tc_vtrader_posi_detail_clear　(24 字段)
> 表含义：交易员询价持仓明细表
用于对询价的成交未交割记录进行持仓虚拟动作　|　估算行数：**32,907**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 结算日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| due_date | varchar(8) | Y |  | 到期日期 |
| bus_type | varchar(3) | N | √ | 业务类型：见tp_public_dict的331 |
| trade_type | varchar(3) | Y |  | 成交类型：见tp_public_dict的253 |
| delivery_type | varchar(3) | Y |  | 交割类型 |
| match_no | varchar(30) | N | √ | 成交号 |
| seq_no | numeric(20,0) | N | √ | 流水号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| bs_flag | varchar(3) | N | √ | 买卖标志 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(16,6) | Y |  | 数量 |
| day_profit | numeric(24,6) | Y |  | 日盈亏 |
| float_profit | numeric(24,6) | Y |  | 合约盈亏 |
| calc_price | numeric(20,8) | Y |  | 公允价 |
| last_calc_price | numeric(20,8) | Y |  | 上日公允价 |
| fn_flag | varchar(3) | Y |  | 远近端：见tp_public_dict的250 |
| convert_rate | numeric(20,8) | Y |  | 汇率 |
| calc_amt | numeric(24,6) | Y |  | 估值金额 |
| move_flag | varchar(3) | N | √ | 调转标志(0:非调转 1:调入 2:调出) |

---

## 671. dimple.tc_warehouse_info　(4 字段)
> 表含义：仓库信息　|　估算行数：**69**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| warehouse_id | varchar(4) | N | √ | 仓库代码 |
| ware_name | varchar(60) | Y |  | 仓库名称 |
| storage_state | varchar(3) | Y |  | 仓库状态:0-有效 |
| ware_ename | varchar(60) | Y |  | 仓库英文名称 |

---

## 672. dimple.tc_xml_name　(2 字段)
> 表含义：文件名表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| file_type | bpchar(1) | N | √ | 文件类型 |
| file_id | numeric(10,0) | N | √ | 文件序号 |

---

## 673. dimple.tc_zx_quantized_match　(6 字段)
> 表含义：中信银行：量化成交单　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| trader_no | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 674. dimple.tmp_clear_posi_detail_trader　(17 字段)
> 表含义：交易员结算持仓明细临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| match_batch_no | varchar(20) | N |  | 成交批次号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 675. dimple.tmp_cmb_account_future　(12 字段)
> 表含义：招商银行-期货账务临时表　|　估算行数：**392**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | Y |  | 成交日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| sh_flag | varchar(3) | Y |  | 投保标志:见tp_public_dict的004 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 676. dimple.tmp_data_sync_def　(9 字段)
> 表含义：TMP_DATA_SYNC_DEF　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| s_owner | varchar(20) | N |  | S_OWNER |
| s_tname | varchar(30) | N |  | S_TNAME |
| d_owner | varchar(20) | N |  | D_OWNER |
| d_tname | varchar(30) | N |  | D_TNAME |
| s_tdesc | varchar(255) | Y |  | S_TDESC |
| sync_type | bpchar(1) | N |  | SYNC_TYPE |
| sync_field | varchar(30) | Y |  | SYNC_FIELD |
| bdate | varchar(8) | Y |  | BDATE |
| edate | varchar(8) | Y |  | EDATE |

---

## 677. dimple.tmp_date_margin_rate　(17 字段)
> 表含义：日期梯度保证金率临时表，日终结算前计算保证金参数使用。因日期梯度保证金率表有品种，结算帐号的记录，此表记录将品种解析到合约的数据　|　估算行数：**1,545**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | Y |  | 交易所 |
| variety_id | varchar(4) | Y |  | 品种代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| contract_id | varchar(20) | Y |  | 合约代码:$表示所有合约 |
| margin_type | bpchar(1) | Y |  | 保证金类型:预留，用于确定保证金率是比率值还是固定值。参考常量表。－》见tp_public_dict的092。 |
| month | float8 | Y |  | 月份: -1普通月份 1 交割前一月 0 交割月份 |
| day | float8 | Y |  | 天:对于普通月份该值为-1，其他月份为交割日 |
| spec_buy_rate | numeric(10,6) | Y |  | 投机买率 |
| spec_sell_rate | numeric(10,6) | Y |  | 投机卖率 |
| hedge_buy_rate | numeric(10,6) | Y |  | 套保买率 |
| hedge_sell_rate | numeric(10,6) | Y |  | 套保卖率 |
| arbi_buy_rate | numeric(10,6) | N |  | 套利买率 |
| arbi_sell_rate | numeric(10,6) | N |  | 套利卖率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| recheck_date | varchar(8) | Y |  | 审核日期:对于品种合约保证金管理，该项即操作日期;对于特殊结算帐号保证金管理，该项即审核日期 |
| recheck_oper | varchar(30) | Y |  | 审核员:对于品种合约保证金管理，该项即操作员;对于特殊结算帐号保证金管理，该项即审核操作的操作员 |

---

## 678. dimple.tmp_delivery_fee　(7 字段)
> 表含义：临时交割手续费率表　|　估算行数：**124**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号:可为$ |
| variety_id | varchar(4) | N | √ | 品种代码 |
| delivery_fee | numeric(22,6) | N |  | 交割手续费率 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| exch_code | varchar(6) | N | √ | 交易所代码 |

---

## 679. dimple.tmp_etf_nomatch　(24 字段)
> 表含义：对账临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| exch_seq_no | varchar(20) | Y |  | 交易所ETF编号 |
| client_id | varchar(20) | Y |  | 投资人黄金账号 |
| member_id | varchar(8) | Y |  | 会员代码 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| qty_1 | numeric(20,6) | Y |  | 重量1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| qty_2 | numeric(20,6) | Y |  | 重量2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| qty_3 | numeric(20,6) | Y |  | 重量3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| qty_4 | numeric(20,6) | Y |  | 重量4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| qty_5 | numeric(20,6) | Y |  | 重量5 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| local_seq_no | varchar(20) | Y |  | 本地编号 |
| status | varchar(4) | Y |  | 状态 |
| trade_type | varchar(4) | N |  | 交易类型：见数据字典268 |
| compare_type | varchar(3) | Y |  | 对账类型：1 系统 2 交易所 |

---

## 680. dimple.tmp_fn_lend_remain_qty　(9 字段)
> 表含义：拆借剩余数量临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 系统流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量 |
| price | numeric(20,8) | Y |  | 成交价 |
| contract_id | varchar(20) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 681. dimple.tmp_ftr_fee　(16 字段)
> 表含义：期货手续费率临时表　|　估算行数：**60**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码:$表示所有合约 |
| client_id | varchar(16) | N | √ | 客户号:$表示所有客户 |
| member_id | varchar(8) | N | √ | 会员号:$表示所有会员 |
| open_fee | numeric(22,6) | N |  | 开仓结算手续费 |
| offset_fee | numeric(22,6) | N |  | 平仓结算手续费 |
| t_open_fee | numeric(22,6) | N |  | 开仓交易手续费 |
| t_offset_fee | numeric(22,6) | N |  | 平仓交易手续费 |
| short_open_fee | numeric(22,6) | N |  | 短线开仓手续费 |
| short_offset_fee | numeric(22,6) | N |  | 短线平仓手续费 |
| fee_type | bpchar(1) | N |  | 手续费类型:见tp_public_dict的092 |
| spot_fee | numeric(22,6) | Y |  | 现货手续费 |
| attr | varchar(3) | N | √ | 交易编码属性::$-代表全部,见tp_public_dict263 |
| app_type | varchar(3) | N | √ | 定价成交申报类型:0-默认,见tp_public_dict330 |

---

## 682. dimple.tmp_ftr_match_sum　(13 字段)
> 表含义：期货成交汇总临时表，会员级期货持仓结算使用;1-场上成交,D-递延交割成交,C-延期现金交割,O-期权行权产生期货持仓,S-期权业务引发的期货持仓自对冲平仓　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| eo_flag | bpchar(1) | N |  | 开平标志 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| sh_flag | bpchar(1) | N |  | 投保标志 |
| amt | numeric(24,6) | Y |  | 成交金额 |
| qty | numeric(12,0) | N |  | 成交量 |
| type | varchar(3) | Y |  | 类型:cn_ms_match,1-场上成交;cn_defer_delivery_match,D-递延交割成交;cn_cash_delivery_match,C-延期现金交割;cn_opt_exec_ftr_match,O-期权行权产生期货持仓;cn_opt_ftr_self,S-期权业务引发的期货持仓自对冲平仓 |
| trade_fee | numeric(18,2) | Y |  | 交易手续费 |
| account_type | varchar(4) | Y |  | 结算帐号类型 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |

---

## 683. dimple.tmp_ftr_match_sum_trader　(15 字段)
> 表含义：交易员成交汇总明细临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| eo_flag | varchar(3) | N |  | 开平标志 |
| bs_flag | varchar(3) | N |  | 买卖标志 |
| sh_flag | varchar(3) | N |  | 投保标志 |
| amt | numeric(24,6) | Y |  | 成交金额 |
| qty | numeric(12,0) | N |  | 成交量 |
| type | varchar(3) | Y |  | 类型:CN_MS_MATCH,1,场上成交;CN_MS_DELIPOSI,3,交割持仓;CN_MS_SPECTOHEDGE,8,投机转套保;CN_MS_AM_EXECOPEN,9,期权执行的期货建仓; |
| trade_fee | numeric(18,2) | Y |  | 交易手续费 |
| account_type | varchar(4) | Y |  | 账户类型 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 684. dimple.tmp_ftr_purpose_posi_clear　(33 字段)
> 表含义：交易目的期货结算持仓临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_open_amt | numeric(18,2) | Y |  | 今日买开仓额 |
| sell_open_amt | numeric(18,2) | Y |  | 今日卖开仓额 |
| buy_offset_amt | numeric(18,2) | Y |  | 今日买平仓额 |
| sell_offset_amt | numeric(18,2) | Y |  | 今日卖平仓额 |
| buy_amt | numeric(18,2) | Y |  | 买持仓额 |
| sell_amt | numeric(18,2) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| buy_float_profitloss | numeric(18,2) | Y |  | 买持仓盈亏 |
| sell_float_profitloss | numeric(18,2) | Y |  | 卖持仓盈亏 |
| buy_margin | numeric(18,2) | Y |  | 买保证金 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金 |
| buy_margin_exch | numeric(18,2) | Y |  | 交易所买保证金 |
| sell_margin_exch | numeric(18,2) | Y |  | 交易所卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| float_profitloss_tot | numeric(18,2) | Y |  | 累积持仓盈亏 |
| buy_offset_profitloss | numeric(18,2) | Y |  | 买平仓盈亏 |
| sell_offset_profitloss | numeric(18,2) | Y |  | 卖平仓盈亏 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 685. dimple.tmp_ftr_trader_posi_clear　(38 字段)
> 表含义：交易员期货结算持仓临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_open_amt | numeric(18,2) | Y |  | 今日买开仓额 |
| sell_open_amt | numeric(18,2) | Y |  | 今日卖开仓额 |
| buy_offset_amt | numeric(18,2) | Y |  | 今日买平仓额 |
| sell_offset_amt | numeric(18,2) | Y |  | 今日卖平仓额 |
| buy_amt | numeric(18,2) | Y |  | 买持仓额 |
| sell_amt | numeric(18,2) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| open_fee | numeric(18,2) | Y |  | 开仓结算手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| t_open_fee | numeric(18,2) | Y |  | 开仓交易手续费 |
| t_offset_fee | numeric(18,2) | Y |  | 平仓交易手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费 |
| buy_margin | numeric(18,2) | Y |  | 买保证金 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金 |
| buy_margin_exch | numeric(18,2) | Y |  | 交易所买保证金 |
| sell_margin_exch | numeric(18,2) | Y |  | 交易所卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| float_profitloss_tot | numeric(18,2) | Y |  | 累积持仓盈亏 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |
| buy_offset_profitloss | numeric(18,2) | Y |  | 买平仓盈亏 |
| sell_offset_profitloss | numeric(18,2) | Y |  | 卖平仓盈亏 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 686. dimple.tmp_hm_lease_remain_qty　(9 字段)
> 表含义：拆借剩余数量临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 系统流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量 |
| price | numeric(20,8) | Y |  | 成交价 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 687. dimple.tmp_hm_lend_remain_qty　(9 字段)
> 表含义：拆借剩余数量临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 系统流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| remain_qty | numeric(16,6) | Y |  | 剩余数量 |
| price | numeric(20,8) | Y |  | 成交价 |
| variety_id | varchar(3) | Y |  | 交易品种 |
| lend_flag | varchar(3) | Y |  | 拆借方向 |
| trade_party | varchar(40) | Y |  | 交易对手 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 688. dimple.tmp_hz_account_future　(12 字段)
> 表含义：杭州银行-期货账务临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | Y |  | 成交日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| sh_flag | varchar(3) | Y |  | 投机套保标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 689. dimple.tmp_import_file　(123 字段)
> 表含义：（无注释）　|　估算行数：**215,492**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  |  |
| file_type | varchar(3) | Y |  |  |
| member_id | varchar(6) | Y |  |  |
| data_1 | varchar(200) | Y |  |  |
| data_2 | varchar(200) | Y |  |  |
| data_3 | varchar(200) | Y |  |  |
| data_4 | varchar(200) | Y |  |  |
| data_5 | varchar(200) | Y |  |  |
| data_6 | varchar(200) | Y |  |  |
| data_7 | varchar(200) | Y |  |  |
| data_8 | varchar(200) | Y |  |  |
| data_9 | varchar(200) | Y |  |  |
| data_10 | varchar(200) | Y |  |  |
| data_11 | varchar(200) | Y |  |  |
| data_12 | varchar(200) | Y |  |  |
| data_13 | varchar(200) | Y |  |  |
| data_14 | varchar(200) | Y |  |  |
| data_15 | varchar(200) | Y |  |  |
| data_16 | varchar(200) | Y |  |  |
| data_17 | varchar(200) | Y |  |  |
| data_18 | varchar(200) | Y |  |  |
| data_19 | varchar(200) | Y |  |  |
| data_20 | varchar(200) | Y |  |  |
| data_21 | varchar(200) | Y |  |  |
| data_22 | varchar(200) | Y |  |  |
| data_23 | varchar(200) | Y |  |  |
| data_24 | varchar(200) | Y |  |  |
| data_25 | varchar(200) | Y |  |  |
| data_26 | varchar(200) | Y |  |  |
| data_27 | varchar(200) | Y |  |  |
| data_28 | varchar(200) | Y |  |  |
| data_29 | varchar(200) | Y |  |  |
| data_30 | varchar(200) | Y |  |  |
| data_31 | varchar(200) | Y |  |  |
| data_32 | varchar(200) | Y |  |  |
| data_33 | varchar(200) | Y |  |  |
| data_34 | varchar(200) | Y |  |  |
| data_35 | varchar(200) | Y |  |  |
| data_36 | varchar(200) | Y |  |  |
| data_37 | varchar(200) | Y |  |  |
| data_38 | varchar(200) | Y |  |  |
| data_39 | varchar(200) | Y |  |  |
| data_40 | varchar(200) | Y |  |  |
| data_41 | varchar(200) | Y |  |  |
| data_42 | varchar(200) | Y |  |  |
| data_43 | varchar(200) | Y |  |  |
| data_44 | varchar(200) | Y |  |  |
| data_45 | varchar(200) | Y |  |  |
| data_46 | varchar(200) | Y |  |  |
| data_47 | varchar(200) | Y |  |  |
| data_48 | varchar(200) | Y |  |  |
| data_49 | varchar(200) | Y |  |  |
| data_50 | varchar(200) | Y |  |  |
| data_51 | varchar(200) | Y |  |  |
| data_52 | varchar(200) | Y |  |  |
| data_53 | varchar(200) | Y |  |  |
| data_54 | varchar(200) | Y |  |  |
| data_55 | varchar(200) | Y |  |  |
| data_56 | varchar(200) | Y |  |  |
| data_57 | varchar(200) | Y |  |  |
| data_58 | varchar(200) | Y |  |  |
| data_59 | varchar(200) | Y |  |  |
| data_60 | varchar(200) | Y |  |  |
| data_61 | varchar(200) | Y |  |  |
| data_62 | varchar(200) | Y |  |  |
| data_63 | varchar(200) | Y |  |  |
| data_64 | varchar(200) | Y |  |  |
| data_65 | varchar(200) | Y |  |  |
| data_66 | varchar(200) | Y |  |  |
| data_67 | varchar(200) | Y |  |  |
| data_68 | varchar(200) | Y |  |  |
| data_69 | varchar(200) | Y |  |  |
| data_70 | varchar(200) | Y |  |  |
| data_71 | varchar(200) | Y |  |  |
| data_72 | varchar(200) | Y |  |  |
| data_73 | varchar(200) | Y |  |  |
| data_74 | varchar(200) | Y |  |  |
| data_75 | varchar(200) | Y |  |  |
| data_76 | varchar(220) | Y |  |  |
| data_77 | varchar(200) | Y |  |  |
| data_78 | varchar(200) | Y |  |  |
| data_79 | varchar(200) | Y |  |  |
| data_80 | varchar(200) | Y |  |  |
| data_81 | varchar(200) | Y |  |  |
| data_82 | varchar(200) | Y |  |  |
| data_83 | varchar(200) | Y |  |  |
| data_84 | varchar(200) | Y |  |  |
| data_85 | varchar(200) | Y |  |  |
| data_86 | varchar(200) | Y |  |  |
| data_87 | varchar(200) | Y |  |  |
| data_88 | varchar(200) | Y |  |  |
| data_89 | varchar(200) | Y |  |  |
| data_90 | varchar(200) | Y |  |  |
| data_91 | varchar(200) | Y |  |  |
| data_92 | varchar(200) | Y |  |  |
| data_93 | varchar(200) | Y |  |  |
| data_94 | varchar(200) | Y |  |  |
| data_95 | varchar(200) | Y |  |  |
| data_96 | varchar(200) | Y |  |  |
| data_97 | varchar(200) | Y |  |  |
| data_98 | varchar(200) | Y |  |  |
| data_99 | varchar(200) | Y |  |  |
| data_100 | varchar(200) | Y |  |  |
| data_101 | varchar(200) | Y |  |  |
| data_102 | varchar(200) | Y |  |  |
| data_103 | varchar(200) | Y |  |  |
| data_104 | varchar(200) | Y |  |  |
| data_105 | varchar(200) | Y |  |  |
| data_106 | varchar(200) | Y |  |  |
| data_107 | varchar(200) | Y |  |  |
| data_108 | varchar(200) | Y |  |  |
| data_109 | varchar(200) | Y |  |  |
| data_110 | varchar(200) | Y |  |  |
| data_111 | varchar(200) | Y |  |  |
| data_112 | varchar(200) | Y |  |  |
| data_113 | varchar(200) | Y |  |  |
| data_114 | varchar(200) | Y |  |  |
| data_115 | varchar(200) | Y |  |  |
| data_116 | varchar(200) | Y |  |  |
| data_117 | varchar(200) | Y |  |  |
| data_118 | varchar(200) | Y |  |  |
| data_119 | varchar(200) | Y |  |  |
| data_120 | varchar(200) | Y |  |  |

---

## 690. dimple.tmp_inquire_nomatch　(16 字段)
> 表含义：境内询价:对账临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| match_no | varchar(20) | Y |  | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| contract_id | varchar(20) | Y |  | 合约 |
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| fn_flag | varchar(3) | N |  | 远近端：见tp_public_dict的250 |
| due_date | varchar(8) | Y |  | 到期交割日 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| qty | numeric(24,6) | Y |  | 交易量 |
| price | numeric(20,8) | Y |  | 成交价格 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| related_match_no | varchar(20) | Y |  | 相关成交单号:用来记录行权的期权成交单号，或为未来其他业务备用 |
| reference_price | numeric(20,8) | Y |  | 参考价格 |
| reference_adjust | numeric(20,8) | Y |  | 参考价格调整项 |
| compare_type | varchar(3) | Y |  | 对账类型：1 系统 2 交易所 |

---

## 691. dimple.tmp_lend_nomatch　(11 字段)
> 表含义：境内拆借:对账临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| tradedate | varchar(8) | N |  | 交易日 |
| member_id | varchar(8) | N |  | 会员号 |
| agreement_sn | varchar(30) | N |  | 金交所租借登记号 |
| lend_flag | varchar(3) | Y |  | 拆借方向：见tp_public_dict的221.拆入和拆出 |
| variety_id | varchar(3) | Y |  | 交易品种(实际存放合约号信息) |
| trade_qty | numeric(16,6) | Y |  | 交易重量 |
| base_amt | numeric(24,6) | Y |  | 名义本金 |
| due_date | varchar(8) | Y |  | 到期日 |
| isexch_clearint | varchar(3) | Y |  | 是否交易所清算利息 |
| compare_type | varchar(3) | Y |  | 对账类型：1 系统 2 交易所 |
| reg_date | varchar(8) | Y |  | 起息日 |

---

## 692. dimple.tmp_lend_remain_qty　(3 字段)
> 表含义：拆借剩余数量临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N |  | 系统流水号 |
| bill_no | varchar(30) | N |  | 合同号 |
| remain_qty | numeric(12,0) | Y |  | 剩余数量 |

---

## 693. dimple.tmp_load_file　(21 字段)
> 表含义：金交所临时交割成交文件　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| qty | numeric(12,0) | Y |  | 数量 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| localorderno | varchar(16) | Y |  | 本地委托号 |
| member_id | varchar(8) | Y |  | 会员号 |
| clienttype | varchar(10) | Y |  | 客户类型 |
| match_time | varchar(10) | Y |  | 成交时间 |
| order_no | varchar(10) | Y |  | 委托号 |
| price | numeric(20,8) | Y |  | 成交价 |
| match_no | varchar(20) | Y |  | 成交号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| eo_flag | varchar(2) | Y |  | 开平标志 |
| bs_flag | varchar(2) | Y |  | 买卖标志 |
| client_id | varchar(16) | Y |  | 客户号 |
| sh_flag | varchar(2) | Y |  | 投保标志 |
| exch_code | varchar(2) | Y |  | 交易所号 |
| middleflag | varchar(2) | Y |  | 是否中立仓 |
| file_type | varchar(2) | Y |  | 文件类型 |
| match_type | varchar(2) | Y |  | 现货类型 |
| operator_id | varchar(20) | Y |  | 操作员 |
| checker_id | varchar(20) | Y |  | 复核员 |
| if_checked | varchar(3) | Y |  | 复核标志 |

---

## 694. dimple.tmp_load_lend　(27 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | Y |  | 录入日期 |
| lendregno | varchar(16) | N |  | 询价拆借登记单编号 |
| regno | varchar(16) | N |  | 主系统拆借登记单编号 |
| memberid1 | varchar(8) | Y |  | 本方会员代码 |
| clientid1 | varchar(12) | N |  | 本方客户代码 |
| memberid2 | varchar(8) | Y |  | 对手方会员代码 |
| mabbr2 | varchar(20) | N |  | 对手方会员简称 |
| varietyid | varchar(3) | Y |  | 拆借品种代码 |
| weight | numeric(16,6) | Y |  | 拆借标重 |
| mybj | numeric(18,2) | Y |  | 名义本金 |
| valuedate | varchar(8) | Y |  | 拆借起息日 |
| interestref | numeric(8,3) | Y |  | 拆借计息基准 |
| interestrefprice | numeric(8,3) | Y |  | 拆借计息基准价 |
| lendperiod | varchar(16) | Y |  | 拆借期限 |
| duedate | varchar(8) | Y |  | 拆借到期日 |
| yearrate | numeric(10,6) | Y |  | 拆借年利率 |
| transferkind | varchar(1) | Y |  | 过户类型 |
| flag | varchar(4) | Y |  | 本方拆借方向 |
| regfeerate | numeric(10,6) | Y |  | 手续费率 |
| regratetype | varchar(1) | Y |  | 手续费率类型 |
| regfee | numeric(18,2) | Y |  | 手续费 |
| matchdate | varchar(8) | Y |  | 成交日期 |
| matchtime | varchar(8) | Y |  | 成交时间 |
| matchregtype | varchar(1) | Y |  | 拆借类型 |
| prelendregno | varchar(16) | Y |  | 前接登记单编号 |
| impdate | varchar(8) | Y |  | 导入日期 |
| imptime | varchar(8) | Y |  | 导入时间 |

---

## 695. dimple.tmp_match_progress　(6 字段)
> 表含义：对账过程日志记录表　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| jour_no | float8 | N |  | 进度流水号 |
| status | varchar(2) | Y |  | 当前能否生成文件 |
| rec_time | varchar(8) | Y |  | 记录的时间 |
| percent | numeric(10,6) | Y |  | 对账的进度 |
| title | varchar(20) | Y |  | 对账信息，大标题 |
| content | varchar(254) | Y |  | 对账信息，小标题 |

---

## 696. dimple.tmp_matchconfirm　(13 字段)
> 表含义：农行交易确认单临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| member_abbr | varchar(20) | Y |  | 会员简称 |
| contract_id | varchar(20) | N | √ | 合约号 |
| bs_flag | varchar(3) | N | √ | 多空方向 |
| trans_type | varchar(30) | N | √ | 交易类型 |
| total_qty | numeric(12,0) | Y |  | 交易数量 |
| ave_price | numeric(12,0) | Y |  | 交易均价 |
| last_total_storage | varchar(20) | Y |  | 上日库存(持仓) |
| total_storage | varchar(20) | Y |  | 当日库存 |
| cost | varchar(20) | Y |  | 当日成本 |
| last_total_exposure | varchar(20) | Y |  | 上日总敞口 |
| total_exposure | varchar(20) | Y |  | 当日总敞口 |
| clear_price | varchar(20) | Y |  | 当日收盘价 |

---

## 697. dimple.tmp_nb_account_future　(12 字段)
> 表含义：宁波银行-期货账务临时表　|　估算行数：**392**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | Y |  | 成交日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| sh_flag | varchar(3) | Y |  | 投机套保标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 698. dimple.tmp_not_match_offset　(14 字段)
> 表含义：当日非场上成交平仓临时表，日终结算时处理非场上成交的平仓记录使用。记录交割持仓对冲，强制减仓，期转现，滚动交割，一次性交割。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(20) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(9,0) | N |  | 成交量 |
| margin | numeric(18,2) | N |  | 保证金 |
| type | varchar(3) | N |  | 类型:见tp_public_code的179 |
| user_id | varchar(30) | Y |  |  |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 699. dimple.tmp_not_match_offset_purpose　(14 字段)
> 表含义：当日非场上成交平仓临时表，日终结算时处理非场上成交的平仓记录使用。记录交割持仓对冲，强制减仓，期转现，滚动交割，一次性交割。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(20) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(9,0) | N |  | 成交量 |
| margin | numeric(18,2) | N |  | 保证金 |
| type | varchar(3) | N |  | 类型:见tp_public_code的179 |
| user_id | varchar(30) | Y |  |  |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 700. dimple.tmp_offset_profitloss_trader　(16 字段)
> 表含义：交易员平仓盈亏临时表　|　估算行数：**18**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| offset_type | varchar(2) | Y |  | 平仓类型:见tp_public_dict的179 |
| match_no | varchar(20) | Y |  | 成交号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 701. dimple.tmp_opt_clear_posi_detail　(13 字段)
> 表含义：期权结算持仓明细临时表，日终结算时使用，此表功能同期权持仓明细表，但仅有当天数据　|　估算行数：**5**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(30) | N |  | 合约号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| qty | numeric(12,0) | N |  | 数量 |
| price | numeric(20,8) | N |  | 成交价 |

---

## 702. dimple.tmp_opt_client_posi　(23 字段)
> 表含义：期权持仓临时表，日终结算时使用，此表功能同客户期权结算持仓表，但仅有当天数据　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额 |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| premium_out | numeric(19,2) | Y |  | 权利金支出 |
| premium_in | numeric(19,2) | Y |  | 权利金收入 |
| sell_margin | numeric(19,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 703. dimple.tmp_opt_offset_profitloss　(13 字段)
> 表含义：期权平仓盈亏临时表，日终结算时使用，此表功能同期权平仓盈亏表，但仅有当天数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(30) | N |  | 合约号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| match_no | varchar(20) | Y |  | 成交号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 704. dimple.tmp_opt_offset_purpose　(13 字段)
> 表含义：交易目的期权平仓临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | Y |  | 交易员号 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| match_no | varchar(20) | Y |  | 成交号 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 705. dimple.tmp_opt_offset_trader　(13 字段)
> 表含义：交易员期权平仓临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| match_no | varchar(20) | Y |  | 成交号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 706. dimple.tmp_opt_posi_clear_purpose　(24 字段)
> 表含义：交易目的期权结算持仓临时表:日终结算时计算，也是次日持仓初始数据的来源。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量＋非持仓变动变动引起的量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| premium_out | numeric(19,2) | Y |  | 权利金支出 |
| premium_in | numeric(19,2) | Y |  | 权利金收入 |
| sell_margin | numeric(19,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 707. dimple.tmp_opt_posi_clear_trader　(25 字段)
> 表含义：交易员期权结算持仓表:日终结算时计算，也是次日持仓初始数据的来源。　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| contract_id | varchar(30) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量:=上日买持仓量+今日买开仓量-今日卖平仓量＋非持仓变动变动引起的量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量:算法与买持仓量类似。 |
| buy_open_amt | numeric(24,6) | Y |  | 今日买开仓额:=SUM(买开仓价×买开仓量×单位) |
| sell_open_amt | numeric(24,6) | Y |  | 今日卖开仓额:与上类似 |
| buy_offset_amt | numeric(24,6) | Y |  | 今日买平仓额:与上类似 |
| sell_offset_amt | numeric(24,6) | Y |  | 今日卖平仓额:与上类似 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额:=根据持仓明细中的买开仓价和买开仓量计算，初始化时需要将此数据同步到交易持仓表 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额:与上类似 |
| premium_out | numeric(19,2) | Y |  | 权利金支出 |
| premium_in | numeric(19,2) | Y |  | 权利金收入 |
| sell_margin | numeric(19,2) | Y |  | 卖保证金 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 708. dimple.tmp_opt_posi_detail_notrade　(14 字段)
> 表含义：此表为处理交易员和交易目的级别的非持仓变动明细临时表　|　估算行数：**5**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | Y |  | 序号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(30) | N |  | 合约号 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 709. dimple.tmp_opt_posi_detail_purpose　(12 字段)
> 表含义：交易目的期权结算持仓明细临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| contract_id | varchar(30) | N |  | 合约号 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 710. dimple.tmp_opt_posi_detail_trader　(13 字段)
> 表含义：交易员期权结算持仓明细临时表　|　估算行数：**5**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| contract_id | varchar(30) | N |  | 合约号 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 711. dimple.tmp_pc_clear_offset_detail　(15 字段)
> 表含义：当日结算平仓记录明细临时表[会员级+交易员级+交易目的级]　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| trader_no | varchar(16) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| match_no | varchar(20) | N |  | 成交单号 |
| bs_flag | varchar(1) | N |  | 原买卖方向 |
| bs_flag_new | varchar(1) | N |  | 新买卖方向 |
| sh_flag | varchar(1) | N |  | 投保标志 |
| offset_type | varchar(1) | Y |  | 原平仓标志 |
| offset_type_new | varchar(1) | Y |  | 新平仓标志 |
| qty | numeric(12,0) | N |  | 数量(手) |
| price | numeric(20,8) | N |  | 成交价 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |

---

## 712. dimple.tmp_pc_clear_posi_detail　(16 字段)
> 表含义：结算持仓明细临时表，日终结算时使用，此表功能同结算持仓明细表，但仅有当天数据　|　估算行数：**120,079**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| match_batch_no | varchar(20) | N |  | 成交批次号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| trader_no | varchar(16) | Y |  | 席位号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 713. dimple.tmp_pc_clear_posi_detail2　(17 字段)
> 表含义：结算持仓明细临时表，日终结算时使用，此表功能同结算持仓明细表，但仅有当天数据　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| match_batch_no | varchar(20) | N |  | 成交批次号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| trader_no | varchar(16) | Y |  | 席位号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 714. dimple.tmp_pc_exch_margin_rate　(16 字段)
> 表含义：交易所临近交割月保证金表,存储临近交割月保证金的参数　|　估算行数：**96**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | numeric(10,0) | N | √ | 序号 |
| exch_code | varchar(2) | N | √ | 交易所 |
| variety_id | varchar(4) | N | √ | 品种代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| month | float8 | N | √ | 月份 |
| day | float8 | N | √ | 天 |
| spec_buy_rate | numeric(10,6) | Y |  | 投机买率 |
| spec_sell_rate | numeric(10,6) | Y |  | 投机卖率 |
| hedge_buy_rate | numeric(10,6) | Y |  | 套保买率 |
| hedge_sell_rate | numeric(10,6) | Y |  | 套保卖率 |
| arbi_buy_rate | numeric(10,6) | Y |  | 套利买率 |
| arbi_sell_rate | numeric(10,6) | Y |  | 套利卖率 |
| margin_type | bpchar(1) | Y |  | 保证金类型 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | N | √ | 操作员 |

---

## 715. dimple.tmp_pc_fee　(21 字段)
> 表含义：当日手续费临时表，日终结算时计算交易手续费使用。记录期货和期权的交易手续费。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | Y |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| ftr_opt_flag | varchar(3) | Y |  | 交易类型:见tp_public_code的060 |
| eo_flag | bpchar(1) | Y |  | 开平标志 |
| sh_flag | bpchar(1) | Y |  | 投保标志 |
| t_trade_fee | numeric(22,6) | Y |  | 交易手续费率 |
| trade_fee | numeric(22,6) | Y |  | 结算手续费率 |
| exch_t_trade_fee | numeric(22,6) | Y |  | 交易所交易手续费率 |
| exch_trade_fee | numeric(22,6) | Y |  | 交易所结算手续费率 |
| match_qty | numeric(12,0) | Y |  | 成交量 |
| t_fee | numeric(18,2) | Y |  | 交易手续费 |
| fee | numeric(18,2) | Y |  | 结算手续费 |
| exch_t_fee | numeric(18,2) | Y |  | 交易所交易手续费 |
| exch_fee | numeric(18,2) | Y |  | 交易所结算手续费 |
| fee_type | bpchar(1) | Y |  | 手续费类型:交易手续费,0 |
| match_amt | numeric(18,2) | Y |  | 成交金额 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 716. dimple.tmp_pc_ftr_client_posi　(34 字段)
> 表含义：期货持仓临时表，日终结算时使用，此表功能同客户期货结算持仓表，但仅有当天数据　|　估算行数：**27**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| buy_open_amt | numeric(18,2) | Y |  | 今日买开仓额 |
| sell_open_amt | numeric(18,2) | Y |  | 今日卖开仓额 |
| buy_offset_amt | numeric(18,2) | Y |  | 今日买平仓额 |
| sell_offset_amt | numeric(18,2) | Y |  | 今日卖平仓额 |
| buy_amt | numeric(18,2) | Y |  | 买持仓额 |
| sell_amt | numeric(18,2) | Y |  | 卖持仓额 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| float_profitloss | numeric(18,2) | Y |  | 持仓盈亏 |
| open_fee | numeric(18,2) | Y |  | 开仓结算手续费 |
| offset_fee | numeric(18,2) | Y |  | 平仓结算手续费 |
| t_open_fee | numeric(18,2) | Y |  | 开仓交易手续费 |
| t_offset_fee | numeric(18,2) | Y |  | 平仓交易手续费 |
| ret_fee | numeric(18,2) | Y |  | 返还手续费 |
| exch_open_fee | numeric(18,2) | Y |  | 交易所开仓结算手续费 |
| exch_offset_fee | numeric(18,2) | Y |  | 交易所平仓结算手续费 |
| exch_t_open_fee | numeric(18,2) | Y |  | 交易所开仓交易手续费 |
| exch_t_offset_fee | numeric(18,2) | Y |  | 交易所平仓交易手续费 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| exch_ret_fee | numeric(18,2) | Y |  | 交易所返还手续费 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |

---

## 717. dimple.tmp_pc_not_perf_client_posi　(17 字段)
> 表含义：客户非优惠组合持仓临时表，日终结算时使用，此表功能同客户非优惠持仓表，但仅有当天数据　|　估算行数：**27**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号:各腿的合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见t_public_code的004 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| impawn_qty | numeric(12,0) | Y |  | 冲抵仓单数 |
| exch_buy_margin | numeric(18,2) | Y |  | 交易所买保证金 |
| exch_sell_margin | numeric(18,2) | Y |  | 交易所卖保证金 |
| buy_margin | numeric(18,2) | Y |  | 买保证金：考虑大边 |
| sell_margin | numeric(18,2) | Y |  | 卖保证金：考虑大边 |
| ftr_clear_price | numeric(18,2) | Y |  | 期货结算价 |
| opt_clear_price | numeric(18,2) | Y |  | 期权结算价 |
| group_no | numeric(10,0) | Y |  | 组合代码 |
| largeside_flag | bpchar(1) | Y |  | 大边方向:见tp_public_dict的002 |
| discount_amount | numeric(18,2) | Y |  | 保证金优惠金额 |

---

## 718. dimple.tmp_pc_offset_profitloss　(16 字段)
> 表含义：期货平仓盈亏临时表，日终结算时使用，此表功能同期货平仓盈亏表，但仅有当天数据　|　估算行数：**9**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| offset_type | varchar(2) | Y |  | 平仓类型:见tp_public_dict的179 |
| match_no | varchar(20) | Y |  | 成交号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 719. dimple.tmp_pc_trader_spot_clear　(11 字段)
> 表含义：交易员现货合约结算临时表　|　估算行数：**6**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N |  | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| buy_qty | numeric(12,0) | Y |  | 当日买入 |
| sell_qty | numeric(12,0) | Y |  | 当日买出 |
| trade_fee | numeric(18,2) | Y |  | 手续费 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 720. dimple.tmp_pi_date　(4 字段)
> 表含义：日期临时表，用于临时存储交易日节假日信息　|　估算行数：**199**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 日期 |
| note | varchar(254) | Y |  | 备注 |
| type | bpchar(1) | Y |  | 日期类型 |
| operator_id | varchar(30) | Y |  | 操作员 |

---

## 721. dimple.tmp_pi_period_month　(2 字段)
> 表含义：交易期间月份临时表，用于临时存储特定交易期间的所有月份信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| month | varchar(8) | Y |  | 月份 |
| operator_id | varchar(30) | Y |  | 操作员 |

---

## 722. dimple.tmp_pingan_account　(32 字段)
> 表含义：平安账务表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| group_no | varchar(30) | Y |  | 组号 |
| trade_logno | varchar(30) | Y |  | 交易流水号 |
| currency | varchar(10) | Y |  | 币种 |
| org1 | varchar(20) | Y |  | 借方机构代码1 |
| account1 | varchar(50) | Y |  | 借方账号1 |
| subject1 | varchar(20) | Y |  | 借方科目1 |
| amt1 | numeric(24,6) | Y |  | 借方发生额1 |
| org2 | varchar(20) | Y |  | 借方机构代码2 |
| account2 | varchar(50) | Y |  | 借方账号2 |
| subject2 | varchar(20) | Y |  | 借方科目2 |
| amt2 | numeric(24,6) | Y |  | 借方发生额2 |
| org3 | varchar(20) | Y |  | 贷方机构代码1 |
| account3 | varchar(50) | Y |  | 贷方账号1 |
| subject3 | varchar(20) | Y |  | 贷方科目1 |
| amt3 | numeric(24,6) | Y |  | 贷方发生额1 |
| org4 | varchar(20) | Y |  | 贷方机构代码2 |
| account4 | varchar(50) | Y |  | 贷方账号2 |
| subject4 | varchar(20) | Y |  | 贷方科目2 |
| amt4 | numeric(24,6) | Y |  | 贷方发生额2 |
| remark | varchar(255) | Y |  | 备注 |
| isrecal | varchar(2) | Y |  | 是否为日终估值账务：0否；1是 |
| accounting_no | varchar(9) | Y |  | ICS产生的传票号 |
| account_date | varchar(9) | Y |  | 会计日期 |
| trans_status | varchar(2) | Y |  | 发送状态：0未发送；1 成功；2失败 |
| trans_result | varchar(20) | Y |  | 发送返回代码 |
| trans_msg | varchar(100) | Y |  | 发送返回信息 |
| check_status | varchar(2) | Y |  | 对账状态：0未对账；1已对账 |
| check_result | varchar(20) | Y |  | 对账返回代码 |
| check_msg | varchar(100) | Y |  | 对账返回信息 |
| member_id | varchar(8) | N |  | 会员号:$表示所有会员 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 723. dimple.tmp_pingan_account_defer　(11 字段)
> 表含义：平安银行-递延账务临时表　|　估算行数：**392**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | Y |  | 成交日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| exch_code | varchar(2) | Y |  |  |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 724. dimple.tmp_pingan_account_future　(12 字段)
> 表含义：平安银行-期货账务临时表　|　估算行数：**392**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_date | varchar(8) | Y |  | 成交日期 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(3) | Y |  | 买卖标志 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(30) | Y |  | 交易员 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量 |
| sh_flag | varchar(3) | Y |  | 投机套保标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 725. dimple.tmp_profitloss_clear　(8 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员 |
| variety_id | varchar(4) | N |  | 品种 |
| market_type | bpchar(1) | N |  | 市场 |
| day_profitloss | numeric(24,6) | Y |  | 日盈亏 |
| month_profitloss | numeric(24,6) | Y |  | 月盈亏 |
| year_profitloss | numeric(24,6) | Y |  | 年盈亏 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 726. dimple.tmp_purpose_clear_posi_detail　(16 字段)
> 表含义：交易目的结算持仓明细临时表，日终结算时使用，此表功能同结算持仓明细表，但仅有当天数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| match_date | varchar(8) | N |  | 成交日期 |
| match_no | varchar(20) | N |  | 成交号 |
| match_batch_no | varchar(20) | N |  | 成交批次号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 727. dimple.tmp_purpose_offset_profitloss　(16 字段)
> 表含义：期货平仓盈亏临时表，日终结算时使用，此表功能同期货平仓盈亏表，但仅有当天数据　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| last_clear_price | numeric(20,8) | N |  | 昨结算价 |
| open_price | numeric(20,8) | N |  | 开仓价 |
| offset_price | numeric(20,8) | N |  | 平仓价 |
| buy_offset_qty | numeric(12,0) | Y |  | 买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 卖平仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| offset_type | varchar(2) | Y |  | 平仓类型:见tp_public_dict的179 |
| match_no | varchar(20) | Y |  | 成交号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| purpose_code | varchar(3) | N |  | 交易目的 |

---

## 728. dimple.tmp_rule_para　(7 字段)
> 表含义：（无注释）　|　估算行数：**169**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N |  |  |
| variety_id | varchar(4) | N |  |  |
| contract_id | varchar(20) | N |  |  |
| alarm_type | bpchar(1) | N |  |  |
| cancel_times | numeric(10,0) | Y |  |  |
| alarm_times | numeric(10,0) | Y |  |  |
| alarm_qty_times | numeric(10,0) | Y |  |  |

---

## 729. dimple.tmp_sge_home_inquire_match　(49 字段)
> 表含义：交易所询价成交表：掉期二合一　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_type | varchar(3) | N |  | 业务类型：见tp_public_dict的253 |
| source_id | varchar(3) | Y |  | 来源：见tp_public_dict的249 |
| match_no | varchar(20) | Y |  | 成交单号 |
| cfets_match_no | varchar(30) | Y |  | 外汇成交单编号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| contract_id | varchar(20) | Y |  | 合约 |
| trade_party | varchar(40) | Y |  | 交易对手方 |
| delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的051 |
| bs_flag | varchar(3) | N |  | 买卖标志:见tp_public_dict的002 |
| currency_buy_j | varchar(8) | Y |  | 买入币种_近端 |
| num_buy_j | numeric(24,6) | Y |  | 买入量_近端 |
| currency_sell_j | varchar(8) | Y |  | 卖出币种_近端 |
| num_sell_j | numeric(24,6) | Y |  | 卖出量_近端 |
| price_j | numeric(20,8) | Y |  | 成交价格_近端 |
| due_date_j | varchar(8) | Y |  | 到期交割日_近端 |
| trade_type_j | varchar(3) | Y |  | 成交类型_近端：见tp_public_dict的253只包含即期和远期 |
| reference_type_j | varchar(3) | Y |  | 参考价类型_近端：见tp_public_dict的288 |
| reference_date_j | varchar(8) | Y |  | 参考价日期_近端 |
| reference_price_j | numeric(20,8) | Y |  | 参考价格_近端 |
| reference_adjust_j | numeric(20,8) | Y |  | 参考价格调整项_近端 |
| currency_buy_y | varchar(8) | Y |  | 买入币种_远端 |
| num_buy_y | numeric(24,6) | Y |  | 买入量_远端 |
| currency_sell_y | varchar(8) | Y |  | 卖出币种_远端 |
| num_sell_y | numeric(24,6) | Y |  | 卖出量_远端 |
| price_y | numeric(20,8) | Y |  | 成交价格_远端 |
| due_date_y | varchar(8) | Y |  | 到期交割日_远端 |
| trade_type_y | varchar(3) | Y |  | 成交类型_远端：见tp_public_dict的253只包含即期和远期 |
| reference_type_y | varchar(3) | Y |  | 参考价类型_远端：见tp_public_dict的288 |
| reference_date_y | varchar(8) | Y |  | 参考价日期_远端 |
| reference_price_y | numeric(20,8) | Y |  | 参考价格_远端 |
| reference_adjust_y | numeric(20,8) | Y |  | 参考价格调整项_远端 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| inquire_type | varchar(3) | Y |  | 询价类型：见Dict的325 |
| party_broker_no | varchar(10) | Y |  | 对手方经纪机构代码 |
| period_j | varchar(10) | Y |  | 期限_近端：见tp_public_dict的344 |
| trade_volume_j | numeric(16,0) | Y |  | 交易手数_近端 |
| refprice_info_j | varchar(50) | Y |  | 其他参考价格说明_近端 |
| storage_no_j | varchar(4) | Y |  | 指定仓库代码_近端,白银合约时字段有值 |
| period_y | varchar(10) | Y |  | 期限_远端：见tp_public_dict的344 |
| trade_volume_y | numeric(16,0) | Y |  | 交易手数_远端 |
| refprice_info_y | varchar(50) | Y |  | 其他参考价格说明_远端 |
| storage_no_y | varchar(4) | Y |  | 指定仓库代码_远端,白银合约时字段有值 |
| if_exch_clearfund | varchar(4) | Y |  | 是否交易所清算资金：见tp_public_dict的027 |
| party_member_id | varchar(40) | Y |  | 对手方席位号 |
| party_client_id | varchar(10) | Y |  | 对手方客户代码 |
| broker_no | varchar(10) | Y |  | 本方经纪机构代码 |
| related_match_no | varchar(20) | Y |  | 相关成交单号:用来记录行权的期权成交单号，或为未来其他业务备用 |
| remark | varchar(254) | Y |  | 附加条款 |

---

## 730. dimple.tmp_sge_predelivery_jour　(11 字段)
> 表含义：预交割单表临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| predelivery_no | varchar(16) | N |  | 预交割单号 |
| delivery_date | varchar(8) | Y |  | 交割日期 |
| apply_date | varchar(8) | Y |  | 申报日期 |
| bs_flag | bpchar(1) | N |  | 买卖标志：见TP_PUBLIC_DICT的002 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(20,6) | Y |  | 数量：3代交割重量(kg) |
| amount | numeric(18,2) | Y |  | 金额 |
| qty_s | numeric(12,0) | Y |  | 交割手数 |

---

## 731. dimple.tmp_shfe_client_storage_jour　(6 字段)
> 表含义：SHFE客户库存流水临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_seq_no | varchar(10) | N |  | 交易所流水号 |
| price | numeric(9,2) | Y |  | 价格 |
| qty | numeric(15,3) | Y |  | 数量 |
| weighted_price | numeric(16,2) | Y |  | 加权平均价 |
| remain_qty | numeric(15,3) | Y |  | 剩余数量 |

---

## 732. dimple.tmp_tc_cffex_bond_delivery　(10 字段)
> 表含义：交割匹配文件导入临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| input_date | varchar(8) | N |  |  |
| contract_id | varchar(20) | Y |  |  |
| member_id | varchar(8) | Y |  |  |
| member_attr | varchar(16) | Y |  |  |
| accountid | varchar(8) | Y |  |  |
| accattr | varchar(8) | Y |  |  |
| price | numeric(20,8) | Y |  |  |
| order_qty | numeric(12,0) | Y |  |  |
| qty | numeric(12,0) | Y |  |  |
| delivery_fee | numeric(22,2) | Y |  |  |

---

## 733. dimple.tmp_tc_delivery_calendar　(12 字段)
> 表含义：合约交割日历临时表　|　估算行数：**11**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| delivery_start | varchar(6) | Y |  | 开始交割 |
| delivery_start_date | varchar(8) | Y |  | 开始交割日期(倒退) |
| delivery_end | varchar(6) | Y |  | 交割结束 |
| delivery_end_date | varchar(8) | Y |  | 交割结束日期(倒退) |
| release_inv_start | varchar(6) | Y |  | 开发票 |
| release_start_date | varchar(8) | Y |  | 开发票开始日期(倒退) |
| release_inv_end | varchar(6) | Y |  | 开发票结束 |
| release_end_date | varchar(8) | Y |  | 开发票结束日期(倒退) |
| overdue_start | varchar(6) | Y |  | 超期 |
| overdue_start_date | varchar(8) | Y |  | 超期日期(倒退) |
| delivery_amount_type | bpchar(1) | Y |  | 交割货款方式：见tp_public_dict的234 |

---

## 734. dimple.tmp_tc_delivery_posi_nomatch　(8 字段)
> 表含义：交割持仓对账临时表。用来存放交易所与系统交割持仓对账时，不匹配数据。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_date | varchar(8) | N |  | 交割日期 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| bs_flag | bpchar(1) | N |  | 买卖标志：见TP_PUBLIC_DICT的002 |
| price | numeric(18,3) | Y |  | 交割价格 |
| qty | numeric(10,0) | Y |  | 交割数量 |
| amount | numeric(18,2) | Y |  | 交割金额 |

---

## 735. dimple.tmp_tc_nomatch　(16 字段)
> 表含义：用来存放交易所与系统对账临时数据的　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| exch_code | varchar(2) | Y |  | 交易所代码 |
| match_no | varchar(20) | Y |  | 成交号 |
| bs_flag | varchar(20) | Y |  | 买卖标志 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| qty | numeric(12,0) | Y |  | 数量 |
| price | numeric(20,4) | Y |  | 价格 |
| match_time | varchar(12) | Y |  | 成交时间 |
| eo_flag | varchar(20) | Y |  | 开平标志:见tp_public_dict的003 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| trader_no | varchar(16) | Y |  | 席位号 |
| sh_flag | varchar(20) | Y |  | 投保标志：见tp_public_dict的004 |
| middle_flag | varchar(2) | Y |  | 是否中立仓：见tp_public_dict的027 |
| file_type | varchar(2) | Y |  | 成交文件类型：03-交割申报成交，04-报价成交，空-非(03和04) |

---

## 736. dimple.tmp_tc_origin_money　(50 字段)
> 表含义：原始金交所资金临时表：已废弃　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N |  | 结算日期 |
| clear_account_no | varchar(14) | N |  |  |
| exch_code | varchar(2) | N |  | 交易所代码 |
| accounttype | varchar(2) | Y |  | 帐户类型 |
| last_remain | numeric(18,2) | Y |  | 上日实有货币资金余额 |
| recv_money | numeric(18,2) | Y |  | 当日收入资金 |
| profitloss | numeric(18,2) | Y |  | 当日盈亏 |
| pay_money | numeric(18,2) | Y |  | 当日付出资金 |
| fee | numeric(18,2) | Y |  | 手续费 |
| trade_fee | numeric(18,2) | Y |  | 交易手续费 |
| clear_fee | numeric(18,2) | Y |  | 结算手续费 |
| delivery_fee | numeric(18,2) | Y |  | 交割手续费 |
| move_posi_fee | numeric(18,2) | Y |  | 移仓手续费 |
| deposit | numeric(18,2) | Y |  | 当日实有货币资金余额 |
| margin | numeric(18,2) | Y |  | 交易保证金 |
| remain | numeric(18,2) | Y |  | 结算准备金 |
| money_in | numeric(18,2) | Y |  | 申报划入金额 |
| money_out | numeric(18,2) | Y |  | 申报划出金额 |
| prepare_margin | numeric(18,2) | Y |  | 开仓准备金 |
| pay_fee | numeric(18,2) | Y |  | 支付手续费 |
| deposit_chg | numeric(18,2) | Y |  | 实有货币资金变动 |
| margin_chg | numeric(18,2) | Y |  | 交易保证金变动 |
| remain_chg | numeric(18,2) | Y |  | 结算准备金变动 |
| if_cmp | varchar(2) | Y |  | 是否资金对帐 |
| currency | varchar(2) | N |  | 币种 |
| right_valid | numeric(18,2) | Y |  | 权利凭证实际可用金额 |
| right_used | numeric(18,2) | Y |  | 权利凭证实际占用 |
| spec_margin | numeric(18,2) | Y |  | 投机头寸保证金 |
| hedge_margin | numeric(18,2) | Y |  | 保值头寸保证金 |
| delivery_margin | numeric(18,2) | Y |  | 交割头寸保证金 |
| free_trade_fee | numeric(18,2) | Y |  | 减免交易手续费 |
| mate_money | numeric(18,2) | Y |  | 最大配比金额 |
| right_off_money | numeric(18,2) | Y |  | 权利凭证折后金额 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| call_margin | numeric(18,2) | Y |  | 追加保证金 |
| other_money | numeric(18,2) | Y |  | 其他费用 |
| reserve | numeric(18,2) | Y |  | 利息 |
| last_balance | numeric(18,2) | Y |  | 上日结算准备金余额 |
| last_frozen_margin | numeric(18,2) | Y |  | 上日占用保证金 |
| last_base_margin | numeric(18,2) | Y |  | 上日基础保证金 |
| forzen_margin | numeric(18,2) | Y |  | 当日占用保证金 |
| base_margin | numeric(18,2) | Y |  | 当日基础保证金 |
| frozen_profitloss | numeric(18,2) | Y |  | 当日远期盈亏冻结 |
| pt_frozen_amount | numeric(18,2) | Y |  | 当日铂金冻结金额 |
| ag_frozen_amount | numeric(18,2) | Y |  | 当日白银冻结金额 |
| manual_frozen_amount | numeric(18,2) | Y |  | 当日手工冻结金额 |
| last_frozen_profitloss | numeric(18,2) | Y |  | 上日盈亏冻结 |
| last_frozen_amount | numeric(18,2) | Y |  | 上日货款冻结 |
| last_delivery_margin | numeric(18,2) | Y |  | 上日交割保证金 |

---

## 737. dimple.tmp_tc_storage_nomatch　(14 字段)
> 表含义：库存不匹配临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日 |
| exch_seq_no | varchar(20) | Y |  | 交易所流水号 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| variety_id | varchar(3) | Y |  | 品种号 |
| total_store | numeric(15,3) | Y |  | 总库存 |
| trans_type | varchar(2) | Y |  | 交易所库存流水类型 |
| nomatch_type | varchar(2) | Y |  |  |
| available_storage | numeric(16,6) | Y |  | 可用库存 |
| pend_storage | numeric(16,6) | Y |  | 待提库存 |
| mort_storage | numeric(16,6) | Y |  | 质押库存 |
| law_frozen_storage | numeric(16,6) | Y |  | 法律冻结库存 |
| setoff_frozen_storage | numeric(16,6) | Y |  | 充抵冻结库存 |
| transfer_frozen_storage | numeric(16,6) | Y |  | 过户业务冻结库存 |

---

## 738. dimple.tmp_trader_credit_clear　(14 字段)
> 表含义：交易员结算信用额度临时表　|　估算行数：**146**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| exch_code | varchar(2) | N |  | 交易所 |
| member_id | varchar(8) | N |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员号 |
| currency | varchar(3) | N |  | 币种 |
| credit_tot | numeric(18,2) | Y |  | 信用额度 |
| credit_used | numeric(18,2) | Y |  | 已用信用额度 |
| credit_remain | numeric(18,2) | Y |  | 剩余信用额度 |
| operator | varchar(30) | Y |  | 操作员 |
| float_profitloss | numeric(18,2) | Y |  | 浮动盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| if_check | varchar(3) | Y |  | 是否检查：见 Dict 027 |

---

## 739. dimple.tmp_trader_credit_clear_own　(14 字段)
> 表含义：交易员结算信用额度临时表--保存不考虑交易员树的数据　|　估算行数：**146**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| exch_code | varchar(2) | N |  | 交易所 |
| member_id | varchar(8) | N |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员号 |
| currency | varchar(3) | N |  | 币种 |
| credit_tot | numeric(18,2) | Y |  | 信用额度 |
| credit_used | numeric(18,2) | Y |  | 已用信用额度 |
| credit_remain | numeric(18,2) | Y |  | 剩余信用额度 |
| operator | varchar(30) | Y |  | 操作员 |
| float_profitloss | numeric(18,2) | Y |  | 浮动盈亏 |
| offset_profitloss | numeric(18,2) | Y |  | 平仓盈亏 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| if_check | varchar(3) | Y |  | 是否检查：见 Dict 027 |

---

## 740. dimple.tmp_user_rights　(6 字段)
> 表含义：用户角色临时表　|　估算行数：**2,492**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| event_id | float8 | Y |  | EVENT_ID |
| user_id | varchar(30) | Y |  | USER_ID |
| right_type | float8 | Y |  | RIGHT_TYPE |
| right_1 | varchar(2000) | Y |  | RIGHT_1 |
| right_2 | varchar(2000) | Y |  | RIGHT_2 |
| right_3 | varchar(2000) | Y |  | RIGHT_3 |

---

## 741. dimple.tmp_user_roles　(3 字段)
> 表含义：用户角色临时表　|　估算行数：**445**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| event_id | float8 | Y |  | EVENT_ID |
| user_id | varchar(30) | Y |  | USER_ID |
| role_id | float8 | Y |  | ROLE_ID |

---

## 742. dimple.tmp_vaexp_clear　(11 字段)
> 表含义：结算品种敞口额度临时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| operator | varchar(30) | Y |  | 操作员 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| ifcheck | varchar(3) | Y |  | 是否检查敞敞口:见tp_public_dict的120 |

---

## 743. dimple.tmp_variety_exposure　(11 字段)
> 表含义：品种敞口额度换算临时表　|　估算行数：**5,712**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| member_id | varchar(8) | N |  | 会员号 |
| user_id | varchar(30) | N |  | 交易员号 |
| variety_id | varchar(4) | N |  | 品种代码 |
| day_exposure | numeric(22,6) | Y |  | 日中敞口额度 |
| overnight_exposure | numeric(22,6) | Y |  | 隔夜敞口额度 |
| used_exposure | numeric(22,6) | Y |  | 已用敞口 |
| operator | varchar(30) | Y |  | 操作员 |
| market_type | bpchar(1) | N |  | 市场:见tp_public_dict的001 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| ifcheck | varchar(1) | Y |  | 是否设置检查:见tp_public_dict的120 |

---

## 744. dimple.tp_biz_ctrl　(4 字段)
> 表含义：系统控制表:目前只存放系统状态变化的时间，由交易核心写入，做市商日终评价算全部的交易时间用以及结算价计算（收盘前几分钟）也用。　|　估算行数：**23,544**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| type | varchar(2) | N | √ | 类型:见tp_public_dict的167 |
| code | varchar(20) | N | √ | 代码:对于系统状态类型，存放状态 |
| value | varchar(20) | N | √ | 值:对于系统状态类型，存放时间 |

---

## 745. dimple.tp_cmd　(6 字段)
> 表含义：上场指令表　|　估算行数：**292,930**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| cmd_no | float8 | N | √ | 上场序号 |
| cmd_type | varchar(2) | N |  | 指令类型:见tp_public_dict的149 |
| org_jour_no | varchar(20) | Y |  | 原表操作流水号:客户开户，填写的是交易编码（会员号＋客户号），其他填写流水号。 |
| status | bpchar(1) | Y |  | 上场状态:见tp_public_dict的150 |
| err_info | varchar(254) | Y |  | 错误描述 |

---

## 746. dimple.tp_contract_logout_date　(4 字段)
> 表含义：合约停牌日期表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| start_date | varchar(8) | N | √ | 停牌起始日期 |
| stop_date | varchar(8) | N |  | 停牌终止日期 |
| trade_type | varchar(2) | N |  | 交易类型:见tp_public_dict的001 |

---

## 747. dimple.tp_contract_trade_date　(2 字段)
> 表含义：合约的交易日表:根据交易所的交易日表和合约停牌日期表计算得到，包括合约整个生命周期的全部日期。　|　估算行数：**75,633**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| trade_date | varchar(8) | N | √ | 交易日期 |

---

## 748. dimple.tp_contract_trade_day　(7 字段)
> 表含义：合约交易日统计表:初始化时,根据合约交易日表计算.　|　估算行数：**22**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| year_day_no | float8 | Y |  | 当日在本年的交易日数 |
| month_day_no | float8 | Y |  | 当日在本月的交易日数 |
| if_logout | bpchar(1) | Y |  | 是否停牌 |
| if_hedge_reused | bpchar(1) | Y |  | 保值是否重复使用:仅期货合约使用 |
| next_date | varchar(8) | Y |  | 下一交易日 |
| before_delivery_pos | float8 | Y |  | 交割月的前几个月 |

---

## 749. dimple.tp_data_check_log　(9 字段)
> 表含义：数据检查日志表:记录数据检查的结果　|　估算行数：**33,276**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| check_date | varchar(8) | N | √ | 日期 |
| check_time | varchar(8) | Y |  | 时间 |
| check_item | varchar(30) | N |  | 检查类型:见tp_public_dict的142 |
| check_contents | varchar(1000) | Y |  | 检查内容 |
| op_flag | bpchar(1) | Y |  | 操作结果:参见tp_public_dict的177 |
| operator | varchar(30) | Y |  | 操作员 |
| err_desc | varchar(4000) | Y |  | 错误原因 |
| exch_code | varchar(2) | Y |  | 交易所代码 |

---

## 750. dimple.tp_delivery_calendar　(7 字段)
> 表含义：合约交割日历表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| delivery_start | varchar(6) | Y |  | 开始交割 |
| delivery_end | varchar(6) | Y |  | 交割结束 |
| release_inv_start | varchar(6) | Y |  | 开发票 |
| release_inv_end | varchar(6) | Y |  | 开发票结束 |
| overdue_start | varchar(6) | Y |  | 超期 |
| delivery_amount_type | bpchar(1) | Y |  | 交割货款方式：见tp_public_dict的234 |

---

## 751. dimple.tp_err_info　(3 字段)
> 表含义：错误描述表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| err_no | varchar(20) | N | √ | 错误号 |
| err_info | varchar(254) | Y |  | 原错误描述 |
| new_err_info | varchar(254) | Y |  | 新错误描述 |

---

## 752. dimple.tp_exch_trade_date　(2 字段)
> 表含义：交易所的交易日表:据节假日表生成.　|　估算行数：**1,869**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| note | varchar(254) | Y |  | 备注 |

---

## 753. dimple.tp_hint　(6 字段)
> 表含义：业务提示表(业务库):作废　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_id | varchar(80) | N | √ | 提示代码 |
| hint_name | varchar(80) | N |  | 提示名称 |
| hint_type | varchar(2) | N |  | 提示类型:见tp_public_dict的079 |
| urgency_degree | bpchar(1) | N |  | 紧急程度:见tp_public_dict的080 |
| if_return | bpchar(1) | N |  | 是否产生回执 |
| gen_style | varchar(2) | N |  | 接收者生成方式:见tp_public_dict的172 |

---

## 754. dimple.tp_hint_list　(14 字段)
> 表含义：业务提示列表(业务库):作废　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_no | float8 | N | √ | 提示流水号 |
| hint_id | varchar(80) | Y |  | 提示代码 |
| hint_type | varchar(2) | N |  | 提示类型:见tp_public_dict的079 |
| title | varchar(80) | Y |  | 标题 |
| content | varchar(254) | Y |  | 内容 |
| biz_id | varchar(80) | Y |  | 业务标识 |
| come_from | varchar(2) | Y |  | 消息源:见tp_public_dict的170 |
| gen_date | varchar(8) | Y |  | 产生日期 |
| gen_time | varchar(8) | Y |  | 产生时间 |
| if_return | bpchar(1) | Y |  | 是否产生回执 |
| urgency_degree | bpchar(1) | Y |  | 紧急程度:见tp_public_dict的080 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的171 |
| begin_date | varchar(8) | Y |  | 有效期起始日期 |
| end_date | varchar(8) | Y |  | 有效期终止日期 |

---

## 755. dimple.tp_holiday　(3 字段)
> 表含义：节假日表:存放非交易日.　|　估算行数：**2,128**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| holiday_date | varchar(8) | N | √ | 节假日 |
| holiday_name | varchar(80) | Y |  | 节假日名称 |
| note | varchar(254) | Y |  | 备注 |

---

## 756. dimple.tp_holiday_mold　(6 字段)
> 表含义：节假日模板表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| holiday_name | varchar(80) | Y |  | 节假日名称 |
| start_date | varchar(8) | N |  | 开始日期 |
| day_num | float8 | N |  | 延续的工作日数 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 757. dimple.tp_inst_idtocode　(5 字段)
> 表含义：G4合约ID与合约CODE对照表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sort | varchar(4) | N | √ | 交易所 |
| contract_id | varchar(10) | N | √ | 合约序号 |
| contract_code | varchar(80) | Y |  | 合约代码 |
| ename | varchar(80) | Y |  | 英文名称 |
| exch_code | varchar(20) | Y |  | 交易所定制:见interface.tp_public_dict的235 |

---

## 758. dimple.tp_master_para　(18 字段)
> 表含义：万能参数主表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| code | float8 | N | √ | 参数号 |
| code_name | varchar(100) | Y |  | 参数号名称 |
| subcode_name_id | float8 | Y |  | 参数子号名称数据字典:从1开始,0代表不控制 |
| if_dept_code | varchar(1) | Y |  | 是否控制到部门代码:见tp_public_dict的027 |
| if_exch_code | varchar(1) | Y |  | 是否控制到交易所:见tp_public_dict的027 |
| if_member_id | varchar(1) | Y |  | 是否控制到会员号:见tp_public_dict的027 |
| if_client_id | varchar(1) | Y |  | 是否控制到客户号:见tp_public_dict的027 |
| if_trader_no | varchar(1) | Y |  | 是否控制到交易员号:见tp_public_dict的027 |
| if_purpose_code | varchar(1) | Y |  | 是否控制到交易目的:见tp_public_dict的027 |
| if_portfolio_code | varchar(1) | Y |  | 是否控制到投组号:见tp_public_dict的027 |
| if_trade_type | varchar(1) | Y |  | 是否控制到交易类型/市场:见tp_public_dict的027 |
| if_unique | varchar(1) | Y |  | 参数子号是否唯一:见tp_public_dict的027 |
| if_updateable | varchar(1) | Y |  | 参数是否可新增/修改/删除:见tp_public_dict的027 |
| update_rule | varchar(1000) | Y |  | 参数修改规范:当参数可新增/修改/删除时使用，新增或修改界面展示,零级数据刷入 |
| remark_system | varchar(500) | Y |  | 其他说明：非对外展示字段 |
| para_string_id | float8 | Y |  | 参数值数据字典:从1开始,0代表不控制 |
| if_immediate_effect | varchar(1) | Y |  | 是否实时生效:见tp_public_dict的027 |
| if_init_up | varchar(1) | Y |  | 是否初始化上场:见tp_public_dict的027 |

---

## 759. dimple.tp_master_para_dict　(4 字段)
> 表含义：万能参数可选项字典表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| options_id | float8 | N | √ | 数据字典ID |
| options_name | varchar(500) | Y |  | 参数值名称 |
| options_string | varchar(500) | N | √ | 参数值：与para_string_id对应时#入表TP_MASTER_PARA_SUB.para_string；与subcode_name_id对应时#入表TP_MASTER_PARA_SUB.subcode_name |
| options_remark | varchar(500) | Y |  | 其他说明：非对外展示字段 |

---

## 760. dimple.tp_master_para_sub　(19 字段)
> 表含义：万能参数附表　|　估算行数：**69**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| code | float8 | N | √ | 参数号 |
| subcode | float8 | N | √ | 参数子号 |
| subcode_name | varchar(500) | Y |  | 参数子号名称：由参数子号名称数据字典控制，不控制时为空 |
| para_string | varchar(500) | Y |  | 参数值：由参数值数据字典控制，不控制时，可输入 |
| dept_code | varchar(10) | Y |  | 部门代码:$代表不控制到此维度 |
| exch_code | varchar(2) | Y |  | 交易所:$代表不控制到此维度 |
| member_id | varchar(8) | Y |  | 会员号:$代表不控制到此维度 |
| client_id | varchar(16) | Y |  | 客户号:$代表不控制到此维度 |
| trader_no | varchar(30) | Y |  | 交易员号:$代表不控制到此维度 |
| purpose_code | varchar(3) | Y |  | 交易目的:$代表不控制到此维度 |
| portfolio_code | varchar(5) | Y |  | 投组号:$代表不控制到此维度 |
| trade_type | varchar(1) | Y |  | 交易类型/市场:$代表不控制到此维度；控制时的数据字典tp_public_dict的001 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |
| para_string_name | varchar(500) | Y |  | 参数值备注：由参数值数据字典控制，不控制时，可输入 |

---

## 761. dimple.tp_master_para_sub_jour　(22 字段)
> 表含义：万能参数附表流水表　|　估算行数：**445**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 流水号 |
| code | float8 | N | √ | 参数号 |
| subcode | float8 | N | √ | 参数子号 |
| subcode_name | varchar(500) | Y |  | 参数子号名称：由参数子号名称数据字典控制，不控制时为空 |
| para_string | varchar(500) | Y |  | 参数值：由参数值数据字典控制，不控制时，可输入 |
| dept_code | varchar(10) | Y |  | 部门代码:$代表不控制到此维度 |
| exch_code | varchar(2) | Y |  | 交易所:$代表不控制到此维度 |
| member_id | varchar(8) | Y |  | 会员号:$代表不控制到此维度 |
| client_id | varchar(16) | Y |  | 客户号:$代表不控制到此维度 |
| trader_no | varchar(30) | Y |  | 交易员号:$代表不控制到此维度 |
| purpose_code | varchar(3) | Y |  | 交易目的:$代表不控制到此维度 |
| portfolio_code | varchar(5) | Y |  | 投组号:$代表不控制到此维度 |
| trade_type | varchar(1) | Y |  | 交易类型/市场:$代表不控制到此维度；控制时的数据字典tp_public_dict的001 |
| op_status | varchar(3) | Y |  | 操作状态：见tp_public_dict的068 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |
| para_string_name | varchar(500) | Y |  | 参数值备注：由参数值数据字典控制，不控制时，可输入 |
| status | varchar(1) | Y |  | 上场流水状态:见tp_public_dict的209 |

---

## 762. dimple.tp_para　(9 字段)
> 表含义：业务参数表:存放各个系统的业务参数，可分部门管理。包括做市商通知发送时刻,强平单时刻，重检报送时限(天),合格注册时限(天),期货合约不参与组合期限,期权合约不参与组合期限,期货对锁保证金比例,期权对锁保证金比例，无风险利率，免报送天数，密码有效期，失败登录次数等。　|　估算行数：**150**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| code | varchar(80) | N | √ | 系统参数代码 |
| para_name | varchar(60) | Y |  | 中文名称 |
| ename | varchar(40) | Y |  | 英文名称 |
| para_value | numeric(10,6) | Y |  | 参数值 |
| para_string | varchar(80) | Y |  | 参数字符串 |
| note | varchar(700) | Y |  | 备注 |
| operator | varchar(30) | Y |  | 操作员 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| if_fixed | bpchar(1) | Y |  | 是否固化 |

---

## 763. dimple.tp_para_check　(19 字段)
> 表含义：业务参数复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| code | varchar(80) | N |  | 系统参数代码 |
| para_name | varchar(40) | Y |  | 中文名称 |
| ename | varchar(40) | Y |  | 英文名称 |
| para_value | numeric(10,6) | Y |  | 参数值 |
| para_string | varchar(80) | Y |  | 参数字符串 |
| note | varchar(254) | Y |  | 备注 |
| operator | varchar(30) | Y |  | 操作员 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| if_fixed | bpchar(1) | Y |  | 是否固化 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 764. dimple.tp_public_category　(5 字段)
> 表含义：业务数据字典类别表:存放常量的大类，可分部门管理。见constant.xml　|　估算行数：**350**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sort | varchar(4) | N | √ | 类别 |
| type_name | varchar(80) | Y |  | 名称 |
| ename | varchar(80) | Y |  | 英文名称 |
| dept_code | varchar(10) | Y |  | 部门代码:指由谁来维护 |
| if_fixed | bpchar(1) | Y |  | 是否固化 |

---

## 765. dimple.tp_public_counter　(5 字段)
> 表含义：公用计数器表:交割匹配号，仓单打印表的打印编号，期权执行配对号，指标代码的序号,期转现编号,投机转套保序号等。　|　估算行数：**113**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| counter_no | varchar(80) | N | √ | 计数器代码 |
| counter_name | varchar(60) | Y |  | 名称 |
| init_value | float8 | N |  | 初始值 |
| cur_value | float8 | N |  | 当前值 |
| counter_type | varchar(2) | Y |  | 类型:见tp_public_code的144 |

---

## 766. dimple.tp_public_dict　(5 字段)
> 表含义：业务数据字典表:存放常量值,见constant.xml　|　估算行数：**1,981**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| sort | varchar(4) | N | √ | 类别 |
| type | varchar(10) | N | √ | 类型 |
| code_name | varchar(120) | Y |  | 名称 |
| ename | varchar(80) | Y |  | 英文名称 |
| exch_code | varchar(20) | Y |  | 交易所定制:见interface.tp_public_dict的235 |

---

## 767. dimple.tp_shell_crtl　(2 字段)
> 表含义：shell状态控制表　|　估算行数：**701**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 日期 |
| status | bpchar(2) | N |  | 状态：见tp_public_dict:241 |

---

## 768. dimple.tp_trade_calendar　(5 字段)
> 表含义：交易日历表:存放交易日的合约的相关业务,自动生成。　|　估算行数：**266**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| calendar_date | varchar(8) | N | √ | 日期 |
| trade_type | varchar(2) | N | √ | 交易类型:见tp_public_dict的001 |
| contract_id | varchar(20) | N | √ | 合约号 |
| event_type | varchar(2) | N | √ | 事件类型:见tp_public_dict的098 |
| note | varchar(1000) | Y |  | 事件说明 |

---

## 769. dimple.tp_trade_period　(7 字段)
> 表含义：交易期间管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| period_name | varchar(80) | Y |  | 交易期间名称 |
| start_date | varchar(8) | N |  | 开始日期 |
| end_date | varchar(8) | N |  | 结束日期 |
| status | bpchar(1) | N |  | 状态:见tp_public_code的181 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 770. dimple.tp_weekend　(4 字段)
> 表含义：公休日表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| if_sat | bpchar(1) | N |  | 周六 |
| if_sun | bpchar(1) | N |  | 周日 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 771. dimple.transfer_batch　(4 字段)
> 表含义：迁移批次　|　估算行数：**173**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| batch_no | varchar(20) | N | √ | 批次号 |
| run_flag | bpchar(1) | N |  | 运行标志 |
| transfer_date | varchar(10) | N |  | 迁移日期 |
| create_time | varchar(20) | Y |  | 创建时间 |

---

## 772. dimple.transfer_log　(5 字段)
> 表含义：迁移日志　|　估算行数：**29,872**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| batch_no | varchar(20) | N |  | 批次号 |
| topic | varchar(50) | N |  | 主题 |
| time_use | numeric(64,0) | Y |  | 耗时 |
| note | text | Y |  | 备注 |
| create_time | varchar(20) | Y |  | 创建时间 |

---

## 773. dimple.transfer_result　(5 字段)
> 表含义：迁移结果　|　估算行数：**3**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| step | varchar(50) | N | √ | 步骤 |
| status | bpchar(1) | N |  | 状态 |
| note | text | Y |  | 备注 |
| create_time | varchar(20) | Y |  | 创建时间 |
| update_time | varchar(20) | Y |  | 更新时间 |

---

## 774. dimple.transfer_result_batch　(6 字段)
> 表含义：迁移结果　|　估算行数：**471**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| batch_no | varchar(20) | N | √ | 批次号 |
| step | varchar(50) | N | √ | 步骤 |
| status | bpchar(1) | N |  | 状态 |
| note | text | Y |  | 备注 |
| create_time | varchar(20) | Y |  | 创建时间 |
| update_time | varchar(20) | Y |  | 更新时间 |

---

## 775. dimple.transfer_table_info　(5 字段)
> 表含义：迁移表信息　|　估算行数：**2,576**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| table_name | varchar(50) | N | √ | 表名 |
| column_name | varchar(50) | N | √ | 字段名 |
| key | bpchar(1) | Y |  | 是否为主键 |
| create_time | varchar(20) | Y |  | 创建时间 |
| update_time | varchar(20) | Y |  | 更新时间 |

---

## 776. dimple.transfer_table_info_batch　(6 字段)
> 表含义：迁移表信息　|　估算行数：**423,698**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| batch_no | varchar(20) | N | √ | 批次号 |
| table_name | varchar(50) | N | √ | 表名 |
| column_name | varchar(50) | N | √ | 字段名 |
| key | bpchar(1) | Y |  | 是否为主键 |
| create_time | varchar(20) | Y |  | 创建时间 |
| update_time | varchar(20) | Y |  | 更新时间 |

---

## 777. dimple.transfer_table_result　(10 字段)
> 表含义：迁移表结果　|　估算行数：**116**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| table_name | varchar(50) | N | √ | 表名 |
| batch_part | numeric(32,0) | N | √ | 分片 |
| source_owner | varchar(50) | Y |  | 源库所有者 |
| target_owner | varchar(50) | Y |  | 目标库所有者 |
| status | bpchar(1) | N |  | 状态 |
| total_num | numeric(32,0) | Y |  | 总记录数 |
| transfer_num | numeric(32,0) | Y |  | 迁移记录数 |
| note | text | Y |  | 备注 |
| create_time | varchar(20) | Y |  | 创建时间 |
| update_time | varchar(20) | Y |  | 更新时间 |

---

## 778. dimple.transfer_table_result_batch　(11 字段)
> 表含义：迁移表结果　|　估算行数：**22,705**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| batch_no | varchar(20) | N | √ | 批次号 |
| table_name | varchar(50) | N | √ | 表名 |
| batch_part | numeric(32,0) | N | √ | 分片 |
| source_owner | varchar(50) | Y |  | 源库所有者 |
| target_owner | varchar(50) | Y |  | 目标库所有者 |
| status | bpchar(1) | N |  | 状态 |
| total_num | numeric(32,0) | Y |  | 总记录数 |
| transfer_num | numeric(32,0) | Y |  | 迁移记录数 |
| note | text | Y |  | 备注 |
| create_time | varchar(20) | Y |  | 创建时间 |
| update_time | varchar(20) | Y |  | 更新时间 |

---

## 779. dimple.ts_app_version　(5 字段)
> 表含义：应用程序版本表　|　估算行数：**1,049**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| app_no | varchar(30) | N | √ | 应用程序ID |
| app_version | varchar(30) | N |  | 应用程序版本 |
| ip_addr | varchar(30) | N | √ | IP地址 |
| upd_date | varchar(8) | N |  | 更新日期 |
| upd_time | varchar(8) | N |  | 更新时间 |

---

## 780. dimple.ts_apps　(5 字段)
> 表含义：应用程序表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| app_no | varchar(30) | N | √ | 应用标识 |
| name | varchar(80) | Y |  | 名称 |
| status | bpchar(1) | Y |  | 状态:参见tp_public_dict的120 |
| operator | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 781. dimple.ts_apps_db_rela　(3 字段)
> 表含义：应用程序和数据库连接关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| app_no | varchar(30) | N | √ | 应用标识 |
| db_name | varchar(30) | N | √ | 数据库连接标识 |
| ip_addr | varchar(30) | N | √ | IP地址 |

---

## 782. dimple.ts_cert　(9 字段)
> 表含义：证书表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| security_id | varchar(30) | N | √ | 安全标识号 |
| user_type | bpchar(1) | N | √ | 用户类型:见tp_public_dict的213 |
| cert_uid | varchar(80) | N | √ | 证书唯一标识 |
| cert_serial | varchar(30) | Y |  | 证书的序列号 |
| open_date | varchar(8) | Y |  | 有效开始日期 |
| expires | varchar(8) | Y |  | 到期日 |
| status | bpchar(1) | Y |  | 证书状态:参见tp_public_dict的110 |
| op_user_id | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 783. dimple.ts_cert_his　(10 字段)
> 表含义：证书历史表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 日期 |
| security_id | varchar(30) | N |  | 安全标识号 |
| user_type | bpchar(1) | N |  | 用户类型:见tp_public_dict的109 |
| cert_uid | varchar(80) | N |  | 证书唯一标识 |
| cert_serial | varchar(30) | Y |  | 证书的序列号 |
| open_date | varchar(8) | Y |  | 有效开始日期 |
| expires | varchar(8) | Y |  | 到期日 |
| status | bpchar(1) | Y |  | 证书状态:参见tp_public_dict的110 |
| op_user_id | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 784. dimple.ts_cfg　(12 字段)
> 表含义：配置信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| app_no | varchar(30) | N | √ | 应用程序ID |
| app_version | varchar(30) | N | √ | 应用程序版本 |
| cfg_id | varchar(30) | N | √ | 配置文件ID |
| ip_addr | varchar(30) | N | √ | 个性化IP地址 |
| group_name | varchar(80) | N | √ | 配置节名字 |
| item_name | varchar(80) | N |  | 配置项名字 |
| item_value | varchar(255) | N |  | 配置项值 |
| seq_no | float8 | N | √ | 排列顺序 |
| create_date | varchar(8) | Y |  | 创建日期 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| item_note | varchar(254) | Y |  | 配置项说明 |

---

## 785. dimple.ts_cfg_md5　(5 字段)
> 表含义：配置文件的MD5信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| app_no | varchar(30) | N | √ | 应用程序ID |
| app_version | varchar(30) | N | √ | 应用程序版本 |
| cfg_id | varchar(30) | N | √ | 配置文件ID |
| ip_addr | varchar(30) | N | √ | 个性化IP地址 |
| cfg_md5str | varchar(80) | N |  | MD5信息 |

---

## 786. dimple.ts_data_clean_def　(8 字段)
> 表含义：数据清理定义表:数据的清理操作仅针对日增型数据，　|　估算行数：**137**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| s_owner | varchar(20) | N | √ | 源表所有者 |
| s_table_name | varchar(30) | N | √ | 源表名 |
| s_table_desc | varchar(254) | Y |  | 源表描述 |
| clean_field | varchar(30) | N |  | 判定字段名 |
| reserve_days | float8 | N |  | 数据保留周期(天) |
| last_clean_date | varchar(8) | Y |  | 上次清理日期 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 787. dimple.ts_data_clean_log　(11 字段)
> 表含义：数据清理日志表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| seq_no | float8 | N | √ | 序号 |
| owner | varchar(20) | Y |  | 表所有者 |
| table_name | varchar(30) | Y |  | 表名 |
| begin_date | varchar(8) | Y |  | 起始日期 |
| begin_time | varchar(8) | Y |  | 起始时间 |
| end_date | varchar(8) | Y |  | 结束日期 |
| end_time | varchar(8) | Y |  | 结束时间 |
| op_flag | bpchar(1) | Y |  | 操作结果:参见tp_public_dict的119 |
| operator | varchar(30) | Y |  | 操作员 |
| note | varchar(254) | Y |  | 备注 |

---

## 788. dimple.ts_db_connection　(6 字段)
> 表含义：数据库连接信息:该信息在服务层连接数据层时使用　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| db_name | varchar(30) | N | √ | 数据库连接标识 |
| db_service_name | varchar(30) | Y |  | 数据库服务名 |
| db_user | varchar(30) | Y |  | 登陆用户 |
| pwd | varchar(40) | Y |  | 登陆密码 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 789. dimple.ts_dept_managed_rights　(2 字段)
> 表含义：部门管理权限表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| dept_code | varchar(10) | N | √ | 部门代码 |
| right_id | float8 | N | √ | 权限ID |

---

## 790. dimple.ts_dept_rights　(2 字段)
> 表含义：部门操作权限　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| dept_code | varchar(10) | N | √ | 部门代码 |
| right_id | float8 | N | √ | 权限ID |

---

## 791. dimple.ts_depts　(12 字段)
> 表含义：部门表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| dept_code | varchar(10) | N | √ | 部门代码 |
| dept_name | varchar(80) | Y |  | 部门名称 |
| tel | varchar(40) | Y |  | 电话 |
| fax | varchar(40) | Y |  | 传真 |
| dept_code_up | varchar(10) | Y |  | 上级部门代码 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| note | varchar(254) | Y |  | 备注 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 792. dimple.ts_depts_check　(15 字段)
> 表含义：部门复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| dept_code | varchar(10) | N |  | 部门代码 |
| dept_name | varchar(80) | Y |  | 部门名称 |
| tel | varchar(40) | Y |  | 电话 |
| fax | varchar(40) | Y |  | 传真 |
| dept_code_up | varchar(10) | Y |  | 上级部门代码 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| note | varchar(254) | Y |  | 备注 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 793. dimple.ts_func_right_relation　(2 字段)
> 表含义：功能权限对照表　|　估算行数：**949**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| func_id | float8 | N | √ | 功能点ID |
| right_id | float8 | N | √ | 权限ID |

---

## 794. dimple.ts_functions　(5 字段)
> 表含义：功能表:功能点描述表　|　估算行数：**949**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| func_id | float8 | N | √ | 功能点ID |
| func_type | float8 | N |  | 功能类型 |
| name | varchar(80) | Y |  | 名称 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的122 |
| note | varchar(254) | Y |  | 备注 |

---

## 795. dimple.ts_grant_code　(10 字段)
> 表含义：授权码表　|　估算行数：**62**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| security_id | varchar(30) | N | √ | 安全标识号:用户ID或者席位ID |
| user_type | bpchar(1) | N | √ | 用户类型:见tp_public_dict的213 |
| grant_pwd | varchar(200) | Y |  | 授权码 |
| grant_type | varchar(2) | Y |  | 授权码类型:见tp_public_code的187 |
| grant_sdate | varchar(8) | Y |  | 授权码生效开始日期 |
| grant_edate | varchar(8) | Y |  | 授权码生效结束日期 |
| grant_used | float8 | Y |  | 授权码已经使用次数 |
| grant_cnt | float8 | Y |  | 授权码最多使用次数 |
| op_user_id | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 796. dimple.ts_hint　(6 字段)
> 表含义：业务提示表:作废　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_id | varchar(80) | N | √ | 提示代码 |
| hint_name | varchar(80) | N |  | 提示名称 |
| hint_type | varchar(2) | N |  | 提示类型:见tp_public_dict的079 |
| urgency_degree | bpchar(1) | N |  | 紧急程度:见tp_public_dict的080 |
| if_return | bpchar(1) | N |  | 是否产生回执 |
| gen_style | varchar(2) | N |  | 接收者生成方式:见tp_public_dict的172 |

---

## 797. dimple.ts_hint_list　(14 字段)
> 表含义：业务提示列表　|　估算行数：**132**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_no | float8 | N | √ | 提示流水号 |
| hint_id | varchar(80) | Y |  | 提示代码 |
| hint_type | varchar(2) | N |  | 提示类型:见tp_public_dict的079 |
| title | varchar(80) | Y |  | 标题 |
| content | varchar(1000) | Y |  | 内容 |
| biz_id | varchar(80) | Y |  | 业务标识 |
| come_from | varchar(2) | Y |  | 消息源:见tp_public_dict的170 |
| gen_date | varchar(8) | Y |  | 产生日期 |
| gen_time | varchar(8) | Y |  | 产生时间 |
| if_return | bpchar(1) | Y |  | 是否产生回执 |
| urgency_degree | bpchar(1) | Y |  | 紧急程度:见tp_public_dict的080 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的171 |
| begin_date | varchar(8) | Y |  | 有效期起始日期 |
| end_date | varchar(8) | Y |  | 有效期终止日期 |

---

## 798. dimple.ts_hint_menu　(2 字段)
> 表含义：提示与菜单对照表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_id | varchar(80) | N | √ | 提示代码 |
| menu_id | float8 | N | √ | 菜单ID |

---

## 799. dimple.ts_hint_recv　(4 字段)
> 表含义：业务提示接收者列表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_id | varchar(80) | Y |  | 提示代码 |
| recv_dept | varchar(10) | Y |  | 接收部门 |
| recv_user | varchar(30) | Y |  | 接收者 |
| gen_style | varchar(2) | N |  | 接收者生成方式:见tp_public_dict的172 |

---

## 800. dimple.ts_login_mode　(3 字段)
> 表含义：登录模式表　|　估算行数：**61**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| security_id | varchar(30) | N | √ | 安全标识号:用户ID或者席位ID |
| user_type | bpchar(1) | N | √ | 用户类型:见tp_public_dict的213 |
| login_mode | varchar(2) | Y |  | 登录模式:见tp_public_dict的197 |

---

## 801. dimple.ts_login_users　(10 字段)
> 表含义：登录用户与系统用户关系管理表　|　估算行数：**15**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| login_user_id | varchar(32) | N | √ | 登录用户ID |
| login_user_name | varchar(64) | Y |  | 登录用户名 |
| sys_user_id | varchar(32) | Y |  | 绑定的系统用户ID（关联TS_USERS.USER_ID） |
| login_password | varchar(128) | Y |  | 登录密码（密文存储） |
| login_status | varchar(2) | Y |  | 登录用户状态：0-正常、1-冻结、2-注销 |
| last_login_date | varchar(8) | Y |  | 最后登录日期（YYYYMMDD） |
| last_login_time | varchar(8) | Y |  | 最后登录时间（HHMMSS） |
| operator | varchar(32) | Y |  | 操作人员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 802. dimple.ts_member_security_ips　(3 字段)
> 表含义：会服用户IP管理表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| security_id | varchar(30) | N |  | 会服ID，与TS_MEMBER_USERS中的USER_ID对应 |
| buser_type | bpchar(1) | N |  | 保留字段 |
| ip_addr | varchar(30) | N |  | 会服用户被限制的IP地址，可有多个；255255255255表示没有限制 |

---

## 803. dimple.ts_member_users　(25 字段)
> 表含义：会员服务系统用户表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| user_name | varchar(40) | Y |  | 用户名 |
| pwd | varchar(40) | Y |  | 用户口令 |
| gender | bpchar(1) | Y |  | 性别:见tp_public_dict的028 |
| member_id | varchar(8) | Y |  | 投资者号 |
| member_abbr | varchar(80) | Y |  | 投资者简称 |
| user_desc | varchar(80) | Y |  | 用户描述 |
| email | varchar(60) | Y |  | 邮箱 |
| tel1 | varchar(40) | Y |  | 联系电话1 |
| tel2 | varchar(40) | Y |  | 联系电话2 |
| zip | varchar(6) | Y |  | 邮编 |
| addr | varchar(120) | Y |  | 联系地址 |
| status | bpchar(1) | Y |  | 用户状态:见tp_public_dict的106 |
| note | varchar(254) | Y |  | 备注 |
| last_login_date | varchar(8) | Y |  | 最新登陆日期 |
| last_login_time | varchar(8) | Y |  | 最新登陆时间 |
| last_fail_login_date | varchar(8) | Y |  | 最新失败登陆日期 |
| last_fail_login_time | varchar(8) | Y |  | 最新失败登陆时间 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| last_modify_date | varchar(8) | Y |  | 修改日期 |
| last_modify_time | varchar(8) | Y |  | 修改时间 |
| last_pwd_modify_date | varchar(8) | Y |  | 口令修改日期 |
| pwd_err_count | float8 | Y |  | 口令错误次数 |

---

## 804. dimple.ts_menu_assist_relation　(4 字段)
> 表含义：菜单辅助功能点关系表:存储菜单与辅助功能点的对应关系信息　|　估算行数：**218**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| menu_id | float8 | N | √ | 菜单ID |
| func_id | float8 | N | √ | 功能点ID |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的122 |
| note | varchar(254) | Y |  | 备注 |

---

## 805. dimple.ts_menu_func_relation　(3 字段)
> 表含义：菜单功能对照表　|　估算行数：**969**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| menu_id | float8 | N | √ | 菜单ID |
| func_id | float8 | N | √ | 功能点ID |
| rela_type | bpchar(1) | Y |  | 功能点类型:见tp_public_dict的121 |

---

## 806. dimple.ts_menus　(13 字段)
> 表含义：菜单表　|　估算行数：**428**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| menu_id | float8 | N | √ | 菜单ID |
| menu_type | float8 | N |  | 菜单类型 |
| name | varchar(80) | Y |  | 名称 |
| spell | varchar(80) | Y |  | 菜单名拼音简写 |
| menu_id_up | float8 | Y |  | 上级菜单ID |
| is_parent | bpchar(1) | Y |  | 是否上级菜单:见tp_public_dict的027 |
| is_operate | bpchar(1) | Y |  | 是否操作级菜单:见tp_public_dict的027 |
| interface_id | float8 | Y |  | 界面ID |
| add_id | float8 | Y |  | 附加ID |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的122 |
| note | varchar(254) | Y |  | 备注 |
| pos | float8 | Y |  | 同级菜单顺序 |
| exch_code | varchar(20) | Y |  | 交易所号:见interface.tp_public_dict的235 |

---

## 807. dimple.ts_notice_list　(13 字段)
> 表含义：业务通知列表　|　估算行数：**42,361**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| notice_seq | float8 | N | √ | 业务通知流水 |
| title | varchar(80) | Y |  | 标题 |
| content | varchar(254) | Y |  | 内容 |
| come_from | varchar(2) | Y |  | 消息源:见tp_public_dict的170 |
| sender | varchar(30) | Y |  | 发送者 |
| send_limit | varchar(2) | Y |  | 发送限制:见tp_public_dict的173 |
| if_return | bpchar(1) | Y |  | 是否产生回执:默认为是 |
| urgency_degree | bpchar(1) | Y |  | 紧急程度:见tp_public_dict的080 |
| begin_date | varchar(8) | Y |  | 有效期起始日期 |
| end_date | varchar(8) | Y |  | 有效期终止日期 |
| gen_date | varchar(8) | Y |  | 产生日期 |
| gen_time | varchar(8) | Y |  | 产生时间 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的171 |

---

## 808. dimple.ts_notice_recv　(4 字段)
> 表含义：业务通知接收者列表　|　估算行数：**42,361**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| notice_seq | float8 | N |  | 业务通知流水 |
| recv_dept | varchar(10) | Y |  | 接收部门 |
| recv_user | varchar(30) | Y |  | 接收者 |
| gen_date | varchar(8) | Y |  | 产生日期 |

---

## 809. dimple.ts_other_functions　(10 字段)
> 表含义：其他功能点表:存储除主功能点外的其它功能点信息　|　估算行数：**180**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| func_id | float8 | N | √ | 功能点ID |
| func_name | varchar(254) | N |  | 功能点名称 |
| note | varchar(254) | Y |  | 备注 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的122 |
| if_out_right | bpchar(1) | Y |  | 是否权限外 |
| if_native | bpchar(1) | Y |  | 是否SBU本地调用 |
| if_binary | bpchar(1) | Y |  | 是否二进制 |
| if_out_audit | bpchar(1) | Y |  | 是否审计外 |
| if_out_session | bpchar(1) | Y |  | 是否会话外 |
| if_assistant | bpchar(1) | Y |  | 是否辅助 |

---

## 810. dimple.ts_other_functions_cwd　(10 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| func_id | float8 | N |  |  |
| func_name | varchar(254) | N |  |  |
| note | varchar(254) | Y |  |  |
| status | bpchar(1) | Y |  |  |
| if_out_right | bpchar(1) | Y |  |  |
| if_native | bpchar(1) | Y |  |  |
| if_binary | bpchar(1) | Y |  |  |
| if_out_audit | bpchar(1) | Y |  |  |
| if_out_session | bpchar(1) | Y |  |  |
| if_assistant | bpchar(1) | Y |  |  |

---

## 811. dimple.ts_rights　(5 字段)
> 表含义：权限表　|　估算行数：**949**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| right_id | float8 | N | √ | 权限ID |
| right_type | float8 | N |  | 权限类型 |
| name | varchar(80) | Y |  | 名称 |
| keywords | varchar(80) | Y |  | 关键字 |
| note | varchar(254) | Y |  | 备注 |

---

## 812. dimple.ts_rights_cwd　(5 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| right_id | float8 | N | √ |  |
| right_type | float8 | N |  |  |
| name | varchar(80) | Y |  |  |
| keywords | varchar(80) | Y |  |  |
| note | varchar(254) | Y |  |  |

---

## 813. dimple.ts_role_managed_rights　(2 字段)
> 表含义：角色管理权限表　|　估算行数：**2,564**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| role_id | float8 | N | √ | 角色ID |
| right_id | float8 | N | √ | 权限ID |

---

## 814. dimple.ts_role_rights　(2 字段)
> 表含义：角色权限表　|　估算行数：**2,564**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| role_id | float8 | N | √ | 角色ID |
| right_id | float8 | N | √ | 权限ID |

---

## 815. dimple.ts_roles　(10 字段)
> 表含义：角色表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| role_id | float8 | N | √ | 角色ID |
| name | varchar(80) | Y |  | 名称 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| note | varchar(254) | Y |  | 备注 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 816. dimple.ts_roles_check　(13 字段)
> 表含义：角色复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| role_id | float8 | Y |  | 角色ID |
| name | varchar(80) | Y |  | 名称 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| note | varchar(254) | Y |  | 备注 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 817. dimple.ts_security_ips　(9 字段)
> 表含义：安全标识表:允许使用的IP地址，针对用户，席位，控制平台用户和应用标识.安全标识号的数据包括用户ID，席位号和应用程序标识号，需要保证标识的唯一性，这里最好能够通过在命名规则上进行控制，保证标识之间不会出现重复的现象。　|　估算行数：**25**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| security_id | varchar(30) | N | √ | 安全标识号 |
| user_type | bpchar(1) | N | √ | 用户类型:见tp_public_dict的213 |
| ip_addr | varchar(30) | N | √ | IP地址 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 818. dimple.ts_security_ips_check　(13 字段)
> 表含义：安全标识复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| security_id | varchar(30) | N |  | 安全标识号 |
| user_type | bpchar(1) | N |  | 用户类型:见tp_public_dict的213 |
| ip_addr | varchar(30) | N |  | IP地址 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 819. dimple.ts_sign_log　(11 字段)
> 表含义：签名认证日志表:记录签名操作的日志信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| txdate | varchar(8) | N | √ | 日期 |
| txtime | varchar(8) | Y |  | 时间 |
| serial | float8 | N | √ | 序号 |
| security_id | varchar(30) | N |  | 安全标识号 |
| user_type | bpchar(1) | N | √ | 用户类型:见tp_public_dict的109 |
| op_type | bpchar(1) | N |  | 操作类型:见tp_public_dict的111 |
| sign | bytea | Y |  | 签名 |
| signlen | float8 | Y |  | 签名长度 |
| sign_desc | bytea | Y |  | 签名证书 |
| status | bpchar(1) | Y |  | 状态:参见tp_public_dict的112 |
| note | varchar(254) | Y |  | 备注 |

---

## 820. dimple.ts_sync_user_info　(4 字段)
> 表含义：用户同步信息表　|　估算行数：**10,738**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| group_no | numeric(12,0) | N |  | 同步组号 |
| user_id | varchar(30) | N |  | 用户ID |
| info_type | varchar(2) | N |  | 信息类型:见tp_public_code的195 |
| deal_flag | bpchar(1) | N |  | 处理标志 |

---

## 821. dimple.ts_sys_audit　(19 字段)
> 表含义：系统审计表　|　估算行数：**146,683**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 流水号 |
| dept_code | varchar(10) | N |  | 部门代码 |
| app_no | varchar(30) | N |  | 应用标识 |
| app_version | varchar(30) | N |  | 应用版本号码 |
| user_id | varchar(30) | N |  | 用户ID |
| ip_addr | varchar(30) | N |  | IP地址 |
| action | varchar(20) | Y |  | 操作 |
| content1 | varchar(4000) | N |  | 操作内容1 |
| content2 | varchar(4000) | Y |  | 操作内容2 |
| result | varchar(10) | N |  | 操作结果:填写错误代码 |
| result_str | varchar(511) | N |  | 操作结果串 |
| start_date | varchar(8) | N |  | 执行开始日期 |
| start_time | varchar(8) | N |  | 执行开始时间 |
| end_date | varchar(8) | N |  | 执行结束日期 |
| end_time | varchar(8) | N |  | 执行结束时间 |
| note | varchar(255) | N |  | 附加信息 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 822. dimple.ts_trader_cert　(5 字段)
> 表含义：交易员交易所证书表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 交易员号 |
| exch_code | varchar(2) | N |  | 交易所号 |
| cert_id | varchar(10) | N | √ | 交易所证书号 |
| op_user_id | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 823. dimple.ts_trader_groups　(12 字段)
> 表含义：交易员分组表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| group_code | varchar(8) | N | √ | 交易组代码 |
| group_name | varchar(40) | N |  | 交易组名称 |
| fuser_id | varchar(30) | N |  | 交易组组长 |
| user_id | varchar(255) | Y |  | 组员 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 824. dimple.ts_trader_groups_check　(16 字段)
> 表含义：交易员分组复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| group_code | varchar(8) | N |  | 交易组代码 |
| group_name | varchar(40) | N |  | 交易组名称 |
| fuser_id | varchar(30) | N |  | 交易组组长 |
| user_id | varchar(255) | Y |  | 组员 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 825. dimple.ts_trader_tid　(2 字段)
> 表含义：席位功能类型指令表　|　估算行数：**61**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| func_type | varchar(2) | N | √ | 席位功能类型:见t_public_code的018 |
| tid | varchar(20) | N | √ | 指令TID |

---

## 826. dimple.ts_user_accreditcode　(8 字段)
> 表含义：用户授权码表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| accreditcode | varchar(21) | Y |  | 授权码 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| limittype | bpchar(1) | Y |  | 限值类型:见tp_public_dict的139 |
| usecount | float8 | Y |  | 使用次数 |
| valid_date | float8 | Y |  | 有效天数 |
| valid_time | float8 | Y |  | 有效时间 |

---

## 827. dimple.ts_user_fbd_rights　(2 字段)
> 表含义：用户禁止权限表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| right_id | float8 | N | √ | 权限ID |

---

## 828. dimple.ts_user_hint　(6 字段)
> 表含义：用户提示清单表　|　估算行数：**66,312**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| hint_no | float8 | N | √ | 提示流水号 |
| recv_user | varchar(30) | N | √ | 接收者 |
| send_date | varchar(8) | Y |  | 发送日期 |
| return_date | varchar(8) | Y |  | 回执日期 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的171 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 829. dimple.ts_user_login_info　(13 字段)
> 表含义：用户会话表:用户的登录信息，也就是用户的会话　|　估算行数：**341**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| session_id | varchar(30) | N | √ | 会话ID |
| trade_session_id | varchar(30) | Y |  | 交易端会话ID |
| randomstring | varchar(21) | Y |  | 验证随机串 |
| symmetrickey | varchar(21) | Y |  | 对称密钥 |
| create_date | varchar(8) | N |  | 创建日期 |
| create_time | varchar(8) | N |  | 创建时间 |
| refresh_date | varchar(8) | Y |  | 刷新日期 |
| refresh_time | varchar(8) | Y |  | 刷新时间 |
| valid_date | float8 | Y |  | 有效天数 |
| valid_time | float8 | Y |  | 有效时间 |
| matrix | varchar(255) | Y |  | 用户联结串 |
| ip_addr | varchar(30) | Y |  | 用户联结地址 |

---

## 830. dimple.ts_user_managed_fbd_rights　(2 字段)
> 表含义：用户禁止管理权限表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| right_id | float8 | N | √ | 权限ID |

---

## 831. dimple.ts_user_managed_rights　(2 字段)
> 表含义：用户管理权限表　|　估算行数：**1,267**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| right_id | float8 | N | √ | 权限ID |

---

## 832. dimple.ts_user_managed_roles　(2 字段)
> 表含义：用户管理角色表　|　估算行数：**72**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| role_id | float8 | N | √ | 角色ID |

---

## 833. dimple.ts_user_managed_users　(2 字段)
> 表含义：用户管理用户表　|　估算行数：**1,522**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| managed_user_id | varchar(30) | N | √ | 被管理用户ID |

---

## 834. dimple.ts_user_rights　(2 字段)
> 表含义：用户权限表　|　估算行数：**3,939**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| right_id | float8 | N | √ | 权限ID |

---

## 835. dimple.ts_user_roles　(2 字段)
> 表含义：用户角色表　|　估算行数：**76**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| role_id | float8 | N | √ | 角色ID |

---

## 836. dimple.ts_user_tid　(2 字段)
> 表含义：用户指令表:废表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| tid | varchar(20) | N | √ | 指令TID |

---

## 837. dimple.ts_user_trustee　(4 字段)
> 表含义：用户托管表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 用户ID |
| trustee_user_id | varchar(30) | Y |  | 托管用户ID |
| begin_date | varchar(8) | N | √ | 起始日期 |
| end_date | varchar(8) | N | √ | 结束日期 |

---

## 838. dimple.ts_users　(41 字段)
> 表含义：用户表　|　估算行数：**53**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 操作员号 |
| user_name | varchar(60) | Y |  | 操作员名称 |
| pwd | varchar(200) | N |  | 操作员口令 |
| invest_id | varchar(8) | Y |  | 投资者号 |
| fuser_id | varchar(30) | Y |  | 上级操作员号 |
| user_type | varchar(2) | Y |  | 操作员类型:见tp_public_dict的213 |
| user_note | varchar(254) | Y |  | 操作员描述 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| managed_flag | bpchar(1) | N |  | 是否管理用户:见tp_public_dict的027 |
| pwd_err_count | float8 | Y |  | 口令错误次数 |
| status | bpchar(1) | N |  | 用户状态:见tp_public_dict的106 |
| func_type | varchar(2) | Y |  | 席位功能类型:见t_public_code的018 |
| pos_type | varchar(2) | Y |  | 席位位置类型:见t_public_code的020 |
| if_direct | bpchar(1) | Y |  | 是否直接接入席位 |
| recv_range | varchar(2) | Y |  | 接受回报范围:见t_public_code的102 |
| install_addr | varchar(120) | Y |  | 席位安装地址 |
| login_addr | varchar(30) | Y |  | 用户登陆地址 |
| login_max_num | float8 | Y |  | 用户登陆次数 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| modify_oper | varchar(30) | Y |  | 修改者 |
| last_modify_date | varchar(8) | Y |  | 修改日期 |
| last_modify_time | varchar(8) | Y |  | 修改时间 |
| last_login_date | varchar(8) | Y |  | 最新登陆日期 |
| last_login_time | varchar(8) | Y |  | 最新登陆时间 |
| last_exit_date | varchar(8) | Y |  | 最后退出日期 |
| last_exit_time | varchar(8) | Y |  | 最后退出时间 |
| last_pwd_modify_date | varchar(8) | Y |  | 口令修改日期 |
| online_flag | bpchar(1) | Y |  | 是否在线:见tp_public_dict的027 |
| addr_limit_flag | bpchar(1) | Y |  | 站点限制标志 |
| expired_type | bpchar(1) | Y |  | 有效类型 |
| expired_date | varchar(8) | Y |  | 有效期限 |
| ca_style | varchar(2) | Y |  | 认证方法:见tp_public_dict的152 |
| ip_addr | varchar(30) | Y |  | 位置 |
| last_fail_login_date | varchar(8) | Y |  | 最新失败登陆日期 |
| last_fail_login_time | varchar(8) | Y |  | 最新失败登陆时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |
| node_no | varchar(5) | Y |  | 推送节点号 |

---

## 839. dimple.ts_users_check　(44 字段)
> 表含义：用户复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| user_id | varchar(30) | N |  | 操作员号 |
| user_name | varchar(40) | Y |  | 操作员名称 |
| pwd | varchar(40) | N |  | 操作员口令 |
| invest_id | varchar(8) | Y |  | 投资者号 |
| fuser_id | varchar(30) | Y |  | 上级操作员号 |
| user_type | varchar(2) | Y |  | 操作员类型:见tp_public_dict的213 |
| user_note | varchar(254) | Y |  | 操作员描述 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| managed_flag | bpchar(1) | Y |  | 是否管理用户:见tp_public_dict的027 |
| pwd_err_count | float8 | Y |  | 口令错误次数 |
| status | bpchar(1) | N |  | 用户状态:见tp_public_dict的106 |
| func_type | varchar(2) | Y |  | 席位功能类型:见t_public_code的018 |
| pos_type | varchar(2) | Y |  | 席位位置类型:见t_public_code的020 |
| if_direct | bpchar(1) | Y |  | 是否直接接入席位 |
| recv_range | varchar(2) | Y |  | 接受回报范围:见t_public_code的102 |
| install_addr | varchar(120) | Y |  | 席位安装地址 |
| login_addr | varchar(30) | Y |  | 用户登陆地址 |
| login_max_num | float8 | Y |  | 用户登陆次数 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| modify_oper | varchar(30) | Y |  | 修改者 |
| last_modify_date | varchar(8) | Y |  | 修改日期 |
| last_modify_time | varchar(8) | Y |  | 修改时间 |
| last_login_date | varchar(8) | Y |  | 最新登陆日期 |
| last_login_time | varchar(8) | Y |  | 最新登陆时间 |
| last_exit_date | varchar(8) | Y |  | 最后退出日期 |
| last_exit_time | varchar(8) | Y |  | 最后退出时间 |
| last_pwd_modify_date | varchar(8) | Y |  | 口令修改日期 |
| online_flag | bpchar(1) | Y |  | 是否在线:见tp_public_dict的027 |
| addr_limit_flag | bpchar(1) | Y |  | 站点限制标志 |
| expired_type | bpchar(1) | Y |  | 有效类型 |
| expired_date | varchar(8) | Y |  | 有效期限 |
| ca_style | varchar(2) | Y |  | 认证方法:见tp_public_dict的152 |
| ip_addr | varchar(30) | Y |  | 位置 |
| last_fail_login_date | varchar(8) | Y |  | 最新失败登陆日期 |
| last_fail_login_time | varchar(8) | Y |  | 最新失败登陆时间 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 840. dimple.ts_users_his_pwd　(7 字段)
> 表含义：用户历史密码表　|　估算行数：**141**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 操作员号 |
| seq_no | float8 | N | √ | 序号 |
| pwd | varchar(200) | N |  | 密码 |
| pwd_type | varchar(2) | N |  | 密码类型：见t_public_code的425 |
| creator | varchar(30) | Y |  | 创建者ID |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |

---

## 841. dimple.ts_users_um_pal　(5 字段)
> 表含义：操作员与外部账户对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N |  | 操作员号 |
| um_id | varchar(300) | N | √ | 外部账户 |
| op_oper | varchar(30) | Y |  | 操作员 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 842. dimple.tt_arbi_client_posi　(9 字段)
> 表含义：场上客户套利持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| arbi_contract_id | varchar(80) | N | √ | 套利合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见t_public_code的004 |
| buy_open_qty | numeric(12,0) | Y |  | 今日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 今日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 今日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 今日卖平仓量 |

---

## 843. dimple.tt_arbi_rule　(10 字段)
> 表含义：套利策略规则表:定义了各腿的各种关系。　|　估算行数：**21**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| arbi_code | varchar(10) | N | √ | 策略代码 |
| leg_no | float8 | N | √ | 腿号 |
| trade_type | varchar(2) | N |  | 各腿交易类型:见tp_public_dict的001 |
| variety_rel | float8 | N |  | 品种关系 |
| month_rel | varchar(10) | N |  | 月份关系:1,2,3,9. 其中3代表小于等于；9代表任意月 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| cp_flag | bpchar(1) | Y |  | 看涨看跌标志:见tp_public_dict的033 |
| strike_price_rel | varchar(10) | Y |  | 执行价格关系 |
| ratio | float8 | Y |  | 数量比例 |
| calc_way | float8 | Y |  | 计算方式:填写-1,+1 |

---

## 844. dimple.tt_arbi_variety　(6 字段)
> 表含义：套利策略表:期货的套利和期权的套利均在此表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| arbi_code | varchar(10) | N | √ | 策略代码 |
| arbi_eabbr | varchar(40) | Y |  | 策略英文简称 |
| arbi_ename | varchar(40) | N |  | 策略英文名称 |
| arbi_name | varchar(40) | Y |  | 策略中文名称 |
| arbi_type | varchar(2) | N |  | 套利类别:见tp_public_dict的060 |
| add_type | varchar(2) | N |  | 套利合约增加方式:见tp_public_dict的034 |

---

## 845. dimple.tt_back_log　(4 字段)
> 表含义：留痕日志表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 日期 |
| offset_num | numeric(12,0) | N | √ | 强平次数 |
| op_time | varchar(8) | Y |  | 时间 |
| user_id | varchar(30) | N |  | 操作员 |

---

## 846. dimple.tt_bpt_match　(14 字段)
> 表含义：定价实时成交数据　|　估算行数：**56**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exchcode | varchar(6) | N | √ | 交易所代码 |
| memberid | varchar(8) | Y |  | 席位代码	  |
| clientid | varchar(16) | Y |  | 客户代码	  |
| traderno | varchar(16) | Y |  | 交易员	  |
| contractid | varchar(20) | Y |  | 合约代码	  |
| sessionid | varchar(10) | Y |  | 场次编号	  |
| bsflag | bpchar(1) | N | √ | 买卖方向	  |
| matchmode | bpchar(1) | Y |  | 成交模式	  |
| qty | numeric(12,0) | Y |  | 成交手数	  |
| price | numeric(20,8) | Y |  | 成交价格	  |
| margin | numeric(20,8) | Y |  | 保证金金额 |
| matchtime | varchar(12) | Y |  | 成交时间	  |
| matchdate | varchar(10) | Y |  | 成交日期	  |
| matchno | varchar(20) | N | √ | 成交编号	  |

---

## 847. dimple.tt_bpt_order　(22 字段)
> 表含义：定价实时委托数据　|　估算行数：**386**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| tradedate | varchar(10) | N | √ | 交易日期 |
| exchcode | varchar(6) | N | √ | 交易所代码 |
| memberid | varchar(8) | Y |  | 会员号 |
| clientid | varchar(16) | Y |  | 客户号 |
| traderno | varchar(16) | Y |  | 交易员号 |
| contractid | varchar(20) | Y |  | 合约代码 |
| entrytype | bpchar(1) | Y |  | 报单类型 |
| entryphase | bpchar(1) | Y |  | 申报阶段 |
| canceltype | bpchar(1) | Y |  | 撤单类型 |
| bsflag | bpchar(1) | Y |  | 买卖方向 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 申报手数 |
| sessionid | varchar(10) | Y |  | 场次编号 |
| roundid | varchar(10) | Y |  | 轮次编号 |
| localorderno | varchar(20) | Y |  | 本地报单号 |
| orderno | varchar(20) | N | √ | 系统报单号 |
| applytime | varchar(12) | Y |  | 报入时间 |
| status | bpchar(1) | Y |  | 状态 |
| frozencash | numeric(20,8) | Y |  | 冻结保证金 |
| purposecode | varchar(3) | Y |  | 交易目的 |
| strategyno | varchar(4) | Y |  | 投资策略编号 |
| subaccount | varchar(12) | Y |  | 子账户 |

---

## 848. dimple.tt_btp_quote　(4 字段)
> 表含义：定价定盘价行情同步表　|　估算行数：**3,351**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约 |
| tsessionid | varchar(10) | N | √ | 场次 |
| price | numeric(20,8) | Y |  | 定盘价 |

---

## 849. dimple.tt_bulletin　(12 字段)
> 表含义：公告表:由控制台界面发出公告，发布对象是席位，为空则全部。　|　估算行数：**130**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| no | float8 | N | √ | 序号 |
| prom_date | varchar(8) | N | √ | 发布日期 |
| prom_time | varchar(8) | Y |  | 发布时间 |
| dept_code | varchar(10) | Y |  | 部门代码 |
| title | varchar(80) | Y |  | 标题 |
| content | varchar(2000) | Y |  | 内容 |
| prom_object | varchar(80) | Y |  | 发布对象 |
| urgency_degree | bpchar(1) | Y |  | 紧急程度 |
| type | varchar(2) | Y |  | 类型 |
| url_link | varchar(254) | Y |  | 此消息的WEB联结 |
| user_id | varchar(30) | Y |  | 操作员代码 |
| exch_code | varchar(6) | N | √ | 交易所代码 |

---

## 850. dimple.tt_cfets_match　(36 字段)
> 表含义：外汇交易表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exec_id | varchar(50) | Y |  | CFETS序号 |
| market_indicator | varchar(3) | Y |  | 交易类型 |
| fn_flag | varchar(3) | Y |  | 远近端：见tp_public_dict的250 |
| trade_instrument | varchar(3) | Y |  | 交易方式 |
| trade_method | varchar(3) | Y |  | 交易模式 |
| trade_date | varchar(8) | Y |  | 交易日期 |
| trade_time | varchar(8) | Y |  | 成交时间 |
| net_gross_ind | varchar(3) | Y |  | 清算方式 |
| taker_party_id | varchar(21) | Y |  | 发起方唯一编号 |
| maker_party_id | varchar(21) | Y |  | 做市方唯一编号 |
| taker_org_id | varchar(100) | Y |  | 发起方组织机构名称 |
| maker_org_id | varchar(100) | Y |  | 做市方组织机构名称 |
| taker_dealer_id | varchar(20) | Y |  | 发起方交易员 |
| maker_dealer_id | varchar(20) | Y |  | 做市方交易员 |
| taker_dealer | varchar(20) | Y |  | 发起方会员简称 |
| maker_dealer | varchar(20) | Y |  | 做市方会员简称 |
| cash_account | varchar(30) | Y |  | 发生货币资金清算账户名称 |
| cont_cash_account | varchar(30) | Y |  | 对应货币资金清算账户名称 |
| side | varchar(3) | Y |  | 本方买卖方向 |
| settl_type | varchar(3) | Y |  | 远端交易期限 |
| l_currency | varchar(3) | Y |  | 第一货币 |
| r_currency | varchar(3) | Y |  | 第二货币 |
| cal_amount | varchar(3) | Y |  | 输入货币 |
| symbol | varchar(8) | Y |  | 交易货币对 |
| last_qty | varchar(18) | Y |  | 第一货币交易量 |
| risk_last_qty | varchar(18) | Y |  | 折美元交易量 |
| calculated_ccy_last_qty | varchar(18) | Y |  | 第二货币交易量 |
| settl_date | varchar(8) | Y |  | 起息日 |
| spot_date | varchar(8) | Y |  | 即期起息日 |
| last_spot_rate | varchar(15) | Y |  | 即期价格 |
| last_forward_points | varchar(8) | Y |  | 升水点 |
| last_px | varchar(15) | Y |  | 交易价格 |
| cfets_cnfm_indicator | varchar(3) | Y |  | 交易确认标识 |
| deal_trans_type | varchar(3) | Y |  | 成交单状态 |
| is_op_spot_indic | varchar(3) | Y |  | 是否为行权的EXOP交易 |
| is_ex_delta_indic | varchar(3) | Y |  | 是否为ExchangeDelta交易 |

---

## 851. dimple.tt_cfets_quot　(11 字段)
> 表含义：外汇交易中心行情表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| product_type | varchar(20) | Y |  | 产品类别 |
| data_type | varchar(3) | Y |  | 数据来源 |
| ccypair_name | varchar(8) | Y |  | 货币对名称 |
| feed_name | varchar(20) | Y |  | 价源名称 |
| period_code | varchar(6) | Y |  | 期限名称 |
| bid | varchar(16) | Y |  | 买价(即期汇率/升贴水) |
| offer | varchar(16) | Y |  | 卖价(即期汇率/升贴水) |
| mid | varchar(16) | Y |  | 中间价(即期汇率/升贴水) |
| quote_unit | varchar(20) | Y |  | 报价单位 |
| update_date | varchar(8) | Y |  | 生成日期 |
| update_time | varchar(8) | Y |  | 生成时间 |

---

## 852. dimple.tt_client　(7 字段)
> 表含义：客户表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| client_id | varchar(16) | N | √ | 客户号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| invest_id | varchar(8) | N |  | 投资者号 |
| status | bpchar(1) | N |  | 状态:见tp_public_dict的012 |
| open_date | varchar(8) | Y |  | 开户日期 |
| logout_date | varchar(8) | Y |  | 注销日期 |
| op_date | varchar(8) | Y |  | 操作日期:方便数据同步 |

---

## 853. dimple.tt_client_member　(49 字段)
> 表含义：交易编码表　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| grant_name | varchar(40) | Y |  | 开户授权人姓名(单位) |
| grant_cert_type | varchar(2) | Y |  | 开户授权人证件类型(单位):见tp_public_dict的025 |
| grant_cert_no | varchar(40) | Y |  | 开户授权人证件号码(单位) |
| grant_zip | varchar(6) | Y |  | 开户授权人邮政编码(单位) |
| grant_region_code | varchar(6) | Y |  | 开户授权人地区代码(单位) |
| grant_region_name | varchar(80) | Y |  | 开户授权人地区名称(单位) |
| grant_addr | varchar(120) | Y |  | 开户授权人地址(单位) |
| grant_tel | varchar(40) | Y |  | 开户授权人联系电话(单位) |
| cmd_name | varchar(40) | Y |  | 指定下单人姓名 |
| cmd_cert_type | varchar(2) | Y |  | 指定下单人证件类型:见tp_public_dict的025 |
| cmd_cert_no | varchar(40) | Y |  | 指定下单人证件号码 |
| cmd_zip | varchar(6) | Y |  | 指定下单人邮政编码 |
| cmd_region_code | varchar(6) | Y |  | 指定下单人地区代码 |
| cmd_region_name | varchar(80) | Y |  | 指定下单人地区名称 |
| cmd_addr | varchar(120) | Y |  | 指定下单人地址 |
| cmd_tel | varchar(40) | Y |  | 指定下单人联系电话 |
| trans_name | varchar(40) | Y |  | 资金调拨人姓名 |
| trans_cert_type | varchar(2) | Y |  | 资金调拨人证件类型:见tp_public_dict的025 |
| trans_cert_no | varchar(40) | Y |  | 资金调拨人证件号码 |
| trans_zip | varchar(6) | Y |  | 资金调拨人邮政编码 |
| trans_region_code | varchar(6) | Y |  | 资金调拨人地区代码 |
| trans_region_name | varchar(80) | Y |  | 资金调拨人地区名称 |
| trans_addr | varchar(120) | Y |  | 资金调拨人地址 |
| trans_tel | varchar(40) | Y |  | 资金调拨人联系电话 |
| confirm_name | varchar(40) | Y |  | 结算单确认人姓名 |
| confirm_cert_type | varchar(2) | Y |  | 资金调拨人证件类型:见tp_public_dict的025 |
| confirm_cert_no | varchar(40) | Y |  | 结算单确认人证件号码 |
| confirm_zip | varchar(6) | Y |  | 结算单确认人邮政编码 |
| confirm_region_code | varchar(6) | Y |  | 结算单确认人地区代码 |
| confirm_region_name | varchar(80) | Y |  | 结算单确认人地区名称 |
| confirm_addr | varchar(120) | Y |  | 结算单确认人地址 |
| confirm_tel | varchar(40) | Y |  | 结算单确认人联系电话 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的015 |
| open_date | varchar(8) | Y |  | 开户日期 |
| logout_date | varchar(8) | Y |  | 注销日期 |
| logout_reason | varchar(2) | Y |  | 销户原因:见tp_public_dict的016 |
| last_match_date | varchar(8) | Y |  | 最后成交日:日终结算后续处理，统计成交表写入 |
| op_date | varchar(8) | Y |  | 操作日期 |
| attr | varchar(3) | Y |  | 交易编码属性:见tp_public_dict263 |
| abbr | varchar(15) | Y |  | 客户简称 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 854. dimple.tt_client_member_check　(54 字段)
> 表含义：交易编码表复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| invest_type | varchar(3) | Y |  | 投资者类型 |
| grant_name | varchar(40) | Y |  | 开户授权人姓名(单位) |
| grant_cert_type | varchar(2) | Y |  | 开户授权人证件类型(单位):见tp_public_dict的025 |
| grant_cert_no | varchar(40) | Y |  | 开户授权人证件号码(单位) |
| grant_zip | varchar(6) | Y |  | 开户授权人邮政编码(单位) |
| grant_region_code | varchar(6) | Y |  | 开户授权人地区代码(单位) |
| grant_region_name | varchar(80) | Y |  | 开户授权人地区名称(单位) |
| grant_addr | varchar(120) | Y |  | 开户授权人地址(单位) |
| grant_tel | varchar(40) | Y |  | 开户授权人联系电话(单位) |
| cmd_name | varchar(40) | Y |  | 指定下单人姓名 |
| cmd_cert_type | varchar(2) | Y |  | 指定下单人证件类型:见tp_public_dict的025 |
| cmd_cert_no | varchar(40) | Y |  | 指定下单人证件号码 |
| cmd_zip | varchar(6) | Y |  | 指定下单人邮政编码 |
| cmd_region_code | varchar(6) | Y |  | 指定下单人地区代码 |
| cmd_region_name | varchar(80) | Y |  | 指定下单人地区名称 |
| cmd_addr | varchar(120) | Y |  | 指定下单人地址 |
| cmd_tel | varchar(40) | Y |  | 指定下单人联系电话 |
| trans_name | varchar(40) | Y |  | 资金调拨人姓名 |
| trans_cert_type | varchar(2) | Y |  | 资金调拨人证件类型:见tp_public_dict的025 |
| trans_cert_no | varchar(40) | Y |  | 资金调拨人证件号码 |
| trans_zip | varchar(6) | Y |  | 资金调拨人邮政编码 |
| trans_region_code | varchar(6) | Y |  | 资金调拨人地区代码 |
| trans_region_name | varchar(80) | Y |  | 资金调拨人地区名称 |
| trans_addr | varchar(120) | Y |  | 资金调拨人地址 |
| trans_tel | varchar(40) | Y |  | 资金调拨人联系电话 |
| confirm_name | varchar(40) | Y |  | 结算单确认人姓名 |
| confirm_cert_type | varchar(2) | Y |  | 资金调拨人证件类型:见tp_public_dict的025 |
| confirm_cert_no | varchar(40) | Y |  | 结算单确认人证件号码 |
| confirm_zip | varchar(6) | Y |  | 结算单确认人邮政编码 |
| confirm_region_code | varchar(6) | Y |  | 结算单确认人地区代码 |
| confirm_region_name | varchar(80) | Y |  | 结算单确认人地区名称 |
| confirm_addr | varchar(120) | Y |  | 结算单确认人地址 |
| confirm_tel | varchar(40) | Y |  | 结算单确认人联系电话 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的015 |
| open_date | varchar(8) | Y |  | 开户日期 |
| logout_date | varchar(8) | Y |  | 注销日期 |
| logout_reason | varchar(2) | Y |  | 销户原因:见tp_public_dict的016 |
| last_match_date | varchar(8) | Y |  | 最后成交日:日终结算后续处理，统计成交表写入 |
| op_date | varchar(8) | Y |  | 操作日期 |
| attr | varchar(3) | Y |  | 交易编码属性:见tp_public_dict263 |
| abbr | varchar(10) | Y |  | 客户简称 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 855. dimple.tt_client_member_operator　(8 字段)
> 表含义：操作员与交易编码对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| operator_no | varchar(30) | N | √ | 操作员 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号:$-代表全部 |
| client_id | varchar(16) | N | √ | 客户号:$-代表全部 |
| if_default | varchar(3) | N |  | 是否默认：见dict027 |
| op_oper | varchar(30) | N |  | 操作员 |
| op_date | varchar(8) | N |  | 操作日期 |
| op_time | varchar(8) | N |  | 操作时间 |

---

## 856. dimple.tt_client_member_trader　(9 字段)
> 表含义：查询交易员与交易编码对应关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(30) | N | √ | 交易员 |
| attr | varchar(3) | N | √ | 交易编码属性::$-代表全部,见tp_public_dict263 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号:$-代表全部 |
| client_id | varchar(16) | N | √ | 客户号:$-代表全部 |
| if_default | varchar(3) | N | √ | 是否默认：见dict |
| op_oper | varchar(30) | N |  | 操作员 |
| op_date | varchar(8) | N |  | 操作日期 |
| op_time | varchar(8) | N |  | 操作时间 |

---

## 857. dimple.tt_client_property　(2 字段)
> 表含义：客户单位性质表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| property_code | varchar(10) | N | √ | 性质代码 |
| property_name | varchar(80) | Y |  | 性质名称 |

---

## 858. dimple.tt_client_quote_posi　(12 字段)
> 表含义：报价商交易持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | N | √ | 客户代码 |
| contract_id | varchar(20) | N | √ | 合约代码 |
| last_buy_qty | numeric(18,0) | Y |  | 上一日多头持仓量 |
| last_sell_qty | numeric(18,0) | Y |  | 上一日空头持仓量 |
| buy_qty | numeric(18,0) | Y |  | 多头持仓量;公式=上一日多头持仓量 + 今日买入量 |
| sell_qty | numeric(18,0) | Y |  | 空头持仓量;公式=上一日空头持仓量 + 今日卖出量 |
| t_buy_qty | numeric(18,0) | Y |  | 今日买入量 |
| t_buy_amt | numeric(24,6) | Y |  | 今日买入金额 |
| t_sell_qty | numeric(18,0) | Y |  | 今日卖出量 |
| t_sell_amt | numeric(24,6) | Y |  | 今日卖出金额 |

---

## 859. dimple.tt_client_range　(2 字段)
> 表含义：客户经营范围表　|　估算行数：**1,068**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| range_code | varchar(10) | N | √ | 范围代码 |
| range_name | varchar(80) | Y |  | 范围名称 |

---

## 860. dimple.tt_client_region　(2 字段)
> 表含义：客户地区表　|　估算行数：**3,236**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| region_code | varchar(6) | N | √ | 地区代码 |
| region_name | varchar(80) | Y |  | 地区名称 |

---

## 861. dimple.tt_client_right　(7 字段)
> 表含义：客户交易权限表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| client_id | varchar(16) | N | √ | 客户号:不可为$ |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号:可以为$ |
| trade_type | varchar(2) | N | √ | 交易类型:见tp_public_dict的001 |
| variety_id | varchar(4) | N | √ | 品种代码:可为$ |
| contract_id | varchar(20) | N | √ | 合约号:可以为$ |
| trade_right | varchar(2) | N |  | 交易权限:见tp_public_dict的021 |

---

## 862. dimple.tt_client_right_seq　(9 字段)
> 表含义：客户交易权限操作流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 流水号 |
| client_id | varchar(16) | N |  | 客户号:不可为$ |
| member_id | varchar(8) | N |  | 会员号:可以为$ |
| trade_type | varchar(2) | N |  | 交易类型:见tp_public_dict的001 |
| variety_id | varchar(4) | N |  | 品种代码:可为$ |
| contract_id | varchar(20) | N |  | 合约号:可以为$ |
| trade_right | varchar(2) | Y |  | 交易权限:见tp_public_dict的021 |
| op_type | bpchar(1) | N |  | 操作类型:见tp_public_dict的091 |

---

## 863. dimple.tt_client_upd_log　(27 字段)
> 表含义：客户变更表:记录更改前的数据。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| seq_no | float8 | N | √ | 序号 |
| client_id | varchar(16) | Y |  | 客户号 |
| member_id | varchar(8) | Y |  | 会员号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| client_name | varchar(80) | Y |  | 客户名称 |
| client_property | varchar(2) | Y |  | 客户性质:见tp_public_dict的029 |
| cert_type | varchar(2) | Y |  | 证件类型(个人):见tp_public_dict的025 |
| cert_no | varchar(40) | Y |  | 证件号码(个人) |
| corp_name | varchar(40) | Y |  | 法人代表(单位) |
| revenue_no | varchar(40) | Y |  | 营业执照(单位) |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的012 |
| open_date | varchar(8) | Y |  | 开户日期 |
| logout_date | varchar(8) | Y |  | 注销日期 |
| grant_name | varchar(40) | Y |  | 开户授权人姓名(单位) |
| grant_cert_type | varchar(2) | Y |  | 开户授权人证件类型(单位):见tp_public_dict的025 |
| grant_cert_no | varchar(40) | Y |  | 开户授权人证件号码(单位) |
| cmd_name | varchar(40) | Y |  | 指定下单人姓名 |
| cmd_cert_type | varchar(2) | Y |  | 指定下单人证件类型:见tp_public_dict的025 |
| cmd_cert_no | varchar(40) | Y |  | 指定下单人证件号码 |
| trans_name | varchar(40) | Y |  | 资金调拨人姓名 |
| trans_cert_type | varchar(2) | Y |  | 资金调拨人证件类型:见tp_public_dict的025 |
| trans_cert_no | varchar(40) | Y |  | 资金调拨人证件号码 |
| confirm_name | varchar(40) | Y |  | 结算单确认人姓名 |
| confirm_cert_type | varchar(2) | Y |  | 资金调拨人证件类型:见tp_public_dict的025 |
| confirm_cert_no | varchar(40) | Y |  | 结算单确认人证件号码 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 864. dimple.tt_contract_exposure　(10 字段)
> 表含义：合约敞口倍率设置表　|　估算行数：**161**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| exposure_ratio | numeric(22,6) | Y |  | 敞口倍率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 865. dimple.tt_contract_exposure_check　(15 字段)
> 表含义：合约敞口倍率设置复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| variety_id | varchar(4) | Y |  | 品种代码 |
| contract_id | varchar(20) | N |  | 合约号 |
| exposure_ratio | numeric(22,6) | Y |  | 敞口倍率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 866. dimple.tt_contract_para　(63 字段)
> 表含义：合约有效参数表:初始化和结算时生成。查询用表。　|　估算行数：**271,774**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| last_clear_price | numeric(20,8) | Y |  | 最新结算价 |
| spec_new_buy_rate | numeric(10,6) | Y |  | 投机新开仓买率 |
| spec_new_sell_rate | numeric(10,6) | Y |  | 投机新开仓卖率 |
| hedge_new_buy_rate | numeric(10,6) | Y |  | 套保新开仓买率 |
| hedge_new_sell_rate | numeric(10,6) | Y |  | 套保新开仓卖率 |
| spec_buy_rate | numeric(10,6) | Y |  | 投机买率 |
| spec_sell_rate | numeric(10,6) | Y |  | 投机卖率 |
| hedge_buy_rate | numeric(10,6) | Y |  | 套保买率 |
| hedge_sell_rate | numeric(10,6) | Y |  | 套保卖率 |
| spec_new_buy | numeric(18,2) | Y |  | 投机新开仓买 |
| spec_new_sell | numeric(18,2) | Y |  | 投机新开仓卖 |
| hedge_new_buy | numeric(18,2) | Y |  | 套保新开仓买 |
| hedge_new_sell | numeric(18,2) | Y |  | 套保新开仓卖 |
| spec_buy | numeric(18,2) | Y |  | 投机买 |
| spec_sell | numeric(18,2) | Y |  | 投机卖 |
| hedge_buy | numeric(18,2) | Y |  | 套保买 |
| hedge_sell | numeric(18,2) | Y |  | 套保卖 |
| open_fee | numeric(22,6) | Y |  | 开仓结算手续费 |
| offset_fee | numeric(22,6) | Y |  | 平仓结算手续费 |
| t_open_fee | numeric(22,6) | Y |  | 开仓交易手续费 |
| t_offset_fee | numeric(22,6) | Y |  | 平仓交易手续费 |
| short_open_fee | numeric(22,6) | Y |  | 短线开仓手续费 |
| short_offset_fee | numeric(22,6) | Y |  | 短线平仓手续费 |
| exec_fee | numeric(22,6) | Y |  | 执行手续费 |
| perform_fee | numeric(22,6) | Y |  | 履约手续费 |
| delivery_fee | numeric(22,6) | Y |  | 交割手续费率 |
| rise_limit | numeric(9,2) | Y |  | 涨停板 |
| fall_limit | numeric(9,2) | Y |  | 跌停板 |
| rise_limit_rate | numeric(10,6) | Y |  | 涨停板率 |
| fall_limit_rate | numeric(10,6) | Y |  | 跌停板率 |
| rise_range | numeric(9,2) | Y |  | 涨停板(幅度) |
| fall_range | numeric(9,2) | Y |  | 跌停板(幅度) |
| rise_diff | numeric(9,2) | Y |  | 涨停板与前收盘价差值 |
| fall_diff | numeric(9,2) | Y |  | 跌停板与前收盘价差值 |
| all_self_sell_posi_quota | numeric(18,2) | Y |  | 综合会员自营卖持仓限额 |
| all_agent_sell_posi_quota | numeric(18,2) | Y |  | 综合会员经纪卖持仓限额 |
| all_tot_sell_posi_quota | numeric(18,2) | Y |  | 综合会员卖限仓总额 |
| self_tot_sell_posi_quota | numeric(18,2) | Y |  | 自营会员卖持仓限额 |
| agent_tot_sell_posi_quota | numeric(18,2) | Y |  | 经纪会员卖持仓限额 |
| client_sell_posi_quota | numeric(18,2) | Y |  | 客户卖持仓限额 |
| all_self_buy_posi_quota | numeric(18,2) | Y |  | 综合会员自营买持仓限额 |
| all_agent_buy_posi_quota | numeric(18,2) | Y |  | 综合会员经纪买持仓限额 |
| all_tot_buy_posi_quota | numeric(18,2) | Y |  | 综合会员买限仓总额 |
| self_tot_buy_posi_quota | numeric(18,2) | Y |  | 自营会员买持仓限额 |
| agent_tot_buy_posi_quota | numeric(18,2) | Y |  | 经纪会员买持仓限额 |
| client_buy_posi_quota | numeric(18,2) | Y |  | 客户买持仓限额 |
| out_money | numeric(9,2) | Y |  | 虚值额 |
| in_money | numeric(9,2) | Y |  | 实值额 |
| before_delivery_pos | float8 | Y |  | 交割月的前几个月 |
| month_day_no | float8 | Y |  | 当日在本月的交易日数 |
| middle_apply_margin_rate | numeric(22,6) | Y |  | 中立仓申报保证金率 |
| delivery_apply_margin_rate | numeric(22,6) | Y |  | 交割申报保证金率 |
| arbi_new_buy_rate | numeric(10,6) | Y |  | 套利新开仓买率 |
| arbi_new_sell_rate | numeric(10,6) | Y |  | 套利新开仓卖率 |
| arbi_buy_rate | numeric(10,6) | Y |  | 套利买率 |
| arbi_sell_rate | numeric(10,6) | Y |  | 套利卖率 |
| arbi_new_buy | numeric(18,2) | Y |  | 套利新开仓买 |
| arbi_new_sell | numeric(18,2) | Y |  | 套利新开仓卖 |
| arbi_buy | numeric(18,2) | Y |  | 套利买 |
| arbi_sell | numeric(18,2) | Y |  | 套利卖 |

---

## 867. dimple.tt_contract_right　(4 字段)
> 表含义：合约交易权限表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_type | varchar(2) | N | √ | 交易类型:见tp_public_dict的001 |
| variety_id | varchar(4) | N | √ | 品种代码:不可为$ |
| contract_id | varchar(20) | N | √ | 合约号:可为$ |
| trade_right | varchar(2) | N |  | 交易权限:见tp_public_dict的021 |

---

## 868. dimple.tt_contract_right_seq　(7 字段)
> 表含义：合约交易权限操作流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 流水号 |
| trade_type | varchar(2) | N |  | 交易类型:见tp_public_dict的001 |
| variety_id | varchar(4) | N |  | 品种代码:不可为$ |
| contract_id | varchar(20) | N |  | 合约号:可为$ |
| trade_right | varchar(2) | Y |  | 交易权限:见tp_public_dict的021 |
| op_type | bpchar(1) | N |  | 操作类型:见tp_public_dict的091 |

---

## 869. dimple.tt_contract_state_ctrl　(3 字段)
> 表含义：合约交易状态控制表:时间序列，非界面维护此表，系统初始化时根据系统交易状态控制表自动生成此表数据。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| start_time | varchar(8) | N | √ | 进入时间 |
| state | varchar(2) | N |  | 交易状态:见tp_public_dict的031 |

---

## 870. dimple.tt_contract_trade_state　(3 字段)
> 表含义：合约交易状态表　|　估算行数：**16**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N |  | 交易所代码:见tp_public_dict的217 |
| contract_id | varchar(20) | N | √ | 合约号 |
| trade_state | varchar(1) | N |  | 合约交易状态:询价合约见tp_public_dict的384；报价合约见tp_public_dict的408； |

---

## 871. dimple.tt_currency　(4 字段)
> 表含义：币种表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| location_code | varchar(4) | N | √ | 地区代码 |
| currency_id | varchar(3) | N | √ | 货币代码 |
| name_chn | varchar(80) | Y |  | 货币中文名称 |
| name_eng | varchar(40) | Y |  | 货币英文名称 |

---

## 872. dimple.tt_defer_delivery_apply　(21 字段)
> 表含义：递延交割申报表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | Y |  | 委托号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(6) | N |  | 交易所号 |
| contract_id | varchar(20) | N |  | 合约号 |
| trader_no | varchar(16) | N | √ | 交易员 |
| local_no | varchar(16) | N | √ | 本地委托号 |
| qty | numeric(12,0) | Y |  | 委托数量 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| apply_time | varchar(8) | Y |  | 委托时间 |
| order_status | bpchar(1) | Y |  | 申报状态:见tp_public_dict的228 |
| match_qty | numeric(12,0) | Y |  | 成交数量 |
| notes | varchar(254) | Y |  | 备注 |
| cancel_time | varchar(8) | Y |  | 撤单时间 |
| cancel_user | varchar(16) | Y |  | 撤单交易员 |
| middle_flag | bpchar(1) | Y |  | 是否中立仓:0否，1是 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |
| umcancelid | bpchar(40) | Y |  | UM撤销账号 |
| subaccount | varchar(12) | Y |  | 子账户 |

---

## 873. dimple.tt_defer_delivery_quot　(8 字段)
> 表含义：递延交割行情表　|　估算行数：**7**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | Y |  | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_qty | numeric(12,0) | Y |  | 买量 |
| sell_qty | numeric(12,0) | Y |  | 卖量 |
| mid_buy_qty | numeric(12,0) | Y |  | 中立仓买量 |
| mid_sell_qty | numeric(12,0) | Y |  | 中立仓卖量 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 874. dimple.tt_delivery_date_log　(3 字段)
> 表含义：合约最后交割日修改日志表:交割部手工修改最后交割日时记录。计算日期时，以手工设置的优先　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号 |
| if_upd | bpchar(1) | N |  | 最后交割日是否被修改 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 875. dimple.tt_delivery_substitute_variety　(5 字段)
> 表含义：交割替代品种表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N |  | 合约号 |
| inst_id | float8 | N |  | 替代序号 |
| delivery_variety_id | varchar(3) | N |  | 交割品种代码 |
| op_user | varchar(30) | Y |  | 操作人 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 876. dimple.tt_delivery_variety　(8 字段)
> 表含义：交割品种表信息　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_variety_id | varchar(3) | N | √ | 交割品种号 |
| name | varchar(80) | Y |  | 交割品种全称 |
| abbr | varchar(40) | Y |  | 简称 |
| unit | bpchar(1) | Y |  | 重量单位:状态:见tp_public_dict的216 |
| notes | varchar(254) | Y |  | 备注 |
| status | bpchar(1) | Y |  | 状态:见tp_public_dict的012 |
| std_weight | numeric(16,6) | Y |  | 默认条块标重 |
| variety_id | varchar(4) | Y |  | 品种代码 |

---

## 877. dimple.tt_delivery_variety_exposure　(4 字段)
> 表含义：交割品种敞口倍率设置表　|　估算行数：**18**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_variety_id | varchar(3) | N | √ | 交割品种代码 |
| exposure_ratio | numeric(22,6) | Y |  | 敞口倍率 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 878. dimple.tt_etf_match　(29 字段)
> 表含义：ETF成交明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| compare_date | varchar(8) | Y |  | 对账日期 |
| trade_date | varchar(8) | N | √ | 交易日期 |
| trade_time | varchar(8) | Y |  | 交易时间 |
| trader_no | varchar(30) | N | √ | 交易员 |
| self_local_no | varchar(30) | Y |  | Fund编号 |
| local_seq_no | varchar(20) | N | √ | 本地编号 |
| exch_seq_no | varchar(16) | Y |  | 交易所ETF编号 |
| trade_type | varchar(4) | Y |  | 交易类型：见数据字典268 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| member_id | varchar(8) | N | √ | 会员代码 |
| client_id | varchar(16) | N | √ | 客户号 |
| etf_code | varchar(8) | Y |  | ETF基金代码 |
| bond_account_no | varchar(20) | Y |  | 投资人证券账号 |
| deposit_unit | varchar(50) | Y |  | 托管单元 |
| percent_qty | numeric(16,0) | Y |  | 份额 |
| total_qty | numeric(20,6) | Y |  | 总重量 |
| contract_id_1 | varchar(20) | Y |  | 合约代码1 |
| qty_1 | numeric(20,6) | Y |  | 重量1 |
| contract_id_2 | varchar(20) | Y |  | 合约代码2 |
| qty_2 | numeric(20,6) | Y |  | 重量2 |
| contract_id_3 | varchar(20) | Y |  | 合约代码3 |
| qty_3 | numeric(20,6) | Y |  | 重量3 |
| contract_id_4 | varchar(20) | Y |  | 合约代码4 |
| qty_4 | numeric(20,6) | Y |  | 重量4 |
| contract_id_5 | varchar(20) | Y |  | 合约代码5 |
| qty_5 | numeric(20,6) | Y |  | 重量5 |
| status | varchar(4) | Y |  | 状态:见tp_public_dict的269 |
| confirm_date | varchar(8) | Y |  | 确认日期 |
| system_status | varchar(3) | Y |  | 系统状态:见tp_public_dict的271 |

---

## 879. dimple.tt_exch_code　(6 字段)
> 表含义：交易所表:系统中的交易所信息。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| location_code | varchar(4) | N |  | 地区代码 |
| abbr | varchar(40) | N |  | 中文简称 |
| exch_name | varchar(80) | Y |  | 中文全称 |
| eabbr | varchar(40) | N |  | 英文简称 |
| ename | varchar(80) | Y |  | 英文全称 |

---

## 880. dimple.tt_exch_money_real　(28 字段)
> 表含义：实时交易所资金表　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(4) | N | √ | 交易所编码 |
| member_id | varchar(8) | N | √ | 会员号 |
| remain | numeric(24,6) | Y |  | 资金余额/3代当日额度可报价余额 |
| margin | numeric(24,6) | Y |  | 交易保证金/3代当日额度保证金占用 |
| forzen_margin | numeric(24,6) | Y |  | 冻结保证金/3代额度冻结保证金 |
| money_in | numeric(24,6) | Y |  | 入金 |
| money_out | numeric(24,6) | Y |  | 出金 |
| buy_amount | numeric(24,6) | Y |  | 支付货款 |
| sell_amount | numeric(24,6) | Y |  | 收到货款 |
| profitloss | numeric(24,6) | Y |  | 盈亏 |
| setoff_out_limit | numeric(24,6) | Y |  | 充抵出金限制金额 |
| last_available | numeric(24,6) | Y |  | 上日可提资金 |
| available | numeric(24,6) | Y |  | 当日可提资金 |
| last_cash_balance | numeric(24,6) | Y |  | 上日货币可报价余额 |
| cash_balance | numeric(24,6) | Y |  | 当日货币可报价余额 |
| last_quota_balance | numeric(24,6) | Y |  | 上日额度可报价余额 |
| setoff_quota | numeric(24,6) | Y |  | 当日实际充抵额度 |
| last_setoff_usedquota | numeric(24,6) | Y |  | 上日已用充抵额度 |
| setoff_usedquota | numeric(24,6) | Y |  | 当日已用充抵额度 |
| setoff_avaliablequota | numeric(24,6) | Y |  | 待用充抵额度/当日剩余充抵额度 |
| last_cash_occupied | numeric(24,6) | Y |  | 上日货币保证金占用 |
| cash_occupied | numeric(24,6) | Y |  | 当日货币保证金占用 |
| last_quota_occupied | numeric(24,6) | Y |  | 上日额度保证金占用 |
| cash_forzen_margin | numeric(24,6) | Y |  | 货币冻结保证金 |
| fee | numeric(24,6) | Y |  | 费用 |
| base_margin | numeric(24,6) | Y |  | 基础保证金 |
| frozen_premium | numeric(24,6) | Y |  | 冻结权利金 |
| buy_sell_premium | numeric(24,6) | Y |  | 权利金收支 |

---

## 881. dimple.tt_exch_rfq_posi　(18 字段)
> 表含义：保证金询价会员持仓实时表　|　估算行数：**3**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约代码 |
| contract_no | numeric(12,0) | Y |  | 合约编号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| due_date | varchar(8) | N | √ | 到期日 |
| last_buy_qty | numeric(12,0) | Y |  | 上日多头持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日空头持仓量 |
| last_net_qty | numeric(12,0) | Y |  | 上日净持仓量 |
| today_buy_qty | numeric(12,0) | Y |  | 当日买量 |
| today_sell_qty | numeric(12,0) | Y |  | 当日卖量 |
| today_buy_amt | numeric(18,2) | Y |  | 当日买额 |
| today_sell_amt | numeric(18,2) | Y |  | 当日卖额 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| net_qty | numeric(12,0) | Y |  | 净持仓量 |
| profit | numeric(18,2) | Y |  | 盈亏 |
| buy_amt | numeric(18,2) | Y |  | 买额 |
| sell_amt | numeric(18,2) | Y |  | 卖额 |

---

## 882. dimple.tt_exch_state_ctrl　(3 字段)
> 表含义：系统交易状态控制表:时间序列，界面录入　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(6) | N | √ | 交易所代码 |
| start_time | varchar(8) | N | √ | 进入时间 |
| state | varchar(2) | N |  | 交易状态:见tp_public_dict的067 |

---

## 883. dimple.tt_exchange　(6 字段)
> 表含义：系统状态表：表明系统当前是何状态。　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(6) | N | √ | 系统代码 |
| abbr | varchar(40) | N |  | 中文简称 |
| exch_name | varchar(80) | Y |  | 中文全称 |
| eabbr | varchar(40) | N |  | 英文简称 |
| ename | varchar(80) | Y |  | 英文全称 |
| status | varchar(2) | N |  | 状态:见tp_public_dict的030 |

---

## 884. dimple.tt_ftr_arbi_contract　(24 字段)
> 表含义：期货套利合约表:手工录入或者自动生成。此表有每腿数量，是因为跨品种的数量需要在此定义。　|　估算行数：**65**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| arbi_contract_id | varchar(40) | N | √ | 套利合约号 |
| arbi_code | varchar(10) | N |  | 策略代码 |
| arbi_type | varchar(2) | Y |  | 套利合约类型：见tp_public_dict的404 |
| leg1 | varchar(8) | N |  | 腿1合约号 |
| leg2 | varchar(8) | N |  | 腿2合约号 |
| leg3 | varchar(8) | Y |  | 腿3合约号 |
| leg1_qty | numeric(12,0) | N |  | 腿1数量 |
| leg2_qty | numeric(12,0) | N |  | 腿2数量 |
| leg3_qty | numeric(12,0) | Y |  | 腿3数量 |
| max_hand | float8 | N |  | 最大下单手数 |
| min_hand | float8 | N |  | 最小下单手数 |
| tick | numeric(20,8) | N |  | 最小变动价位(元/吨) |
| if_display | bpchar(1) | N |  | 推导价格是否在行情中显示 |
| buy_perf_contract_id | varchar(40) | Y |  | 买组合合约号 |
| buy_ftr_ratio | numeric(10,6) | Y |  | 买组合合约的期货保证金和比例 |
| sell_perf_contract_id | varchar(40) | Y |  | 卖组合合约号 |
| sell_ftr_ratio | numeric(10,6) | Y |  | 卖组合合约的期货保证金和比例 |
| logout_date | varchar(8) | Y |  | 摘牌日期 |
| status | bpchar(1) | N |  | 合约状态:见tp_public_dict的026 |
| add_type | varchar(2) | Y |  | 增加方式:见tp_public_dict的034 |
| create_date | varchar(8) | Y |  | 创建日期 |
| op_date | varchar(8) | Y |  | 操作日期 |
| operator | varchar(30) | Y |  | 操作员 |
| arbi_code_type | varchar(2) | N |  | 套利合约类别：见tp_public_dict的496 |

---

## 885. dimple.tt_ftr_arbi_match　(18 字段)
> 表含义：套利期货成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| contract_id | varchar(30) | N |  | 合约号 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| trader_no | varchar(16) | N | √ | 席位号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |

---

## 886. dimple.tt_ftr_arbi_para　(4 字段)
> 表含义：期货套利策略参数表:规定了期货套利的参数，可以不设置　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| arbi_code | varchar(10) | N | √ | 策略代码 |
| single_min_qty | numeric(12,0) | Y |  | 单腿合约的最小持仓量:通过此项可以控制靠近交割月份的合约参与组合 |
| contract_qty | float8 | Y |  | 同品种中合约个数:参与组合的各腿期货合约的空盘量下限 |
| arbi_qty | float8 | Y |  | 每合约可组合套利合约个数:限制一张期货合约在当前策略中最多能参与几个套利合约 |

---

## 887. dimple.tt_ftr_arbi_quot　(20 字段)
> 表含义：期货套利行情表:精确到套利合约，价格是spread，非完整市场的价格；无开盘价，收盘价，结算价，成交量，持仓量　|　估算行数：**37**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| arbi_contract_id | varchar(40) | N | √ | 套利合约号 |
| low_price | numeric(20,8) | Y |  | 最低价 |
| high_price | numeric(20,8) | Y |  | 最高价 |
| life_low | numeric(20,8) | Y |  | 历史最低价 |
| life_high | numeric(20,8) | Y |  | 历史最高价 |
| multiple | float8 | Y |  | 价格因子 |
| rise_limit | numeric(20,8) | Y |  | 涨停板 |
| fall_limit | numeric(20,8) | Y |  | 跌停板 |
| last_price | numeric(20,8) | Y |  | 最新价 |
| bid_price | numeric(20,8) | Y |  | 最高买价 |
| bid_qty | numeric(12,0) | Y |  | 最高买量 |
| ask_price | numeric(20,8) | Y |  | 最低卖价 |
| ask_qty | numeric(12,0) | Y |  | 最低卖量 |
| gen_time | varchar(8) | Y |  | 生成时间 |
| open_price | numeric(20,8) | Y |  | 开盘价 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| last_clear | numeric(20,8) | Y |  | 前结算价 |
| last_close | numeric(20,8) | Y |  | 前收盘价 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 888. dimple.tt_ftr_arbi_variety　(11 字段)
> 表含义：期货套利策略品种表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| arbi_code | varchar(10) | N | √ | 策略代码 |
| group_no | float8 | N | √ | 组号 |
| variety_id1 | varchar(4) | N |  | 品种代码1 |
| variety_id2 | varchar(4) | N |  | 品种代码2 |
| variety_id3 | varchar(4) | Y |  | 品种代码3 |
| bs_flag_rel | float8 | N |  | 买卖方向关系1:填写-1,+1 |
| bs_flag_rel2 | float8 | N |  | 买卖方向关系2:填写-1,+1 |
| bs_flag_rel3 | float8 | Y |  | 买卖方向关系3:填写-1,+1 |
| coef1 | float8 | N |  | 系数1 |
| coef2 | float8 | N |  | 系数2 |
| coef3 | float8 | Y |  | 系数3 |

---

## 889. dimple.tt_ftr_client_posi　(26 字段)
> 表含义：期货客户交易持仓表　|　估算行数：**25**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |
| buy_margin_rate | numeric(18,2) | Y |  | 买固定保证金 |
| sell_margin_rate | numeric(18,2) | Y |  | 卖固定保证金 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |

---

## 890. dimple.tt_ftr_contract　(45 字段)
> 表含义：合约表　|　估算行数：**138**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N |  | 交易所代码 |
| contract_id | varchar(20) | N | √ | 合约号 |
| currency | varchar(3) | N |  | 币种:见tp_public_dict的435 |
| contract_name | varchar(40) | N |  | 合约名称 |
| variety_id | varchar(4) | N |  | 品种代码 |
| delivery_month | varchar(6) | N |  | 交割月 |
| unit | float8 | N |  | 合约乘数 |
| measure_unit | varchar(2) | Y |  | 计量单位:见tp_public_dict的129 |
| tick | numeric(16,8) | N |  | 最小变动价位 |
| max_hand | float8 | N |  | 最大下单手数 |
| min_hand | float8 | N |  | 最小下单手数 |
| mo_max_hand | float8 | Y |  | 市价单最大下单手数 |
| mo_min_hand | float8 | Y |  | 市价单最小下单手数 |
| start_trade_date | varchar(8) | Y |  | 开始交易日 |
| end_trade_date | varchar(8) | Y |  | 最后交易日:每日系统初始化重新计算 |
| end_delivery_date | varchar(8) | Y |  | 最后交割日:可被交割部手工修改，每日初始化重新计算。手工修改优先 |
| last_pos | float8 | N |  | 期货合约最后交易日在交割月的位置 |
| no_rise_limit | numeric(10,6) | N |  | 无成交涨停板率 |
| no_fall_limit | numeric(10,6) | N |  | 无成交跌停板率 |
| rise_limit | numeric(10,6) | N |  | 已成交涨停板率 |
| fall_limit | numeric(10,6) | N |  | 已成交跌停板率 |
| delivery_rise_limit | numeric(10,6) | N |  | 交割月涨停板率 |
| delivery_fall_limit | numeric(10,6) | N |  | 交割月跌停板率 |
| rise_fuse | numeric(10,6) | N |  | 涨停熔断点 |
| fall_fuse | numeric(10,6) | N |  | 跌停熔断点 |
| ref_price | numeric(20,8) | Y |  | 挂牌基准价 |
| wedy_mark | varchar(2) | Y |  | 周日标识:见tp_public_dict的214 |
| nacl_mark | varchar(2) | Y |  | 自然日交易日标识:见tp_public_dict的046 |
| week_num | float8 | Y |  | 最后交易日相关：周数 |
| day_num | float8 | Y |  | 周日标识为0-周时：星期数，为1-日时:日数 |
| status | bpchar(1) | N |  | 合约状态:见tp_public_dict的104 |
| trade_type | bpchar(1) | Y |  | 交易类型:交易类型:见tp_public_dict的001 |
| delivery_variety_id | varchar(3) | Y |  | 交割品种 |
| trans_coef | numeric(22,6) | Y |  | 单位转换系数 |
| holiday_flag | bpchar(1) | Y |  | 节假日是否有效:见Tp_public_dict的027 |
| deli_month_mark | varchar(1) | Y |  | 最后交易日相关：0-交割月份，1-交割月份前一月份；见tp_public_dict的370 |
| sort_mark | varchar(1) | Y |  | 最后交易日相关：0-顺序，1-逆序；见tp_public_dict的371 |
| contract_no | numeric(8,0) | Y |  | 合约编号：目前仅金交所报价合约使用 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |
| con_delivery_type | varchar(3) | Y |  | 交割方式：见tp_public_dict的432 |

---

## 891. dimple.tt_ftr_contract_check　(48 字段)
> 表含义：合约管理复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| contract_id | varchar(20) | N |  | 合约号 |
| currency | varchar(3) | N |  | 币种 |
| contract_name | varchar(40) | N |  | 合约名称 |
| variety_id | varchar(4) | N |  | 品种代码 |
| delivery_month | varchar(6) | N |  | 交割月 |
| unit | float8 | N |  | 合约乘数 |
| measure_unit | varchar(2) | Y |  | 计量单位:见tp_public_dict的129 |
| tick | numeric(16,8) | N |  | 最小变动价位 |
| max_hand | float8 | N |  | 最大下单手数 |
| min_hand | float8 | N |  | 最小下单手数 |
| mo_max_hand | float8 | Y |  | 市价单最大下单手数 |
| mo_min_hand | float8 | Y |  | 市价单最小下单手数 |
| start_trade_date | varchar(8) | Y |  | 开始交易日 |
| end_trade_date | varchar(8) | Y |  | 最后交易日:每日系统初始化重新计算 |
| end_delivery_date | varchar(8) | Y |  | 最后交割日:可被交割部手工修改，每日初始化重新计算。手工修改优先 |
| last_pos | float8 | N |  | 期货合约最后交易日在交割月的位置 |
| no_rise_limit | numeric(10,6) | N |  | 无成交涨停板率 |
| no_fall_limit | numeric(10,6) | N |  | 无成交跌停板率 |
| rise_limit | numeric(10,6) | N |  | 已成交涨停板率 |
| fall_limit | numeric(10,6) | N |  | 已成交跌停板率 |
| delivery_rise_limit | numeric(10,6) | N |  | 交割月涨停板率 |
| delivery_fall_limit | numeric(10,6) | N |  | 交割月跌停板率 |
| rise_fuse | numeric(10,6) | N |  | 涨停熔断点 |
| fall_fuse | numeric(10,6) | N |  | 跌停熔断点 |
| ref_price | numeric(20,8) | Y |  | 挂牌基准价 |
| wedy_mark | varchar(2) | Y |  | 周日标识:见tp_public_dict的214 |
| nacl_mark | varchar(2) | Y |  | 自然日交易日标识:见tp_public_dict的046 |
| week_num | float8 | Y |  | 最后交易日相关：周数 |
| day_num | float8 | Y |  | 周日标识为0-周时：星期数，为1-日时:日数 |
| status | bpchar(1) | N |  | 合约状态:见tp_public_dict的104 |
| trade_type | bpchar(1) | Y |  | 交易类型:交易类型:见tp_public_dict的001 |
| delivery_variety_id | varchar(3) | Y |  | 交割品种 |
| trans_coef | numeric(22,6) | Y |  | 单位转换系数 |
| holiday_flag | bpchar(1) | Y |  | 节假日是否有效:见Tp_public_dict的027 |
| deli_month_mark | varchar(1) | Y |  | 最后交易日相关：0-交割月份，1-交割月份前一月份；见tp_public_dict的370 |
| sort_mark | varchar(1) | Y |  | 最后交易日相关：0-顺序，1-逆序；见tp_public_dict的371 |
| contract_no | numeric(8,0) | Y |  | 合约编号：目前仅金交所报价合约使用 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 892. dimple.tt_ftr_contract_temp　(0 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|

---

## 893. dimple.tt_ftr_err_order　(37 字段)
> 表含义：期货错误委托表　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| tid | numeric(10,0) | N |  | 事务编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | N | √ | 委托席位号:对强平单，填写操作员；其他的填写交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(20) | N | √ | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| eo_flag | varchar(2) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | varchar(2) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| last_match_price | numeric(20,8) | Y |  | 最新成交价 |
| stop_price | numeric(9,2) | Y |  | 止损(盈)价 |
| match_qty | numeric(12,0) | Y |  | 成交量 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| force_offset_reason | varchar(2) | Y |  | 强平原因:见tp_public_dict的040 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| if_mktmk | bpchar(1) | Y |  | 是否做市商下单 |
| reason | varchar(254) | Y |  | 错误原因 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| self_cancel_trader_no | varchar(16) | Y |  | 内部撤单席位号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |

---

## 894. dimple.tt_ftr_match　(22 字段)
> 表含义：期货成交表:新增成交影响行情，持仓，持仓明细　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| tid | numeric(10,0) | N |  | 事务编号 |
| contract_id | varchar(30) | N |  | 合约号 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| trader_no | varchar(16) | N | √ | 席位号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| app_type | varchar(3) | N | √ | 定价成交申报类型:0-默认,见tp_public_dict330 |
| org_trade_type | bpchar(1) | N |  | 成交类型:0-普通成交,见tp_public_dict497 |

---

## 895. dimple.tt_ftr_match_tmp　(23 字段)
> 表含义：交易员成交表:新增成交影响行情，持仓，持仓明细　|　估算行数：**6**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| trade_date | varchar(8) | N |  | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| tid | numeric(10,0) | N |  | TID |
| contract_id | varchar(30) | N |  | 合约号 |
| match_time | varchar(12) | Y |  | 成交时间 |
| price | numeric(20,8) | Y |  | 价格 |
| qty | numeric(12,0) | Y |  | 数量（手） |
| trader_no | varchar(16) | Y |  | 席位号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| eo_flag | bpchar(1) | Y |  | 开平标志:见tp_public_dict的003 |
| sh_flag | bpchar(1) | Y |  | 投保标志:见tp_public_dict的004 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| match_type | bpchar(1) | Y |  | 成交类型:见tp_public_dict237，此表不含6-报价成交 7-保证金询价成交 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| app_type | varchar(3) | N | √ | 定价成交申报类型:0-默认,见tp_public_dict330 |
| notes | varchar(250) | Y |  | 备注 |

---

## 896. dimple.tt_ftr_match_transed　(5 字段)
> 表含义：成交已传输表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| trader_no | varchar(16) | N | √ | 席位号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| purpose | varchar(2) | N |  | 成交目的：1#自营;2#套利 |

---

## 897. dimple.tt_ftr_mbl_quot　(6 字段)
> 表含义：期货深度行情表:交易系统产生。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| order_price | numeric(9,2) | N | √ | 委托价 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| order_qty | numeric(12,0) | Y |  | 委托量 |
| gen_time | varchar(8) | Y |  | 生成时间 |

---

## 898. dimple.tt_ftr_member_posi　(24 字段)
> 表含义：期货会员交易持仓表:更新客户持仓时，需要更新此表。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |
| buy_margin_rate | numeric(18,2) | Y |  | 买固定保证金 |
| sell_margin_rate | numeric(18,2) | Y |  | 卖固定保证金 |

---

## 899. dimple.tt_ftr_order　(39 字段)
> 表含义：期货委托表:影响成交，行情，持仓　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | N | √ | 系统委托号 |
| tid | numeric(10,0) | N |  | TID:此值即为包中的SeqNo，便于追踪数据和恢复 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | Y |  | 委托席位号:对强平单，填写操作员；其他的填写交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号:对强平单，填写操作员；其他的填写交易员 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(20) | Y |  | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| eo_flag | varchar(2) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | varchar(2) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| last_match_price | numeric(20,8) | Y |  | 最新成交价 |
| stop_price | numeric(9,2) | Y |  | 止损(盈)价 |
| match_qty | numeric(12,0) | Y |  | 成交量 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| force_offset_reason | varchar(2) | Y |  | 强平原因:见tp_public_dict的040 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金:计算字段 |
| if_mktmk | bpchar(1) | Y |  | 是否做市商下单 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| self_cancel_trader_no | varchar(16) | Y |  | 内部撤单席位号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |
| umcancelid | varchar(40) | Y |  | UM撤销账号 |
| strategyno | varchar(4) | Y |  | 投资策略编号 |
| subaccount | varchar(12) | Y |  | 子账户 |

---

## 900. dimple.tt_ftr_purpose_posi　(27 字段)
> 表含义：期货交易目的交易持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| client_id | varchar(16) | N | √ | 客户号 |
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |
| buy_margin_rate | numeric(18,2) | Y |  | 买固定保证金 |
| sell_margin_rate | numeric(18,2) | Y |  | 卖固定保证金 |
| defer_fee | numeric(18,2) | Y |  | 递延费 |

---

## 901. dimple.tt_ftr_quot　(32 字段)
> 表含义：期货行情表:由交易系统产生，一个合约仅有一条记录。记录了价格，成交量，委托量，涨跌等信息。　|　估算行数：**69**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(30) | N | √ | 合约号 |
| contract_name | varchar(40) | Y |  | 合约名称 |
| open_price | numeric(20,8) | Y |  | 开盘价 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| low_price | numeric(20,8) | Y |  | 最低价 |
| high_price | numeric(20,8) | Y |  | 最高价 |
| turnover | numeric(18,2) | Y |  | 成交额 |
| match_tot_qty | numeric(12,0) | Y |  | 成交量 |
| open_interest | numeric(12,0) | Y |  | 持仓量 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| life_low | numeric(20,8) | Y |  | 历史最低价 |
| life_high | numeric(20,8) | Y |  | 历史最高价 |
| multiple | float8 | Y |  | 价格因子 |
| rise_limit | numeric(9,2) | Y |  | 涨停板 |
| fall_limit | numeric(9,2) | Y |  | 跌停板 |
| last_match_qty | numeric(12,0) | Y |  | 最新成交量 |
| last_clear | numeric(20,8) | Y |  | 前结算价 |
| last_close | numeric(20,8) | Y |  | 前收盘价 |
| init_open_interest | numeric(12,0) | Y |  | 初始持仓量 |
| last_price | numeric(20,8) | Y |  | 最新价 |
| bid_price | numeric(20,8) | Y |  | 最高买价 |
| bid_qty | numeric(12,0) | Y |  | 最高买量 |
| bid_imply_qty | numeric(12,0) | Y |  | 最高买推导量 |
| ask_price | numeric(20,8) | Y |  | 最低卖价 |
| ask_qty | numeric(12,0) | Y |  | 最低卖量 |
| ask_imply_qty | numeric(12,0) | Y |  | 最低卖推导量 |
| avg_price | numeric(20,8) | Y |  | 当日均价 |
| gen_time | varchar(8) | Y |  | 生成时间 |
| match_weight | numeric(15,3) | Y |  | 成交重量 |
| delta | numeric(17,8) | Y |  | 虚实度(上期所期权增加) |
| last_delta | numeric(17,8) | Y |  | 前虚实度(上期所期权增加) |

---

## 902. dimple.tt_ftr_variety　(35 字段)
> 表含义：期货品种表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| variety_id | varchar(4) | N | √ | 品种代码 |
| currency | varchar(3) | N |  | 币种 |
| variety_name | varchar(20) | N |  | 品种名称 |
| variety_ename | varchar(80) | Y |  | 品种英文名称 |
| shortcut | varchar(2) | N |  | 快捷输入:只能输入1位，必须是数字或字母 |
| unit | float8 | N |  | 交易单位数量(吨/手) |
| measure_unit | varchar(2) | Y |  | 计量单位:见tp_public_dict的129 |
| tick | numeric(16,8) | N |  | 最小变动价位(元/吨) |
| max_hand | float8 | N |  | 最大下单手数 |
| min_hand | float8 | N |  | 最小下单手数 |
| mo_max_hand | float8 | Y |  | 市价单最大下单手数 |
| mo_min_hand | float8 | Y |  | 市价单最小下单手数 |
| no_rise_limit | numeric(10,6) | N |  | 无成交涨停板率 |
| no_fall_limit | numeric(10,6) | N |  | 无成交跌停板率 |
| rise_limit | numeric(10,6) | N |  | 已成交涨停板率 |
| fall_limit | numeric(10,6) | N |  | 已成交跌停板率 |
| delivery_rise_limit | numeric(10,6) | N |  | 交割月涨停板率 |
| delivery_fall_limit | numeric(10,6) | N |  | 交割月跌停板率 |
| rise_fuse | numeric(10,6) | N |  | 涨停熔断点 |
| fall_fuse | numeric(10,6) | N |  | 跌停熔断点 |
| status | bpchar(1) | N |  | 品种状态:见tp_public_dict的032 |
| last_trade_date | varchar(80) | Y |  | 最后交易日 |
| wedy_mark | varchar(2) | Y |  | 周日标识:见tp_public_dict的214 |
| nacl_mark | varchar(2) | Y |  | 自然日交易日标识:见tp_public_dict的046 |
| week_num | float8 | Y |  | 最后交易日相关：周数 |
| day_num | float8 | Y |  | 交易日为星期数，自然日为日数 |
| deli_month_mark | varchar(1) | Y |  | 最后交易日相关：0-交割月份，1-交割月份前一月份；见tp_public_dict的370 |
| sort_mark | varchar(1) | Y |  | 最后交易日相关：0-顺序，1-逆序；见tp_public_dict的371 |
| logout_date | varchar(8) | Y |  | 摘牌日期 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 903. dimple.tt_ftr_variety_check　(39 字段)
> 表含义：期货品种复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| variety_id | varchar(4) | N |  | 品种代码 |
| currency | varchar(3) | N |  | 币种 |
| variety_name | varchar(20) | N |  | 品种名称 |
| variety_ename | varchar(80) | Y |  | 品种英文名称 |
| shortcut | varchar(2) | N |  | 快捷输入:只能输入1位，必须是数字或字母 |
| unit | float8 | N |  | 交易单位数量(吨/手) |
| measure_unit | varchar(2) | Y |  | 计量单位:见tp_public_dict的129 |
| tick | numeric(16,8) | N |  | 最小变动价位(元/吨) |
| max_hand | float8 | N |  | 最大下单手数 |
| min_hand | float8 | N |  | 最小下单手数 |
| mo_max_hand | float8 | Y |  | 市价单最大下单手数 |
| mo_min_hand | float8 | Y |  | 市价单最小下单手数 |
| no_rise_limit | numeric(10,6) | N |  | 无成交涨停板率 |
| no_fall_limit | numeric(10,6) | N |  | 无成交跌停板率 |
| rise_limit | numeric(10,6) | N |  | 已成交涨停板率 |
| fall_limit | numeric(10,6) | N |  | 已成交跌停板率 |
| delivery_rise_limit | numeric(10,6) | N |  | 交割月涨停板率 |
| delivery_fall_limit | numeric(10,6) | N |  | 交割月跌停板率 |
| rise_fuse | numeric(10,6) | N |  | 涨停熔断点 |
| fall_fuse | numeric(10,6) | N |  | 跌停熔断点 |
| status | bpchar(1) | N |  | 品种状态:见tp_public_dict的032 |
| last_trade_date | varchar(80) | Y |  | 最后交易日 |
| wedy_mark | varchar(2) | Y |  | 周日标识:见tp_public_dict的214 |
| nacl_mark | varchar(2) | Y |  | 自然日交易日标识:见tp_public_dict的046 |
| week_num | float8 | Y |  | 最后交易日相关：周数 |
| day_num | float8 | Y |  | 交易日为星期数，自然日为日数 |
| deli_month_mark | varchar(1) | Y |  | 最后交易日相关：0-交割月份，1-交割月份前一月份；见tp_public_dict的370 |
| sort_mark | varchar(1) | Y |  | 最后交易日相关：0-顺序，1-逆序；见tp_public_dict的371 |
| logout_date | varchar(8) | Y |  | 摘牌日期 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 904. dimple.tt_his_client_opt_exec　(14 字段)
> 表含义：会员期权行权汇总历史表　|　估算行数：**52**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| contract_id | varchar(30) | N | √ | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| exec_qty | numeric(10,0) | Y |  | 已申请执行量 |
| last_exec_qty | numeric(10,0) | Y |  | 已申请执行昨量 |
| today_exec_qty | numeric(10,0) | Y |  | 已申请执行今量 |
| self_close_qty | numeric(10,0) | Y |  | 执行后期货自对冲量 |
| abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃量 |
| last_abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃昨量 |
| today_abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃今量 |

---

## 905. dimple.tt_his_defer_delivery_apply　(21 字段)
> 表含义：递延交割申报历史表　|　估算行数：**699**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | Y |  | 委托号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(6) | N | √ | 交易所号 |
| contract_id | varchar(20) | N |  | 合约号 |
| trader_no | varchar(16) | N | √ | 交易员 |
| local_no | varchar(16) | N | √ | 本地委托号 |
| qty | numeric(12,0) | Y |  | 委托数量 |
| bs_flag | bpchar(1) | N |  | 买卖标志 |
| apply_time | varchar(8) | Y |  | 委托时间 |
| order_status | bpchar(1) | Y |  | 申报状态:见tp_public_dict的228 |
| match_qty | numeric(12,0) | Y |  | 成交数量 |
| notes | varchar(254) | Y |  | 备注 |
| cancel_time | varchar(8) | Y |  | 撤单时间 |
| cancel_user | varchar(16) | Y |  | 撤单交易员 |
| middle_flag | bpchar(1) | Y |  | 是否中立仓:0否，1是 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| umid | bpchar(40) | Y |  | Um账号 |
| umcancelid | varchar(40) | Y |  | UM撤销账号 |
| subaccount | varchar(12) | Y |  | 子账户编号 |

---

## 906. dimple.tt_his_defer_delivery_quot　(8 字段)
> 表含义：递延交割行情历史表　|　估算行数：**5,166**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| buy_qty | numeric(12,0) | Y |  | 买量 |
| sell_qty | numeric(12,0) | Y |  | 卖量 |
| mid_buy_qty | numeric(12,0) | Y |  | 中立仓买量 |
| mid_sell_qty | numeric(12,0) | Y |  | 中立仓卖量 |
| op_user | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 907. dimple.tt_his_ftr_arbi_quot　(20 字段)
> 表含义：历史期货套利行情表　|　估算行数：**14,923**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| arbi_contract_id | varchar(40) | N | √ | 套利合约号 |
| low_price | numeric(20,8) | Y |  | 最低价 |
| high_price | numeric(20,8) | Y |  | 最高价 |
| life_low | numeric(20,8) | Y |  | 历史最低价 |
| life_high | numeric(20,8) | Y |  | 历史最高价 |
| multiple | float8 | Y |  | 价格因子 |
| rise_limit | numeric(20,8) | Y |  | 涨停板 |
| fall_limit | numeric(20,8) | Y |  | 跌停板 |
| last_price | numeric(20,8) | Y |  | 最新价 |
| bid_price | numeric(20,8) | Y |  | 最高买价 |
| bid_qty | numeric(12,0) | Y |  | 最高买量 |
| ask_price | numeric(20,8) | Y |  | 最低卖价 |
| ask_qty | numeric(12,0) | Y |  | 最低卖量 |
| gen_time | varchar(8) | Y |  | 生成时间 |
| open_price | numeric(20,8) | Y |  | 开盘价 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| last_clear | numeric(20,8) | Y |  | 前结算价 |
| last_close | numeric(20,8) | Y |  | 前收盘价 |
| clear_price | numeric(20,8) | Y |  | 结算价 |

---

## 908. dimple.tt_his_ftr_err_order　(37 字段)
> 表含义：历史期货错误委托表　|　估算行数：**81,962**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| tid | numeric(10,0) | N |  | 事务编号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(20) | N |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | N | √ | 委托席位号:对强平单，填写操作员；其他的填写交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | N | √ | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| eo_flag | varchar(2) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | varchar(2) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| last_match_price | numeric(20,8) | Y |  | 最新成交价 |
| stop_price | numeric(9,2) | Y |  | 止损(盈)价 |
| match_qty | numeric(12,0) | Y |  | 成交量 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| force_offset_reason | varchar(2) | Y |  | 强平原因:见tp_public_dict的040 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| if_mktmk | bpchar(1) | Y |  | 是否做市商下单 |
| reason | varchar(254) | Y |  | 错误原因 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| self_cancel_trader_no | varchar(16) | Y |  | 内部撤单席位号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |

---

## 909. dimple.tt_his_ftr_order　(39 字段)
> 表含义：历史期货委托表　|　估算行数：**565,239**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | N | √ | 系统委托号 |
| tid | numeric(10,0) | N |  | TID:此值即为包中的SeqNo，便于追踪数据和恢复 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | Y |  | 委托席位号:对强平单，填写操作员；其他的填写交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号:对强平单，填写操作员；其他的填写交易员 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| eo_flag | varchar(2) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | varchar(2) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| last_match_price | numeric(20,8) | Y |  | 最新成交价 |
| stop_price | numeric(9,2) | Y |  | 止损(盈)价 |
| match_qty | numeric(12,0) | Y |  | 成交量 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| force_offset_reason | varchar(2) | Y |  | 强平原因:见tp_public_dict的040 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金:计算字段 |
| if_mktmk | bpchar(1) | Y |  | 是否做市商下单 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| self_cancel_trader_no | varchar(16) | Y |  | 内部撤单席位号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |
| umcancelid | varchar(40) | Y |  | UM撤销账号 |
| strategyno | varchar(4) | Y |  | 投资策略编号 |
| subaccount | varchar(12) | Y |  | 子账户编号 |

---

## 910. dimple.tt_his_ftr_quot　(32 字段)
> 表含义：历史期货行情表　|　估算行数：**63,327**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| contract_id | varchar(20) | N | √ | 合约号 |
| contract_name | varchar(40) | Y |  | 合约名称 |
| open_price | numeric(20,8) | Y |  | 开盘价 |
| close_price | numeric(20,8) | Y |  | 收盘价 |
| low_price | numeric(20,8) | Y |  | 最低价 |
| high_price | numeric(20,8) | Y |  | 最高价 |
| turnover | numeric(18,2) | Y |  | 成交额 |
| match_tot_qty | numeric(12,0) | Y |  | 成交量 |
| open_interest | numeric(12,0) | Y |  | 持仓量 |
| clear_price | numeric(20,8) | Y |  | 结算价 |
| life_low | numeric(20,8) | Y |  | 历史最低价 |
| life_high | numeric(20,8) | Y |  | 历史最高价 |
| multiple | float8 | Y |  | 价格因子 |
| rise_limit | numeric(9,2) | Y |  | 涨停板 |
| fall_limit | numeric(9,2) | Y |  | 跌停板 |
| last_match_qty | numeric(12,0) | Y |  | 最新成交量 |
| last_clear | numeric(20,8) | Y |  | 前结算价 |
| last_close | numeric(20,8) | Y |  | 前收盘价 |
| init_open_interest | numeric(12,0) | Y |  | 初始持仓量 |
| last_price | numeric(20,8) | Y |  | 最新价 |
| bid_price | numeric(20,8) | Y |  | 最高买价 |
| bid_qty | numeric(12,0) | Y |  | 最高买量 |
| bid_imply_qty | numeric(12,0) | Y |  | 最高买推导量 |
| ask_price | numeric(20,8) | Y |  | 最低卖价 |
| ask_qty | numeric(12,0) | Y |  | 最低卖量 |
| ask_imply_qty | numeric(12,0) | Y |  | 最低卖推导量 |
| avg_price | numeric(20,8) | Y |  | 当日均价 |
| gen_time | varchar(8) | Y |  | 生成时间 |
| match_weight | numeric(15,3) | Y |  | 成交重量 |
| delta | numeric(17,8) | Y |  | 虚实度(上期所期权增加) |
| last_delta | numeric(17,8) | Y |  | 前虚实度(上期所期权增加) |

---

## 911. dimple.tt_his_opt_selfclose_order　(16 字段)
> 表含义：场上自营交易员自对冲申报表　|　估算行数：**292**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(30) | N |  | 合约号 |
| apply_time | varchar(12) | Y |  | 申请时间 |
| self_close_type | varchar(2) | Y |  | 自对冲类型:见tp_public_dict的433 |
| self_close_local_id | varchar(16) | N | √ | 本地自对冲编号 |
| self_close_sys_id | varchar(16) | Y |  | 系统自对冲编号 |
| exec_qty | numeric(10,0) | Y |  | 申请自对冲量 |
| status | varchar(2) | Y |  | 状态:见tp_public_dict的434 |
| cancel_trader_no | varchar(16) | Y |  | 撤销交易员 |
| cancel_time | varchar(12) | Y |  | 撤销时间 |
| self_trader_no | varchar(16) | N |  | 报盘委托席位号 |
| self_local_no | varchar(16) | N |  | 报盘本地委托号 |

---

## 912. dimple.tt_his_order_para　(15 字段)
> 表含义：委托参数历史表　|　估算行数：**74,628**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| clear_date | varchar(8) | N | √ | 日期 |
| contract_id | varchar(40) | N | √ | 合约 |
| trader_no | varchar(30) | N | √ | 交易员 |
| min_hand | numeric(10,0) | Y |  | 最小下单手数 |
| max_hand | numeric(10,0) | Y |  | 最大下单手数 |
| price_diff | numeric(20,8) | Y |  | 价差 |
| op_date | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作员 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |
| if_trader_ctl | varchar(3) | Y |  | 是否控制交易员：见tp_public_dict的027 |

---

## 913. dimple.tt_his_pre_order　(26 字段)
> 表含义：历史预委托表　|　估算行数：**1,437,314**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| local_no | varchar(16) | N | √ | 本地委托号，强平单以FA开头 |
| tid | numeric(10,0) | N |  | TID:此值即为包中的SeqNo，便于追踪数据和恢复 |
| trader_no | varchar(16) | N | √ | 委托席位号:对强平单，填写操作员；其他的填写交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号:对强平单，填写操作员；其他的填写交易员 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| eo_flag | varchar(2) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | varchar(2) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| stop_price | numeric(9,2) | Y |  | 止损(盈)价 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| rechk_oper | varchar(30) | Y |  | 复核人 |
| rechk_time | varchar(12) | Y |  | 复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |

---

## 914. dimple.tt_his_quote_err_order　(24 字段)
> 表含义：报价错误委托历史表　|　估算行数：**15,126**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | N | √ | 委托交易员 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | N | √ | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量：手 |
| match_qty | numeric(12,0) | Y |  | 成交量：手 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| cancel_qty | numeric(12,0) | Y |  | 撤单量：手 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| if_checked | varchar(2) | Y |  | 是否经过检查 |
| reason | varchar(254) | Y |  | 错误原因 |

---

## 915. dimple.tt_his_quote_order　(22 字段)
> 表含义：报价委托历史表:影响成交，行情，持仓　|　估算行数：**98,898**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | N | √ | 系统委托号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | Y |  | 委托交易员 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量：手 |
| match_qty | numeric(12,0) | Y |  | 成交量：手 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_trader_no | varchar(16) | Y |  | 撤单交易员 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| cancel_qty | numeric(12,0) | Y |  | 撤单量：手 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |

---

## 916. dimple.tt_his_quoter_quot　(10 字段)
> 表含义：报价商报价行情历史表　|　估算行数：**154,279**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| market_no | numeric(2,0) | Y |  | 市场编号：报价保证金市场使用60 |
| contract_no | numeric(8,0) | N | √ | 合约编码：mkt_no(2位)+2位自增序号 |
| ask_price | numeric(12,6) | Y |  | 卖价 |
| bid_price | numeric(12,6) | Y |  | 买价 |
| ask_lot | numeric(12,0) | Y |  | 卖量 |
| bid_lot | numeric(12,0) | Y |  | 买量 |
| quote_date | varchar(8) | N | √ | 行情日期 |
| quote_time | varchar(8) | Y |  | 行情时间 |
| natual_date | varchar(8) | Y |  | 自然日期 |
| seq_no | numeric(32,0) | N | √ | 流水号 |

---

## 917. dimple.tt_his_trader_opt_exec　(16 字段)
> 表含义：交易员期权行权汇总历史表　|　估算行数：**62**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| exec_qty | numeric(10,0) | Y |  | 已申请执行量 |
| last_exec_qty | numeric(10,0) | Y |  | 已申请执行昨量 |
| today_exec_qty | numeric(10,0) | Y |  | 已申请执行今量 |
| self_close_qty | numeric(10,0) | Y |  | 执行后期货自对冲量 |
| abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃量 |
| last_abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃昨量 |
| today_abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃今量 |

---

## 918. dimple.tt_interface_exchange　(3 字段)
> 表含义：交易接口规范:交易所状态信息　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(6) | N | √ | 交易所代码:见tp_public_dict的217;02-金交所99-上证所98-深证所 |
| exch_status | varchar(1) | Y |  | 交易所运行状态:见tp_public_dict的398 |
| announce_time | varchar(8) | Y |  | 发布时间:交易所状态为0-初始化1-初始化完成2-开市时为空 |

---

## 919. dimple.tt_investor　(24 字段)
> 表含义：投资者表:是原会员表和原客户表的综合　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| invest_id | varchar(8) | N | √ | 投资者号 |
| invest_abbr | varchar(40) | N |  | 投资者简称 |
| invest_name | varchar(80) | N |  | 投资者名称 |
| invest_type | bpchar(1) | N |  | 状态:见tp_public_dict的212 |
| invest_prop | bpchar(1) | N |  | 状态:见tp_public_dict的029 |
| currency | varchar(3) | Y |  | 币种 |
| reg_money | numeric(18,2) | N |  | 注册资金 |
| location_code | varchar(6) | N |  | 地区代码 |
| region_name | varchar(80) | Y |  | 地区名称 |
| addr | varchar(120) | N |  | 注册地址 |
| conn_addr | varchar(120) | N |  | 联系地址 |
| connect_person | varchar(40) | N |  | 联系人 |
| tel | varchar(40) | N |  | 联系电话 |
| fax | varchar(40) | N |  | 联系传真 |
| zip | varchar(6) | N |  | 邮编 |
| revenue_no | varchar(40) | N |  | 税务登记号 |
| license_type | varchar(2) | Y |  | 证件类别：零售投资者填写。见public_dic:025. |
| license_no | varchar(40) | N |  | 证件号码：零售投资者：身份证号；批发投资者：营业执照号； |
| org_code | varchar(20) | N |  | 组织机构代码 |
| open_date | varchar(8) | Y |  | 开户日期 |
| status | bpchar(1) | N |  | 状态 |
| logout_date | varchar(8) | Y |  | 销户日期 |
| logout_reason | varchar(120) | Y |  | 注销原因 |
| op_date | varchar(8) | Y |  | 操作日期 |

---

## 920. dimple.tt_kondor_match　(18 字段)
> 表含义：Kondor成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| match_no | varchar(20) | N | √ | 成交号 |
| seq_no | numeric(8,0) | N | √ | 流水号 |
| bs_flag | bpchar(1) | N |  | 买卖方向:见tp_public_dict的002 |
| trade_date | varchar(8) | N | √ | 交易日 |
| match_time | varchar(20) | Y |  | 录入时间 |
| price_usa | numeric(20,8) | Y |  | 价格(美元/盎司) |
| exchange_rate | numeric(9,4) | Y |  | 实时汇率 |
| price_cny | numeric(20,8) | Y |  | 价格(元/克) |
| qty | numeric(15,2) | Y |  | 数量（盎司） |
| amt | numeric(24,6) | Y |  | 交易金额（美元） |
| paris_currency | varchar(8) | N |  | 货币对 |
| trader_no | varchar(16) | Y |  | 交易员简称 |
| trader_dir | varchar(16) | Y |  | 交易目录 |
| counterparty_name | varchar(16) | Y |  | 交易对手方 |
| add_type | bpchar(1) | Y |  | 增加方式:见tp_public_dict的034 |
| op_type | bpchar(1) | N | √ | 操作方式:见tp_public_dict的091 |
| his_trade_date | varchar(8) | Y |  | 历史成交日期 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 921. dimple.tt_kondor_match_jour　(21 字段)
> 表含义：Kondor成交上场流水表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| jour_no | float8 | N | √ | 流水号:ORACLE的seq |
| match_no | varchar(20) | N |  | 成交号 |
| seq_no | numeric(8,0) | N |  | 流水号 |
| bs_flag | bpchar(1) | N |  | 买卖方向:见tp_public_dict的002 |
| match_time | varchar(20) | Y |  | 录入时间 |
| price_usa | numeric(20,8) | Y |  | 价格(美元/盎司) |
| exchange_rate | numeric(9,4) | Y |  | 实时汇率 |
| price_cny | numeric(20,8) | Y |  | 价格(元/克) |
| qty | numeric(15,2) | Y |  | 数量（盎司） |
| amt | numeric(24,6) | Y |  | 交易金额（美元） |
| paris_currency | varchar(8) | N |  | 货币对 |
| trader_no | varchar(16) | Y |  | 交易员简称 |
| trader_dir | varchar(16) | Y |  | 交易目录 |
| counterparty_name | varchar(16) | Y |  | 交易对手方 |
| add_type | bpchar(1) | Y |  | 增加方式:见tp_public_dict的034 |
| op_type | bpchar(1) | N |  | 操作方式:见tp_public_dict的091 |
| his_trade_date | varchar(8) | Y |  | 历史成交日期 |
| status | bpchar(1) | N |  | 流水状态:见tp_public_dict的209 |
| enter_type | bpchar(1) | N |  | 上场类型(增加or删除):见tp_public_dict的091 |
| purpose_code | varchar(3) | Y |  | 交易目的 |

---

## 922. dimple.tt_location　(5 字段)
> 表含义：地区代码表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| location_code | varchar(4) | N | √ | 地区代码 |
| cname | varchar(80) | Y |  | 中文全称 |
| cabbr | varchar(40) | N |  | 中文简称 |
| ename | varchar(80) | Y |  | 英文全称 |
| eabbr | varchar(40) | N |  | 英文简称 |

---

## 923. dimple.tt_member　(13 字段)
> 表含义：会员表　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| member_abbr | varchar(50) | Y |  | 会员简称 |
| reused_count | numeric(12,0) | N | √ | 重用次数 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| invest_id | varchar(8) | N |  | 投资者号 |
| open_date | varchar(8) | Y |  | 开户日期 |
| status | bpchar(1) | N |  | 状态:见tp_public_dict的126 |
| logout_date | varchar(8) | Y |  | 销户日期 |
| logout_reason | varchar(2) | Y |  | 注销原因:见tp_public_dict的013 |
| op_date | varchar(8) | Y |  | 操作日期 |
| seat_type | varchar(3) | Y |  | 会员类型: 1 主板,2国际版;只金交所使用;见tp_public_dict的332 |
| if_quote | varchar(3) | Y |  | 是否上金所报价商席位：见tp_public_dict的027;只上金所使用 |
| spmmcateid | varchar(1) | Y |  | 组保客户分类代码:见tp_public_dict的478 |

---

## 924. dimple.tt_member_holder　(3 字段)
> 表含义：投资者股东信息表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 投资者 |
| holder_name | varchar(80) | N | √ | 股东单位名称 |
| ratio | numeric(10,6) | N |  | 股东投资比例 |

---

## 925. dimple.tt_member_notice　(9 字段)
> 表含义：会员服务系统通知表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| op_date | varchar(8) | N | √ | 操作日期 |
| seq_no | float8 | N | √ | 流水号 |
| start_date | varchar(8) | Y |  | 开始日期 |
| end_date | varchar(8) | Y |  | 结束日期 |
| notice_member | varchar(1000) | Y |  | 送达投资者:可为空；多个会员号时，以;分开 |
| notice_title | varchar(254) | Y |  | 通知主题 |
| notice_content | varchar(4000) | Y |  | 通知内容 |
| operator | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 926. dimple.tt_member_reg_rights　(4 字段)
> 表含义：会员开户权限表:控制会员的开户权限　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| reason | varchar(254) | Y |  | 原因 |
| op_date | varchar(8) | Y |  | 禁止开户设定日期 |
| operator | varchar(30) | Y |  | 操作员 |

---

## 927. dimple.tt_metal_offset_posi　(19 字段)
> 表含义：贵金属平盘实时头寸　|　估算行数：**6**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 席位代码 |
| client_id | varchar(16) | N |  | 客户代码 |
| paris_currency | varchar(8) | N |  | 货币对 |
| offset_buy_qty1 | numeric(24,8) | Y |  | 平盘买量:克 |
| offset_sell_qty1 | numeric(24,8) | Y |  | 平盘卖量:克 |
| net_offset_qty1 | numeric(24,8) | Y |  | 平盘轧差头寸:克 |
| t_offset_buy_qty1 | numeric(24,8) | Y |  | 今日平盘买量:克 |
| t_offset_sell_qty1 | numeric(24,8) | Y |  | 今日平盘卖量:克 |
| offset_buy_qty2 | numeric(24,8) | Y |  | 平盘买量:盎司;公式=上一日平盘买头寸 + 今日平盘买量 |
| offset_sell_qty2 | numeric(24,8) | Y |  | 平盘卖量:盎司;公式=上一日平盘卖头寸 + 今日平盘卖量 |
| net_offset_qty2 | numeric(24,8) | Y |  | 平盘轧差头寸:盎司 |
| t_offset_buy_qty2 | numeric(24,8) | Y |  | 今日平盘买量:盎司 |
| t_offset_sell_qty2 | numeric(24,8) | Y |  | 今日平盘卖量:盎司 |
| money_in | numeric(24,8) | Y |  | 平盘卖出收入金额：美元;公式=上一日平盘卖出收入头寸 + 今日平盘卖出收入金额 |
| money_out | numeric(24,8) | Y |  | 平盘买入支出金额：美元;公式=上一日平盘买入支出头寸 + 今日平盘买入支出金额 |
| net_money | numeric(24,8) | Y |  | 平盘轧差头寸：美元；公式=平盘卖出收入金额-平盘买入支出金额 |
| t_money_in | numeric(24,8) | Y |  | 今日平盘卖出收入金额：美元 |
| t_money_out | numeric(24,8) | Y |  | 今日平盘买入支出金额：美元 |

---

## 928. dimple.tt_monitor_target_alarm　(5 字段)
> 表含义：监控指标报警值表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| monitor_target | varchar(2) | N | √ | 监控指标:见tp_public_dict的082 |
| price_change_target_type | varchar(2) | N | √ | 价格变化指标类型:当监控指标是价格变化指标，此字段有效，取值为m1,m2,m3;其他指标填写0 |
| alarm_value | numeric(18,2) | Y |  | 报警值 |
| alarm_time | float8 | Y |  | 时间值 |
| alarm_msg | varchar(254) | Y |  | 报警信息 |

---

## 929. dimple.tt_offset_order_log　(17 字段)
> 表含义：强平操作留痕表:记录强平单调整前后的顺序。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| old_local_no | varchar(16) | N | √ | 原本地号 |
| local_no | varchar(16) | N |  | 本地号 |
| client_id | varchar(16) | N |  | 客户号 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| qty | numeric(12,0) | N |  | 数量 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| force_offset_reason | varchar(2) | Y |  | 强平原因:见tp_public_dict的040 |
| trader_no | varchar(16) | Y |  | 委托席位号 |
| batch_no | float8 | Y |  | 强平次数 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| if_send | bpchar(1) | Y |  | 是否发送成功 |
| self_trader_no | varchar(16) | Y |  | 内部本地席位号 |
| if_order | bpchar(1) | Y |  | 是否委托成功 |

---

## 930. dimple.tt_offset_order_match　(20 字段)
> 表含义：平盘委托成交当日表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_time | varchar(12) | Y |  | 时间 |
| offset_type | varchar(2) | N |  | 平盘类型：见tp_public_dict的405 |
| paris_currency | varchar(8) | N |  | 货币对 |
| offset_mode | varchar(2) | N |  | 平盘模式：见tp_public_dict的034 |
| offset_strategy | varchar(2) | Y |  | 平盘策略: 见tp_public_dict的406，手工没有平盘策略，自动默认1-普通 |
| offset_channel | varchar(50) | Y |  | 平盘方: 标注外资行,可为空 |
| member_id | varchar(8) | Y |  | 平盘席位号:美元平盘不填 |
| client_id | varchar(16) | Y |  | 平盘客户号:美元平盘不填 |
| local_no | varchar(64) | N | √ | 本地报单号:即本地流水号 |
| order_id | varchar(64) | Y |  | 订单号:接口返回，等同于外系统报单号;即系统委托号 |
| global_seq_no | varchar(64) | Y |  | 全局流水号 |
| offset_flag | varchar(2) | N |  | 平盘方向: 见tp_public_dict的002 |
| offset_qty1 | numeric(24,8) | Y |  | 平盘重量(克)：美元平盘不填 |
| offset_qty2 | numeric(24,8) | Y |  | 平盘重量(盎司)：美元平盘不填 |
| price | numeric(24,8) | Y |  | 成交价格：即成交汇率 |
| offset_amt1 | numeric(24,8) | Y |  | 平盘金额(元)：贵金属平盘不填 |
| offset_amt2 | numeric(24,8) | Y |  | 平盘金额(美元) |
| trade_state | varchar(2) | Y |  | 交易状态：见tp_public_dict的407 |
| trader_no | varchar(16) | Y |  | 操作员 |

---

## 931. dimple.tt_opt_client_posi　(23 字段)
> 表含义：期权交易持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(30) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |

---

## 932. dimple.tt_opt_contract　(17 字段)
> 表含义：期权合约表　|　估算行数：**320**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N |  | 交易所代码 |
| variety_id | varchar(4) | N |  | 品种代码 |
| currency | varchar(3) | N |  | 币种:见tp_public_dict的435 |
| trade_type | bpchar(1) | N |  | 产品类型:见tp_public_dict的001,此表只有1-期权 |
| op_trade_type | bpchar(1) | N |  | 期权类型:见tp_public_dict的328 |
| contract_id | varchar(30) | N | √ | 合约号 |
| ftr_contract_id | varchar(20) | N |  | 标的期货合约号 |
| ftr_con_yearmonth | varchar(10) | N |  | 标的期货合约年月 |
| strike_price | numeric(12,2) | Y |  | 执行价 |
| unit | float8 | N |  | 合约乘数 |
| price_unit | varchar(4) | Y |  | 报价单位:见tp_public_dict的357;根据交易品种处理au为元/克，ag为元/千克 |
| tick | numeric(16,8) | N |  | 最小变动价位 |
| limit_min_hand | float8 | N |  | 限价单最小下单量(手) |
| limit_max_hand | float8 | N |  | 限价单最大下单量(手) |
| end_trade_date | varchar(8) | Y |  | 到期日:接口推下来时调用场下新增合约SP计算，也可通过管理端"同步交易所"按钮去接口查询修改，也可以手工修改 |
| start_trade_date | varchar(8) | Y |  | 开始交易日期 |
| status | bpchar(1) | N |  | 合约状态:见tp_public_dict的104;新增合约默认1-已上市,初始化时，到期日<初始化日期，更新为2-已摘牌 |

---

## 933. dimple.tt_opt_posi_detail　(11 字段)
> 表含义：期权结算持仓明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(30) | N | √ | 合约号 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 934. dimple.tt_opt_posi_detail_purpose　(12 字段)
> 表含义：交易目的期权结算持仓明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 935. dimple.tt_opt_posi_detail_trader　(13 字段)
> 表含义：交易员期权结算持仓明细表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量（手） |

---

## 936. dimple.tt_opt_purpose_posi　(24 字段)
> 表含义：交易目的期权交易持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |

---

## 937. dimple.tt_opt_selfclose_order　(15 字段)
> 表含义：场上自营交易员自对冲申报表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| contract_id | varchar(30) | N |  | 合约号 |
| apply_time | varchar(12) | Y |  | 申请时间 |
| self_close_type | varchar(2) | Y |  | 自对冲类型:见tp_public_dict的433 |
| self_close_local_id | varchar(16) | N | √ | 本地自对冲编号 |
| self_close_sys_id | varchar(16) | Y |  | 系统自对冲编号 |
| exec_qty | numeric(10,0) | Y |  | 申请自对冲量 |
| status | varchar(2) | Y |  | 状态:见tp_public_dict的434 |
| cancel_trader_no | varchar(16) | Y |  | 撤销交易员 |
| cancel_time | varchar(12) | Y |  | 撤销时间 |
| self_trader_no | varchar(16) | N |  | 报盘委托席位号 |
| self_local_no | varchar(16) | N |  | 报盘本地委托号 |

---

## 938. dimple.tt_opt_trader_posi　(25 字段)
> 表含义：交易员期权交易持仓表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| last_buy_qty | numeric(12,0) | Y |  | 上日买持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日卖持仓量 |
| buy_qty_new | numeric(12,0) | Y |  | 今日新买持仓量 |
| sell_qty_new | numeric(12,0) | Y |  | 今日新卖持仓量 |
| buy_qty | numeric(12,0) | Y |  | 买持仓量 |
| sell_qty | numeric(12,0) | Y |  | 卖持仓量 |
| buy_amt | numeric(24,6) | Y |  | 买持仓额 |
| sell_amt | numeric(24,6) | Y |  | 卖持仓额 |
| buy_open_qty | numeric(12,0) | Y |  | 当日买开仓量 |
| sell_open_qty | numeric(12,0) | Y |  | 当日卖开仓量 |
| buy_offset_qty | numeric(12,0) | Y |  | 当日买平仓量 |
| sell_offset_qty | numeric(12,0) | Y |  | 当日卖平仓量 |
| buy_open_frozen_qty | numeric(12,0) | Y |  | 当日买开仓冻结 |
| sell_open_frozen_qty | numeric(12,0) | Y |  | 当日卖开仓冻结 |
| last_buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平昨仓冻结 |
| buy_offset_frozen_qty | numeric(12,0) | Y |  | 当日买平今仓冻结 |
| last_sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平昨仓冻结 |
| sell_offset_frozen_qty | numeric(12,0) | Y |  | 当日卖平今仓冻结 |

---

## 939. dimple.tt_order_manage　(4 字段)
> 表含义：定单管理表:在特定交易状态下支持哪些定单。　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_status | bpchar(1) | N |  | 交易状态:见tp_public_dict的089，这里的交易状态实际是交易阶段，一个阶段包括多个状态 |
| order_sort | varchar(2) | N |  | 定单类别:见tp_public_dict的005 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_attr | varchar(2) | Y |  | 定单属性:见tp_public_dict的006 |

---

## 940. dimple.tt_order_para　(14 字段)
> 表含义：委托参数表　|　估算行数：**20**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(40) | N | √ | 合约 |
| trader_no | varchar(30) | N | √ | 交易员 |
| min_hand | numeric(10,0) | Y |  | 最小下单手数 |
| max_hand | numeric(10,0) | Y |  | 最大下单手数 |
| price_diff | numeric(20,8) | Y |  | 价差 |
| op_date | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作员 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |
| if_trader_ctl | varchar(3) | Y |  | 是否控制交易员：见tp_public_dict的027 |

---

## 941. dimple.tt_order_para_check　(16 字段)
> 表含义：委托参数复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| contract_id | varchar(40) | Y |  | 合约 |
| min_hand | numeric(10,0) | Y |  | 最小下单手数 |
| max_hand | numeric(10,0) | Y |  | 最大下单手数 |
| price_diff | numeric(20,8) | Y |  | 价差 |
| op_date | varchar(8) | Y |  | 操作时间 |
| op_user | varchar(30) | Y |  | 操作员 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 942. dimple.tt_posi_change_alarm　(3 字段)
> 表含义：持仓变化报警量表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| member_id | varchar(8) | N | √ | 会员号 |
| contract_id | varchar(20) | N | √ | 合约号:可为期货合约，期权合约，品种代码 |
| posi_change_alarm | numeric(12,0) | N |  | 持仓变化报警量 |

---

## 943. dimple.tt_posi_detail　(15 字段)
> 表含义：交易持仓明细表:包括期货和期权.　|　估算行数：**120,079**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量:非套利数量 |
| arbi_qty | numeric(12,0) | Y |  | 套利数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |

---

## 944. dimple.tt_posi_detail_purpose　(16 字段)
> 表含义：交易目的持仓明细表:包括期货和期权.　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | N |  | 合约号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量:非套利数量 |
| arbi_qty | numeric(12,0) | Y |  | 套利数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |

---

## 945. dimple.tt_posi_detail_trader　(17 字段)
> 表含义：交易员持仓明细表:包括期货和期权.　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| match_date | varchar(8) | N | √ | 成交日期 |
| match_no | varchar(20) | N | √ | 成交号 |
| match_batch_no | varchar(20) | Y |  | 成交批次号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| exch_code | varchar(2) | N | √ | 交易所代码 |
| user_id | varchar(30) | N | √ | 交易员号 |
| contract_id | varchar(20) | N |  | 合约号 |
| arbi_contract_id | varchar(80) | Y |  | 套利合约号 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| price | numeric(20,8) | N |  | 成交价 |
| qty | numeric(12,0) | N |  | 数量:非套利数量 |
| margin_rate | numeric(18,2) | Y |  | 固定保证金 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| member_id | varchar(8) | Y |  | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |

---

## 946. dimple.tt_pre_order　(26 字段)
> 表含义：预委托表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| local_no | varchar(16) | N | √ | 本地委托号，强平单以FA开头 |
| tid | numeric(10,0) | N |  | TID:此值即为包中的SeqNo，便于追踪数据和恢复 |
| trader_no | varchar(16) | N | √ | 委托席位号:对强平单，填写操作员；其他的填写交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号:对强平单，填写操作员；其他的填写交易员 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| eo_flag | varchar(2) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | varchar(2) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| stop_price | numeric(9,2) | Y |  | 止损(盈)价 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| rechk_oper | varchar(30) | Y |  | 复核人 |
| rechk_time | varchar(12) | Y |  | 复核时间 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| umid | varchar(40) | Y |  | Um账号 |

---

## 947. dimple.tt_pre_strategy_order　(37 字段)
> 表含义：预备单表　|　估算行数：**4,223**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| local_pre_orderno | varchar(16) | N | √ | 本地预备单号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| exch_code | varchar(2) | N |  | 交易所代码 |
| arbi_contract_id | varchar(40) | Y |  | 套利合约号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | Y |  | 委托席位号:交易员 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号:交易员 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量 |
| ref_price_type | bpchar(1) | Y |  | 参考价类型：0-买一价，1-卖一价，2-最新价，3-最高价，4-最低价 |
| ref_price | numeric(20,8) | Y |  | 参考价 |
| stop_price | numeric(20,8) | Y |  | 止损(盈)价 |
| trig | bpchar(1) | Y |  | 触发条件：0-涨破，1-跌破 |
| trailingstop | numeric(20,8) | Y |  | 移动止损值 |
| eo_flag | bpchar(1) | N |  | 开平标志:见tp_public_dict的003 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N |  | 投保标志:见tp_public_dict的004 |
| order_attr | varchar(2) | N |  | 定单属性:见tp_public_dict的006 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_sort | varchar(2) | Y |  | 定单类别:见tp_public_dict的005 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态：0-已报入，1-已触发，2-已撤销，3-已失效 |
| valid_through | varchar(8) | Y |  | 有效时间约束 |
| trig_date | varchar(8) | Y |  | 触发日期 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_date | varchar(8) | Y |  | 撤单日期 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008,对于强平单有效，若非强平单填写'0' |
| if_mktmk | bpchar(1) | Y |  | 是否做市商下单 |
| trade_type | varchar(2) | Y |  | 交易类型 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| if_retain | bpchar(1) | N |  | 是否结算后保留 |
| trigmethod | bpchar(1) | Y |  | 触发方式:0-自动触发，1-开盘触发，2-手动触发 |

---

## 948. dimple.tt_quot_subs　(10 字段)
> 表含义：行情订阅表:用户订阅哪些行情数据.　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(16) | N | √ | 席位号 |
| trade_type | varchar(2) | N | √ | 交易类型:见tp_public_dict的001 |
| if_arbi | bpchar(1) | N | √ | 是否套利 |
| variety_id | varchar(4) | N | √ | 品种代码:对于套利，填写$；对于期货，期权存放品种代码 |
| series_id | varchar(80) | N | √ | 期权系列号:可能为空，用$代替。 对于套利,填写$；对于期货则填写$;对于期权填写系列号 |
| contract_id | varchar(20) | N | √ | 合约号:可能为空，用$代替。对于套利，存放$；对于期权，存放期权合约号；对于期货，存放期货合约号 |
| if_quot | bpchar(1) | N |  | 选择最优价行情 |
| mbl_level | float8 | N |  | MBL行情级别:1-5级,默认是5 |
| if_opt_para | bpchar(1) | Y |  | 选择期权参数 |
| if_clear_price | bpchar(1) | Y |  | 选择结算价 |

---

## 949. dimple.tt_quot_subs_det　(10 字段)
> 表含义：行情订阅解析表:初始化生成　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(16) | N | √ | 席位号 |
| contract_id | varchar(80) | N | √ | 合约号 |
| trade_type | varchar(2) | N |  | 交易类型:见tp_public_dict的001 |
| if_arbi | bpchar(1) | N |  | 是否套利 |
| variety_id | varchar(4) | Y |  | 品种代码 |
| series_id | varchar(80) | Y |  | 期权系列号 |
| if_quot | bpchar(1) | N |  | 选择最优价行情 |
| mbl_level | float8 | N |  | MBL行情级别:1-5级,默认是5 |
| if_opt_para | bpchar(1) | Y |  | 选择期权参数 |
| if_clear_price | bpchar(1) | Y |  | 选择结算价 |

---

## 950. dimple.tt_quote_err_order　(24 字段)
> 表含义：报价错误委托表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | N | √ | 委托交易员 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | N | √ | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量：手 |
| match_qty | numeric(12,0) | Y |  | 成交量：手 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_trader_no | varchar(16) | Y |  | 撤单席位号 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| cancel_qty | numeric(12,0) | Y |  | 撤单量：手 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |
| if_checked | varchar(2) | Y |  | 是否经过检查 |
| reason | varchar(254) | Y |  | 错误原因 |

---

## 951. dimple.tt_quote_match　(13 字段)
> 表含义：报价交易成交表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 成交日期 |
| member_id | varchar(8) | N | √ | 席位代码 |
| client_id | varchar(16) | Y |  | 客户代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| match_time | varchar(12) | Y |  | 成交时间 |
| match_no | varchar(20) | N | √ | 报价成交编号 |
| bs_flag | varchar(3) | N | √ | 买卖方向:见tp_public_dict的002 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| price | numeric(20,8) | Y |  | 价格：元/克 |
| qty | numeric(12,0) | Y |  | 数量：手 |
| order_no | varchar(20) | Y |  | 系统委托号 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | Y |  | 本地委托号 |

---

## 952. dimple.tt_quote_order　(22 字段)
> 表含义：报价委托表:影响成交，行情，持仓　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| order_no | varchar(20) | N | √ | 系统委托号 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(20) | Y |  | 合约号 |
| trader_no | varchar(16) | Y |  | 委托交易员 |
| order_batch_no | numeric(10,0) | Y |  | 委托批次号 |
| local_no | varchar(16) | Y |  | 本地委托号 |
| price | numeric(20,8) | N |  | 价格 |
| qty | numeric(12,0) | N |  | 数量：手 |
| match_qty | numeric(12,0) | Y |  | 成交量：手 |
| bs_flag | bpchar(1) | N |  | 买卖标志:见tp_public_dict的002 |
| order_type | varchar(2) | Y |  | 定单类型:见tp_public_dict的007 |
| order_time | varchar(12) | Y |  | 委托时间 |
| status | bpchar(1) | N |  | 委托状态:见tp_public_dict的010 |
| trig_time | varchar(12) | Y |  | 触发时间 |
| cancel_trader_no | varchar(16) | Y |  | 撤单交易员 |
| cancel_time | varchar(12) | Y |  | 撤单时间 |
| cancel_qty | numeric(12,0) | Y |  | 撤单量：手 |
| order_src | varchar(2) | Y |  | 定单来源:见tp_public_dict的008 |
| self_trader_no | varchar(16) | Y |  | 内部委托席位号 |
| self_local_no | varchar(16) | Y |  | 内部本地委托号 |

---

## 953. dimple.tt_quoter_quot　(10 字段)
> 表含义：报价商报价行情表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| market_no | numeric(2,0) | Y |  | 市场编号：报价保证金市场使用60 |
| contract_no | numeric(8,0) | N | √ | 合约编码：mkt_no(2位)+2位自增序号 |
| ask_price | numeric(12,6) | Y |  | 卖价 |
| bid_price | numeric(12,6) | Y |  | 买价 |
| ask_lot | numeric(12,0) | Y |  | 卖量 |
| bid_lot | numeric(12,0) | Y |  | 买量 |
| quote_date | varchar(8) | N | √ | 行情日期 |
| quote_time | varchar(8) | Y |  | 行情时间 |
| natual_date | varchar(8) | Y |  | 自然日期 |
| seq_no | numeric(32,0) | N | √ | 流水号 |

---

## 954. dimple.tt_rfq_breach　(9 字段)
> 表含义：保证金询价实时违约申报表(会员)　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约代码 |
| trader_no | varchar(16) | Y |  | 交易员 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| due_date | varchar(8) | N | √ | 到期日 |
| breach_qty | numeric(12,0) | Y |  | 违约申报量 |
| status | varchar(2) | Y |  | 申报状态:见tp_public_dict的440 |
| apply_time | varchar(12) | Y |  | 申报时间 |
| long_posi | numeric(12,0) | Y |  | 多头持仓数量 |

---

## 955. dimple.tt_rfq_breach_jour　(10 字段)
> 表含义：保证金询价实时违约申报表(操作员)　|　估算行数：**2**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N |  | 合约代码 |
| trader_no | varchar(16) | N | √ | 交易员 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| due_date | varchar(8) | N |  | 到期日 |
| breach_qty | numeric(12,0) | Y |  | 违约申报量 |
| status | varchar(2) | Y |  | 申报状态:见tp_public_dict的440 |
| apply_time | varchar(12) | Y |  | 申报时间 |
| long_posi | numeric(12,0) | Y |  | 多头持仓数量 |
| local_no | varchar(20) | N | √ | 本地报单编号 |

---

## 956. dimple.tt_rfq_unchmatch　(35 字段)
> 表含义：保证金询价实时待确认成交单表　|　估算行数：**9**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| trader_no | varchar(16) | Y |  | 交易员 |
| purpose_code | varchar(3) | Y |  | 交易目的 |
| trade_type | varchar(2) | Y |  | 交易类型:见tp_public_dict的253 |
| member_id | varchar(8) | Y |  | 本方席位代码 |
| client_id | varchar(16) | Y |  | 本方客户代码 |
| broker_id | varchar(10) | Y |  | 本方经纪机构 |
| party_member_id | varchar(8) | Y |  | 对方席位代码 |
| party_client_id | varchar(16) | Y |  | 对方客户代码 |
| party_broker_id | varchar(10) | Y |  | 对方经纪机构 |
| party_trader_no | varchar(16) | Y |  | 对方交易员 |
| match_date | varchar(8) | Y |  | 成交日期 |
| contract_id | varchar(20) | Y |  | 合约代码 |
| contract_no | numeric(12,0) | Y |  | 合约编号 |
| bs_flag | varchar(2) | N | √ | 买卖方向:见tp_public_dict的002 |
| qty | numeric(12,0) | Y |  | 数量 |
| weight | numeric(12,6) | Y |  | 重量 |
| price | numeric(12,6) | Y |  | 价格 |
| due_date | varchar(8) | Y |  | 到期日 |
| ternor_name | varchar(8) | Y |  | 期限 |
| add_clause | varchar(200) | Y |  | 附加条款 |
| far_due_date | varchar(8) | Y |  | 远端到期日 |
| far_ternor_name | varchar(8) | Y |  | 远期期限 |
| far_price | numeric(12,6) | Y |  | 远端价格 |
| local_no | varchar(20) | Y |  | 本地待确认成交单编号 |
| apply_date | varchar(8) | Y |  | 申报日期 |
| apply_time | varchar(20) | Y |  | 申报时间 |
| unchmatch_no | varchar(20) | N | √ | 待确认成交单编号 |
| force_order_flag | varchar(2) | Y |  | 是否强平:见tp_public_dict的027 |
| match_type | varchar(2) | Y |  | 成交类型:见tp_public_dict的436 |
| client_confirm_state | varchar(2) | Y |  | 客户确认状态:见tp_public_dict的443 |
| member_confirm_state | varchar(2) | Y |  | 会员确认状态:见tp_public_dict的442 |
| sge_confirm_state | varchar(2) | Y |  | 交易所确认状态:见tp_public_dict的380 |
| confirm_state | varchar(2) | Y |  | 确认状态:见tp_public_dict的441 |
| reg_submit | varchar(2) | Y |  | 登记提交方:见tp_public_dict的439 |

---

## 957. dimple.tt_self_match_alarm　(2 字段)
> 表含义：自成交报警量表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约号:可为期货合约，期权合约，品种代码 |
| self_match_alarm | numeric(12,0) | N |  | 自成交报警量 |

---

## 958. dimple.tt_sge_inquire_bulletin　(8 字段)
> 表含义：场外询价业务平台推送公告表　|　估算行数：**26**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| prom_date | varchar(8) | N |  | 发布日期 |
| prom_time | varchar(8) | Y |  | 发布时间 |
| seq_no | numeric(32,0) | Y |  | 公告流水号 |
| title | varchar(100) | Y |  | 公告标题 |
| content | varchar(1024) | Y |  | 公告内容 |
| language_type | varchar(1) | Y |  | 语言类型：见tp_public_dict的377 |
| if_read | varchar(1) | Y |  | 是否已阅读：见tp_public_dict的027 |
| exch_code | varchar(6) | N |  | 交易所代码 |

---

## 959. dimple.tt_srcb_accumugold_match　(26 字段)
> 表含义：上海农商行-积存金申赎表　|　估算行数：**19**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| source_id | varchar(2) | N |  | 交易渠道：见tp_public_dict的361 |
| member_id | varchar(8) | N |  | 会员号 |
| client_id | varchar(16) | N |  | 客户号 |
| contract_id | varchar(50) | Y |  | 积存金合约代码 |
| contract_name | varchar(50) | N |  | 积存金合约名称/合约类型 |
| trade_type | varchar(2) | N |  | 积存金交易类型：见tp_public_dict的362 |
| trade_direction | varchar(2) | N |  | 交易方向：见tp_public_dict的363 |
| dpp_qty | numeric(28,6) | N |  | 待平盘交易量：克 |
| ref_price | numeric(24,2) | N |  | 报价基准价：元/克 |
| apply_price | numeric(24,2) | N |  | 客户申购价：元/克 |
| ransom_price | numeric(24,2) | N |  | 客户赎回价：元/克 |
| trader_no | varchar(16) | N |  | 交易员 |
| purpose_code | varchar(3) | N |  | 交易目的 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 修改人 |
| update_date | varchar(8) | Y |  | 修改日期 |
| update_time | varchar(8) | Y |  | 修改时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |

---

## 960. dimple.tt_srcb_accumugold_match_jour　(16 字段)
> 表含义：上海农商行-积存金申赎流水表：JOUR_NO上场使用　|　估算行数：**69**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| jour_no | float8 | N | √ | 流水号 |
| seq_no | float8 | N |  | 序号 |
| trade_date | varchar(8) | N |  | 交易日期 |
| member_id | varchar(8) | N |  | 会员号 |
| contract_name | varchar(50) | N |  | 积存金合约名称/合约类型 |
| trade_type | varchar(2) | N |  | 积存金交易类型：见tp_public_dict的362 |
| trade_direction | varchar(2) | N |  | 交易方向：见tp_public_dict的363 |
| dpp_qty | numeric(28,6) | N |  | 待平盘交易量：克 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |
| oper_type | varchar(3) | Y |  | 上场时操作类型：见Dict的265 |
| status | varchar(1) | Y |  | 流水状态:见tp_public_dict的209 |
| op_id | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 961. dimple.tt_srcb_accumulate_gold　(27 字段)
> 表含义：上海农商行-积存金合约表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(50) | N | √ | 积存金合约代码 |
| contract_name | varchar(50) | N |  | 积存金合约名称/合约类型 |
| variety_id | varchar(4) | N |  | 品种代码 |
| currency | varchar(3) | N |  | 币种:见tp_public_dict的036 |
| max_amt | numeric(24,2) | N |  | 最大下单金额：元 |
| min_amt | numeric(24,2) | N |  | 最小下单金额：元 |
| max_weight | numeric(24,4) | Y |  | 最大下单重量：克 |
| min_weight | numeric(24,4) | Y |  | 最小下单重量：克 |
| value_contract_id | varchar(20) | N |  | 估值标的：合约 |
| value_coefficient | numeric(24,2) | N |  | 估值系数 |
| exp_contract_id | varchar(20) | N |  | 敞口标的：合约 |
| exp_coefficient | numeric(24,2) | N |  | 敞口系数 |
| period | float8 | N |  | 存期：个月 |
| apply_diff | numeric(24,2) | Y |  | 申购点差：元/克 |
| ransom_diff | numeric(24,2) | Y |  | 赎回点差：元/克 |
| expect_yield | numeric(24,2) | N |  | 预期收益率：% |
| status | bpchar(1) | N |  | 积存金合约状态:见tp_public_dict的359 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 修改人 |
| update_date | varchar(8) | Y |  | 修改日期 |
| update_time | varchar(8) | Y |  | 修改时间 |
| check_id | varchar(30) | Y |  | 复核人员 |
| check_date | varchar(8) | Y |  | 复核日期 |
| check_time | varchar(8) | Y |  | 复核时间 |
| check_status | varchar(3) | Y |  | 复核状态：见tp_public_dict的282 |

---

## 962. dimple.tt_storage_setting　(4 字段)
> 表含义：库存检查设置　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| delivery_variety_id | bpchar(10) | N | √ | 交割品种代码 |
| check_flag | bpchar(10) | N | √ | 是否检查:见tp_public_dict的027 |
| op_user | bpchar(10) | Y |  | 操作人员 |
| op_time | bpchar(10) | Y |  | 操作时间 |

---

## 963. dimple.tt_trade_date　(1 字段)
> 表含义：交易日期表:交易初始化时写入交易日，整个系统取交易日期用。　|　估算行数：**1,470**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |

---

## 964. dimple.tt_trade_money　(59 字段)
> 表含义：交易资金表:场上控制资金用，资金控制到结算帐号。初始化时，从结算资金表得到数据。　|　估算行数：**4**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| currency | varchar(3) | N | √ | 币种 |
| last_remain | numeric(18,2) | Y |  | 上日结存 |
| init_margin | numeric(18,2) | Y |  | 初始保证金 |
| margin | numeric(18,2) | Y |  | 交易保证金 |
| bs_open_occupied_margin | numeric(18,2) | Y |  | 买投开仓占用保证金(单腿) |
| bh_open_occupied_margin | numeric(18,2) | Y |  | 买保开仓占用保证金(单腿) |
| ba_open_occupied_margin | numeric(18,2) | Y |  | 买套开仓占用保证金(单腿) |
| ss_open_occupied_margin | numeric(18,2) | Y |  | 卖投开仓占用保证金(单腿) |
| sh_open_occupied_margin | numeric(18,2) | Y |  | 卖保开仓占用保证金(单腿) |
| sa_open_occupied_margin | numeric(18,2) | Y |  | 卖套开仓占用保证金(单腿) |
| buy_add_margin | numeric(18,2) | Y |  | 组合平仓后买加收保证金(单腿) |
| sell_add_margin | numeric(18,2) | Y |  | 组合平仓后卖加收保证金(单腿) |
| bs_open_frozen_margin | numeric(18,2) | Y |  | 买投开仓冻结保证金(单腿) |
| bh_open_frozen_margin | numeric(18,2) | Y |  | 买保开仓冻结保证金(单腿) |
| ba_open_frozen_margin | numeric(18,2) | Y |  | 买套开仓冻结保证金(单腿) |
| ss_open_frozen_margin | numeric(18,2) | Y |  | 卖投开仓冻结保证金(单腿) |
| sh_open_frozen_margin | numeric(18,2) | Y |  | 卖保开仓冻结保证金(单腿) |
| sa_open_frozen_margin | numeric(18,2) | Y |  | 卖套开仓冻结保证金(单腿) |
| bs_return_margin | numeric(18,2) | Y |  | 买投平昨仓返回保证金(单腿) |
| bh_return_margin | numeric(18,2) | Y |  | 买保平昨仓返回保证金(单腿) |
| ba_return_margin | numeric(18,2) | Y |  | 买套平昨仓返回保证金(单腿) |
| ss_return_margin | numeric(18,2) | Y |  | 卖投平昨仓返回保证金(单腿) |
| sh_return_margin | numeric(18,2) | Y |  | 卖保平昨仓返回保证金(单腿) |
| sa_return_margin | numeric(18,2) | Y |  | 卖套平昨仓返回保证金(单腿) |
| ptfl_open_occupied_margin | numeric(18,2) | Y |  | 开仓占用保证金(组合) |
| ptfl_open_frozen_margin | numeric(18,2) | Y |  | 开仓冻结保证金(组合) |
| ptfl_return_margin | numeric(18,2) | Y |  | 平昨仓返回保证金(组合) |
| bs_offset_profit | numeric(18,2) | Y |  | 买投平仓盈亏(全) |
| bh_offset_profit | numeric(18,2) | Y |  | 买保平仓盈亏(全) |
| ba_offset_profit | numeric(18,2) | Y |  | 买套平仓盈亏(全) |
| ss_offset_profit | numeric(18,2) | Y |  | 卖投平仓盈亏(全) |
| sh_offset_profit | numeric(18,2) | Y |  | 卖保平仓盈亏(全) |
| sa_offset_profit | numeric(18,2) | Y |  | 卖套平仓盈亏(全) |
| bs_turnover | numeric(18,2) | Y |  | 买投成交额(全) |
| bh_turnover | numeric(18,2) | Y |  | 买保成交额(全) |
| ba_turnover | numeric(18,2) | Y |  | 买套成交额(全) |
| ss_turnover | numeric(18,2) | Y |  | 卖投成交额(全) |
| sh_turnover | numeric(18,2) | Y |  | 卖保成交额(全) |
| sa_turnover | numeric(18,2) | Y |  | 卖套成交额(全) |
| today_in | numeric(18,2) | Y |  | 当日入金 |
| today_out | numeric(18,2) | Y |  | 当日出金 |
| frozen_premium | numeric(18,2) | Y |  | 冻结权利金 |
| buy_premium | numeric(18,2) | Y |  | 权利金支出 |
| sell_premium | numeric(18,2) | Y |  | 权利金收入 |
| avail | numeric(18,2) | Y |  | 可用资金:=上日结存＋当日入金－当日出金－开仓冻结保证金(单腿和组合)－组合平仓后加收保证金－冻结权利金－开仓占用保证金＋平昨仓返回保证金(单腿和组合)＋平仓盈亏＋权利金收入－权利金支出 |
| buy_amount | numeric(18,2) | Y |  | 买货款 |
| sell_amount | numeric(18,2) | Y |  | 卖货款 |
| frozen_profitloss | numeric(18,2) | Y |  | 盈亏冻结 |
| frozen_amount | numeric(18,2) | Y |  | 货款冻结 |
| swap_margin | numeric(18,2) | Y |  | 掉期保证金 |
| uniltr_margin | numeric(18,2) | Y |  | 单边保证金 |
| uniltr_margin_occupied | numeric(18,2) | Y |  | 单边占用保证金 |
| uniltr_frozen_margin | numeric(18,2) | Y |  | 单边冻结保证金 |
| deli_margin_occupied | numeric(18,2) | Y |  | 交割占用保证金 |
| deli_frozen_margin | numeric(18,2) | Y |  | 交割冻结保证金 |
| inq_offset_profitloss | numeric(18,2) | Y |  | 保证金询价平仓盈亏 |

---

## 965. dimple.tt_trader_money　(41 字段)
> 表含义：交易员资金表:场上控制资金用，资金控制到交易员。初始化时，从结算资金表得到数据。　|　估算行数：**72**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所 |
| member_id | varchar(8) | N | √ | 会员号 |
| trader_no | varchar(30) | N | √ | 交易员号 |
| currency | varchar(3) | N | √ | 币种 |
| bs_open_occupied_margin | numeric(18,2) | Y |  | 买投开仓占用保证金(单腿) |
| bh_open_occupied_margin | numeric(18,2) | Y |  | 买保开仓占用保证金(单腿) |
| ba_open_occupied_margin | numeric(18,2) | Y |  | 买套开仓占用保证金(单腿) |
| ss_open_occupied_margin | numeric(18,2) | Y |  | 卖投开仓占用保证金(单腿) |
| sh_open_occupied_margin | numeric(18,2) | Y |  | 卖保开仓占用保证金(单腿) |
| sa_open_occupied_margin | numeric(18,2) | Y |  | 卖套开仓占用保证金(单腿) |
| bs_open_frozen_margin | numeric(18,2) | Y |  | 买投开仓冻结保证金(单腿) |
| bh_open_frozen_margin | numeric(18,2) | Y |  | 买保开仓冻结保证金(单腿) |
| ba_open_frozen_margin | numeric(18,2) | Y |  | 买套开仓冻结保证金(单腿) |
| ss_open_frozen_margin | numeric(18,2) | Y |  | 卖投开仓冻结保证金(单腿) |
| sh_open_frozen_margin | numeric(18,2) | Y |  | 卖保开仓冻结保证金(单腿) |
| sa_open_frozen_margin | numeric(18,2) | Y |  | 卖套开仓冻结保证金(单腿) |
| bs_offset_profit_total | numeric(18,2) | Y |  | 买投平仓累计盈亏(全) |
| bh_offset_profit_total | numeric(18,2) | Y |  | 买保平仓累计盈亏(全) |
| ba_offset_profit_total | numeric(18,2) | Y |  | 买套平仓累计盈亏(全) |
| ss_offset_profit_total | numeric(18,2) | Y |  | 卖投平仓累计盈亏(全) |
| sh_offset_profit_total | numeric(18,2) | Y |  | 卖保平仓累计盈亏(全) |
| sa_offset_profit_total | numeric(18,2) | Y |  | 卖套平仓累计盈亏(全) |
| bs_open_occupied_premium | numeric(19,2) | Y |  | 买投开仓权利金支出 |
| bh_open_occupied_premium | numeric(19,2) | Y |  | 买保开仓权利金支出 |
| bs_offset_occupied_premium | numeric(19,2) | Y |  | 买投平仓权利金支出 |
| bh_offset_occupied_premium | numeric(19,2) | Y |  | 买保平仓权利金支出 |
| bs_open_frozen_premium | numeric(19,2) | Y |  | 买投开仓冻结权利金 |
| bh_open_frozen_premium | numeric(19,2) | Y |  | 买保开仓冻结权利金 |
| bs_offset_frozen_premium | numeric(19,2) | Y |  | 买投平仓冻结权利金 |
| bh_offset_frozen_premium | numeric(19,2) | Y |  | 买保平仓冻结权利金 |
| ss_open_receive_premium | numeric(19,2) | Y |  | 卖投开仓权利金收入 |
| sh_open_receive_premium | numeric(19,2) | Y |  | 卖保开仓权利金收入 |
| ss_offset_receive_premium | numeric(19,2) | Y |  | 卖投平仓权利金收入 |
| sh_offset_receive_premium | numeric(19,2) | Y |  | 卖保平仓权利金收入 |
| swap_margin | numeric(18,2) | Y |  | 掉期保证金 |
| uniltr_margin | numeric(18,2) | Y |  | 单边保证金 |
| uniltr_margin_occupied | numeric(18,2) | Y |  | 单边占用保证金 |
| uniltr_frozen_margin | numeric(18,2) | Y |  | 单边冻结保证金 |
| deli_margin_occupied | numeric(18,2) | Y |  | 交割占用保证金 |
| deli_frozen_margin | numeric(18,2) | Y |  | 交割冻结保证金 |
| inq_offset_profitloss | numeric(18,2) | Y |  | 保证金询价平仓盈亏 |

---

## 966. dimple.tt_trader_opt_exec　(15 字段)
> 表含义：场上交易员期权行权汇总表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| exch_code | varchar(2) | N | √ | 交易所代码 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | N | √ | 客户号 |
| user_id | varchar(30) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| contract_id | varchar(30) | N | √ | 合约号 |
| bs_flag | bpchar(1) | N | √ | 买卖标志:见tp_public_dict的002 |
| sh_flag | bpchar(1) | N | √ | 投保标志:见tp_public_dict的004 |
| exec_qty | numeric(10,0) | Y |  | 已申请执行量 |
| last_exec_qty | numeric(10,0) | Y |  | 已申请执行昨量 |
| today_exec_qty | numeric(10,0) | Y |  | 已申请执行今量 |
| self_close_qty | numeric(10,0) | Y |  | 执行后期货自对冲量 |
| abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃量 |
| last_abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃昨量 |
| today_abandon_exec_qty | numeric(10,0) | Y |  | 已申请放弃今量 |

---

## 967. dimple.tt_trader_orderrechk　(9 字段)
> 表含义：交易员订单复核设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| user_id | varchar(30) | N | √ | 交易员号 |
| if_chk | bpchar(1) | Y |  | 订单是否复核 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| operator | varchar(30) | Y |  | 操作员 |
| if_credit_control | bpchar(1) | Y |  | 是否事前信用额度控制:见TP_PUBLIC_DICT的027 |
| if_vaexp_control | bpchar(1) | Y |  | 是否事前敞口控制:见TP_PUBLIC_DICT的027 |
| if_rule_control | bpchar(1) | Y |  | 是否规则控制:见TP_PUBLIC_DICT的027 |
| if_mkt_order_support | bpchar(1) | Y |  | 是否支持市价单:见TP_PUBLIC_DICT的027 |

---

## 968. dimple.tt_trader_rfq_posi　(21 字段)
> 表含义：保证金询价自营交易员持仓实时表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| contract_id | varchar(20) | N | √ | 合约代码 |
| contract_no | numeric(12,0) | Y |  | 合约编号 |
| member_id | varchar(8) | N | √ | 会员号 |
| client_id | varchar(16) | Y |  | 客户号 |
| trader_no | varchar(16) | N | √ | 交易员 |
| purpose_code | varchar(3) | N | √ | 交易目的 |
| due_date | varchar(8) | N | √ | 到期日 |
| last_buy_qty | numeric(12,0) | Y |  | 上日多头持仓量 |
| last_sell_qty | numeric(12,0) | Y |  | 上日空头持仓量 |
| last_net_qty | numeric(12,0) | Y |  | 上日净持仓量 |
| today_buy_qty | numeric(12,0) | Y |  | 当日买量 |
| today_sell_qty | numeric(12,0) | Y |  | 当日卖量 |
| today_buy_amt | numeric(18,2) | Y |  | 当日买额 |
| today_sell_amt | numeric(18,2) | Y |  | 当日卖额 |
| buy_qty | numeric(12,0) | Y |  | 多头持仓量 |
| sell_qty | numeric(12,0) | Y |  | 空头持仓量 |
| net_qty | numeric(12,0) | Y |  | 净持仓量 |
| profitloss | numeric(18,2) | Y |  | 盈亏 |
| delivery_margin | numeric(18,2) | Y |  | 交割保证金：到期日=下一交易日 |
| buy_amt | numeric(18,2) | Y |  | 买额 |
| sell_amt | numeric(18,2) | Y |  | 卖额 |

---

## 969. dimple.tt_trader_right　(8 字段)
> 表含义：席位交易权限表　|　估算行数：**58**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(16) | N | √ | 席位号:可为$ |
| member_id | varchar(8) | N | √ | 会员号:可为$ |
| trade_type | varchar(2) | N | √ | 交易类型:见tp_public_dict的001；可为$ |
| variety_id | varchar(4) | N | √ | 品种代码:可为$ |
| contract_id | varchar(20) | N | √ | 合约号:可为$ |
| trade_right | varchar(2) | N |  | 交易权限:见tp_public_dict的021 |
| if_alarm | varchar(3) | Y |  | 是否已预警:见Tp_public_dict的027 |
| pre_trade_right | varchar(2) | Y |  | 前交易权限:见tp_public_dict的021 |

---

## 970. dimple.tt_trader_right_seq　(11 字段)
> 表含义：席位交易权限操作流水表　|　估算行数：**450**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N | √ | 交易日期 |
| seq_no | float8 | N | √ | 流水号 |
| trader_no | varchar(16) | N |  | 席位号:可为$ |
| member_id | varchar(8) | N |  | 会员号:不可为$ |
| trade_type | varchar(2) | N |  | 交易类型:见tp_public_dict的001；可为$ |
| variety_id | varchar(4) | N |  | 品种代码:可为$ |
| contract_id | varchar(20) | N |  | 合约号:可为$ |
| trade_right | varchar(2) | Y |  | 交易权限:见tp_public_dict的021 |
| op_type | bpchar(1) | N |  | 操作类型:见tp_public_dict的091 |
| operator | varchar(30) | Y |  | 操作员 |
| op_time | varchar(8) | Y |  | 操作时间 |

---

## 971. dimple.tt_trader_subs_attr　(5 字段)
> 表含义：席位订阅属性表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trader_no | varchar(16) | N | √ | 席位号 |
| start_time | varchar(8) | N |  | 起始有效时间 |
| end_time | varchar(8) | Y |  | 终止有效时间:为空表示无限大 |
| send_inter | numeric(10,6) | N |  | 发送间隔（秒） |
| send_timeout | numeric(10,6) | N |  | 发送延时（秒） |

---

## 972. dimple.tt_usd_offset_posi　(18 字段)
> 表含义：美元平盘实时头寸　|　估算行数：**1**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| trade_date | varchar(8) | N |  | 交易日期 |
| currency | varchar(3) | N |  | 货币：USD |
| metal_money_in | numeric(24,8) | Y |  | 贵金属平盘卖出收入金额：美元;公式=上一日贵金属平盘卖出收入头寸 + 今日贵金属平盘卖出收入金额 |
| metal_money_out | numeric(24,8) | Y |  | 贵金属平盘买入支出金额：美元;公式=上一日贵金属平盘买入支出头寸 + 今日贵金属平盘买入支出金额 |
| metal_net_money | numeric(24,8) | Y |  | 贵金属平盘轧差头寸：美元；公式=平盘卖出收入金额-平盘买入支出金额 |
| t_metal_money_in | numeric(24,8) | Y |  | 今日贵金属平盘卖出收入金额：美元 |
| t_metal_money_out | numeric(24,8) | Y |  | 今日贵金属平盘买入支出金额：美元 |
| usd_buy_amt1 | numeric(24,8) | Y |  | 美元平盘买入金额：美元;公式=上一日美元平盘买入头寸 + 今日美元平盘买入金额 |
| usd_sell_amt1 | numeric(24,8) | Y |  | 美元平盘卖出金额：美元;公式=上一日美元平盘卖出头寸 + 今日美元平盘卖出金额 |
| usd_net_amt1 | numeric(24,8) | Y |  | 美元平盘轧差头寸：美元 |
| t_usd_buy_amt1 | numeric(24,8) | Y |  | 今日美元平盘买入金额：美元 |
| t_usd_sell_amt1 | numeric(24,8) | Y |  | 今日美元平盘卖出金额：美元 |
| usd_noffset_amt1 | numeric(24,8) | Y |  | 美元待平金额：美元 |
| usd_buy_amt2 | numeric(24,8) | Y |  | 美元平盘买入金额：元；单位从美元换算成元 |
| usd_sell_amt2 | numeric(24,8) | Y |  | 美元平盘卖出金额：元；单位换算 |
| usd_net_amt2 | numeric(24,8) | Y |  | 美元平盘轧差头寸：元；单位换算 |
| t_usd_buy_amt2 | numeric(24,8) | Y |  | 今日美元平盘买入金额：元；单位换算 |
| t_usd_sell_amt2 | numeric(24,8) | Y |  | 今日美元平盘卖出金额：元；单位换算 |

---

## 973. dimple.tt_variety_exch　(2 字段)
> 表含义：品种交易所关系表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| variety_id | varchar(4) | N | √ | 品种代码 |
| exch_code | varchar(6) | N | √ | 交易所代码 |

---

## 974. dimple.tt_variety_exposure　(10 字段)
> 表含义：品种敞口设置表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| variety_id | varchar(4) | N | √ | 品种代码 |
| exposure_unit | varchar(20) | Y |  | 敞口单位描述:见tp_public_dict的216 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| create_id | varchar(30) | Y |  | 新建人 |
| create_date | varchar(8) | Y |  | 新建日期 |
| create_time | varchar(8) | Y |  | 新建时间 |
| update_id | varchar(30) | Y |  | 复核人 |
| update_date | varchar(8) | Y |  | 复核日期 |
| update_time | varchar(8) | Y |  | 复核时间 |

---

## 975. dimple.tt_variety_exposure_check　(14 字段)
> 表含义：品种敞口设置复核表　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| seq_no | float8 | N | √ | 序号：自增 |
| variety_id | varchar(4) | N |  | 品种代码 |
| exposure_unit | varchar(20) | Y |  | 敞口单位描述 |
| op_date | varchar(8) | Y |  | 操作日期 |
| op_time | varchar(8) | Y |  | 操作时间 |
| check_status | varchar(3) | Y |  | 复核状态：见Dict的264 |
| oper_type | varchar(3) | Y |  | 操作类型：见Dict的265 |
| remark | varchar(255) | Y |  | 备注 |
| create_id | varchar(30) | Y |  | 创建人 |
| create_date | varchar(8) | Y |  | 创建日期 |
| create_time | varchar(8) | Y |  | 创建时间 |
| update_id | varchar(30) | Y |  | 更新人 |
| update_date | varchar(8) | Y |  | 更新日期 |
| update_time | varchar(8) | Y |  | 更新时间 |

---

## 976. dimple.v_cnt　(1 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| count | numeric(64,0) | Y |  |  |

---

## 977. dimple.v_count　(1 字段)
> 表含义：（无注释）　|　估算行数：**0**

| 字段名 | 类型 | 可空 | 主键 | 字段含义 |
|---|---|---|---|---|
| count | numeric(64,0) | Y |  |  |

---
