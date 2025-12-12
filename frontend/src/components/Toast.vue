<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`]"
      >
        <span class="toast-icon">{{ icons[toast.type] }}</span>
        <span class="toast-message">{{ toast.message }}</span>
        <button class="toast-close" @click="removeToast(toast.id)">×</button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

const icons = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ'
}

function addToast(message, type = 'info', duration = 4000) {
  const id = ++toastId
  toasts.value.push({ id, message, type })
  
  if (duration > 0) {
    setTimeout(() => removeToast(id), duration)
  }
  
  return id
}

function removeToast(id) {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

// Expose methods for use in other components
defineExpose({
  success: (msg) => addToast(msg, 'success'),
  error: (msg) => addToast(msg, 'error'),
  warning: (msg) => addToast(msg, 'warning'),
  info: (msg) => addToast(msg, 'info'),
  remove: removeToast
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  font-weight: 500;
  min-width: 280px;
}

.toast-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.toast-error {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.toast-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.toast-info {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.toast-icon {
  font-size: 18px;
  font-weight: bold;
}

.toast-message {
  flex: 1;
}

.toast-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Animations */
.toast-enter-active {
  animation: slideIn 0.3s ease-out;
}

.toast-leave-active {
  animation: slideOut 0.3s ease-in;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}
</style>
