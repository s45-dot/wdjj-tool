import type { Insets, Rect } from './types'

/**
 * Validate that insets values are within acceptable range
 * Returns true if valid, false otherwise
 */
export function validateInsets(insets: Insets): boolean {
  if (!insets) return false

  const { top, right, bottom, left } = insets

  // All values must be numbers
  if (typeof top !== 'number' || typeof right !== 'number' ||
      typeof bottom !== 'number' || typeof left !== 'number') {
    return false
  }

  // All values must be non-negative
  if (top < 0 || right < 0 || bottom < 0 || left < 0) {
    return false
  }

  // Values should not exceed reasonable bounds (e.g., 500px)
  const MAX_VALUE = 500
  if (top > MAX_VALUE || right > MAX_VALUE || bottom > MAX_VALUE || left > MAX_VALUE) {
    return false
  }

  return true
}

/**
 * Validate that a rectangle has valid dimensions
 */
export function validateRect(rect: Rect): boolean {
  if (!rect) return false

  const { x, y, w, h } = rect

  // All values must be numbers
  if (typeof x !== 'number' || typeof y !== 'number' ||
      typeof w !== 'number' || typeof h !== 'number') {
    return false
  }

  // Width and height must be positive
  if (w <= 0 || h <= 0) {
    return false
  }

  // Dimensions should not exceed reasonable bounds
  const MAX_DIMENSION = 10000
  if (w > MAX_DIMENSION || h > MAX_DIMENSION) {
    return false
  }

  return true
}

/**
 * Validate that an image dimensions rectangle is valid
 */
export function validateImageDimensions(dims: Rect): boolean {
  return validateRect(dims) && dims.w > 0 && dims.h > 0
}

/**
 * Validate insets against source image dimensions with detailed result.
 * Returns errors (fatal) and warnings (center region too small).
 */
export function validateInsetsResult(
  sourceWidth: number,
  sourceHeight: number,
  insets: { top: number; right: number; bottom: number; left: number },
): { valid: boolean; errors: string[]; warnings: string[] } {
  const errors: string[] = []
  const warnings: string[] = []

  if (insets.left + insets.right >= sourceWidth) {
    errors.push('left + right must be < sourceWidth')
  }
  if (insets.top + insets.bottom >= sourceHeight) {
    errors.push('top + bottom must be < sourceHeight')
  }
  if (sourceWidth - insets.left - insets.right < 2) {
    warnings.push('source center width < 2px')
  }
  if (sourceHeight - insets.top - insets.bottom < 2) {
    warnings.push('source center height < 2px')
  }

  return { valid: errors.length === 0, errors, warnings }
}
