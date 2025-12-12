<template>
  <div class="container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading listing...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-state card">
      <h2>Listing Not Found</h2>
      <p class="text-secondary">{{ error }}</p>
      <router-link to="/listings" class="btn btn-primary mt-lg">Browse Listings</router-link>
    </div>
    
    <!-- Listing Content -->
    <div v-else-if="listing" class="listing-detail">
      <!-- Back Button -->
      <button class="back-btn" @click="$router.back()">
        ← Back to listings
      </button>
      
      <div class="listing-layout">
        <!-- Left Column: Image + Meta + Description -->
        <div class="left-column">
          <!-- Image Gallery -->
          <div class="gallery-section">
            <div class="main-image">
              <img 
                v-if="currentImage" 
                :src="getImageUrl(currentImage)" 
                :alt="listing.title"
              />
              <div v-else class="no-image">
                <span class="no-image-icon">📷</span>
                <p>No images available</p>
              </div>
            </div>
            
            <div v-if="listing.photos && listing.photos.length > 1" class="thumbnail-strip">
              <button 
                v-for="(photo, index) in listing.photos" 
                :key="photo.photo_id"
                :class="['thumbnail', { active: currentImageIndex === index }]"
                @click="currentImageIndex = index"
              >
                <img :src="getImageUrl(photo.url)" :alt="`Image ${index + 1}`" />
              </button>
            </div>
          </div>
          
          <!-- Condition & Quantity -->
          <div class="meta-info">
            <div class="meta-item">
              <span class="meta-label">{{ $t('details.condition') }}</span>
              <span class="condition-badge" :class="`condition-${listing.condition}`">
                {{ formatCondition(listing.condition) }}
              </span>
            </div>
            <div class="meta-item">
              <span class="meta-label">{{ $t('create.form.quantity') }}</span>
              <span class="meta-value">{{ listing.quantity }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Views</span>
              <span class="meta-value">👁 {{ listing.view_count || 0 }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Posted</span>
              <span class="meta-value">{{ formatDate(listing.created_at) }}</span>
            </div>
          </div>
          
          <!-- Description -->
          <div class="description-section">
            <h3>{{ $t('details.description') }}</h3>
            <p>{{ listing.description || 'No description provided.' }}</p>
          </div>
        </div>
        
        <!-- Right Column: Title, Price, Seller -->
        <div class="right-column">
          <div class="listing-header">
            <div>
              <span class="category-badge">{{ listing.category?.name || 'Other' }}</span>
              <h1 class="listing-title">{{ listing.title }}</h1>
              <p class="listing-price">{{ formatPrice(listing.price) }} ₸</p>
            </div>
            
            <button 
              class="favorite-btn"
              :class="{ active: isFavorite }"
              @click="toggleFavorite"
              :title="isFavorite ? $t('details.remove_favorite') : $t('details.add_favorite')"
            >
              <span v-if="isFavorite">❤️</span>
              <span v-else>🤍</span>
            </button>
          </div>
          
          <!-- Seller Card -->
          <div class="seller-card">
            <h3>{{ $t('details.seller') }}</h3>
            <div class="seller-info">
              <UserAvatar :username="listing.seller?.username" size="lg" />
              <div class="seller-details">
                <strong>{{ listing.seller?.display_name || listing.seller?.username }}</strong>
                <p class="text-secondary">@{{ listing.seller?.username }}</p>
              </div>
            </div>
            
            <div class="action-buttons">
              <button 
                v-if="!isOwner" 
                class="btn btn-primary btn-lg btn-block"
                @click="messageSeller"
              >
                💬 {{ $t('details.contact_seller') }}
              </button>
              <router-link 
                v-if="isOwner" 
                :to="`/listings/${listing.listing_id}/edit`"
                class="btn btn-secondary btn-lg btn-block"
              >
                ✏️ Edit Listing
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import UserAvatar from '../components/UserAvatar.vue'

const { t } = useI18n()
import listingsService from '../services/listings'
import favoritesService from '../services/favorites'
import authService from '../services/auth'

const route = useRoute()
const router = useRouter()

const listing = ref(null)
const loading = ref(true)
const error = ref(null)
const currentImageIndex = ref(0)
const isFavorite = ref(false)

const currentUser = authService.currentUser

const isOwner = computed(() => {
  return currentUser.value?.user_id === listing.value?.seller_id
})

const currentImage = computed(() => {
  if (listing.value?.photos && listing.value.photos.length > 0) {
    return listing.value.photos[currentImageIndex.value]?.url
  }
  return null
})

function getImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}


function formatPrice(price) {
  // Convert USD to KZT for display (approx 1 USD = 500 KZT)
  return (parseFloat(price) * 500).toLocaleString('ru-RU')
}

function formatCondition(condition) {
  const conditions = {
    'brand-new': t('listings.condition.new'),
    'like-new': t('listings.condition.like_new'),
    'good': t('listings.condition.good'),
    'fair': t('listings.condition.fair'),
    'poor': t('listings.condition.poor')
  }
  return conditions[condition] || condition
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

async function fetchListing() {
  loading.value = true
  error.value = null
  
  try {
    const id = route.params.id
    listing.value = await listingsService.getListing(id)
    
    // Check if favorited
    if (currentUser.value) {
      try {
        isFavorite.value = await favoritesService.checkFavorite(id)
      } catch (e) {
        // Not logged in or error
      }
    }
  } catch (err) {
    console.error('Error fetching listing:', err)
    error.value = 'This listing could not be found or has been removed.'
  } finally {
    loading.value = false
  }
}

async function toggleFavorite() {
  if (!currentUser.value) {
    router.push('/login')
    return
  }
  
  try {
    if (isFavorite.value) {
      await favoritesService.removeFavorite(listing.value.listing_id)
      isFavorite.value = false
    } else {
      await favoritesService.addFavorite(listing.value.listing_id)
      isFavorite.value = true
    }
  } catch (err) {
    console.error('Error toggling favorite:', err)
  }
}

function messageSeller() {
  if (!currentUser.value) {
    router.push('/login')
    return
  }
  
  router.push({
    path: '/messages',
    query: {
      to: listing.value.seller_id,
      listing: listing.value.listing_id
    }
  })
}

onMounted(() => {
  fetchListing()
})
</script>

<style scoped>
.loading-state {
  text-align: center;
  padding: var(--spacing-3xl);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-gray-200);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-lg);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: var(--spacing-3xl);
}

.back-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  cursor: pointer;
  padding: var(--spacing-sm) 0;
  margin-bottom: var(--spacing-lg);
  transition: color var(--transition-base);
}

.back-btn:hover {
  color: var(--color-primary);
}

.listing-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: var(--spacing-2xl);
  align-items: start;
}

/* Left Column */
.left-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.gallery-section {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.main-image {
  aspect-ratio: 4/3;
  background: var(--color-gray-100);
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.no-image {
  text-align: center;
  color: var(--color-text-tertiary);
}

.no-image-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: var(--spacing-md);
}

.thumbnail-strip {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  overflow-x: auto;
  background: var(--color-gray-50);
}

.thumbnail {
  width: 80px;
  height: 60px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 3px solid transparent;
  cursor: pointer;
  flex-shrink: 0;
  padding: 0;
  background: none;
  transition: all var(--transition-base);
}

.thumbnail:hover {
  border-color: var(--color-gray-300);
}

.thumbnail.active {
  border-color: var(--color-primary);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Meta Info */
.meta-info {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-sm);
  background: var(--color-white);
  padding: var(--spacing-lg);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
}

.meta-item {
  text-align: center;
  padding: var(--spacing-sm);
}

.meta-label {
  display: block;
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--spacing-xs);
}

.meta-value {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.condition-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
}

.condition-brand-new { background: #dcfce7; color: #16a34a; }
.condition-like-new { background: #dbeafe; color: #2563eb; }
.condition-good { background: #fef3c7; color: #d97706; }
.condition-fair { background: #fed7aa; color: #ea580c; }
.condition-poor { background: #fee2e2; color: #dc2626; }

/* Description */
.description-section {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
}

.description-section h3 {
  margin: 0 0 var(--spacing-md);
  color: var(--color-text-primary);
  font-size: var(--font-size-lg);
}

.description-section p {
  color: var(--color-text-secondary);
  line-height: 1.7;
  margin: 0;
  white-space: pre-wrap;
}

/* Right Column */
.right-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  position: sticky;
  top: var(--spacing-lg);
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
}

.category-badge {
  display: inline-block;
  background: var(--gradient-primary);
  color: white;
  padding: 6px 16px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-sm);
}

.listing-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--spacing-sm);
  color: var(--color-text-primary);
  line-height: 1.3;
}

.listing-price {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.favorite-btn {
  background: var(--color-gray-100);
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  padding: var(--spacing-sm);
  border-radius: var(--radius-full);
  transition: all var(--transition-bounce);
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.favorite-btn:hover {
  transform: scale(1.15);
  background: var(--color-danger-light);
}

.favorite-btn.active {
  animation: heartBeat 0.3s ease;
}

@keyframes heartBeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

/* Seller Card */
.seller-card {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
}

.seller-card h3 {
  margin: 0 0 var(--spacing-lg);
  color: var(--color-text-primary);
  font-size: var(--font-size-lg);
}

.seller-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-md);
  background: var(--color-gray-50);
  border-radius: var(--radius-lg);
}

.seller-details strong {
  display: block;
  margin-bottom: 2px;
}

.seller-details p {
  margin: 0;
  font-size: var(--font-size-sm);
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.btn-block {
  width: 100%;
}

/* Responsive */
@media (max-width: 900px) {
  .listing-layout {
    grid-template-columns: 1fr;
  }
  
  .right-column {
    position: static;
  }
  
  .meta-info {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .meta-info {
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-xs);
  }
  
  .meta-item {
    padding: var(--spacing-xs);
  }
}
</style>
