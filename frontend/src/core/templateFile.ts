/**
 * Template file (.bubble-template.json) format for Bubble Stretch Tool.
 *
 * Stores reusable presets: capInsets, contentInsets, scale, and direction
 * that can be applied to any image project.
 */

import type { Insets } from './types'

// ---------------------------------------------------------------------------
// Interfaces
// ---------------------------------------------------------------------------

export interface BubbleTemplate {
  format: 'bubble-template'
  version: 1
  name: string
  description: string
  capInsets: Insets
  contentInsets: Insets
  scale: number
  direction: 'left' | 'right'
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function validateInsetsFields(
  val: unknown,
  label: string,
  errors: string[],
): void {
  if (typeof val !== 'object' || val === null) {
    errors.push(`${label} must be an object`)
    return
  }
  const i = val as Record<string, unknown>
  for (const side of ['top', 'right', 'bottom', 'left'] as const) {
    if (typeof i[side] !== 'number' || !Number.isFinite(i[side])) {
      errors.push(`${label}.${side} must be a finite number`)
    }
  }
}

// ---------------------------------------------------------------------------
// Serialize
// ---------------------------------------------------------------------------

export interface TemplateFileInput {
  name: string
  description: string
  capInsets: Insets
  contentInsets: Insets
  scale: number
  direction: 'left' | 'right'
}

export function serializeTemplate(state: TemplateFileInput): BubbleTemplate {
  return {
    format: 'bubble-template',
    version: 1,
    name: state.name,
    description: state.description,
    capInsets: { ...state.capInsets },
    contentInsets: { ...state.contentInsets },
    scale: state.scale,
    direction: state.direction,
  }
}

// ---------------------------------------------------------------------------
// Deserialize
// ---------------------------------------------------------------------------

export function deserializeTemplate(json: string): BubbleTemplate {
  let parsed: unknown
  try {
    parsed = JSON.parse(json)
  } catch {
    throw new Error('Invalid JSON')
  }

  const errors = validateTemplate(parsed)
  if (errors.length > 0) {
    throw new Error(`Invalid template file: ${errors.join('; ')}`)
  }

  return parsed as BubbleTemplate
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

export function validateTemplate(obj: unknown): string[] {
  const errors: string[] = []

  if (typeof obj !== 'object' || obj === null) {
    errors.push('Root must be a JSON object')
    return errors
  }

  const o = obj as Record<string, unknown>

  // format field
  if (o.format !== 'bubble-template') {
    errors.push(
      `format must be "bubble-template", got "${String(o.format)}"`,
    )
  }

  // version field
  if (o.version !== 1) {
    errors.push(`version must be 1, got "${String(o.version)}"`)
  }

  // name
  if (typeof o.name !== 'string') {
    errors.push('name must be a string')
  }

  // description
  if (typeof o.description !== 'string') {
    errors.push('description must be a string')
  }

  // capInsets
  validateInsetsFields(o.capInsets, 'capInsets', errors)

  // contentInsets
  validateInsetsFields(o.contentInsets, 'contentInsets', errors)

  // scale
  if (typeof o.scale !== 'number' || ![1, 2, 3].includes(o.scale)) {
    errors.push('scale must be 1, 2, or 3')
  }

  // direction
  if (typeof o.direction !== 'string' || !['left', 'right'].includes(o.direction)) {
    errors.push('direction must be "left" or "right"')
  }

  return errors
}
