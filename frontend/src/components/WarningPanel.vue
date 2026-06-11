<script setup lang="ts">
import type { WarningItem } from '../core/warnings'

defineProps<{
  warnings: WarningItem[]
}>()
</script>

<template>
  <div class="warning-panel">
    <details v-if="warnings.length > 0" open>
      <summary>警告与提示 ({{ warnings.length }})</summary>
      <ul class="warning-list">
        <li
          v-for="w in warnings"
          :key="w.code"
          :class="`warning-item warning-${w.level}`"
        >
          {{ w.message }}
        </li>
      </ul>
    </details>
    <div v-else class="warning-empty">
      <span class="ok-icon">✓</span> 无警告
    </div>
  </div>
</template>

<style scoped>
.warning-panel {
  font-size: 0.85rem;
}
details {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 0.4rem 0.6rem;
}
summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
}
.warning-list {
  list-style: none;
  padding: 0.25rem 0 0;
  margin: 0;
}
.warning-item {
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  margin-top: 0.2rem;
  font-size: 0.85rem;
}
.warning-info {
  background: #e3f2fd;
  color: #1565c0;
}
.warning-warning {
  background: #fff3e0;
  color: #e65100;
}
.warning-error {
  background: #ffebee;
  color: #c62828;
}
.warning-empty {
  color: #2e7d32;
  font-size: 0.85rem;
}
.ok-icon {
  font-weight: 700;
}
</style>
