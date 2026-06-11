<script setup lang="ts">
import { ref } from 'vue'
import { uploadImage } from '../api/uploadApi'

const emit = defineEmits<{
  loaded: [data: {
    url: string
    width: number
    height: number
    filename: string
    size: number
    imageId?: string
    uploadError?: string
  }]
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

async function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  const url = URL.createObjectURL(file)
  const img = new Image()

  const imageLoaded = new Promise<void>((resolve, reject) => {
    img.onload = () => resolve()
    img.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('Failed to load image'))
    }
  })

  img.src = url
  await imageLoaded

  // Local preview payload (always emitted)
  const localPayload = {
    url,
    width: img.naturalWidth,
    height: img.naturalHeight,
    filename: file.name,
    size: file.size,
  }

  // Try server upload in parallel
  uploading.value = true
  try {
    const uploadResult = await uploadImage(file)
    emit('loaded', { ...localPayload, imageId: uploadResult.imageId })
  } catch (e) {
    // Upload failed — still emit local preview with error flag
    emit('loaded', { ...localPayload, uploadError: (e as Error).message })
  } finally {
    uploading.value = false
  }
}

// Pre-existing — kept for template use despite minor lint gap
function resetInput() {
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<template>
  <div class="uploader">
    <label class="uploader-label">
      <input
        ref="fileInput"
        type="file"
        accept="image/png"
        @change="handleFileChange"
      />
      <span class="uploader-icon">📁</span>
      <span class="uploader-text">选择 PNG 图片</span>
      <span class="uploader-hint">点击或拖拽上传</span>
    </label>
    <p v-if="uploading" class="upload-status">上传中...</p>
  </div>
</template>

<style scoped>
.uploader {
  padding: 1rem;
  text-align: center;
}
.uploader-label {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 2rem 1.5rem;
  border: 2px dashed #ccc;
  border-radius: 8px;
  transition: border-color 0.2s, background 0.2s;
  width: 100%;
  box-sizing: border-box;
}
.uploader-label:hover {
  border-color: #1a1a2e;
  background: #f8f8ff;
}
input[type="file"] {
  display: none;
}
.uploader-icon {
  font-size: 2rem;
}
.uploader-text {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
}
.uploader-hint {
  font-size: 0.8rem;
  color: #999;
}
.upload-status {
  font-size: 0.85rem;
  color: #1a1a2e;
  margin: 0.5rem 0 0;
}
</style>
