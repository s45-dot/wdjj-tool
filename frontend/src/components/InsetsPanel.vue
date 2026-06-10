<script setup lang="ts">
const props = withDefaults(defineProps<{
  insets?: { top: number; right: number; bottom: number; left: number }
  maxTop?: number
  maxRight?: number
  maxBottom?: number
  maxLeft?: number
}>(), {
  insets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  maxTop: 999,
  maxRight: 999,
  maxBottom: 999,
  maxLeft: 999,
})

const emit = defineEmits<{
  change: [insets: { top: number; right: number; bottom: number; left: number }]
}>()

const fields: { key: 'top' | 'right' | 'bottom' | 'left'; label: string; max: number }[] = [
  { key: 'top', label: '上', max: props.maxTop },
  { key: 'right', label: '右', max: props.maxRight },
  { key: 'bottom', label: '下', max: props.maxBottom },
  { key: 'left', label: '左', max: props.maxLeft },
]

function update(key: 'top' | 'right' | 'bottom' | 'left', value: string) {
  const num = parseInt(value, 10)
  if (isNaN(num)) return
  const field = fields.find(f => f.key === key)
  const clamped = Math.max(0, Math.min(num, field?.max ?? 999))
  emit('change', { ...props.insets, [key]: clamped })
}
</script>

<template>
  <div class="insets-panel">
    <h3>九宫格内边距</h3>
    <p class="insets-desc">设置要保留的边缘区域大小</p>
    <div
      class="inset-row"
      v-for="field in fields"
      :key="field.key"
    >
      <label :for="'range-' + field.key">{{ field.label }}</label>
      <input
        :id="'range-' + field.key"
        type="range"
        :min="0"
        :max="field.max"
        :value="insets[field.key]"
        @input="update(field.key, ($event.target as HTMLInputElement).value)"
      />
      <input
        :id="'num-' + field.key"
        type="number"
        :min="0"
        :max="field.max"
        :value="insets[field.key]"
        @input="update(field.key, ($event.target as HTMLInputElement).value)"
        class="num-input"
      />
    </div>
  </div>
</template>

<style scoped>
.insets-panel {
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
