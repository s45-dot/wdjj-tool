<script setup lang="ts">
import { SCALES, pxToPt } from '../core/scale'
import type { Insets } from '../core/types'

defineProps<{
  scale: number
  capInsets: Insets
  contentInsets: Insets
}>()

const emit = defineEmits<{
  (e: 'update:scale', value: number): void
}>()

function selectScale(s: number) {
  emit('update:scale', s)
}
</script>

<template>
  <div class="scale-panel">
    <h3>缩放比例</h3>
    <div class="scale-options">
      <label v-for="s in SCALES" :key="s" class="scale-radio">
        <input
          type="radio"
          :value="s"
          :checked="scale === s"
          @change="selectScale(s)"
        />
        <span class="scale-label">{{ s }}×</span>
      </label>
    </div>

    <div class="scale-details">
      <div class="scale-row">
        <span class="scale-dim-label">Cap Insets</span>
        <table class="scale-table">
          <tr>
            <th>方向</th>
            <th>px</th>
            <th>pt</th>
          </tr>
          <tr>
            <td>上</td>
            <td>{{ capInsets.top }}</td>
            <td>{{ pxToPt(capInsets.top, scale).toFixed(1) }}</td>
          </tr>
          <tr>
            <td>右</td>
            <td>{{ capInsets.right }}</td>
            <td>{{ pxToPt(capInsets.right, scale).toFixed(1) }}</td>
          </tr>
          <tr>
            <td>下</td>
            <td>{{ capInsets.bottom }}</td>
            <td>{{ pxToPt(capInsets.bottom, scale).toFixed(1) }}</td>
          </tr>
          <tr>
            <td>左</td>
            <td>{{ capInsets.left }}</td>
            <td>{{ pxToPt(capInsets.left, scale).toFixed(1) }}</td>
          </tr>
        </table>
      </div>

      <div class="scale-row">
        <span class="scale-dim-label">Content Insets</span>
        <table class="scale-table">
          <tr>
            <th>方向</th>
            <th>px</th>
            <th>pt</th>
          </tr>
          <tr>
            <td>上</td>
            <td>{{ contentInsets.top }}</td>
            <td>{{ pxToPt(contentInsets.top, scale).toFixed(1) }}</td>
          </tr>
          <tr>
            <td>右</td>
            <td>{{ contentInsets.right }}</td>
            <td>{{ pxToPt(contentInsets.right, scale).toFixed(1) }}</td>
          </tr>
          <tr>
            <td>下</td>
            <td>{{ contentInsets.bottom }}</td>
            <td>{{ pxToPt(contentInsets.bottom, scale).toFixed(1) }}</td>
          </tr>
          <tr>
            <td>左</td>
            <td>{{ contentInsets.left }}</td>
            <td>{{ pxToPt(contentInsets.left, scale).toFixed(1) }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scale-panel {
  font-size: 0.85rem;
}
.scale-panel h3 {
  margin: 0 0 0.4rem;
  font-size: 0.9rem;
}
.scale-options {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}
.scale-radio {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
}
.scale-label {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-weight: 600;
}
.scale-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.scale-row {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.scale-dim-label {
  font-weight: 600;
  color: #555;
  font-size: 0.8rem;
}
.scale-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}
.scale-table th,
.scale-table td {
  border: 1px solid #e0e0e0;
  padding: 0.15rem 0.4rem;
  text-align: center;
}
.scale-table th {
  background: #f5f5f5;
  font-weight: 600;
  color: #555;
}
.scale-table td {
  font-family: 'SF Mono', 'Fira Code', monospace;
}
</style>
