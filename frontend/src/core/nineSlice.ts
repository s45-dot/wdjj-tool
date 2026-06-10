import type { NineSliceInput, NineSlicePatch } from './types'
import { createRect } from './rect'

/**
 * Validate nine-slice input.
 * Throws Error with a descriptive message if any rule is violated.
 */
export function validateNineSliceInput(input: NineSliceInput): void {
  const { sourceWidth, sourceHeight, targetWidth, targetHeight, insets } = input

  if (typeof sourceWidth !== 'number' || sourceWidth <= 0) {
    throw new Error(`sourceWidth must be > 0, got ${sourceWidth}`)
  }
  if (typeof sourceHeight !== 'number' || sourceHeight <= 0) {
    throw new Error(`sourceHeight must be > 0, got ${sourceHeight}`)
  }
  if (typeof targetWidth !== 'number' || targetWidth <= 0) {
    throw new Error(`targetWidth must be > 0, got ${targetWidth}`)
  }
  if (typeof targetHeight !== 'number' || targetHeight <= 0) {
    throw new Error(`targetHeight must be > 0, got ${targetHeight}`)
  }

  const { top, right, bottom, left } = insets

  if (
    !Number.isInteger(top) || top < 0 ||
    !Number.isInteger(right) || right < 0 ||
    !Number.isInteger(bottom) || bottom < 0 ||
    !Number.isInteger(left) || left < 0
  ) {
    throw new Error(
      `insets (top:${top}, right:${right}, bottom:${bottom}, left:${left}) ` +
      `must be non-negative integers`
    )
  }

  if (left + right >= sourceWidth) {
    throw new Error(
      `left(${left}) + right(${right}) must be < sourceWidth(${sourceWidth})`
    )
  }
  if (top + bottom >= sourceHeight) {
    throw new Error(
      `top(${top}) + bottom(${bottom}) must be < sourceHeight(${sourceHeight})`
    )
  }
  if (targetWidth < left + right + 1) {
    throw new Error(
      `targetWidth(${targetWidth}) must be >= left(${left}) + right(${right}) + 1 = ${left + right + 1}`
    )
  }
  if (targetHeight < top + bottom + 1) {
    throw new Error(
      `targetHeight(${targetHeight}) must be >= top(${top}) + bottom(${bottom}) + 1 = ${top + bottom + 1}`
    )
  }
}

/**
 * Compute exactly 9 nine-slice patches (3x3 grid, row-major order).
 * Pure function — same input always produces the same output.
 * Does NOT re-validate; caller must call validateNineSliceInput first.
 */
export function computeNineSlicePatches(input: NineSliceInput): NineSlicePatch[] {
  const { sourceWidth, sourceHeight, targetWidth, targetHeight, insets } = input
  const { top, right, bottom, left } = insets

  // Source slice boundaries along X and Y axes
  const sx = [0, left, sourceWidth - right, sourceWidth]
  const sy = [0, top, sourceHeight - bottom, sourceHeight]

  // Target slice boundaries along X and Y axes
  const dx = [0, left, targetWidth - right, targetWidth]
  const dy = [0, top, targetHeight - bottom, targetHeight]

  const patches: NineSlicePatch[] = []

  for (let row = 0; row < 3; row++) {
    for (let col = 0; col < 3; col++) {
      patches.push({
        source: createRect(sx[col], sy[row], sx[col + 1] - sx[col], sy[row + 1] - sy[row]),
        target: createRect(dx[col], dy[row], dx[col + 1] - dx[col], dy[row + 1] - dy[row]),
        row,
        col,
      })
    }
  }

  return patches
}

/**
 * Draw a nine-slice stretched image onto a canvas.
 * Validates input, computes 9 patches via computeNineSlicePatches,
 * clears the canvas, and draws each patch from source to target.
 */
export function drawNineSlice(
  ctx: CanvasRenderingContext2D,
  image: HTMLImageElement | HTMLCanvasElement,
  input: NineSliceInput,
): void {
  const patches = computeNineSlicePatches(input)
  const { targetWidth, targetHeight } = input

  ctx.clearRect(0, 0, targetWidth, targetHeight)

  for (const patch of patches) {
    ctx.drawImage(
      image,
      patch.source.x, patch.source.y, patch.source.w, patch.source.h,
      patch.target.x, patch.target.y, patch.target.w, patch.target.h,
    )
  }
}
