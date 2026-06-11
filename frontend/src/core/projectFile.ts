/**
 * Project file (.bubble.json) format for Bubble Stretch Tool.
 *
 * Full workspace serialization: stores all editor state including
 * asset metadata, insets, scale, preview settings, and export options.
 */

import type { Insets } from './types'

// ---------------------------------------------------------------------------
// Interfaces
// ---------------------------------------------------------------------------

export interface BubbleAsset {
  filename: string
  width: number
  height: number
  mimeType: string
}

export interface BubblePreview {
  text: string
  fontSize: number
  lineHeight: number
  maxBubbleWidth: number
  direction: 'left' | 'right'
}

export interface BubbleExportOptions {
  outputs: {
    androidNinePatch: boolean
    iosJson: boolean
    androidJson: boolean
    previewPng: boolean
    readme: boolean
    sourcePng: boolean
  }
  targetWidth: number
  targetHeight: number
  scale: number
}

export interface BubbleProject {
  format: 'bubble-project'
  version: 1
  createdAt: string
  updatedAt: string
  asset: BubbleAsset
  capInsets: Insets
  contentInsets: Insets
  scale: number
  preview: BubblePreview
  exportOptions?: BubbleExportOptions
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

export interface ProjectFileInput {
  asset: BubbleAsset
  capInsets: Insets
  contentInsets: Insets
  scale: number
  preview: BubblePreview
  exportOptions?: BubbleExportOptions
}

export function serializeProject(state: ProjectFileInput): BubbleProject {
  const now = new Date().toISOString()
  return {
    format: 'bubble-project',
    version: 1,
    createdAt: now,
    updatedAt: now,
    asset: { ...state.asset },
    capInsets: { ...state.capInsets },
    contentInsets: { ...state.contentInsets },
    scale: state.scale,
    preview: { ...state.preview },
    exportOptions: state.exportOptions
      ? JSON.parse(JSON.stringify(state.exportOptions))
      : undefined,
  }
}

// ---------------------------------------------------------------------------
// Deserialize
// ---------------------------------------------------------------------------

export function deserializeProject(json: string): BubbleProject {
  let parsed: unknown
  try {
    parsed = JSON.parse(json)
  } catch {
    throw new Error('Invalid JSON')
  }

  const errors = validateProjectFile(parsed)
  if (errors.length > 0) {
    throw new Error(`Invalid project file: ${errors.join('; ')}`)
  }

  return parsed as BubbleProject
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

export function validateProjectFile(obj: unknown): string[] {
  const errors: string[] = []

  if (typeof obj !== 'object' || obj === null) {
    errors.push('Root must be a JSON object')
    return errors
  }

  const o = obj as Record<string, unknown>

  // format field
  if (o.format !== 'bubble-project') {
    errors.push(
      `format must be "bubble-project", got "${String(o.format)}"`,
    )
  }

  // version field
  if (o.version !== 1) {
    errors.push(`version must be 1, got "${String(o.version)}"`)
  }

  // timestamps
  if (typeof o.createdAt !== 'string') {
    errors.push('createdAt must be a string')
  }
  if (typeof o.updatedAt !== 'string') {
    errors.push('updatedAt must be a string')
  }

  // asset
  if (typeof o.asset !== 'object' || o.asset === null) {
    errors.push('asset must be an object')
  } else {
    const a = o.asset as Record<string, unknown>
    if (typeof a.filename !== 'string') {
      errors.push('asset.filename must be a string')
    }
    if (typeof a.width !== 'number' || !Number.isFinite(a.width) || a.width <= 0) {
      errors.push('asset.width must be a positive number')
    }
    if (typeof a.height !== 'number' || !Number.isFinite(a.height) || a.height <= 0) {
      errors.push('asset.height must be a positive number')
    }
    if (typeof a.mimeType !== 'string') {
      errors.push('asset.mimeType must be a string')
    }
  }

  // capInsets
  validateInsetsFields(o.capInsets, 'capInsets', errors)

  // contentInsets
  validateInsetsFields(o.contentInsets, 'contentInsets', errors)

  // scale
  if (typeof o.scale !== 'number' || ![1, 2, 3].includes(o.scale)) {
    errors.push('scale must be 1, 2, or 3')
  }

  // preview
  if (typeof o.preview !== 'object' || o.preview === null) {
    errors.push('preview must be an object')
  } else {
    const p = o.preview as Record<string, unknown>
    if (typeof p.text !== 'string') {
      errors.push('preview.text must be a string')
    }
    if (typeof p.fontSize !== 'number' || !Number.isFinite(p.fontSize)) {
      errors.push('preview.fontSize must be a finite number')
    }
    if (typeof p.lineHeight !== 'number' || !Number.isFinite(p.lineHeight)) {
      errors.push('preview.lineHeight must be a finite number')
    }
    if (typeof p.maxBubbleWidth !== 'number' || !Number.isFinite(p.maxBubbleWidth)) {
      errors.push('preview.maxBubbleWidth must be a finite number')
    }
    if (typeof p.direction !== 'string' || !['left', 'right'].includes(p.direction)) {
      errors.push('preview.direction must be "left" or "right"')
    }
  }

  return errors
}
