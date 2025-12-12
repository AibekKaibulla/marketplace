<template>
  <div class="filter-bar">
    <div class="filter-row">
      <!-- Search Input -->
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input 
          type="text" 
          class="search-input"
          :placeholder="$t('listings.filter.search_placeholder')"
          v-model="search"
          @input="handleSearchDebounced"
        />
        <button 
          v-if="search" 
          class="clear-btn" 
          @click="clearSearch"
        >×</button>
      </div>
    </div>
    
    <div class="filter-row">
      <!-- Category -->
      <select class="form-select filter-select" v-model="category" @change="handleFilterChange">
        <option value="">{{ $t('listings.filter.all_categories') }}</option>
        <option 
          v-for="cat in categories" 
          :key="cat.category_id || cat.name" 
          :value="cat.name"
        >
          {{ cat.icon }} {{ cat.name }}
        </option>
      </select>
      
      <!-- Condition -->
      <select class="form-select filter-select" v-model="condition" @change="handleFilterChange">
        <option value="">{{ $t('listings.filter.condition') }}</option>
        <option value="brand-new">{{ $t('listings.condition.new') }}</option>
        <option value="like-new">{{ $t('listings.condition.like_new') }}</option>
        <option value="good">{{ $t('listings.condition.good') }}</option>
        <option value="fair">{{ $t('listings.condition.fair') }}</option>
        <option value="poor">{{ $t('listings.condition.poor') }}</option>
      </select>
      
      <!-- Price Range -->
      <select class="form-select filter-select" v-model="priceRange" @change="handleFilterChange">
        <option value="">{{ $t('listings.filter.price_range') }}</option>
        <option value="0-12500">0 - 12 500 ₸</option>
        <option value="12500-25000">12 500 - 25 000 ₸</option>
        <option value="25000-50000">25 000 - 50 000 ₸</option>
        <option value="50000-125000">50 000 - 125 000 ₸</option>
        <option value="125000+">125 000+ ₸</option>
      </select>
      
      <!-- Sort -->
      <select class="form-select filter-select sort-select" v-model="sortBy" @change="handleFilterChange">
        <option value="newest">{{ $t('listings.filter.sort_by') }} (Newest)</option>
        <option value="oldest">{{ $t('listings.filter.sort_by') }} (Oldest)</option>
        <option value="price_low">{{ $t('listings.filter.price_range') }}: Low to High</option>
        <option value="price_high">{{ $t('listings.filter.price_range') }}: High to Low</option>
      </select>
    </div>
    
    <!-- Active Filters -->
    <div v-if="hasActiveFilters" class="active-filters">
      <span class="active-filters-label">Active filters:</span>
      <button 
        v-if="category" 
        class="filter-tag" 
        @click="removeFilter('category')"
      >
        {{ category }} ×
      </button>
      <button 
        v-if="condition" 
        class="filter-tag" 
        @click="removeFilter('condition')"
      >
        {{ formatCondition(condition) }} ×
      </button>
      <button 
        v-if="priceRange" 
        class="filter-tag" 
        @click="removeFilter('priceRange')"
      >
        {{ formatPriceRange(priceRange) }} ×
      </button>
      <button class="clear-all-btn" @click="clearAllFilters">
        Clear All
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['filter'])

const search = ref('')
const category = ref('')
const condition = ref('')
const priceRange = ref('')
const sortBy = ref('newest')

let searchTimeout = null

const hasActiveFilters = computed(() => {
  return category.value || condition.value || priceRange.value
})

function emitFilters() {
  emit('filter', {
    search: search.value,
    category: category.value,
    condition: condition.value,
    priceRange: priceRange.value,
    sortBy: sortBy.value
  })
}

function handleSearchDebounced() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    emitFilters()
  }, 300)
}

function handleFilterChange() {
  emitFilters()
}

function clearSearch() {
  search.value = ''
  emitFilters()
}

function removeFilter(filterName) {
  if (filterName === 'category') category.value = ''
  if (filterName === 'condition') condition.value = ''
  if (filterName === 'priceRange') priceRange.value = ''
  emitFilters()
}

function clearAllFilters() {
  category.value = ''
  condition.value = ''
  priceRange.value = ''
  emitFilters()
}

function formatCondition(cond) {
  const conditions = {
    'brand-new': t('listings.condition.new'),
    'like-new': t('listings.condition.like_new'),
    'good': t('listings.condition.good'),
    'fair': t('listings.condition.fair'),
    'poor': t('listings.condition.poor')
  }
  return conditions[cond] || cond
}

function formatPriceRange(range) {
  const ranges = {
    '0-12500': 'Under 12 500 ₸',
    '12500-25000': '12 500 - 25 000 ₸',
    '25000-50000': '25 000 - 50 000 ₸',
    '50000-125000': '50 000 - 125 000 ₸',
    '125000+': 'Over 125 000 ₸'
  }
  return ranges[range] || range
}
</script>

<style scoped>
.filter-bar {
  background: var(--color-white);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-xl);
  box-shadow: var(--shadow-md);
}

.filter-row {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  align-items: center;
}

.filter-row + .filter-row {
  margin-top: var(--spacing-md);
}

.search-wrapper {
  flex: 1;
  min-width: 280px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 44px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-base);
  transition: all var(--transition-base);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.clear-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  border: none;
  background: var(--color-gray-200);
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  color: var(--color-text-secondary);
  transition: all var(--transition-base);
}

.clear-btn:hover {
  background: var(--color-gray-300);
  color: var(--color-text-primary);
}

.filter-select {
  min-width: 150px;
  flex: 1;
}

.sort-select {
  background: linear-gradient(135deg, var(--color-primary-light), #e0e7ff);
  border-color: var(--color-primary);
  font-weight: var(--font-weight-medium);
}

.active-filters {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.active-filters-label {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border: none;
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-base);
}

.filter-tag:hover {
  background: var(--color-primary);
  color: white;
}

.clear-all-btn {
  padding: 4px 12px;
  background: none;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.clear-all-btn:hover {
  border-color: var(--color-danger);
  color: var(--color-danger);
}

@media (max-width: 768px) {
  .search-wrapper {
    min-width: 100%;
    flex: 1 1 100%;
  }
  
  .filter-select {
    flex: 1 1 calc(50% - var(--spacing-sm));
    min-width: 0;
  }
}
</style>
