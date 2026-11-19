<script setup lang="ts">
import { onMounted, ref } from 'vue'

import {
  annotateDiagnosis,
  getDiagnoses,
  getDiagnosisDetail,
  type DiagListParams,
} from '@/api/diagnoses'
import { ApiError } from '@/api/client'
import { message } from 'ant-design-vue'
import { SOURCES } from '@/constants/sources'
import type { DiagLogItem } from '@/types/contract'

const PAGE_SIZE = 10

const items = ref<DiagLogItem[]>([])
const total = ref(0)
const page = ref(1)
const loading = ref(false)
const errorMsg = ref('')

// 筛选条件
const source = ref<string>()
const diagClass = ref<string>()
const diagType = ref<string>()
const annotFilter = ref<string>()
const startDate = ref('')
const endDate = ref('')

const classOptions = [
  { value: 'biz', label: '业务报错' },
  { value: 'noise', label: '噪音' },
  { value: 'ora', label: 'DBA 技术错误' },
  { value: 'other', label: '其他/未识别' },
]
const annotOptions = [
  { value: 'correct', label: '确认正确' },
  { value: 'wrong', label: '确认错误' },
]

const columns = [
  { title: 'ID', dataIndex: 'id', width: 70 },
  { title: '业务日期', dataIndex: 'business_date' },
  { title: '来源', dataIndex: 'source' },
  { title: '分类', dataIndex: 'diag_class' },
  { title: '类型', dataIndex: 'diag_type' },
  { title: '置信度', dataIndex: 'confidence' },
  { title: '状态', dataIndex: 'diag_status' },
  { title: '标注', dataIndex: 'annot_status' },
  { title: '诊断时间', dataIndex: 'created_at' },
  { title: '操作', dataIndex: 'action', width: 150 },
]

// 详情抽屉
const drawerOpen = ref(false)
const detail = ref<DiagLogItem | null>(null)
const detailLoading = ref(false)

// 标注弹窗
const annotModalOpen = ref(false)
const annotTarget = ref<DiagLogItem | null>(null)
const annotStatus = ref<'correct' | 'wrong'>('correct')
const correctAnswer = ref('')
const annotator = ref('')
const submitLoading = ref(false)

onMounted(load)

function buildParams(): DiagListParams {
  return {
    source: source.value,
    diag_class: diagClass.value,
    diag_type: diagType.value,
    annot_status: annotFilter.value,
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined,
    offset: (page.value - 1) * PAGE_SIZE,
    limit: PAGE_SIZE,
  }
}

async function load() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await getDiagnoses(buildParams())
    items.value = res.items
    total.value = res.total
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError
        ? `加载失败（${e.status}）：${e.message}`
        : '加载异常，请稍后重试'
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  load()
}

function reset() {
  source.value = undefined
  diagClass.value = undefined
  diagType.value = undefined
  annotFilter.value = undefined
  startDate.value = ''
  endDate.value = ''
  search()
}

function onPageChange(p: number) {
  page.value = p
  load()
}

function onTableChange(pag: { current?: number }) {
  onPageChange(pag.current ?? 1)
}

async function openDetail(record: DiagLogItem) {
  drawerOpen.value = true
  detailLoading.value = true
  detail.value = null
  try {
    detail.value = await getDiagnosisDetail(record.id)
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError ? `详情加载失败：${e.message}` : '详情加载失败'
  } finally {
    detailLoading.value = false
  }
}

function openAnnot(record: DiagLogItem, status: 'correct' | 'wrong') {
  annotTarget.value = record
  annotStatus.value = status
  correctAnswer.value = record.correct_answer ?? ''
  annotator.value = ''
  annotModalOpen.value = true
}

async function submitAnnot() {
  if (!annotator.value.trim()) {
    message.warning('请填写标注人')
    return
  }
  if (annotStatus.value === 'wrong' && !correctAnswer.value.trim()) {
    message.warning('标错时请填写正确答案')
    return
  }
  if (!annotTarget.value) return
  submitLoading.value = true
  try {
    await annotateDiagnosis(annotTarget.value.id, {
      annot_status: annotStatus.value,
      correct_answer: correctAnswer.value || null,
      annotator: annotator.value.trim(),
    })
    message.success('标注已保存')
    annotModalOpen.value = false
    load()
  } catch (e) {
    message.error(
      e instanceof ApiError ? `标注失败：${e.message}` : '标注失败，请稍后重试',
    )
  } finally {
    submitLoading.value = false
  }
}
</script>

<template>
  <a-card title="历史诊断">
    <a-row :gutter="12" align="bottom">
      <a-col :span="4">
        <p class="flabel">来源</p>
        <a-select
          v-model:value="source"
          allow-clear
          style="width: 100%"
          :options="SOURCES.map((s) => ({ value: s.id, label: s.label }))"
        />
      </a-col>
      <a-col :span="3">
        <p class="flabel">分类</p>
        <a-select
          v-model:value="diagClass"
          allow-clear
          style="width: 100%"
          :options="classOptions"
        />
      </a-col>
      <a-col :span="4">
        <p class="flabel">类型</p>
        <a-input v-model:value="diagType" allow-clear placeholder="类型 id" />
      </a-col>
      <a-col :span="3">
        <p class="flabel">标注</p>
        <a-select
          v-model:value="annotFilter"
          allow-clear
          style="width: 100%"
          :options="annotOptions"
        />
      </a-col>
      <a-col :span="4">
        <p class="flabel">日期范围</p>
        <a-input-group compact>
          <a-input
            v-model:value="startDate"
            style="width: 50%"
            placeholder="起"
          />
          <a-input v-model:value="endDate" style="width: 50%" placeholder="止" />
        </a-input-group>
      </a-col>
      <a-col :span="6">
        <a-space>
          <a-button type="primary" @click="search">查询</a-button>
          <a-button @click="reset">重置</a-button>
        </a-space>
      </a-col>
    </a-row>

    <a-alert
      v-if="errorMsg"
      type="error"
      show-icon
      :message="errorMsg"
      class="block"
    />

    <a-table
      :columns="columns"
      :data-source="items"
      :loading="loading"
      row-key="id"
      :pagination="{
        current: page,
        pageSize: PAGE_SIZE,
        total,
        showSizeChanger: false,
      }"
      class="block"
      @change="onTableChange"
    >
      <template #bodyCell="{ column, record }">
        <a v-if="column.dataIndex === 'id'" @click="openDetail(record)">
          {{ record.id }}
        </a>
        <a-space v-else-if="column.dataIndex === 'action'">
          <a-button
            size="small"
            type="link"
            @click="openAnnot(record, 'correct')"
          >正确</a-button>
          <a-button
            size="small"
            type="link"
            danger
            @click="openAnnot(record, 'wrong')"
          >错误</a-button>
        </a-space>
      </template>
    </a-table>
  </a-card>

  <a-modal
    v-model:open="annotModalOpen"
    :title="annotStatus === 'correct' ? '确认结论正确' : '纠错：填写正确答案'"
    :confirm-loading="submitLoading"
    ok-text="保存"
    cancel-text="取消"
    @ok="submitAnnot"
  >
    <a-form layout="vertical" class="annot-form">
      <a-form-item label="标注人（留痕）">
        <a-input v-model:value="annotator" placeholder="请输入你的姓名" />
      </a-form-item>
      <a-form-item
        v-if="annotStatus === 'wrong'"
        label="正确答案"
        :required="true"
      >
        <a-textarea
          v-model:value="correctAnswer"
          :rows="3"
          placeholder="请填写正确的结论/处理方式"
        />
      </a-form-item>
      <p v-else class="tip">将标记该条诊断结论为正确，用于规则可信度沉淀。</p>
    </a-form>
  </a-modal>

  <a-drawer
    v-model:open="drawerOpen"
    title="诊断详情"
    width="560"
  >
    <a-spin :spinning="detailLoading">
      <a-descriptions
        v-if="detail"
        :column="1"
        bordered
        size="small"
      >
        <a-descriptions-item label="ID">{{ detail.id }}</a-descriptions-item>
        <a-descriptions-item label="批次号">{{ detail.batch_id }}</a-descriptions-item>
        <a-descriptions-item label="触发方式">{{ detail.trigger_type }}</a-descriptions-item>
        <a-descriptions-item label="来源 / 日期">
          {{ detail.source }} / {{ detail.business_date }}
        </a-descriptions-item>
        <a-descriptions-item label="报错文本">{{ detail.error_text }}</a-descriptions-item>
        <a-descriptions-item label="分类 / 类型">
          {{ detail.diag_class }} / {{ detail.diag_type }}
        </a-descriptions-item>
        <a-descriptions-item label="根因">{{ detail.root_cause }}</a-descriptions-item>
        <a-descriptions-item label="置信度">{{ detail.confidence }}</a-descriptions-item>
        <a-descriptions-item label="取证步数">{{ detail.evidence_count }}</a-descriptions-item>
        <a-descriptions-item label="标注">
          {{ detail.annot_status }}
          <span v-if="detail.annotator">（{{ detail.annotator }}）</span>
        </a-descriptions-item>
      </a-descriptions>
    </a-spin>
  </a-drawer>
</template>

<style scoped>
.block {
  margin-top: 16px;
}

.flabel {
  margin-bottom: 4px;
  color: #666;
  font-size: 12px;
}

.tip {
  color: #888;
  font-size: 13px;
}
</style>
