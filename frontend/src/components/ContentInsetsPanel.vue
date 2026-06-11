<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  contentInsets?: { top: number; right: number; bottom: number; left: number }
  sourceWidth?: number
  sourceHeight?: number
}>(), {
  contentInsets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  sourceWidth: 0,
  sourceHeight: 0,
})

const emit = defineEmits<{
  change: [insets: { top: number; right: number; bottom: number; left: number }]
}>()

// Content insets use a fixed max cap; source dimensions are not a hard constraint
const MAX = 500

const maxTop = computed(() => MAX)
const maxRight = computed(() => MAX)
const maxBottom = computed(() => MAX)
const maxLeft = computed(() => MAX)

const fields = computed(() => [
  { key: 'top' as const, label: '上', max: maxTop.value },
  { key: 'right' as const, label: '右', max: maxRight.value },
  { key: 'bottom' as const, label: '下', max: maxBottom.value },
  { key: 'left' as const, label: '左', max: maxLeft.value },
])

function update(key: 'top' | 'right' | 'bottom' | 'left', value: string) {
  const num = parseInt(value, 10)
  if (isNaN(num)) return
  const field = fields.value.find(f => f.key === key)
  const clamped = Math.max(0, Math.min(num, field?.max ?? MAX))
  emit('change', { ...props.contentInsets, [key]: clamped })
}
</script>

<template>
  <div class="content-insets-panel">
    <h3>Content Insets (文字安全区)</h3>
    <p class="insets-desc">设置文字/内容的安全区域边界</p>
    <div
      class="inset-row"
      v-for="field in fields"
      :key="field.key"
    >
      <label :for="'ci-range-' + field.key">{{ field.label }}</label>
      <input
        :id="'ci-range-' + field.key"
        type="range"
        :min="0"
        :max="field.max"
        :value="contentInsets[field.key]"
        @input="update(field.key, ($event.target as HTMLInputElement).value)"
      />
      <input
        :id="'ci-num-' + field.key"
        type="number"
        :min="0"
        :max="field.max"
        :value="contentInsets[field.key]"
        @input="update(field.key, ($event.target as HTMLInputElement).value)"
        class="num-input"
      />
    </div>
  </div>
</template>

<style scoped>
.content-insets-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.insets-desc {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
}
.inset-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.inset-row label {
  min-width: 2.5rem;
  font-weight: 500;
  font-size: 0.9rem;
}
input[type="range"] {
  flex: 1;
  height: 1.5rem;
  cursor: pointer;
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
</style>
