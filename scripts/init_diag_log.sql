-- ============================================================================
-- AIOps 诊断结果持久化建表脚本（方向一·阶段 0）
--
-- 用途：由部署方在 GaussDB 中手动执行，本脚本不会被程序自动执行。
-- 约定：
--   * 仅新增独立日志表，不修改任何历史表/已有业务表；
--   * JSON 统一存 TEXT（不依赖 JSONB），类型用 GaussDB 通用类型；
--   * 标注人身份留痕：annotator / annotated_at 记录谁在何时做了人工纠错。
-- 建议配套：使用仅对本表有 INSERT/SELECT/UPDATE 权限的独立数据库账号。
-- ============================================================================

CREATE TABLE IF NOT EXISTS aiops_diag_log (
    id              BIGSERIAL    PRIMARY KEY,
    batch_id        VARCHAR(36),                         -- 同一次批量/巡检的分组标识(UUID)
    trigger_type    VARCHAR(16)  NOT NULL,               -- manual / manual_batch / scheduled
    input_mode      VARCHAR(16)  NOT NULL,               -- text / record
    source          VARCHAR(32),                         -- 来源 id(ftr_err 等)，文本模式为空
    business_date   VARCHAR(8),                          -- 业务日期 yyyyMMdd
    error_text      TEXT,                                -- 报错原文快照
    error_code      INTEGER      DEFAULT 0,              -- 错误码
    key_json        TEXT,                                -- 取数主键 JSON 快照
    fingerprint     VARCHAR(64)  NOT NULL,               -- 去重指纹
    diag_class      VARCHAR(16),                         -- biz / noise / ora / other / error
    diag_type       VARCHAR(48),                         -- 命中类型 id
    root_cause      TEXT,                                -- 根因
    confidence      NUMERIC(3,2),                        -- 置信度
    diag_path       VARCHAR(24),                         -- 规则/降级/LLM
    escalated       BOOLEAN      DEFAULT FALSE,          -- 是否升级 LLM
    evidence_count  INTEGER      DEFAULT 0,              -- 取证步数
    result_json     TEXT,                                -- 完整结果 JSON 快照
    diag_status     VARCHAR(16)  DEFAULT 'success',      -- success / error(诊断异常)
    error_msg       TEXT,                                -- 诊断异常信息
    -- 人工纠错字段（标注人留痕）
    annot_status    VARCHAR(16),                         -- 空 / correct / wrong
    correct_answer  TEXT,                                -- 人工给的正确答案
    annotator       VARCHAR(32),                         -- 标注人（留痕）
    annotated_at    TIMESTAMP,                           -- 标注时间（留痕）
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_aiops_diag_fp UNIQUE (fingerprint)
);

COMMENT ON TABLE aiops_diag_log IS 'AIOps 诊断结果持久化表（人工/批量/巡检统一落库）';
COMMENT ON COLUMN aiops_diag_log.fingerprint IS 'sha256 去重指纹：trigger_type+source+business_date+规范化文本+主键';
COMMENT ON COLUMN aiops_diag_log.annotator IS '人工纠错标注人，用于审计留痕';
COMMENT ON COLUMN aiops_diag_log.annotated_at IS '人工纠错时间，用于审计留痕';
