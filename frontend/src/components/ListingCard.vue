<template>
  <router-link :to="`/listings/${listing.id}`" class="listing-card">
    <div class="listing-image">
      <img 
        v-if="listing.image" 
        :src="getImageUrl(listing.image)" 
        :alt="listing.title"
      />
      <div v-else class="listing-placeholder">
        <span class="placeholder-icon">{{ categoryIcon }}</span>
      </div>
      <span class="category-tag">{{ listing.category }}</span>
      <div v-if="listing.viewCount" class="view-count">
        <span>👁</span> {{ listing.viewCount }}
      </div>
    </div>
    <div class="listing-content">
      <div class="listing-price">{{ formatPrice(listing.price) }} ₸</div>
      <h3 class="listing-title">{{ listing.title }}</h3>
      <p class="listing-desc">{{ truncateDesc(listing.description) }}</p>
      
      <div class="listing-footer">
        <div class="seller">
          <UserAvatar 
            :username="listing.seller?.username" 
            size="sm"
            variant="auto"
          />
          <span class="seller-name">{{ $t('card.by') }} {{ listing.seller?.displayName || listing.seller?.username }}</span>
        </div>
        <button class="message-btn" @click.prevent="handleMessage" :title="$t('card.view_details')">
          <span class="message-icon">💬</span>
        </button>
      </div>
    </div>
  </router-link>
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
    'Musical Instruments': '🎵',
    'Sports': '⚽',
    'Other': '📦'
  }
  return icons[props.listing.category] || '📦'
})

function getImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

function formatPrice(price) {
  return parseFloat(price).toLocaleString('ru-RU') // Formats as 1 000 000
}

function truncateDesc(desc) {
  if (!desc) return 'No description'
  return desc.length > 60 ? desc.substring(0, 60) + '...' : desc
}

const handleMessage = () => {
  emit('message', props.listing)
}
</script>

<style scoped>
.listing-card {
  display: block;
  background: var(--color-white);
  border-radius: var(--radius-xl);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-slow);
}

.listing-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.listing-image {
  position: relative;
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  overflow: hidden;
}

.listing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.listing-card:hover .listing-image img {
  transform: scale(1.08);
}

.listing-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-hero);
}

.placeholder-icon {
  font-size: 4rem;
  filter: brightness(1.2);
}

.category-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  box-shadow: var(--shadow-sm);
}

.view-count {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: white;
  display: flex;
  align-items: center;
  gap: 4px;
}

.listing-content {
  padding: var(--spacing-lg);
}

.listing-price {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--spacing-xs);
}

.listing-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs);
  line-height: 1.3;
}

.listing-desc {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  line-height: 1.5;
  margin: 0 0 var(--spacing-md);
  min-height: 42px;
}

.listing-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
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

.message-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--color-primary-light);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-btn:hover {
  background: var(--gradient-primary);
  transform: scale(1.1);
}

.message-btn:hover .message-icon {
  filter: brightness(1.5);
}

.message-icon {
  font-size: 18px;
  transition: filter var(--transition-base);
}
</style>
