<script setup lang="ts">
import { ref } from 'vue'
import { exportConfig, importConfig, type BubbleConfig } from '../core/config'

const props = defineProps<{
  config: BubbleConfig
}>()

const emit = defineEmits<{
  'config-loaded': [config: BubbleConfig]
}>()

const message = ref<{ text: string; type: 'success' | 'error' } | null>(null)
let messageTimeout: ReturnType<typeof setTimeout> | null = null
const fileInput = ref<HTMLInputElement | null>(null)

function showMessage(text: string, type: 'success' | 'error') {
  if (messageTimeout) clearTimeout(messageTimeout)
  message.value = { text, type }
  messageTimeout = setTimeout(() => {
    message.value = null
  }, 3000)
}

function handleExport() {
  try {
    const json = exportConfig(props.config)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'bubble-config.json'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showMessage('配置已导出', 'success')
  } catch (e) {
    showMessage(`导出失败: ${(e as Error).message}`, 'error')
  }
}

function triggerImport() {
  fileInput.value?.click()
}

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    try {
      const json = reader.result as string
      const config = importConfig(json)
      emit('config-loaded', config)
      showMessage('配置已导入', 'success')
    } catch (e) {
      showMessage(`导入失败: ${(e as Error).message}`, 'error')
    }
  }
  reader.onerror = () => {
    showMessage('读取文件失败', 'error')
  }
  reader.readAsText(file)

  // Reset input so re-selecting the same file triggers the change event
  input.value = ''
}
</script>

<template>
  <div class="config-panel">
    <h3>配置导入/导出</h3>

    <div class="config-actions">
      <button class="config-btn export-btn" @click="handleExport">
        导出配置
      </button>
      <button class="config-btn import-btn" @click="triggerImport">
        导入配置
      </button>
      <input
        ref="fileInput"
        type="file"
        accept=".json"
        style="display: none"
        @change="handleFileChange"
      />
    </div>

    <p v-if="message" :class="['config-message', message.type]">
      {{ message.text }}
    </p>
  </div>
</template>

<style scoped>
.config-panel {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-panel h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #333;
}

.config-actions {
  display: flex;
  gap: 0.5rem;
}

.config-btn {
  flex: 1;
  padding: 0.4rem 0.75rem;
  border: 1px solid #1a1a2e;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.15s;
}

.export-btn {
  background: #1a1a2e;
  color: #fff;
}

.export-btn:hover {
  background: #2d2d5e;
}

.import-btn {
  background: #fff;
  color: #1a1a2e;
}

.import-btn:hover {
  background: #f0f0f5;
}

.config-message {
  margin: 0;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.config-message.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.config-message.error {
  background: #fbe9e7;
  color: #c62828;
}
</style>
