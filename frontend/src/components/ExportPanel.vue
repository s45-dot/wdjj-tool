<script setup lang="ts">
import { ref, computed } from 'vue'
import { exportImage } from '../api/exportApi'

const props = withDefaults(defineProps<{
  imageId: string | null
  capInsets: { top: number; right: number; bottom: number; left: number }
  contentInsets: { top: number; right: number; bottom: number; left: number }
  targetWidth: number
  targetHeight: number
  sourceWidth: number
  sourceHeight: number
}>(), {
  imageId: null,
  capInsets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  contentInsets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  targetWidth: 240,
  targetHeight: 80,
  sourceWidth: 0,
  sourceHeight: 0,
})

const loading = ref(false)
const error = ref<string | null>(null)

// Output format toggles — all default true
const outputs = ref({
  androidNinePatch: true,
  iosJson: true,
  androidJson: true,
  previewPng: true,
  readme: true,
  sourcePng: true,
})

// Scale: 1x / 2x / 3x
const scale = ref(1)

// Custom target width/height — local modifiable copies
const localTargetWidth = ref(props.targetWidth)
const localTargetHeight = ref(props.targetHeight)

// Disable export when no imageId or insets overlap source dimensions
const canExport = computed(() => {
  if (!props.imageId) return false
  const { top, right, bottom, left } = props.capInsets
  if (left + right >= props.sourceWidth) return false
  if (top + bottom >= props.sourceHeight) return false
  return true
})

async function handleExport() {
  if (!props.imageId) return

  loading.value = true
  error.value = null

  const requestPayload = {
    imageId: props.imageId,
    scale: scale.value,
    capInsets: props.capInsets,
    contentInsets: props.contentInsets,
    preview: {
      targetWidth: localTargetWidth.value,
      targetHeight: localTargetHeight.value,
    },
    outputs: { ...outputs.value },
  }

  try {
    const result = await exportImage(requestPayload)

    // Trigger download via hidden anchor
    const fullUrl = `http://127.0.0.1:8080${result.downloadUrl}`
    const a = document.createElement('a')
    a.href = fullUrl
    a.download = result.filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  } catch (e) {
    error.value = (e as Error).message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="export-panel">
    <h3>导出设置</h3>

    <!-- Output format checkboxes -->
    <fieldset class="outputs-fieldset">
      <legend>输出格式</legend>
      <label class="output-checkbox">
        <input type="checkbox" v-model="outputs.androidNinePatch" />
        Android .9.png
      </label>
      <label class="output-checkbox">
        <input type="checkbox" v-model="outputs.iosJson" />
        iOS JSON
      </label>
      <label class="output-checkbox">
        <input type="checkbox" v-model="outputs.androidJson" />
        Android JSON
      </label>
      <label class="output-checkbox">
        <input type="checkbox" v-model="outputs.previewPng" />
        Preview PNG
      </label>
      <label class="output-checkbox">
        <input type="checkbox" v-model="outputs.readme" />
        README
      </label>
      <label class="output-checkbox">
        <input type="checkbox" v-model="outputs.sourcePng" />
        Source PNG
      </label>
    </fieldset>

    <!-- Target dimensions -->
    <fieldset class="dims-fieldset">
      <legend>目标尺寸 (px)</legend>
      <div class="dims-row">
        <label for="export-width">宽</label>
        <input
          id="export-width"
          type="number"
          min="1"
          v-model.number="localTargetWidth"
          class="dims-input"
        />
        <label for="export-height">高</label>
        <input
          id="export-height"
          type="number"
          min="1"
          v-model.number="localTargetHeight"
          class="dims-input"
        />
      </div>
    </fieldset>

    <!-- Scale selector -->
    <fieldset class="scale-fieldset">
      <legend>缩放倍数</legend>
      <div class="scale-row">
        <label class="scale-option">
          <input type="radio" v-model.number="scale" :value="1" />
          1×
        </label>
        <label class="scale-option">
          <input type="radio" v-model.number="scale" :value="2" />
          2×
        </label>
        <label class="scale-option">
          <input type="radio" v-model.number="scale" :value="3" />
          3×
        </label>
      </div>
    </fieldset>

    <!-- Export button -->
    <button
      class="export-btn"
      :disabled="!canExport || loading"
      @click="handleExport"
    >
      {{ loading ? '导出中...' : '导出 ZIP' }}
    </button>

    <!-- Error message -->
    <p v-if="error" class="export-error">{{ error }}</p>
  </div>
</template>

<style scoped>
.export-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
fieldset {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.75rem;
  margin: 0;
}
legend {
  font-size: 0.85rem;
  font-weight: 600;
  color: #555;
  padding: 0 0.25rem;
}
.outputs-fieldset {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.output-checkbox {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.9rem;
  cursor: pointer;
}
.output-checkbox input {
  cursor: pointer;
}
.dims-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.dims-row label {
  font-size: 0.9rem;
}
.dims-input {
  width: 5rem;
  padding: 0.3rem 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
}
.dims-input:focus {
  outline: none;
  border-color: #1a1a2e;
}
.scale-row {
  display: flex;
  gap: 1rem;
}
.scale-option {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  cursor: pointer;
}
.scale-option input {
  cursor: pointer;
}
.export-btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  background: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
.export-btn:hover:not(:disabled) {
  background: #2d2d5e;
}
.export-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.export-error {
  font-size: 0.85rem;
  color: #c62828;
  margin: 0;
}
</style>
