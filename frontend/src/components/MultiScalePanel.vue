<script setup lang="ts">
import { ref, watch } from 'vue'
import { SUPPORTED_SCALES, validateScales } from '../core/multiScale'

const emit = defineEmits<{
  (e: 'update:selectedScales', scales: number[]): void
}>()

// Selected scales — default to current scale only
const selected = ref<number[]>([SUPPORTED_SCALES[0]])

const validationError = ref<string | null>(null)

// Emit on change
watch(selected, (scales) => {
  try {
    validateScales(scales)
    validationError.value = null
    emit('update:selectedScales', [...scales])
  } catch (e) {
    validationError.value = (e as Error).message
    // Still emit — let parent decide what to do with invalid state
    emit('update:selectedScales', [...scales])
  }
}, { deep: true })

function toggleScale(s: number) {
  const idx = selected.value.indexOf(s)
  if (idx >= 0) {
    // Don't allow deselecting the last item
    if (selected.value.length > 1) {
      selected.value.splice(idx, 1)
    }
  } else {
    selected.value.push(s)
  }
  // Trigger reactivity
  selected.value = [...selected.value]
}
</script>

<template>
  <div class="multi-scale-panel">
    <h3>多倍率导出</h3>
    <p class="scale-hint">选择要导出的倍率：</p>
    <div class="scale-checkboxes">
      <label
        v-for="s in SUPPORTED_SCALES"
        :key="s"
        class="scale-checkbox"
      >
        <input
          type="checkbox"
          :checked="selected.includes(s)"
          @change="toggleScale(s)"
        />
        <span class="scale-label">{{ s }}×</span>
      </label>
    </div>
    <p v-if="validationError" class="validation-error">{{ validationError }}</p>
  </div>
</template>

<style scoped>
.multi-scale-panel {
  font-size: 0.85rem;
}
.multi-scale-panel h3 {
  margin: 0 0 0.3rem;
  font-size: 0.9rem;
}
.scale-hint {
  margin: 0 0 0.4rem;
  font-size: 0.8rem;
  color: #666;
}
.scale-checkboxes {
  display: flex;
  gap: 1rem;
}
.scale-checkbox {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  cursor: pointer;
}
.scale-checkbox input {
  cursor: pointer;
}
.scale-label {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-weight: 600;
}
.validation-error {
  color: #c62828;
  font-size: 0.8rem;
  margin: 0.3rem 0 0;
}
</style>
