<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { drawNineSlice, validateNineSliceInput } from '../core/nineSlice'
import type { NineSliceInput } from '../core/types'

const props = withDefaults(defineProps<{
  imageUrl?: string
  sourceWidth?: number
  sourceHeight?: number
  targetWidth?: number
  targetHeight?: number
  insets?: { top: number; right: number; bottom: number; left: number }
}>(), {
  targetWidth: 240,
  targetHeight: 80,
  insets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
})

const canvasRef = ref<HTMLCanvasElement | null>(null)
let loadedImage: HTMLImageElement | null = null

function draw(): void {
  const canvas = canvasRef.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const dpr = window.devicePixelRatio || 1
  const w = props.targetWidth
  const h = props.targetHeight

  canvas.width = w * dpr
  canvas.height = h * dpr
  canvas.style.width = `${w}px`
  canvas.style.height = `${h}px`
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  if (!props.imageUrl || !loadedImage) {
    ctx.clearRect(0, 0, w, h)
    return
  }

  const sourceW = props.sourceWidth ?? loadedImage.naturalWidth
  const sourceH = props.sourceHeight ?? loadedImage.naturalHeight

  const input: NineSliceInput = {
    sourceWidth: sourceW,
    sourceHeight: sourceH,
    targetWidth: w,
    targetHeight: h,
    insets: props.insets,
  }

  try {
    validateNineSliceInput(input)
  } catch {
    // invalid insets — fall back to stretching the full image
    ctx.clearRect(0, 0, w, h)
    ctx.drawImage(loadedImage, 0, 0, w, h)
    return
  }

  drawNineSlice(ctx, loadedImage, input)
}

function loadImage(): void {
  if (!props.imageUrl) {
    loadedImage = null
    draw()
    return
  }

  const img = new Image()
  img.onload = (): void => {
    loadedImage = img
    draw()
  }
  img.onerror = (): void => {
    loadedImage = null
    draw()
  }
  img.src = props.imageUrl
}

onMounted(loadImage)

watch(
  () => props.imageUrl,
  (val) => {
    if (val) {
      loadImage()
    } else {
      loadedImage = null
      draw()
    }
  },
)

watch(
  () => [props.sourceWidth, props.sourceHeight, props.targetWidth, props.targetHeight],
  () => draw(),
)

watch(
  () => props.insets,
  () => draw(),
  { deep: true },
)
</script>

<template>
  <div class="canvas-wrapper">
    <canvas ref="canvasRef" />
  </div>
</template>

<style scoped>
.canvas-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80px;
}
canvas {
  max-width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
