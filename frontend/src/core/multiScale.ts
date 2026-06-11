/**
 * Multi-scale export support for Bubble Stretch Tool.
 *
 * Provides scale constants, request interface, and validation.
 */

/** Supported export scale factors. */
export const SUPPORTED_SCALES = [1, 2, 3] as const

/** Request payload for multi-scale export. */
export interface MultiScaleRequest {
  /** Selected scale factors to include in the export. */
  selectedScales: number[]
}

/**
 * Validate a list of scale selections.
 *
 * @param scales - Array of scale factors to validate.
 * @throws {Error} If scales is empty, contains unsupported values, or duplicates.
 */
export function validateScales(scales: number[]): void {
  if (!Array.isArray(scales) || scales.length === 0) {
    throw new Error('At least one scale must be selected')
  }

  const seen = new Set<number>()
  for (const s of scales) {
    if (!SUPPORTED_SCALES.includes(s as (typeof SUPPORTED_SCALES)[number])) {
      throw new Error(`Invalid scale: ${s}. Supported values: ${SUPPORTED_SCALES.join(', ')}`)
    }
    if (seen.has(s)) {
      throw new Error(`Duplicate scale: ${s}`)
    }
    seen.add(s)
  }
}
