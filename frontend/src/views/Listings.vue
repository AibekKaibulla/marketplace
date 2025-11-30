<template>
  <div class="container">
    <h1 class="page-title mb-xl">Browse Listings</h1>
    
    <FilterBar @filter="handleFilter" />
    
    <div class="grid grid-auto-fit">
      <ListingCard 
        v-for="listing in filteredListings" 
        :key="listing.id"
        :listing="listing"
        @message="handleMessage"
      />
    </div>
    
    <EmptyState 
      v-if="filteredListings.length === 0"
      icon="🔍"
      title="No Listings Found"
      description="Try adjusting your search filters or check back later for new items"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ListingCard from '../components/ListingCard.vue'
import FilterBar from '../components/FilterBar.vue'
import EmptyState from '../components/EmptyState.vue'

const router = useRouter()

// Mock data for demonstration
const listings = ref([
  {
    id: 1,
    title: 'Calculus Textbook - 9th Edition',
    description: 'Excellent condition, barely used. All chapters included.',
    price: 45.00,
    category: 'Textbooks',
    seller: {
      username: 'johnd',
      displayName: 'John D.'
    }
  },
  {
    id: 2,
    title: 'MacBook Pro 13" 2019',
    description: 'Great condition, 256GB SSD, 8GB RAM. Charger included.',
    price: 350.00,
    category: 'Electronics',
    seller: {
      username: 'sarahm',
      displayName: 'Sarah M.'
    }
  },
  {
    id: 3,
    title: 'Desk Chair - Ergonomic',
    description: 'Comfortable office chair, adjustable height, good for long study sessions.',
    price: 80.00,
    category: 'Furniture',
    seller: {
      username: 'miker',
      displayName: 'Mike R.'
    }
  },
  {
    id: 4,
    title: 'Python Programming Book',
    description: 'Learn Python the Hard Way - Like new condition',
    price: 25.00,
    category: 'Textbooks',
    seller: {
      username: 'emilyt',
      displayName: 'Emily T.'
    }
  },
  {
    id: 5,
    title: 'Gaming Keyboard RGB',
    description: 'Mechanical keyboard with RGB lighting, barely used',
    price: 65.00,
    category: 'Electronics',
    seller: {
      username: 'alexw',
      displayName: 'Alex W.'
    }
  },
  {
    id: 6,
    title: 'Mini Fridge',
    description: 'Perfect for dorm room, works great',
    price: 120.00,
    category: 'Furniture',
    seller: {
      username: 'jessical',
      displayName: 'Jessica L.'
    }
  }
])

const filters = ref({
  search: '',
  category: '',
  priceRange: ''
})

const filteredListings = computed(() => {
  return listings.value.filter(listing => {
    // Search filter
    if (filters.value.search) {
      const searchLower = filters.value.search.toLowerCase()
      const matchesSearch = 
        listing.title.toLowerCase().includes(searchLower) ||
        listing.description.toLowerCase().includes(searchLower)
      if (!matchesSearch) return false
    }
    
    // Category filter
    if (filters.value.category && listing.category !== filters.value.category) {
      return false
    }
    
    // Price range filter
    if (filters.value.priceRange) {
      const price = listing.price
      if (filters.value.priceRange === '0-50' && price > 50) return false
      if (filters.value.priceRange === '50-100' && (price < 50 || price > 100)) return false
      if (filters.value.priceRange === '100-500' && (price < 100 || price > 500)) return false
      if (filters.value.priceRange === '500+' && price < 500) return false
    }
    
    return true
  })
})

const handleFilter = (newFilters) => {
  filters.value = newFilters
}

const handleMessage = (listing) => {
  // Navigate to messages with listing context
  router.push({ path: '/messages', query: { listing: listing.id } })
}
</script>

<style scoped>
.page-title {
  color: var(--color-text-primary);
}
</style>
