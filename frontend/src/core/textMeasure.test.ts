import { describe, it, expect, beforeEach, vi } from 'vitest'
import { layoutText } from './textMeasure'

const mockCtx = {
  font: '',
  measureText: vi.fn().mockReturnValue({ width: 10 }),
} as unknown as CanvasRenderingContext2D

describe('layoutText', () => {
  beforeEach(() => {
    mockCtx.measureText = vi.fn().mockReturnValue({ width: 10 })
  })

  it('wraps Chinese characters individually', () => {
    const result = layoutText(mockCtx, {
      text: '中文测试',
      fontSize: 16,
      fontFamily: 'sans-serif',
      lineHeight: 20,
      maxTextWidth: 30,
    })
    expect(result.lines.length).toBeGreaterThan(1)
  })

  it('wraps English by spaces', () => {
    mockCtx.measureText = vi.fn().mockImplementation((text: string) => ({
      width: text.length * 5,
    }))
    const result = layoutText(mockCtx, {
      text: 'hello world foo',
      fontSize: 16,
      fontFamily: 'sans-serif',
      lineHeight: 20,
      maxTextWidth: 30,
    })
    expect(result.lines.some((l) => l.includes(' '))).toBe(true)
  })

  it('handles explicit newline characters', () => {
    const result = layoutText(mockCtx, {
      text: 'line1\nline2',
      fontSize: 16,
      fontFamily: 'sans-serif',
      lineHeight: 20,
      maxTextWidth: 300,
    })
    expect(result.lines).toContain('line1')
    expect(result.lines).toContain('line2')
  })

  it('returns empty lines for empty text', () => {
    const result = layoutText(mockCtx, {
      text: '',
      fontSize: 16,
      fontFamily: 'sans-serif',
      lineHeight: 20,
      maxTextWidth: 300,
    })
    expect(result.lines).toHaveLength(1)
    expect(result.lines[0]).toBe('')
  })
})