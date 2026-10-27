# Java dimple（清算服务）报错结构全量清单

> 生成时间：2026-10-27 | 数据来源：dimple Java 服务全部 `throw new ...Exception("消息")` 提取
> 抛出机制：真异常对象 throw new，全局 `EnhanceExceptionHandler` 兜底转 ErrorResponse
> 总条数：throw 点 **236** / 去重消息 **185** 条 / 异常类型 **18** 种
---

## 0. 总览（异常类型分布）

| 异常类型 | throw 点数 | 去重消息数 | 说明 |
|---|---|---|---|
| BusinessException | 129 | 111 | 业务异常，中文消息，主清单 |
| ManagementException | 85 | 54 | 看板只读查询异常，多为枚举码 |
| IllegalArgumentException | 11 | 10 | 参数校验 |
| RuntimeException | 5 | 4 | 运行时（导出文件失败等） |
| IllegalStateException | 5 | 5 | 状态非法 |
| ExchFileNotFoundException | 1 | 1 | 交易所文件缺失 |
| **合计** | **236** | **185** | |

---

## 1. BusinessException　(111 条去重消息 / 129 个 throw 点)
> 含 `{}` 占位符的消息写 runbook 时需 param_alias 归一化。

| # | 异常消息 | 出现次数 | 首个来源文件 |
|---|---|---|---|
| 1 | 当前收件人邮件信息已存在，请重新填写。 | 4 | ReceiverManageServiceImpl.java:56 |
| 2 | 试算通过材料文件保存失败 | 3 | HomeInquireConfirmManageController.java:116 |
| 3 | 生成业务提示用户清单失败 | 3 | TradeInitServiceImpl.java:879 |
| 4 | 方法[{}]响应类型异常, 批量处理失败 | 2 | BatchHandleAspect.java:163 |
| 5 | 暂不支持的文件类型[{}] | 2 | ExportUtil.java:86 |
| 6 | 加载 | 2 | SlManageServiceImpl.java:96 |
| 7 | 与[节假日=>{}]重叠 | 2 | NontradeTemplateManageServiceImpl.java:143 |
| 8 | 投资计划录入文件保存失败 | 2 | InvestPlanInputServiceImpl.java:631 |
| 9 | 文件有误，请重新导入！ | 2 | InvestPlanInputServiceImpl.java:788 |
| 10 | 未知的标签： | 2 | InternalMatchServiceImpl.java:501 |
| 11 | 标签页名称参数异常 | 2 | TradeSummaryServiceImpl.java:136 |
| 12 | 参数类型异常: {} | 2 | AfterClearServiceImpl.java:2483 |
| 13 | 资金对账不成功，请核对数据！ | 2 | AutomatedSettlementServiceImpl.java:516 |
| 14 | 金统下发响应为空 | 2 | TradeElementSendUtil.java:60 |
| 15 | 方法[{}]参数类型异常, 批量处理失败 | 1 | BatchHandleAspect.java:146 |
| 16 | ks-common无可用服务 | 1 | StartradeAppendHandle.java:68 |
| 17 | 数据字典项类别[{}]类型[{}]不存在 | 1 | BaseCommonServiceImpl.java:177 |
| 18 | 系统状态错误 | 1 | TradeCommonServiceImpl.java:277 |
| 19 | 导入失败，对手方代码不能为空！ | 1 | CounterpartyLimitManageServiceImpl.java:253 |
| 20 | 导入失败，以下交易对手方代码有误，请核实后重试! | 1 | CounterpartyLimitManageServiceImpl.java:313 |
| 21 | 未知套利合约类别: {} | 1 | ArbiContractManageServiceImpl.java:107 |
| 22 | 期权合约[{}]期权类型异常 | 1 | OptionContractManageServiceImpl.java:79 |
| 23 | 同步交易所合约失败,请检查交易网关 | 1 | OptionContractManageServiceImpl.java:142 |
| 24 | 当前交易日在交易期间内，不能删除 | 1 | HolidayManageServiceImpl.java:133 |
| 25 | 当前交易日在交易期间内，不能设置 | 1 | HolidayManageServiceImpl.java:211 |
| 26 | 询价管理试算通过-发起EOA审批失败 | 1 | HomeInquireConfirmManageServiceImpl.java:120 |
| 27 | 文件类型异常！ | 1 | InquireForwardPriceCurveServiceImpl.java:136 |
| 28 | 远期价格曲线数据异常 | 1 | InquireForwardPriceCurveServiceImpl.java:159 |
| 29 | 导入文件交易日期内容有误! | 1 | InquireForwardPriceCurveServiceImpl.java:201 |
| 30 | 导入文件品种内容有误! | 1 | InquireForwardPriceCurveServiceImpl.java:208 |
| 31 | 导入文件 | 1 | InquireForwardPriceCurveServiceImpl.java:222 |
| 32 | 发起租借试算通过审批失败 | 1 | LeaseManageServiceImpl.java:1244 |
| 33 | 未知的参数类型:{ | 1 | EmailTemplateParaReplaceServiceImpl.java:114 |
| 34 | 不支持的文件: [{}] | 1 | InvestPlanInputServiceImpl.java:237 |
| 35 | 生成压缩文件失败 | 1 | InvestPlanInputServiceImpl.java:291 |
| 36 | 黄金品种三个自然月内累计投资金额已超过公司上年末总资产的{}%，禁止继续投资 | 1 | InvestPlanInputServiceImpl.java:408 |
| 37 | 发起EOA审批失败 | 1 | InvestPlanInputServiceImpl.java:722 |
| 38 | 投资计划风控审批单日期有误，不可导入。 | 1 | InvestPlanInputServiceImpl.java:1016 |
| 39 | 投资计划风控审批单的日期与投资计划审批单日期不一致，不可导入。 | 1 | InvestPlanInputServiceImpl.java:1018 |
| 40 | [投资计划风控]上传文件非风控审批单，请重新上传。 | 1 | InvestPlanInputServiceImpl.java:1044 |
| 41 | [投资计划审批单导入]上传文件非领导审批单，请重新上传。 | 1 | InvestPlanInputServiceImpl.java:1048 |
| 42 | 日月结单Excel模板未配置或不存在： | 1 | DayMonthSettlementServiceImpl.java:95 |
| 43 | 写出日月结单Excel失败： | 1 | DayMonthSettlementServiceImpl.java:116 |
| 44 | 导出日月结单PDF失败： | 1 | DayMonthSettlementServiceImpl.java:151 |
| 45 | 生成日月结单模板数据失败 | 1 | DayMonthSettlementServiceImpl.java:201 |
| 46 | 导出文件名编码失败 | 1 | DayMonthSettlementServiceImpl.java:219 |
| 47 | 日月结单标识不可为空 | 1 | DayMonthSettlementServiceImpl.java:241 |
| 48 | 交易所代码只允许01或02 | 1 | DayMonthSettlementServiceImpl.java:244 |
| 49 | 会员号不可为空 | 1 | DayMonthSettlementServiceImpl.java:247 |
| 50 | 查询当前结算日失败 | 1 | DayMonthSettlementServiceImpl.java:250 |
| 51 | 查询当前交易日失败 | 1 | DayMonthSettlementServiceImpl.java:253 |
| 52 | 日结单交易日期不可为空 | 1 | DayMonthSettlementServiceImpl.java:258 |
| 53 | 只可选择当前结算日及之前的日期 | 1 | DayMonthSettlementServiceImpl.java:263 |
| 54 | 月结单交易月份不可为空 | 1 | DayMonthSettlementServiceImpl.java:267 |
| 55 | 只可选择前一个月份及之前的月份 | 1 | DayMonthSettlementServiceImpl.java:272 |
| 56 | 日期格式错误，tradeDate须为yyyyMMdd，tradeMonth须为yyyyMM | 1 | DayMonthSettlementServiceImpl.java:276 |
| 57 | 会员号不存在： | 1 | DayMonthSettlementServiceImpl.java:286 |
| 58 | 当前用户无该会员的数据权限 | 1 | DayMonthSettlementServiceImpl.java:292 |
| 59 | 未配置金交所会员银行账号：day-month-settlement.sge-seat. | 1 | DayMonthSettlementServiceImpl.java:336 |
| 60 | 未找到金交所会员客户号： | 1 | DayMonthSettlementServiceImpl.java:340 |
| 61 | 未配置上期所资金账号：day-month-settlement.shfe-fund. | 1 | DayMonthSettlementServiceImpl.java:625 |
| 62 | 计算金交所资金轧差失败 | 1 | DayMonthSettlementServiceImpl.java:785 |
| 63 | 未找到指定的有效会员！ | 1 | MemberSettlementListServiceImpl.java:332 |
| 64 | 暂无可导出的清单内容 | 1 | TradeSettlementListServiceImpl.java:213 |
| 65 | 未找到有效会员！ | 1 | TradeSettlementListServiceImpl.java:239 |
| 66 | 所选交易日期与条件下无任何会员数据可导出！ | 1 | TradeSettlementListServiceImpl.java:272 |
| 67 | 导出现金流异常 | 1 | CashFlowServiceImpl.java:179 |
| 68 | 现金流处理异常 | 1 | CashFlowServiceImpl.java:325 |
| 69 | 成交数据对账不平，已达到最大重试次数 | 1 | AutomatedSettlementServiceImpl.java:292 |
| 70 | 库存流水对账不平，已达到最大重试次数 | 1 | AutomatedSettlementServiceImpl.java:326 |
| 71 | 询价成交数据对账不成功,请核对数据！ | 1 | AutomatedSettlementServiceImpl.java:359 |
| 72 | 持仓数据对账不成功，请核对数据！ | 1 | AutomatedSettlementServiceImpl.java:424 |
| 73 | 库存总量对账不成功，请核对数据！ | 1 | AutomatedSettlementServiceImpl.java:446 |
| 74 | 交割持仓对账不成功，请核对数据！ | 1 | AutomatedSettlementServiceImpl.java:469 |
| 75 | 账务文件未生成，请生成后再初始化! | 1 | AutomatedSettlementServiceImpl.java:605 |
| 76 | 还未核对数据，请核对数据后再初始化! | 1 | AutomatedSettlementServiceImpl.java:607 |
| 77 | Summit帐务未生成，请生成后再初始化! | 1 | AutomatedSettlementServiceImpl.java:609 |
| 78 | 还未记账，请记账后再初始化! | 1 | AutomatedSettlementServiceImpl.java:611 |
| 79 | 解析文件数据失败，请核对格式重新上传 | 1 | CgbSettlementPriceServiceImpl.java:127 |
| 80 | 结算已在处理中，不能重复启动处理过程 | 1 | ClearCommonServiceImpl.java:292 |
| 81 | 闭市后处理已在处理中，不能重复启动处理过程 | 1 | ClearCommonServiceImpl.java:294 |
| 82 | 闭市处理已在处理中，不能重复启动处理过程 | 1 | ClearCommonServiceImpl.java:296 |
| 83 | 记录结算状态改变时间失败 | 1 | ClearCommonServiceImpl.java:316 |
| 84 | 导出文件类型异常： {} | 1 | ClearProcessServiceImpl.java:82 |
| 85 | 交易对手方业务类型异常 | 1 | CounterpartyClearServiceImpl.java:113 |
| 86 | 拆借库存流水未完全分配，请检查! | 1 | DayEndSettleServiceImpl.java:920 |
| 87 | 停止交易进程: [{}] [{}] 模拟失败 | 1 | DayEndSettleServiceImpl.java:2091 |
| 88 | 合约{}结算价不存在 | 1 | StartCloseJobServiceImpl.java:336 |
| 89 | 合约{}递延费率不存在 | 1 | StartCloseJobServiceImpl.java:341 |
| 90 | 合约{}交割保证金不存在 | 1 | StartCloseJobServiceImpl.java:346 |
| 91 | 期权合约对应的标的期货合约{}...没有在合约管理中维护 | 1 | StartCloseJobServiceImpl.java:353 |
| 92 | 期权合约{}...结算价不存在 | 1 | StartCloseJobServiceImpl.java:358 |
| 93 | 启动交易进程: [{}] [{}] 模拟失败 | 1 | TradeInitHandleServiceImpl.java:248 |
| 94 | 初始化文件传输失败: 模拟失败 | 1 | TradeInitHandleServiceImpl.java:299 |
| 95 | 初始化文件传输失败: {} | 1 | TradeInitHandleServiceImpl.java:309 |
| 96 | 计算贴现率失败:{} | 1 | TradeInitHandleServiceImpl.java:808 |
| 97 | 合约最后交易日整理, {} | 1 | TradeInitServiceImpl.java:400 |
| 98 | 同步生成业务提示用户清单表失败 | 1 | TradeInitServiceImpl.java:841 |
| 99 | 根据重量等要素进行匹配后分配失败:询价库存流水类型自动分配，{} | 1 | TraderInventoryAllocateServiceImpl.java:100 |
| 100 | 查询委托请求等待回调失败 | 1 | TraderForceCancelServiceImpl.java:98 |
| 101 | 签名方式异常[{}] | 1 | ServerConfiguration.java:61 |
| 102 | 获取签名数据请求失败 | 1 | SgeSignHttpHandle.java:63 |
| 103 | 获取签名数据失败,响应码异常[{}] | 1 | SgeSignHttpHandle.java:69 |
| 104 | {}接口失败[{}] | 1 | AbstractShfeService.java:111 |
| 105 | {}接口，读取响应体数据失败 | 1 | AbstractShfeService.java:133 |
| 106 | 文件下载响应数据获取失败 | 1 | SgeExchFileServiceImpl.java:94 |
| 107 | 身份认证失败 | 1 | SgeExchFileServiceImpl.java:102 |
| 108 | 文件无访问权限 | 1 | SgeExchFileServiceImpl.java:105 |
| 109 | 文件下载请求失败[{}] | 1 | SgeExchFileServiceImpl.java:111 |
| 110 | {}获取文件数据失败 | 1 | ShfeExchFileServiceImpl.java:117 |
| 111 | 响应头[Content-Type]值[{}]异常 | 1 | ShfeExchFileServiceImpl.java:120 |

---

## 2. ManagementException　(54 条去重消息 / 85 个 throw 点)
> 含 `{}` 占位符的消息写 runbook 时需 param_alias 归一化。

| # | 异常消息 | 出现次数 | 首个来源文件 |
|---|---|---|---|
| 1 | FILTER_NOT_ALLOWED | 6 | ManagementCatalog.java:31 |
| 2 | EMPTY_DATA_SCOPE | 5 | ManagementAdapters.java:44 |
| 3 | QUERY_LEVEL_UNAVAILABLE | 5 | ManagementAdapters.java:78 |
| 4 | FILTER_NOT_ALLOWED_FOR_LEVEL | 5 | ManagementAdapters.java:89 |
| 5 | UNKNOWN_DATASET | 3 | ManagementAdapters.java:163 |
| 6 | TIMEOUT | 3 | ManagementFacade.java:52 |
| 7 | UNKNOWN_FIELD | 3 | ManagementRequest.java:33 |
| 8 | INVALID_SCAN_BUDGET | 2 | ManagementAdapters.java:32 |
| 9 | SOURCE_DATE_INVALID | 2 | ManagementAdapters.java:83 |
| 10 | HISTORY_UNAVAILABLE | 2 | ManagementAdapters.java:267 |
| 11 | METRIC_NOT_ALLOWED | 2 | ManagementCatalog.java:37 |
| 12 | UNIT_GROUP_REQUIRED | 2 | ManagementCatalog.java:41 |
| 13 | UNAUTHENTICATED | 2 | ManagementFacade.java:48 |
| 14 | DATE_LIMIT | 2 | ManagementFacade.java:68 |
| 15 | CANCELLED | 2 | ManagementQueries.java:22 |
| 16 | REQUEST_ID_MISMATCH | 1 | ManagementQueryController.java:61 |
| 17 | SCAN_LIMIT | 1 | ManagementAdapters.java:36 |
| 18 | SOURCE_SCOPE_AMBIGUOUS | 1 | ManagementAdapters.java:201 |
| 19 | AMBIGUOUS_INSTRUMENT_MAPPING | 1 | ManagementAdapters.java:319 |
| 20 | AMBIGUOUS_SOURCE_UNIT | 1 | ManagementAdapters.java:331 |
| 21 | FIELD_NOT_AVAILABLE | 1 | ManagementCatalog.java:30 |
| 22 | GROUP_NOT_ALLOWED | 1 | ManagementCatalog.java:32 |
| 23 | SORT_NOT_ALLOWED | 1 | ManagementCatalog.java:44 |
| 24 | METRICS_REQUIRED | 1 | ManagementCatalog.java:46 |
| 25 | AGGREGATE_REQUIRED | 1 | ManagementCatalog.java:47 |
| 26 | INVALID_DATE | 1 | ManagementData.java:18 |
| 27 | LOSSY_SOURCE_NUMBER | 1 | ManagementData.java:28 |
| 28 | INVALID_SOURCE_DECIMAL | 1 | ManagementData.java:29 |
| 29 | CROSS_DAY_SUM_FORBIDDEN | 1 | ManagementData.java:61 |
| 30 | CURRENCY_GROUP_REQUIRED | 1 | ManagementData.java:63 |
| 31 | GROUP_LIMIT | 1 | ManagementData.java:69 |
| 32 | TIMINGS_QUERY_UNSUPPORTED | 1 | ManagementFacade.java:60 |
| 33 | BUSINESS_DATE_UNAVAILABLE | 1 | ManagementFacade.java:63 |
| 34 | DATASET_MISMATCH | 1 | ManagementFacade.java:79 |
| 35 | ARGUMENT_NOT_SUPPORTED | 1 | ManagementFacade.java:111 |
| 36 | UNKNOWN_ROUTE | 1 | ManagementFacade.java:176 |
| 37 | BUSINESS_CONTEXT_CHANGED | 1 | ManagementFacade.java:181 |
| 38 | TRADER_MODE_UNKNOWN | 1 | ManagementFacade.java:198 |
| 39 | CHECK_CONFIGURATION_CONFLICT | 1 | ManagementFacade.java:242 |
| 40 | CHECK_EXECUTION_CONFLICT | 1 | ManagementFacade.java:249 |
| 41 | SINGLE_DATE_REQUIRED | 1 | ManagementFacade.java:293 |
| 42 | IDENTITY_MAPPING_MISSING | 1 | ManagementIdentity.java:19 |
| 43 | IDENTITY_DISABLED | 1 | ManagementIdentity.java:22 |
| 44 | NESTED_QUERY | 1 | ManagementQueries.java:19 |
| 45 | DUPLICATE_REQUEST_ID | 1 | ManagementQueries.java:23 |
| 46 | CANCELLATION_LIMIT | 1 | ManagementQueries.java:33 |
| 47 | READ_ONLY_VIOLATION | 1 | ManagementQueryInterceptor.java:26 |
| 48 | TIMINGS_FLAG_INVALID | 1 | ManagementRequest.java:14 |
| 49 | QUERY_LEVEL_INVALID | 1 | ManagementRequest.java:46 |
| 50 | INVALID_SECTIONS | 1 | ManagementRequest.java:47 |
| 51 | PAGE_LIMIT | 1 | ManagementRequest.java:50 |
| 52 | QUERY_LIMIT | 1 | ManagementRequest.java:53 |
| 53 | INVALID_FILTER | 1 | ManagementRequest.java:55 |
| 54 | INVALID_REQUEST_ID | 1 | ManagementRequest.java:58 |

---

## 3. IllegalArgumentException　(10 条去重消息 / 11 个 throw 点)
> 含 `{}` 占位符的消息写 runbook 时需 param_alias 归一化。

| # | 异常消息 | 出现次数 | 首个来源文件 |
|---|---|---|---|
| 1 | 非法传参类型 | 2 | NumberUtils.java:152 |
| 2 | 无法得到下一页参数，请检查注解了@ExportMapping方法的参数有且只有 | 1 | ExportRequestHandle.java:30 |
| 3 | 无法获取导出所需元数据，请检查注解了@ExportMapping方法的请求方式不为GET | 1 | ExportRequestHandle.java:36 |
| 4 | 无法获取导出所需元数据，请检查注解了@ExportMapping方法的参数有且只有 | 1 | ExportRequestHandle.java:40 |
| 5 | response is not BaseResponse | 1 | ExportResponseHandle.java:28 |
| 6 | 未知业务类型码: | 1 | CfexMatchTypeEnum.java:37 |
| 7 | 未知外部交易员来源码: | 1 | ForeignTraderSourceEnum.java:37 |
| 8 | 不存在复核状态[ | 1 | ForeignInquireDealManageServiceImpl.java:163 |
| 9 | Sheet cannot be null | 1 | TradeInitHandleServiceImpl.java:935 |
| 10 | Column index must be non-negative | 1 | TradeInitHandleServiceImpl.java:938 |

---

## 4. RuntimeException　(4 条去重消息 / 5 个 throw 点)
> 含 `{}` 占位符的消息写 runbook 时需 param_alias 归一化。

| # | 异常消息 | 出现次数 | 首个来源文件 |
|---|---|---|---|
| 1 | 导出文件失败 | 2 | AsciiTableDataWriter.java:59 |
| 2 | 密码解密失败 | 1 | DigestUtil.java:59 |
| 3 | 创建PDF中文字体失败 | 1 | SettlementPdfBuilder.java:117 |
| 4 | 重试等待被中断 | 1 | AutomatedSettlementServiceImpl.java:746 |

---

## 5. IllegalStateException　(5 条去重消息 / 5 个 throw 点)
> 含 `{}` 占位符的消息写 runbook 时需 param_alias 归一化。

| # | 异常消息 | 出现次数 | 首个来源文件 |
|---|---|---|---|
| 1 | Unexpected value: | 1 | Calculator.java:172 |
| 2 | 农行DAMS文件打包失败: | 1 | DamsFilePackServiceImpl.java:91 |
| 3 | 农行DAMS文件打包后重命名失败: | 1 | DamsFilePackServiceImpl.java:100 |
| 4 | 生成 PDF 失败 | 1 | GbCjkPdfDocument.java:379 |
| 5 | dictionary temporarily unavailable | 1 | ManagementDictionaryNamesTest.java:87 |

---

## 6. ExchFileNotFoundException　(1 条去重消息 / 1 个 throw 点)
> 含 `{}` 占位符的消息写 runbook 时需 param_alias 归一化。

| # | 异常消息 | 出现次数 | 首个来源文件 |
|---|---|---|---|
| 1 | 文件不存在 | 1 | SgeExchFileServiceImpl.java:108 |

---
