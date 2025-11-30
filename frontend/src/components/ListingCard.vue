<template>
  <div class="listing-card card-hover">
    <div class="listing-image">
      <span class="listing-icon">{{ categoryIcon }}</span>
    </div>
    <div class="listing-content">
      <div class="listing-price">${{ listing.price.toFixed(2) }}</div>
      <div class="listing-title">{{ listing.title }}</div>
      <div class="listing-desc">{{ listing.description }}</div>
      
      <div class="listing-meta">
        <div class="seller">
          <UserAvatar 
            :username="listing.seller.username" 
            size="sm"
            variant="auto"
          />
          <span class="seller-name">{{ listing.seller.displayName }}</span>
        </div>
        <button class="btn btn-primary btn-sm" @click="handleMessage">
          Message
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import UserAvatar from './UserAvatar.vue'

const props = defineProps({
  listing: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['message'])

const categoryIcon = computed(() => {
  const icons = {
    'Textbooks': '📚',
    'Electronics': '💻',
    'Furniture': '🪑',
    'Clothing': '👕',
    'Gaming': '🎮',
    'Musical Instruments': '🎵'
  }
  return icons[props.listing.category] || '📦'
})

const handleMessage = () => {
  emit('message', props.listing)
}
</script>

<style scoped>
.listing-card {
  overflow: hidden;
  padding: 0;
}

.listing-image {
  width: 100%;
  height: 200px;
  background: var(--gradient-hero);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
}

.listing-icon {
  filter: brightness(1.2);
}

.listing-content {
  padding: var(--spacing-lg);
}

.listing-price {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.listing-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.listing-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
}

.listing-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border);
}

.seller {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.seller-name {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}
</style>
