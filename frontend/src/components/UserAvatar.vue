<template>
  <div 
    :class="['avatar', sizeClass, colorClass]"
    :style="customStyle"
  >
    {{ initial }}
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  username: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary'
  }
})

const initial = computed(() => {
  return props.username.charAt(0).toUpperCase()
})

const sizeClass = computed(() => `avatar-${props.size}`)

const colorClass = computed(() => {
  // Generate consistent color based on username
  const variants = ['primary', 'success', 'warning', 'danger']
  const hash = props.username.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  const variantIndex = hash % variants.length
  return props.variant === 'primary' ? '' : `avatar-${variants[variantIndex]}`
})

const customStyle = computed(() => {
  if (props.variant !== 'primary') {
    const gradients = {
      success: 'linear-gradient(135deg, #10b981, #059669)',
      warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
      danger: 'linear-gradient(135deg, #ef4444, #dc2626)'
    }
    const hash = props.username.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
    const variantKeys = Object.keys(gradients)
    const gradient = gradients[variantKeys[hash % variantKeys.length]]
    return { background: gradient }
  }
  return {}
})
</script>

<style scoped>
.avatar {
  flex-shrink: 0;
}
</style>
