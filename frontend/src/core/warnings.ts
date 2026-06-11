import type { Insets } from './types'

export interface WarningItem {
  code: string
  level: 'info' | 'warning' | 'error'
  message: string
}

export const CAP_CENTER_TOO_SMALL = 'CAP_CENTER_TOO_SMALL'
export const CONTENT_CENTER_TOO_SMALL = 'CONTENT_CENTER_TOO_SMALL'
export const TARGET_TOO_SMALL = 'TARGET_TOO_SMALL'
export const SCALE_MISSING = 'SCALE_MISSING'
export const BACKEND_DISCONNECTED = 'BACKEND_DISCONNECTED'

export function collectWarnings(
  imageLoaded: boolean,
  sourceW: number,
  sourceH: number,
  insets: Insets,
  contentInsets: Insets,
  scale: number,
  backendConnected: boolean,
): WarningItem[] {
  const warnings: WarningItem[] = []

  if (imageLoaded && sourceW > 0 && sourceH > 0) {
    const capCenterW = sourceW - insets.left - insets.right
    const capCenterH = sourceH - insets.top - insets.bottom

    if (capCenterW < 2 || capCenterH < 2) {
      warnings.push({
        code: CAP_CENTER_TOO_SMALL,
        level: 'error',
        message: `拉伸中心区域过小 (${capCenterW}×${capCenterH})，可能导致严重变形`,
      })
    } else if (capCenterW < 5 || capCenterH < 5) {
      warnings.push({
        code: CAP_CENTER_TOO_SMALL,
        level: 'warning',
        message: `拉伸中心区域偏小 (${capCenterW}×${capCenterH})，拉伸效果可能不佳`,
      })
    }

    const contentCenterW = sourceW - contentInsets.left - contentInsets.right
    const contentCenterH = sourceH - contentInsets.top - contentInsets.bottom

    if (contentCenterW < 2 || contentCenterH < 2) {
      warnings.push({
        code: CONTENT_CENTER_TOO_SMALL,
        level: 'warning',
        message: `内容区域过小 (${contentCenterW}×${contentCenterH})，文本可能无法正常显示`,
      })
    }
  }

  if (scale <= 0) {
    warnings.push({
      code: SCALE_MISSING,
      level: 'warning',
      message: '缩放比例未设置',
    })
  }

  if (!backendConnected) {
    warnings.push({
      code: BACKEND_DISCONNECTED,
      level: 'info',
      message: '后端服务未连接，导出功能不可用',
    })
  }

  return warnings
}
