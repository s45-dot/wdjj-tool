import { describe, it, expect } from 'vitest'
import { computeBubbleLayout } from './bubbleLayout'

describe('computeBubbleLayout', () => {
  it('bubbleWidth is at least minWidth', () => {
    const result = computeBubbleLayout({
      textWidth: 10,
      textHeight: 10,
      contentInsets: { top: 0, right: 0, bottom: 0, left: 0 },
      minWidth: 100,
      minHeight: 50,
      maxBubbleWidth: 500,
    })
    expect(result.bubbleWidth).toBeGreaterThanOrEqual(100)
  })

  it('bubbleHeight is at least minHeight', () => {
    const result = computeBubbleLayout({
      textWidth: 10,
      textHeight: 10,
      contentInsets: { top: 0, right: 0, bottom: 0, left: 0 },
      minWidth: 100,
      minHeight: 100,
      maxBubbleWidth: 500,
    })
    expect(result.bubbleHeight).toBeGreaterThanOrEqual(100)
  })

  it('bubbleWidth does not exceed maxBubbleWidth', () => {
    const result = computeBubbleLayout({
      textWidth: 1000,
      textHeight: 10,
      contentInsets: { top: 0, right: 0, bottom: 0, left: 0 },
      minWidth: 100,
      minHeight: 50,
      maxBubbleWidth: 200,
    })
    expect(result.bubbleWidth).toBeLessThanOrEqual(200)
  })

  it('contentInsets correctly affect dimensions', () => {
    const result = computeBubbleLayout({
      textWidth: 50,
      textHeight: 30,
      contentInsets: { top: 5, right: 10, bottom: 5, left: 10 },
      minWidth: 0,
      minHeight: 0,
      maxBubbleWidth: 500,
    })
    expect(result.bubbleWidth).toBe(70)
    expect(result.bubbleHeight).toBe(40)
  })
})