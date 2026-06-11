<script setup lang="ts">
import { ref, watch } from 'vue'

const emit = defineEmits<{
  change: [payload: {
    text: string
    fontSize: number
    lineHeight: number
    fontFamily: string
    maxBubbleWidth: number
  }]
}>()

const text = ref('这是一条测试消息')
const fontSize = ref(16)
const lineHeight = ref(22)
const fontFamily = ref('sans-serif')
const maxBubbleWidth = ref(280)

function emitChange() {
  emit('change', {
    text: text.value,
    fontSize: fontSize.value,
    lineHeight: lineHeight.value,
    fontFamily: fontFamily.value,
    maxBubbleWidth: maxBubbleWidth.value,
  })
}

// Emit on mount
watch([text, fontSize, lineHeight, fontFamily, maxBubbleWidth], emitChange, {
  immediate: true,
})
</script>

<template>
  <div class="text-preview-panel">
    <h3>文字预览</h3>

    <label class="field">
      <span>文本内容</span>
      <textarea
        v-model="text"
        rows="3"
        placeholder="输入要显示的文本"
      />
    </label>

    <label class="field">
      <span>字号 (px)</span>
      <input
        type="number"
        v-model.number="fontSize"
        min="8"
        max="72"
        class="num-input"
      />
    </label>

    <label class="field">
      <span>行高 (px)</span>
      <input
        type="number"
        v-model.number="lineHeight"
        min="8"
        max="120"
        class="num-input"
      />
    </label>

    <label class="field">
      <span>最大气泡宽度 (px)</span>
      <div class="slider-row">
        <input
          type="range"
          v-model.number="maxBubbleWidth"
          min="100"
          max="500"
          step="10"
        />
        <span class="slider-value">{{ maxBubbleWidth }}</span>
      </div>
    </label>
  </div>
</template>

<style scoped>
.text-preview-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  font-size: 0.9rem;
  font-weight: 500;
}
textarea {
  width: 100%;
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  resize: vertical;
  font-family: inherit;
  box-sizing: border-box;
}
textarea:focus {
  outline: none;
  border-color: #1a1a2e;
}
.num-input {
  width: 5rem;
  padding: 0.3rem 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
}
.num-input:focus {
  outline: none;
  border-color: #1a1a2e;
}
.slider-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.slider-row input[type="range"] {
  flex: 1;
  height: 1.5rem;
  cursor: pointer;
}
.slider-value {
  min-width: 3rem;
  text-align: center;
  font-size: 0.9rem;
  color: #555;
}
</style>
