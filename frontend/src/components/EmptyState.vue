<template>
  <div class="empty-state">
    <div class="empty-icon">{{ icon }}</div>
    <h3 class="empty-title">{{ title }}</h3>
    <p class="empty-description">{{ description }}</p>
    <button 
      v-if="buttonText" 
      class="btn btn-primary"
      @click="handleAction"
    >
      {{ buttonText }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  icon: {
    type: String,
    default: '📦'
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  buttonText: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['action'])

const handleAction = () => {
  emit('action')
}
</script>

<style scoped>
.empty-state {
  padding: var(--spacing-3xl) var(--spacing-lg);
  text-align: center;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-lg);
  opacity: 0.5;
}

.empty-title {
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-xl);
}

.empty-description {
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}
</style>
