<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ImageUploader from './components/ImageUploader.vue'
import BubbleCanvas from './components/BubbleCanvas.vue'
import InsetsPanel from './components/InsetsPanel.vue'
import DebugPanel from './components/DebugPanel.vue'
import ContentInsetsPanel from './components/ContentInsetsPanel.vue'
import ExportPanel from './components/ExportPanel.vue'
import { getHealth } from './api/healthApi'
import { getNetworkInfo } from './api/networkApi'
import { readTokenFromUrl } from './api/client'
import { createDefaultContentInsets } from './core/contentInsets'

const imageUrl = ref<string | null>(null)
const sourceWidth = ref(0)
const sourceHeight = ref(0)
const filename = ref('')
const sizeBytes = ref(0)
const targetWidth = ref(240)
const targetHeight = ref(80)
const insets = ref({ top: 0, right: 0, bottom: 0, left: 0 })
const imageId = ref<string | null>(null)
const hasImageId = ref(false)
const contentInsets = ref({ top: 0, right: 0, bottom: 0, left: 0 })

const backendStatus = ref<{ connected: boolean; version: string }>({
  connected: false,
  version: '',
})

const lanUrl = ref<string | null>(null)

async function checkHealth() {
  try {
    const res = await getHealth()
    backendStatus.value = { connected: true, version: res.version }
  } catch {
    backendStatus.value = { connected: false, version: '' }
  }
}

async function fetchNetworkInfo() {
  try {
    const info = await getNetworkInfo()
    lanUrl.value = info.url
  } catch {
    // Network info not available — silent fallback
  }
}

onMounted(() => {
  // Cache the auth token from URL query param (if any)
  readTokenFromUrl()
  checkHealth()
  fetchNetworkInfo()
})

function onImageLoaded(payload: {
  url: string
  width: number
  height: number
  filename: string
  size: number
  imageId?: string
  uploadError?: string
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

  // Store imageId if upload succeeded
  if (payload.imageId) {
    imageId.value = payload.imageId
    hasImageId.value = true
  } else {
    imageId.value = null
    hasImageId.value = false
  }

  // Auto-set default stretch insets to 25% of each dimension
  insets.value = {
    top: Math.floor(payload.height * 0.25),
    right: Math.floor(payload.width * 0.25),
    bottom: Math.floor(payload.height * 0.25),
    left: Math.floor(payload.width * 0.25),
  }

  // Auto-set default content insets from helper
  contentInsets.value = createDefaultContentInsets(payload.width, payload.height)

  // Auto-set default target dimensions
  targetWidth.value = Math.max(payload.width, 240)
  targetHeight.value = Math.max(payload.height, 80)
}

function onInsetsChanged(newInsets: { top: number; right: number; bottom: number; left: number }) {
  insets.value = newInsets
}

function onContentInsetsChanged(newContentInsets: { top: number; right: number; bottom: number; left: number }) {
  contentInsets.value = newContentInsets
}
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>Bubble Stretch Tool</h1>
    </header>

    <div v-if="lanUrl" class="lan-banner">
      🌐 LAN URL: <a :href="lanUrl" target="_blank">{{ lanUrl }}</a>
    </div>

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
        <hr class="panel-divider" />
        <ContentInsetsPanel
          :contentInsets="contentInsets"
          :sourceWidth="sourceWidth"
          :sourceHeight="sourceHeight"
          @change="onContentInsetsChanged"
        />
        <hr class="panel-divider" />
        <ExportPanel
          :imageId="imageId"
          :capInsets="insets"
          :contentInsets="contentInsets"
          :targetWidth="targetWidth"
          :targetHeight="targetHeight"
          :sourceWidth="sourceWidth"
          :sourceHeight="sourceHeight"
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

<style scoped>
.panel-divider {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 0.5rem 0;
}

.lan-banner {
  background: #e3f2fd;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  text-align: center;
  border-bottom: 1px solid #bbdefb;
}
.lan-banner a {
  color: #1565c0;
  text-decoration: none;
  font-family: 'SF Mono', 'Fira Code', monospace;
}
.lan-banner a:hover {
  text-decoration: underline;
}
</style>
