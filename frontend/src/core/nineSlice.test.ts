import { describe, it, expect } from 'vitest'
import { computeNineSlicePatches, validateNineSliceInput } from './nineSlice'

describe('computeNineSlicePatches', () => {
  it('returns exactly 9 patches', () => {
    const patches = computeNineSlicePatches({
      sourceWidth: 100,
      sourceHeight: 100,
      targetWidth: 200,
      targetHeight: 200,
      insets: { top: 10, right: 10, bottom: 10, left: 10 },
    })
    expect(patches).toHaveLength(9)
  })

  it('patches are in row-major order (top-left to bottom-right)', () => {
    const patches = computeNineSlicePatches({
      sourceWidth: 100,
      sourceHeight: 100,
      targetWidth: 200,
      targetHeight: 200,
      insets: { top: 10, right: 10, bottom: 10, left: 10 },
    })
    expect(patches[0].row).toBe(0)
    expect(patches[0].col).toBe(0)
    expect(patches[1].row).toBe(0)
    expect(patches[1].col).toBe(1)
    expect(patches[2].row).toBe(0)
    expect(patches[2].col).toBe(2)
    expect(patches[3].row).toBe(1)
    expect(patches[3].col).toBe(0)
    expect(patches[4].row).toBe(1)
    expect(patches[4].col).toBe(1)
    expect(patches[5].row).toBe(1)
    expect(patches[5].col).toBe(2)
    expect(patches[6].row).toBe(2)
    expect(patches[6].col).toBe(0)
    expect(patches[7].row).toBe(2)
    expect(patches[7].col).toBe(1)
    expect(patches[8].row).toBe(2)
    expect(patches[8].col).toBe(2)
  })

  it('throws error for invalid sourceWidth', () => {
    expect(() =>
      validateNineSliceInput({
        sourceWidth: 0,
        sourceHeight: 100,
        targetWidth: 200,
        targetHeight: 200,
        insets: { top: 10, right: 10, bottom: 10, left: 10 },
      })
    ).toThrow()
  })

  it('throws error for invalid insets (negative values)', () => {
    expect(() =>
      validateNineSliceInput({
        sourceWidth: 100,
        sourceHeight: 100,
        targetWidth: 200,
        targetHeight: 200,
        insets: { top: -1, right: 10, bottom: 10, left: 10 },
      })
    ).toThrow()
  })
})