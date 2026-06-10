export interface Insets {
  top: number
  right: number
  bottom: number
  left: number
}

export interface Rect {
  x: number
  y: number
  w: number
  h: number
}

export interface NineSlicePatch {
  source: Rect
  target: Rect
  row: number
  col: number
}

export interface NineSliceInput {
  sourceWidth: number
  sourceHeight: number
  targetWidth: number
  targetHeight: number
  insets: Insets
}
