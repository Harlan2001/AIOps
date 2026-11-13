import axios, { AxiosError } from 'axios'

// 统一可识别的接口错误，携带 HTTP 状态码与后端提示信息。
export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

interface ValidationItem {
  loc?: Array<string | number>
  msg?: string
  type?: string
}

// 把后端 detail 格式化为可读文本：字符串原样返回；Pydantic 校验数组拼接字段路径与 msg；
// 其他对象回退 JSON。
function formatDetail(detail: unknown): string {
  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }
  if (Array.isArray(detail)) {
    const lines = (detail as ValidationItem[]).map((item) => {
      const loc = (item.loc ?? [])
        .filter((p) => p !== 'body')
        .map(String)
        .join('.')
      const msg = item.msg ?? '校验失败'
      return loc ? `${loc}：${msg}` : msg
    })
    if (lines.length) {
      return lines.join('；')
    }
  }
  if (detail && typeof detail === 'object') {
    const obj = detail as ValidationItem
    if (obj.msg) {
      return obj.msg
    }
    return JSON.stringify(detail)
  }
  return ''
}

export const http = axios.create({
  baseURL: '/',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: unknown }>) => {
    const status = error.response?.status ?? 0
    const message =
      formatDetail(error.response?.data?.detail) ||
      error.message ||
      '网络异常或服务不可用，请稍后重试'
    return Promise.reject(new ApiError(status, message))
  },
)
