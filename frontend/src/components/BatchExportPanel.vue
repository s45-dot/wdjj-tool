<script setup lang="ts">
import { ref, computed } from 'vue'
import { batchExport } from '../api/batchApi'

const props = withDefaults(defineProps<{
  exportableItems: number
  imageIds: string[]
  selectedScales: number[]
  capInsets: { top: number; right: number; bottom: number; left: number }
  contentInsets: { top: number; right: number; bottom: number; left: number }
  targetWidth: number
  targetHeight: number
}>(), {
  exportableItems: 0,
  imageIds: () => [],
  selectedScales: () => [1],
  capInsets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  contentInsets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  targetWidth: 240,
  targetHeight: 80,
})

const emit = defineEmits<{
  (e: 'export-complete'): void
}>()

const loading = ref(false)
const error = ref<string | null>(null)

// Valid: at least 1 exported item, at least 1 scale selected
const canExport = computed(() => {
  return props.exportableItems > 0 && props.selectedScales.length > 0
})

async function handleBatchExport() {
  if (props.imageIds.length === 0) return

  loading.value = true
  error.value = null

  const requestPayload = {
    images: props.imageIds.map(id => ({ imageId: id })),
    selectedScales: props.selectedScales,
    capInsets: props.capInsets,
    contentInsets: props.contentInsets,
    preview: {
      targetWidth: props.targetWidth,
      targetHeight: props.targetHeight,
    },
  }

  try {
    const result = await batchExport(requestPayload)

    // Trigger download via hidden anchor
    const fullUrl = `http://127.0.0.1:8080${result.downloadUrl}`
    const a = document.createElement('a')
    a.href = fullUrl
    a.download = result.filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)

    emit('export-complete')
  } catch (e) {
    error.value = (e as Error).message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="batch-export-panel">
    <h3>批量导出</h3>
    <p class="export-summary">
      可导出 <strong>{{ exportableItems }}</strong> 个图片，
      倍率: <strong>{{ selectedScales.map(s => `${s}×`).join(', ') }}</strong>
    </p>
    <button
      class="batch-export-btn"
      :disabled="!canExport || loading"
      @click="handleBatchExport"
    >
      {{ loading ? '导出中...' : '批量导出 ZIP' }}
    </button>
    <p v-if="error" class="export-error">{{ error }}</p>
  </div>
</template>

<style scoped>
.batch-export-panel {
  font-size: 0.85rem;
}
.batch-export-panel h3 {
  margin: 0 0 0.3rem;
  font-size: 0.9rem;
}
.export-summary {
  margin: 0 0 0.5rem;
  font-size: 0.8rem;
  color: #555;
}
.batch-export-btn {
  width: 100%;
  padding: 0.65rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  background: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
.batch-export-btn:hover:not(:disabled) {
  background: #2d2d5e;
}
.batch-export-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.export-error {
  font-size: 0.8rem;
  color: #c62828;
  margin: 0.3rem 0 0;
}
</style>
