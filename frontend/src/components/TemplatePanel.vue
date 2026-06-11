<script setup lang="ts">
import { ref } from 'vue'
import { serializeTemplate, deserializeTemplate, type BubbleTemplate, type TemplateFileInput } from '../core/templateFile'

const props = defineProps<{
  /** Current editor state for serializing a template */
  state: TemplateFileInput
}>()

const emit = defineEmits<{
  'template-loaded': [template: BubbleTemplate]
}>()

const message = ref<{ text: string; type: 'success' | 'error' } | null>(null)
let messageTimeout: ReturnType<typeof setTimeout> | null = null
const fileInput = ref<HTMLInputElement | null>(null)

// Template name/description for export
const templateName = ref('')
const templateDescription = ref('')

function showMessage(text: string, type: 'success' | 'error') {
  if (messageTimeout) clearTimeout(messageTimeout)
  message.value = { text, type }
  messageTimeout = setTimeout(() => {
    message.value = null
  }, 3000)
}

function handleExport() {
  const name = templateName.value.trim() || 'Custom Template'
  const desc = templateDescription.value.trim() || 'Exported from Bubble Stretch Tool'

  try {
    const template = serializeTemplate({
      name,
      description: desc,
      capInsets: props.state.capInsets,
      contentInsets: props.state.contentInsets,
      scale: props.state.scale,
      direction: props.state.direction,
    })
    const json = JSON.stringify(template, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const safeName = name.replace(/[^a-zA-Z0-9_-]/g, '_')
    a.download = `${safeName}.bubble-template.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showMessage('模板已导出', 'success')
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
      const template = deserializeTemplate(json)
      emit('template-loaded', template)
      showMessage('模板已导入并应用', 'success')
    } catch (e) {
      showMessage(`导入失败: ${(e as Error).message}`, 'error')
    }
  }
  reader.onerror = () => {
    showMessage('读取文件失败', 'error')
  }
  reader.readAsText(file)

  // Reset input so re-selecting the same file triggers change
  input.value = ''
}
</script>

<template>
  <div class="template-panel">
    <h3>模板 (.bubble-template.json)</h3>

    <!-- Export section -->
    <div class="template-export-section">
      <input
        v-model="templateName"
        placeholder="模板名称"
        class="template-input"
      />
      <input
        v-model="templateDescription"
        placeholder="模板描述（可选）"
        class="template-input"
      />
      <button class="tmpl-btn export-btn" @click="handleExport">
        导出模板
      </button>
    </div>

    <!-- Import section -->
    <div class="template-import-section">
      <button class="tmpl-btn import-btn" @click="triggerImport">
        导入模板
      </button>
      <input
        ref="fileInput"
        type="file"
        accept=".bubble-template.json,.json"
        style="display: none"
        @change="handleFileChange"
      />
    </div>

    <p v-if="message" :class="['tmpl-message', message.type]">
      {{ message.text }}
    </p>
  </div>
</template>

<style scoped>
.template-panel {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.template-panel h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #333;
}

.template-export-section {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.template-import-section {
  display: flex;
  gap: 0.5rem;
}

.template-input {
  padding: 0.35rem 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.15s;
}

.template-input:focus {
  border-color: #1a1a2e;
}

.tmpl-btn {
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
  flex: 1;
  background: #fff;
  color: #1a1a2e;
}

.import-btn:hover {
  background: #f0f0f5;
}

.tmpl-message {
  margin: 0;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.tmpl-message.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.tmpl-message.error {
  background: #fbe9e7;
  color: #c62828;
}
</style>
