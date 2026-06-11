<script setup lang="ts">
defineProps<{
  previewWidth?: number
}>()
</script>

<template>
  <div class="device-preview">
    <div class="phone-label">Phone Preview</div>
    <div class="phone-frame" :style="{ maxWidth: previewWidth + 'px' }">
      <div class="phone-notch"></div>
      <div class="phone-screen">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.device-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.phone-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.phone-frame {
  width: 100%;
  background: #111;
  border-radius: 36px;
  padding: 12px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.08);
  position: relative;
}

.phone-notch {
  width: 120px;
  height: 24px;
  background: #000;
  border-radius: 0 0 16px 16px;
  margin: -12px auto 8px;
}

.phone-screen {
  background: #fefefe;
  border-radius: 24px;
  overflow: hidden;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
