<script setup lang="ts">
import type { BatchItem } from '../core/batch'

defineProps<{
  items: BatchItem[]
}>()

const emit = defineEmits<{
  (e: 'remove', id: string): void
}>()

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

const statusLabels: Record<string, string> = {
  pending: '等待中',
  uploading: '上传中',
  uploaded: '已上传',
  exporting: '导出中',
  exported: '已导出',
  failed: '失败',
}

const statusColors: Record<string, string> = {
  pending: '#999',
  uploading: '#2196f3',
  uploaded: '#4caf50',
  exporting: '#ff9800',
  exported: '#4caf50',
  failed: '#c62828',
}
</script>

<template>
  <div class="batch-task-list">
    <h3>导入列表 ({{ items.length }})</h3>
    <div v-if="items.length === 0" class="empty-hint">
      暂无导入的图片
    </div>
    <ul v-else class="task-list">
      <li
        v-for="item in items"
        :key="item.id"
        class="task-item"
      >
        <div class="task-info">
          <span class="task-filename" :title="item.filename">{{ item.filename }}</span>
          <span class="task-dims">{{ item.width }}×{{ item.height }}</span>
          <span class="task-size">{{ formatSize(item.sizeBytes) }}</span>
        </div>
        <div class="task-meta">
          <span
            class="task-status"
            :style="{ color: statusColors[item.status] }"
          >
            {{ statusLabels[item.status] || item.status }}
          </span>
          <button
            class="task-remove"
            @click="emit('remove', item.id)"
            title="移除"
          >
            ✕
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.batch-task-list {
  font-size: 0.85rem;
}
.batch-task-list h3 {
  margin: 0 0 0.4rem;
  font-size: 0.9rem;
}
.empty-hint {
  color: #999;
  font-size: 0.8rem;
  text-align: center;
  padding: 0.5rem;
}
.task-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  max-height: 16rem;
  overflow-y: auto;
}
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.4rem 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #fafafa;
  gap: 0.5rem;
}
.task-info {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
  flex: 1;
}
.task-filename {
  font-size: 0.8rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.task-dims {
  font-size: 0.75rem;
  color: #666;
  font-family: 'SF Mono', 'Fira Code', monospace;
}
.task-size {
  font-size: 0.75rem;
  color: #999;
  font-family: 'SF Mono', 'Fira Code', monospace;
}
.task-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
}
.task-status {
  font-size: 0.75rem;
  font-weight: 500;
}
.task-remove {
  background: none;
  border: 1px solid #e0e0e0;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 0.15rem 0.35rem;
  color: #999;
  transition: color 0.15s, border-color 0.15s;
}
.task-remove:hover {
  color: #c62828;
  border-color: #c62828;
}
</style>
