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

export const http = axios.create({
  baseURL: '/',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string }>) => {
    const status = error.response?.status ?? 0
    const detail =
      error.response?.data?.detail ||
      error.message ||
      '网络异常或服务不可用，请稍后重试'
    return Promise.reject(new ApiError(status, detail))
  },
)
