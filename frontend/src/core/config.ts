/**
 * Config export/import for Bubble Stretch Tool.
 *
 * Provides a serializable BubbleConfig interface and
 * functions to export/import config as JSON.
 */

import { Insets } from './types'

export interface BubbleConfig {
  /** Stretch cap insets in pixels (left, right, top, bottom) */
  capInsets: Insets
  /** Content (padding) insets in pixels */
  contentInsets: Insets
  /** Image scale factor (1x, 2x, 3x) */
  scale: number
  /** Preview target width in pixels */
  targetWidth: number
  /** Preview target height in pixels */
  targetHeight: number
  /** Chat bubble direction */
  direction: 'left' | 'right'
  /** Preview text content */
  text: string
  /** Preview font size in pixels */
  fontSize: number
  /** Preview line height in pixels */
  lineHeight: number
  /** Maximum bubble width in pixels */
  maxBubbleWidth: number
}

/**
 * Serialise a BubbleConfig to a pretty-printed JSON string.
 */
export function exportConfig(config: BubbleConfig): string {
  return JSON.stringify(config, null, 2)
}

/**
 * Parse and validate a JSON string into a BubbleConfig.
 *
 * Returns the parsed config on success. Throws on invalid JSON,
 * missing required fields, or type mismatches.
 */
export function importConfig(json: string): BubbleConfig {
  let parsed: unknown
  try {
    parsed = JSON.parse(json)
  } catch {
    throw new Error('Invalid JSON format')
  }

  if (typeof parsed !== 'object' || parsed === null) {
    throw new Error('Root value must be a JSON object')
  }

  const obj = parsed as Record<string, unknown>

  // --- validate required fields ---

  const requiredFields: string[] = [
    'capInsets', 'contentInsets', 'scale',
    'targetWidth', 'targetHeight', 'direction',
    'text', 'fontSize', 'lineHeight', 'maxBubbleWidth',
  ]
  for (const field of requiredFields) {
    if (!(field in obj)) {
      throw new Error(`Missing required field: ${field}`)
    }
  }

  // --- validate insets ---

  function validateInsets(inset: unknown, label: string): Insets {
    if (typeof inset !== 'object' || inset === null) {
      throw new Error(`${label} must be an object`)
    }
    const i = inset as Record<string, unknown>
    for (const side of ['top', 'right', 'bottom', 'left'] as const) {
      if (typeof i[side] !== 'number' || !Number.isFinite(i[side])) {
        throw new Error(`${label}.${side} must be a finite number`)
      }
    }
    return {
      top: i.top as number,
      right: i.right as number,
      bottom: i.bottom as number,
      left: i.left as number,
    }
  }

  const capInsets = validateInsets(obj.capInsets, 'capInsets')
  const contentInsets = validateInsets(obj.contentInsets, 'contentInsets')

  // --- validate scalar fields ---

  function validateNumber(val: unknown, field: string): number {
    if (typeof val !== 'number' || !Number.isFinite(val)) {
      throw new Error(`${field} must be a finite number`)
    }
    return val
  }

  const scale = validateNumber(obj.scale, 'scale')
  if (![1, 2, 3].includes(scale)) {
    throw new Error('scale must be 1, 2, or 3')
  }

  const targetWidth = validateNumber(obj.targetWidth, 'targetWidth')
  const targetHeight = validateNumber(obj.targetHeight, 'targetHeight')
  const fontSize = validateNumber(obj.fontSize, 'fontSize')
  const lineHeight = validateNumber(obj.lineHeight, 'lineHeight')
  const maxBubbleWidth = validateNumber(obj.maxBubbleWidth, 'maxBubbleWidth')

  // --- validate string fields ---

  if (typeof obj.direction !== 'string') {
    throw new Error('direction must be a string')
  }
  if (!['left', 'right'].includes(obj.direction)) {
    throw new Error('direction must be "left" or "right"')
  }

  if (typeof obj.text !== 'string') {
    throw new Error('text must be a string')
  }

  return {
    capInsets,
    contentInsets,
    scale,
    targetWidth,
    targetHeight,
    direction: obj.direction as 'left' | 'right',
    text: obj.text,
    fontSize,
    lineHeight,
    maxBubbleWidth,
  }
}
