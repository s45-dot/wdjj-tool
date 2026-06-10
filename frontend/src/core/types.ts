export interface Rect {
  x: number
  y: number
  width: number
  height: number
}

export interface Insets {
  top: number
  right: number
  bottom: number
  left: number
}

export interface NineSlicePatch {
  rect: Rect
  scaleMode: 'stretch' | 'tile' | 'crop'
}

export interface NineSliceInput {
  imageDimensions: Rect
  insets: Insets
}

export type ScaleMode = NineSlicePatch['scaleMode']
