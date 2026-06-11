<script setup lang="ts">
import { ref } from 'vue'
import type { BatchItem } from '../core/batch'
import { uploadImage } from '../api/uploadApi'

const emit = defineEmits<{
  (e: 'batch-items', items: BatchItem[]): void
}>()

const batchItems = ref<BatchItem[]>([])
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function generateId(): string {
  return `batch-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

async function handleFiles(event: Event) {
  const input = event.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0) return

  uploading.value = true
  const newItems: BatchItem[] = []

  for (let i = 0; i < files.length; i++) {
    const file = files[i]

    // Load image to get dimensions
    const url = URL.createObjectURL(file)
    const img = new Image()
    await new Promise<void>((resolve, reject) => {
      img.onload = () => {
        URL.revokeObjectURL(url)
        resolve()
      }
      img.onerror = () => {
        URL.revokeObjectURL(url)
        reject(new Error(`Failed to load: ${file.name}`))
      }
      img.src = url
    })

    const item: BatchItem = {
      id: generateId(),
      file,
      filename: file.name,
      width: img.naturalWidth,
      height: img.naturalHeight,
      sizeBytes: file.size,
      status: 'pending',
    }

    // Upload to backend in parallel
    item.status = 'uploading'
    try {
      const result = await uploadImage(file)
      item.imageId = result.imageId
      item.status = 'uploaded'
    } catch (e) {
      item.status = 'failed'
      item.error = (e as Error).message
    }

    newItems.push(item)
  }

  batchItems.value = [...batchItems.value, ...newItems]
  emit('batch-items', [...batchItems.value])
  uploading.value = false

  // Reset file input so re-selecting the same files triggers change
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

</script>

<template>
  <div class="batch-import-panel">
    <h3>批量导入</h3>
    <div class="import-area">
      <label class="import-label">
        <input
          ref="fileInput"
          type="file"
          multiple
          accept="image/png"
          @change="handleFiles"
        />
        <span class="import-icon">📥</span>
        <span class="import-text">选择多个 PNG 图片</span>
        <span class="import-hint">支持多选</span>
      </label>
    </div>
    <p v-if="uploading" class="upload-status">上传中...</p>
  </div>
</template>

<style scoped>
.batch-import-panel {
  font-size: 0.85rem;
}
.batch-import-panel h3 {
  margin: 0 0 0.4rem;
  font-size: 0.9rem;
}
.import-area {
  text-align: center;
}
.import-label {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  padding: 1.5rem 1rem;
  border: 2px dashed #ccc;
  border-radius: 8px;
  transition: border-color 0.2s, background 0.2s;
  width: 100%;
  box-sizing: border-box;
}
.import-label:hover {
  border-color: #1a1a2e;
  background: #f8f8ff;
}
input[type="file"] {
  display: none;
}
.import-icon {
  font-size: 1.5rem;
}
.import-text {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
}
.import-hint {
  font-size: 0.75rem;
  color: #999;
}
.upload-status {
  font-size: 0.8rem;
  color: #1a1a2e;
  margin: 0.3rem 0 0;
  text-align: center;
}
</style>
