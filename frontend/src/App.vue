<script setup lang="ts">
import ImageUploader from './components/ImageUploader.vue'
import BubbleCanvas from './components/BubbleCanvas.vue'
import InsetsPanel from './components/InsetsPanel.vue'
import DebugPanel from './components/DebugPanel.vue'

import { ref, shallowRef } from 'vue'
import type { Rect } from './core/types'
import { clampRect, intersectRect } from './core/rect'

const imageLoaded = ref(false)
const imageDimensions = ref<Rect | null>(null)
const insets = ref({ top: 10, right: 10, bottom: 10, left: 10 })
const debugInfo = ref('')

function onImageLoaded(rect: Rect) {
  imageLoaded.value = true
  imageDimensions.value = rect
  debugInfo.value = `Image loaded: ${rect.width}x${rect.height}`
}

function onInsetsChanged(newInsets: typeof insets.value) {
  insets.value = newInsets
  debugInfo.value = `Insets updated: top=${newInsets.top}, right=${newInsets.right}, bottom=${newInsets.bottom}, left=${newInsets.left}`
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
          v-if="imageLoaded && imageDimensions"
          :image-dimensions="imageDimensions"
          :insets="insets"
        />
        <div v-else class="preview-placeholder">
          Upload an image to preview
        </div>
      </section>

      <section class="panel panel-controls">
        <InsetsPanel
          :insets="insets"
          @changed="onInsetsChanged"
        />
      </section>
    </main>

    <footer class="app-footer">
      <DebugPanel :info="debugInfo" />
    </footer>
  </div>
</template>
