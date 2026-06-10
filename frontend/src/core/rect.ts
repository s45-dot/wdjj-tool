import type { Rect } from './types'

export function createRect(x: number, y: number, w: number, h: number): Rect {
  return { x, y, w, h }
}

export function area(rect: Rect): number {
  return rect.w * rect.h
}

export function isEmpty(rect: Rect): boolean {
  return rect.w <= 0 || rect.h <= 0
}

export function equals(a: Rect, b: Rect): boolean {
  return a.x === b.x && a.y === b.y && a.w === b.w && a.h === b.h
}
