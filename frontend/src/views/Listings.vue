<template>
  <div class="container">
    <h1 class="page-title mb-xl">{{ $t('listings.title') }}</h1>
    
    <FilterBar @filter="handleFilter" :categories="categories" />
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p class="text-secondary">{{ $t('listings.loading') }}</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-state card">
      <p class="text-danger">{{ error }}</p>
      <button class="btn btn-primary mt-md" @click="fetchListings">{{ $t('listings.retry') }}</button>
    </div>
    
    <!-- Results Header -->
    <div v-else-if="filteredListings.length > 0" class="results-header">
      <p class="results-count">
        <strong>{{ filteredListings.length }}</strong> {{ $t('listings.count') }}
      </p>
    </div>
    
    <!-- Listings Grid -->
    <div v-if="!loading && !error && filteredListings.length > 0" class="grid grid-auto-fit">
      <ListingCard 
        v-for="listing in filteredListings" 
        :key="listing.listing_id"
        :listing="formatListing(listing)"
        @message="handleMessage"
      />
    </div>
    
    <EmptyState 
      v-if="!loading && !error && filteredListings.length === 0"
      icon="🔍"
      :title="$t('listings.empty.title')"
      :description="$t('listings.empty.desc')"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ListingCard from '../components/ListingCard.vue'
import FilterBar from '../components/FilterBar.vue'
import EmptyState from '../components/EmptyState.vue'
import listingsService from '../services/listings'
import categoriesService from '../services/categories'

const router = useRouter()

const listings = ref([])
const categories = ref([])
const loading = ref(true)
const error = ref(null)

const filters = ref({
  search: '',
  category: '',
  condition: '',
  priceRange: '',
  sortBy: 'newest'
})

// Fetch listings from API
async function fetchListings() {
  loading.value = true
  error.value = null
  
  try {
    const apiFilters = {}
    
    if (filters.value.search) {
      apiFilters.search = filters.value.search
    }
    
    if (filters.value.category) {
      // Find category ID by name
      const cat = categories.value.find(c => c.name === filters.value.category)
      if (cat) apiFilters.category_id = cat.category_id
    }
    
    if (filters.value.condition) {
      apiFilters.condition = filters.value.condition
    }
    
    if (filters.value.priceRange) {
      // 0-25 USD -> 0 - 12,500 KZT
      if (filters.value.priceRange === '0-12500') {
        apiFilters.max_price = 25
      } else if (filters.value.priceRange === '12500-25000') {
        apiFilters.min_price = 25
        apiFilters.max_price = 50
      } else if (filters.value.priceRange === '25000-50000') {
        apiFilters.min_price = 50
        apiFilters.max_price = 100
      } else if (filters.value.priceRange === '50000-125000') {
        apiFilters.min_price = 100
        apiFilters.max_price = 250
      } else if (filters.value.priceRange === '125000+') {
        apiFilters.min_price = 250
      }
    }
    
    apiFilters.sort_by = filters.value.sortBy || 'newest'
    
    listings.value = await listingsService.getListings(apiFilters)
  } catch (err) {
    console.error('Error fetching listings:', err)
    error.value = 'Failed to load listings. Please try again.'
  } finally {
    loading.value = false
  }
}

// Fetch categories from API
async function fetchCategories() {
  try {
    categories.value = await categoriesService.getCategories()
  } catch (err) {
    console.error('Error fetching categories:', err)
  }
}

// Format API listing to component format
function formatListing(listing) {
  return {
    id: listing.listing_id,
    title: listing.title,
    description: listing.description,
    // Convert USD to KZT for display (approx 1 USD = 500 KZT)
    price: parseFloat(listing.price) * 500,
    category: listing.category?.name || 'Other',
    image: listing.photos && listing.photos.length > 0 ? listing.photos[0].url : null,
    viewCount: listing.view_count || 0,
    sellerId: listing.seller_id,
    seller: {
      user_id: listing.seller?.user_id || listing.seller_id,
      username: listing.seller?.username || 'unknown',
      displayName: listing.seller?.display_name || listing.seller?.username || 'Unknown'
    }
  }
}

const filteredListings = computed(() => listings.value)

const handleFilter = async (newFilters) => {
  filters.value = newFilters
  await fetchListings()
}

const handleMessage = (listing) => {
  router.push({ 
    path: '/messages', 
    query: { 
      to: listing.sellerId || listing.seller?.user_id,
      listing: listing.id 
    } 
  })
}

onMounted(async () => {
  await fetchCategories()
  await fetchListings()
})
</script>

<style scoped>
.page-title {
  color: var(--color-text-primary);
}

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
  padding: var(--spacing-xl);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.results-count {
  color: var(--color-text-secondary);
  margin: 0;
}

.results-count strong {
  color: var(--color-text-primary);
}

.grid-auto-fit {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-xl);
}
</style>
