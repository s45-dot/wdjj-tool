/**
 * Bubble dimension computation from text size and content insets.
 * Pure function, no dependencies on Canvas or Vue.
 */

export interface BubbleLayoutInput {
  textWidth: number
  textHeight: number
  contentInsets: { top: number; right: number; bottom: number; left: number }
  minWidth: number
  minHeight: number
  maxBubbleWidth: number
}

export interface BubbleLayout {
  bubbleWidth: number
  bubbleHeight: number
}

/**
 * Compute the final bubble dimensions.
 *
 * bubbleWidth = Math.max(minW, textW + contentInsets.left + contentInsets.right)
 *               clamped to maxBubbleWidth
 *
 * bubbleHeight = Math.max(minH, textH + contentInsets.top + contentInsets.bottom)
 */
export function computeBubbleLayout(input: BubbleLayoutInput): BubbleLayout {
  const textHWidth = input.textWidth + input.contentInsets.left + input.contentInsets.right
  const bubbleWidth = Math.min(
    Math.max(input.minWidth, textHWidth),
    input.maxBubbleWidth,
  )

  const textHHeight = input.textHeight + input.contentInsets.top + input.contentInsets.bottom
  const bubbleHeight = Math.max(input.minHeight, textHHeight)

  return { bubbleWidth, bubbleHeight }
}
