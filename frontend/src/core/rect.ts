import type { Rect } from './types'

/**
 * Check if a point is inside a rectangle
 */
export function pointInRect(point: { x: number; y: number }, rect: Rect): boolean {
  return (
    point.x >= rect.x &&
    point.x < rect.x + rect.width &&
    point.y >= rect.y &&
    point.y < rect.y + rect.height
  )
}

/**
 * Check if two rectangles intersect
 */
export function intersectRect(a: Rect, b: Rect): boolean {
  return (
    a.x < b.x + b.width &&
    a.x + a.width > b.x &&
    a.y < b.y + b.height &&
    a.y + a.height > b.y
  )
}

/**
 * Clamp a rectangle to fit within bounds
 */
export function clampRect(rect: Rect, bounds: Rect): Rect {
  return {
    x: Math.max(bounds.x, Math.min(rect.x, bounds.x + bounds.width - rect.width)),
    y: Math.max(bounds.y, Math.min(rect.y, bounds.y + bounds.height - rect.height)),
    width: Math.min(rect.width, bounds.width),
    height: Math.min(rect.height, bounds.height),
  }
}

/**
 * Create a new rectangle with offset
 */
export function offsetRect(rect: Rect, dx: number, dy: number): Rect {
  return {
    ...rect,
    x: rect.x + dx,
    y: rect.y + dy,
  }
}

/**
 * Get the center point of a rectangle
 */
export function centerOfRect(rect: Rect): { x: number; y: number } {
  return {
    x: rect.x + rect.width / 2,
    y: rect.y + rect.height / 2,
  }
}

/**
 * Scale a rectangle by a factor while keeping center position
 */
export function scaleRect(rect: Rect, factor: number): Rect {
  const center = centerOfRect(rect)
  const newWidth = rect.width * factor
  const newHeight = rect.height * factor

  return {
    x: center.x - newWidth / 2,
    y: center.y - newHeight / 2,
    width: newWidth,
    height: newHeight,
  }
}
