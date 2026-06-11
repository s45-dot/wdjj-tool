<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { computeNineSlicePatches } from '../core/nineSlice'
import { layoutText } from '../core/textMeasure'
import { computeBubbleLayout } from '../core/bubbleLayout'
import type { Insets } from '../core/types'

const PREVIEW_WIDTH = 300
const PADDING = 10
const MIN_BUBBLE_DIM = 30

const props = withDefaults(defineProps<{
  imageUrl?: string
  sourceWidth?: number
  sourceHeight?: number
  insets?: Insets
  contentInsets?: Insets
  text?: string
  fontSize?: number
  fontFamily?: string
  lineHeight?: number
  maxBubbleWidth?: number
  direction?: 'left' | 'right'
  showGuides?: boolean
}>(), {
  imageUrl: undefined,
  sourceWidth: 0,
  sourceHeight: 0,
  insets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  contentInsets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  text: '',
  fontSize: 16,
  fontFamily: 'sans-serif',
  lineHeight: 22,
  maxBubbleWidth: 280,
  direction: 'left',
  showGuides: false,
})

const canvasRef = ref<HTMLCanvasElement | null>(null)
let loadedImage: HTMLImageElement | null = null

function loadImage(): void {
  if (!props.imageUrl) {
    loadedImage = null
    render()
    return
  }

  const img = new Image()
  img.onload = (): void => {
    loadedImage = img
    render()
  }
  img.onerror = (): void => {
    loadedImage = null
    render()
  }
  img.src = props.imageUrl
}

function render(): void {
  const canvas = canvasRef.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // --- Step 1: measure text ---
  const textToLayout = props.text || ' '
  const layout = layoutText(ctx, {
    text: textToLayout,
    fontSize: props.fontSize,
    fontFamily: props.fontFamily,
    lineHeight: props.lineHeight,
    maxTextWidth: props.maxBubbleWidth - props.contentInsets.left - props.contentInsets.right - 2,
  })

  const textWidth = layout.maxLineWidth
  const textHeight = layout.textHeight

  // --- Step 2: compute bubble dimensions ---
  const bubble = computeBubbleLayout({
    textWidth,
    textHeight,
    contentInsets: props.contentInsets,
    minWidth: MIN_BUBBLE_DIM,
    minHeight: MIN_BUBBLE_DIM,
    maxBubbleWidth: props.maxBubbleWidth,
  })

  // --- Step 3: position the bubble ---
  const canvasW = PREVIEW_WIDTH
  const canvasH = bubble.bubbleHeight + PADDING * 2
  const bubbleX =
    props.direction === 'right'
      ? canvasW - bubble.bubbleWidth - PADDING
      : PADDING
  const bubbleY = PADDING

  // --- Step 4: set up canvas ---
  const dpr = window.devicePixelRatio || 1
  canvas.width = canvasW * dpr
  canvas.height = canvasH * dpr
  canvas.style.width = `${canvasW}px`
  canvas.style.height = `${canvasH}px`
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  ctx.clearRect(0, 0, canvasW, canvasH)

  // --- Step 5: draw nine-slice bubble background ---
  const sourceW = props.sourceWidth || (loadedImage ? loadedImage.naturalWidth : 0)
  const sourceH = props.sourceHeight || (loadedImage ? loadedImage.naturalHeight : 0)

  if (loadedImage && sourceW > 0 && sourceH > 0) {
    const patches = computeNineSlicePatches({
      sourceWidth: sourceW,
      sourceHeight: sourceH,
      targetWidth: bubble.bubbleWidth,
      targetHeight: bubble.bubbleHeight,
      insets: props.insets,
    })

    for (const patch of patches) {
      ctx.drawImage(
        loadedImage,
        patch.source.x,
        patch.source.y,
        patch.source.w,
        patch.source.h,
        patch.target.x + bubbleX,
        patch.target.y + bubbleY,
        patch.target.w,
        patch.target.h,
      )
    }
  } else {
    // Fallback: draw a rounded rectangle placeholder
    ctx.fillStyle = '#e0e0e0'
    ctx.beginPath()
    ctx.roundRect(bubbleX, bubbleY, bubble.bubbleWidth, bubble.bubbleHeight, 8)
    ctx.fill()
  }

  // --- Step 6: draw text ---
  if (props.text && layout.lines.length > 0) {
    const contentAreaX = bubbleX + props.contentInsets.left
    const contentAreaY = bubbleY + props.contentInsets.top
    const contentAreaH = bubble.bubbleHeight - props.contentInsets.top - props.contentInsets.bottom

    const verticalOffset = Math.max(0, (contentAreaH - textHeight) / 2)

    ctx.font = `${props.fontSize}px ${props.fontFamily}`
    ctx.fillStyle = '#000000'
    ctx.textBaseline = 'top'

    for (let i = 0; i < layout.lines.length; i++) {
      const lineY = contentAreaY + verticalOffset + i * props.lineHeight
      ctx.fillText(layout.lines[i], contentAreaX, lineY)
    }
  }

  // --- Step 7: draw guide lines ---
  if (props.showGuides && loadedImage) {
    ctx.save()

    // Cap insets guide (red/orange dashed)
    ctx.strokeStyle = 'rgba(220, 80, 70, 0.55)'
    ctx.lineWidth = 1
    ctx.setLineDash([4, 3])
    ctx.strokeRect(
      bubbleX + props.insets.left,
      bubbleY + props.insets.top,
      bubble.bubbleWidth - props.insets.left - props.insets.right,
      bubble.bubbleHeight - props.insets.top - props.insets.bottom,
    )

    // Content insets guide (blue dashed) — different dash pattern
    ctx.strokeStyle = 'rgba(70, 130, 220, 0.55)'
    ctx.setLineDash([3, 4])
    ctx.strokeRect(
      bubbleX + props.contentInsets.left,
      bubbleY + props.contentInsets.top,
      bubble.bubbleWidth - props.contentInsets.left - props.contentInsets.right,
      bubble.bubbleHeight - props.contentInsets.top - props.contentInsets.bottom,
    )

    ctx.restore()
  }
}

onMounted(loadImage)

watch(
  () => props.imageUrl,
  (val) => {
    if (val) {
      loadImage()
    } else {
      loadedImage = null
      render()
    }
  },
)

watch(
  () => [
    props.sourceWidth,
    props.sourceHeight,
    props.insets,
    props.contentInsets,
    props.text,
    props.fontSize,
    props.fontFamily,
    props.lineHeight,
    props.maxBubbleWidth,
    props.direction,
    props.showGuides,
  ],
  () => render(),
  { deep: true },
)
</script>

<template>
  <div class="bubble-scene-wrapper">
    <canvas ref="canvasRef" />
  </div>
</template>

<style scoped>
.bubble-scene-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
canvas {
  max-width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
