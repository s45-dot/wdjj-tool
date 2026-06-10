<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ImageUploader from './components/ImageUploader.vue'
import BubbleCanvas from './components/BubbleCanvas.vue'
import InsetsPanel from './components/InsetsPanel.vue'
import DebugPanel from './components/DebugPanel.vue'
import { getHealth } from './api/healthApi'

const imageUrl = ref<string | null>(null)
const sourceWidth = ref(0)
const sourceHeight = ref(0)
const filename = ref('')
const sizeBytes = ref(0)
const targetWidth = ref(240)
const targetHeight = ref(80)
const insets = ref({ top: 0, right: 0, bottom: 0, left: 0 })

const backendStatus = ref<{ connected: boolean; version: string }>({
  connected: false,
  version: '',
})

async function checkHealth() {
  try {
    const res = await getHealth()
    backendStatus.value = { connected: true, version: res.version }
  } catch {
    backendStatus.value = { connected: false, version: '' }
  }
}

onMounted(() => {
  checkHealth()
})

function onImageLoaded(payload: {
  url: string
  width: number
  height: number
  filename: string
  size: number
}) {
  // Release previous ObjectURL
  if (imageUrl.value) {
    URL.revokeObjectURL(imageUrl.value)
  }

  imageUrl.value = payload.url
  sourceWidth.value = payload.width
  sourceHeight.value = payload.height
  filename.value = payload.filename
  sizeBytes.value = payload.size

  // Auto-set default insets to 25% of each dimension
  insets.value = {
    top: Math.floor(payload.height * 0.25),
    right: Math.floor(payload.width * 0.25),
    bottom: Math.floor(payload.height * 0.25),
    left: Math.floor(payload.width * 0.25),
  }

  // Auto-set default target dimensions
  targetWidth.value = Math.max(payload.width, 240)
  targetHeight.value = Math.max(payload.height, 80)
}

function onInsetsChanged(newInsets: { top: number; right: number; bottom: number; left: number }) {
  insets.value = newInsets
}
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>Bubble Stretch Tool</h1>
    </header>

    <main class="app-main">
      <section class="panel panel-upload">
        <ImageUploader @loaded="onImageLoaded" />
      </section>

      <section class="panel panel-preview">
        <BubbleCanvas
          v-if="imageUrl"
          :imageUrl="imageUrl"
          :sourceWidth="sourceWidth"
          :sourceHeight="sourceHeight"
          :targetWidth="targetWidth"
          :targetHeight="targetHeight"
          :insets="insets"
        />
        <div v-else class="preview-placeholder">
          Upload an image to preview
        </div>
      </section>

      <section class="panel panel-controls">
        <InsetsPanel
          :insets="insets"
          :sourceWidth="sourceWidth"
          :sourceHeight="sourceHeight"
          @change="onInsetsChanged"
        />
      </section>
    </main>

    <footer class="app-footer">
      <DebugPanel
        :filename="filename"
        :sourceWidth="sourceWidth"
        :sourceHeight="sourceHeight"
        :sizeBytes="sizeBytes"
        :targetWidth="targetWidth"
        :targetHeight="targetHeight"
        :insets="insets"
        :backendConnected="backendStatus.connected"
        :backendVersion="backendStatus.version"
      />
    </footer>
  </div>
</template>
