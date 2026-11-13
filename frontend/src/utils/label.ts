// 空/未识别标签归一化（纯函数，便于单测）。
export function labelNull(key: string | null | undefined): string {
  return key === null || key === undefined || key === '' ? '未识别' : key
}
