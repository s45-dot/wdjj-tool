export const SCALES = [1, 2, 3] as const

export function pxToPt(px: number, scale: number): number {
  if (scale <= 0) return px
  return px / scale
}
