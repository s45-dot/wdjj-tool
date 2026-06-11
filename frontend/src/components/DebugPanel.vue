<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  filename?: string
  sourceWidth: number
  sourceHeight: number
  sizeBytes: number
  targetWidth: number
  targetHeight: number
  insets: { top: number; right: number; bottom: number; left: number }
  backendConnected: boolean
  backendVersion: string
  version: string
  scale?: number
}>(), {
  filename: '-',
  sourceWidth: 0,
  sourceHeight: 0,
  sizeBytes: 0,
  targetWidth: 0,
  targetHeight: 0,
  insets: () => ({ top: 0, right: 0, bottom: 0, left: 0 }),
  backendConnected: false,
  backendVersion: '',
  version: '',
  scale: 1,
})

const sourceCenterWidth = computed(() => props.sourceWidth - props.insets.left - props.insets.right)
const sourceCenterHeight = computed(() => props.sourceHeight - props.insets.top - props.insets.bottom)
const targetCenterWidth = computed(() => props.targetWidth - props.insets.left - props.insets.right)
const targetCenterHeight = computed(() => props.targetHeight - props.insets.top - props.insets.bottom)

const errors = computed(() => {
  const e: string[] = []
  if (props.insets.left + props.insets.right >= props.sourceWidth) {
    e.push('水平内边距之和超过源图片宽度')
  }
  if (props.insets.top + props.insets.bottom >= props.sourceHeight) {
    e.push('垂直内边距之和超过源图片高度')
  }
  if (props.insets.left + props.insets.right >= props.targetWidth) {
    e.push('水平内边距之和超过目标宽度')
  }
  if (props.insets.top + props.insets.bottom >= props.targetHeight) {
    e.push('垂直内边距之和超过目标高度')
  }
  return e
})

const warnings = computed(() => {
  const w: string[] = []
  if (sourceCenterWidth.value < 2) w.push('源图片中心区域宽度小于 2px')
  if (sourceCenterHeight.value < 2) w.push('源图片中心区域高度小于 2px')
  if (targetCenterWidth.value < 2) w.push('目标图片中心区域宽度小于 2px')
  if (targetCenterHeight.value < 2) w.push('目标图片中心区域高度小于 2px')
  return w
})

const valid = computed(() => errors.value.length === 0)
</script>

<template>
  <div class="debug-panel">
    <h3>调试信息</h3>
    <dl>
      <dt>版本</dt>
      <dd>{{ version || '-' }}</dd>
      <dt>文件名</dt>
      <dd>{{ filename || '-' }}</dd>
      <dt>源图片尺寸</dt>
      <dd>{{ sourceWidth }} × {{ sourceHeight }}</dd>
      <dt>文件大小</dt>
      <dd>{{ (sizeBytes / 1024).toFixed(1) }} KB</dd>
      <dt>目标尺寸</dt>
      <dd>{{ targetWidth }} × {{ targetHeight }}</dd>
      <dt>内边距</dt>
      <dd>上={{ insets.top }} 右={{ insets.right }} 下={{ insets.bottom }} 左={{ insets.left }}</dd>
      <dt>源图片中心区域</dt>
      <dd>{{ sourceCenterWidth }} × {{ sourceCenterHeight }}</dd>
      <dt>目标中心区域</dt>
      <dd>{{ targetCenterWidth }} × {{ targetCenterHeight }}</dd>
      <dt>缩放比例</dt>
      <dd>{{ scale }}×</dd>
      <dt>后端状态</dt>
      <dd :class="backendConnected ? 'connected' : 'disconnected'">
        {{ backendConnected ? `已连接 (v${backendVersion})` : '未连接' }}
      </dd>
      <dt>状态</dt>
      <dd :class="{ valid, invalid: !valid }">{{ valid ? '有效' : '无效' }}</dd>
    </dl>
    <div v-if="errors.length" class="messages errors">
      <h4>错误</h4>
      <ul>
        <li v-for="err in errors" :key="err">{{ err }}</li>
      </ul>
    </div>
    <div v-if="warnings.length" class="messages warnings">
      <h4>警告</h4>
      <ul>
        <li v-for="warn in warnings" :key="warn">{{ warn }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.debug-panel {
  font-size: 0.85rem;
  line-height: 1.6;
}
dl {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.15rem 1rem;
  margin: 0.5rem 0;
}
dt {
  font-weight: 600;
  color: #555;
}
dd {
  margin: 0;
  font-family: 'SF Mono', 'Fira Code', monospace;
}
.valid {
  color: #2e7d32;
  font-weight: 600;
}
.invalid {
  color: #c62828;
  font-weight: 600;
}
.connected {
  color: #2e7d32;
  font-weight: 600;
}
.disconnected {
  color: #c62828;
  font-weight: 600;
}
.messages {
  margin-top: 0.5rem;
}
.messages h4 {
  margin: 0.5rem 0 0.25rem;
  font-size: 0.85rem;
}
.messages ul {
  margin: 0;
  padding-left: 1.25rem;
}
.errors {
  color: #c62828;
}
.warnings {
  color: #e65100;
}
</style>
