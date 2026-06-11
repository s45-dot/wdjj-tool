<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import ImageUploader from './components/ImageUploader.vue'
import DevicePreview from './components/DevicePreview.vue'
import InsetsPanel from './components/InsetsPanel.vue'
import DebugPanel from './components/DebugPanel.vue'
import ContentInsetsPanel from './components/ContentInsetsPanel.vue'
import ExportPanel from './components/ExportPanel.vue'
import TextPreviewPanel from './components/TextPreviewPanel.vue'
import BubbleScenePreview from './components/BubbleScenePreview.vue'
import ScalePanel from './components/ScalePanel.vue'
import WarningPanel from './components/WarningPanel.vue'
import ConfigPanel from './components/ConfigPanel.vue'
import ProjectPanel from './components/ProjectPanel.vue'
import TemplatePanel from './components/TemplatePanel.vue'
import MultiScalePanel from './components/MultiScalePanel.vue'
import BatchImportPanel from './components/BatchImportPanel.vue'
import BatchTaskList from './components/BatchTaskList.vue'
import BatchExportPanel from './components/BatchExportPanel.vue'
import type { BubbleConfig } from './core/config'
import type { ProjectFileInput, BubbleProject } from './core/projectFile'
import type { TemplateFileInput, BubbleTemplate } from './core/templateFile'
import type { BatchItem } from './core/batch'
import { getHealth } from './api/healthApi'
import { getNetworkInfo } from './api/networkApi'
import { readTokenFromUrl } from './api/client'
import { createDefaultContentInsets } from './core/contentInsets'
import { collectWarnings } from './core/warnings'

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

// Chat bubble preview state
const direction = ref<'left' | 'right'>('left')
const previewText = ref('这是一条测试消息')
const bubbleFontSize = ref(16)
const bubbleLineHeight = ref(22)
const bubbleFontFamily = ref('sans-serif')
const maxBubbleWidth = ref(280)

const backendStatus = ref<{ connected: boolean; version: string }>({
  connected: false,
  version: '',
})

const lanUrl = ref<string | null>(null)

// Scale state
const scale = ref(1)
const showGuides = ref(true)

// Multi-scale state
const selectedScales = ref<number[]>([1])

// Batch state
const batchItems = ref<BatchItem[]>([])

// Computed: exportable batch items (those with imageId and status 'uploaded')
const exportableBatchIds = computed(() =>
  batchItems.value
    .filter(i => i.imageId && i.status === 'uploaded')
    .map(i => i.imageId!)
)

const exportableCount = computed(() => exportableBatchIds.value.length)

// Warning system
const warnings = computed(() => collectWarnings(
  !!imageUrl.value,
  sourceWidth.value,
  sourceHeight.value,
  insets.value,
  contentInsets.value,
  scale.value,
  backendStatus.value.connected,
))

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

function onTextPreviewChange(payload: {
  text: string
  fontSize: number
  lineHeight: number
  fontFamily: string
  maxBubbleWidth: number
}) {
  previewText.value = payload.text
  bubbleFontSize.value = payload.fontSize
  bubbleLineHeight.value = payload.lineHeight
  bubbleFontFamily.value = payload.fontFamily
  maxBubbleWidth.value = payload.maxBubbleWidth
}

function toggleDirection() {
  direction.value = direction.value === 'left' ? 'right' : 'left'
}

// Config export/import — build current state into a BubbleConfig
const currentConfig = computed<BubbleConfig>(() => ({
  capInsets: insets.value,
  contentInsets: contentInsets.value,
  scale: scale.value,
  targetWidth: targetWidth.value,
  targetHeight: targetHeight.value,
  direction: direction.value,
  text: previewText.value,
  fontSize: bubbleFontSize.value,
  lineHeight: bubbleLineHeight.value,
  maxBubbleWidth: maxBubbleWidth.value,
}))

function onConfigLoaded(config: BubbleConfig) {
  insets.value = config.capInsets
  contentInsets.value = config.contentInsets
  scale.value = config.scale
  targetWidth.value = config.targetWidth
  targetHeight.value = config.targetHeight
  direction.value = config.direction
  previewText.value = config.text
  bubbleFontSize.value = config.fontSize
  bubbleLineHeight.value = config.lineHeight
  maxBubbleWidth.value = config.maxBubbleWidth
}

// --- Project / Template file helpers ---

function mimeTypeFromFilename(name: string): string {
  if (!name) return 'image/png'
  const ext = name.split('.').pop()?.toLowerCase()
  switch (ext) {
    case 'png': return 'image/png'
    case 'jpg':
    case 'jpeg': return 'image/jpeg'
    case 'gif': return 'image/gif'
    case 'webp': return 'image/webp'
    default: return 'image/png'
  }
}

const projectFileInput = computed<ProjectFileInput>(() => ({
  asset: {
    filename: filename.value,
    width: sourceWidth.value,
    height: sourceHeight.value,
    mimeType: mimeTypeFromFilename(filename.value),
  },
  capInsets: { ...insets.value },
  contentInsets: { ...contentInsets.value },
  scale: scale.value,
  preview: {
    text: previewText.value,
    fontSize: bubbleFontSize.value,
    lineHeight: bubbleLineHeight.value,
    maxBubbleWidth: maxBubbleWidth.value,
    direction: direction.value,
  },
}))

const templateFileInput = computed<TemplateFileInput>(() => ({
  name: '',
  description: '',
  capInsets: { ...insets.value },
  contentInsets: { ...contentInsets.value },
  scale: scale.value,
  direction: direction.value,
}))

function onProjectLoaded(project: BubbleProject) {
  insets.value = { ...project.capInsets }
  contentInsets.value = { ...project.contentInsets }
  scale.value = project.scale
  direction.value = project.preview.direction
  previewText.value = project.preview.text
  bubbleFontSize.value = project.preview.fontSize
  bubbleLineHeight.value = project.preview.lineHeight
  maxBubbleWidth.value = project.preview.maxBubbleWidth
}

function onTemplateLoaded(template: BubbleTemplate) {
  insets.value = { ...template.capInsets }
  contentInsets.value = { ...template.contentInsets }
  scale.value = template.scale
  direction.value = template.direction
}

// --- Multi-scale event handlers ---

function onSelectedScalesChanged(scales: number[]) {
  selectedScales.value = scales
}

// --- Batch event handlers ---

function onBatchItemsChanged(items: BatchItem[]) {
  batchItems.value = items
}

function onBatchItemRemoved(id: string) {
  batchItems.value = batchItems.value.filter(i => i.id !== id)
}

function onBatchExportComplete() {
  // Clear completed exported items
  batchItems.value = batchItems.value.filter(
    i => i.status !== 'exported' && i.status !== 'exporting'
  )
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
        <DevicePreview v-if="imageUrl">
          <BubbleScenePreview
            :imageUrl="imageUrl"
            :sourceWidth="sourceWidth"
            :sourceHeight="sourceHeight"
            :insets="insets"
            :contentInsets="contentInsets"
            :text="previewText"
            :fontSize="bubbleFontSize"
            :fontFamily="bubbleFontFamily"
            :lineHeight="bubbleLineHeight"
            :maxBubbleWidth="maxBubbleWidth"
            :direction="direction"
            :showGuides="showGuides"
          />
        </DevicePreview>
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
        <TextPreviewPanel @change="onTextPreviewChange" />
        <hr class="panel-divider" />
        <div class="direction-row">
          <button class="direction-toggle" @click="toggleDirection">
            {{ direction === 'left' ? '← Left' : 'Right →' }}
          </button>
          <label class="guides-toggle">
            <input type="checkbox" v-model="showGuides" />
            辅助线
          </label>
        </div>
        <hr class="panel-divider" />
        <ScalePanel
          :scale="scale"
          :capInsets="insets"
          :contentInsets="contentInsets"
          @update:scale="scale = $event"
        />
        <hr class="panel-divider" />
        <MultiScalePanel
          @update:selectedScales="onSelectedScalesChanged"
        />
        <hr class="panel-divider" />
        <ConfigPanel
          :config="currentConfig"
          @config-loaded="onConfigLoaded"
        />
        <hr class="panel-divider" />
        <ProjectPanel
          :state="projectFileInput"
          @project-loaded="onProjectLoaded"
        />
        <hr class="panel-divider" />
        <TemplatePanel
          :state="templateFileInput"
          @template-loaded="onTemplateLoaded"
        />
        <hr class="panel-divider" />
        <WarningPanel :warnings="warnings" />
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
        <hr class="panel-divider" />
        <BatchImportPanel @batch-items="onBatchItemsChanged" />
        <hr class="panel-divider" />
        <BatchTaskList
          :items="batchItems"
          @remove="onBatchItemRemoved"
        />
        <hr class="panel-divider" />
        <BatchExportPanel
          :exportableItems="exportableCount"
          :imageIds="exportableBatchIds"
          :selectedScales="selectedScales"
          :capInsets="insets"
          :contentInsets="contentInsets"
          :targetWidth="targetWidth"
          :targetHeight="targetHeight"
          @export-complete="onBatchExportComplete"
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
        :scale="scale"
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
.direction-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}
.direction-toggle {
  padding: 0.4rem 1rem;
  border: 1px solid #1a1a2e;
  border-radius: 4px;
  background: #1a1a2e;
  color: #fff;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.15s;
}
.direction-toggle:hover {
  background: #2d2d5e;
}
.guides-toggle {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  cursor: pointer;
  color: #555;
}
</style>
