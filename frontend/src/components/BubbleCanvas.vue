<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

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

function draw() {
  const canvas = canvasRef.value
  if (!canvas || !props.imageUrl) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const dpr = window.devicePixelRatio || 1
  const w = props.targetWidth
  const h = props.targetHeight

  canvas.width = w * dpr
  canvas.height = h * dpr
  canvas.style.width = `${w}px`
  canvas.style.height = `${h}px`
  ctx.scale(dpr, dpr)

  if (loadedImage) {
    ctx.clearRect(0, 0, w, h)
    ctx.drawImage(loadedImage, 0, 0, w, h)
  }
}

function loadImage() {
  if (!props.imageUrl) {
    loadedImage = null
    draw()
    return
  }

  const img = new Image()
  img.onload = () => {
    loadedImage = img
    draw()
  }
  img.onerror = () => {
    loadedImage = null
    draw()
  }
  img.src = props.imageUrl
}

onMounted(loadImage)

watch(
  () => [
    props.imageUrl,
    props.sourceWidth,
    props.sourceHeight,
    props.targetWidth,
    props.targetHeight,
    props.insets?.top,
    props.insets?.right,
    props.insets?.bottom,
    props.insets?.left,
  ],
  () => {
    if (props.imageUrl) {
      loadImage()
    } else {
      loadedImage = null
      draw()
    }
  },
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
