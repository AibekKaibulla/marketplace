<template>
  <div class="filter-bar">
    <div class="filter-group">
      <input 
        type="text" 
        class="search-input form-input"
        placeholder="Search for items..."
        v-model="search"
        @input="handleSearchChange"
      />
      
      <select class="form-select filter-select" v-model="category" @change="handleFilterChange">
        <option value="">All Categories</option>
        <option value="Textbooks">Textbooks</option>
        <option value="Electronics">Electronics</option>
        <option value="Furniture">Furniture</option>
        <option value="Clothing">Clothing</option>
        <option value="Gaming">Gaming</option>
        <option value="Musical Instruments">Musical Instruments</option>
      </select>
      
      <select class="form-select filter-select" v-model="priceRange" @change="handleFilterChange">
        <option value="">Price: Any</option>
        <option value="0-50">Under $50</option>
        <option value="50-100">$50 - $100</option>
        <option value="100-500">$100 - $500</option>
        <option value="500+">Over $500</option>
      </select>
      
      <button class="btn btn-primary" @click="handleApply">Apply</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['filter'])

const search = ref('')
const category = ref('')
const priceRange = ref('')

const handleSearchChange = () => {
  emit('filter', {
    search: search.value,
    category: category.value,
    priceRange: priceRange.value
  })
}

const handleFilterChange = () => {
  emit('filter', {
    search: search.value,
    category: category.value,
    priceRange: priceRange.value
  })
}

const handleApply = () => {
  emit('filter', {
    search: search.value,
    category: category.value,
    priceRange: priceRange.value
  })
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

.filter-group {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  align-items: center;
}

.search-input {
  flex: 1;
  min-width: 300px;
}

.filter-select {
  min-width: 150px;
}

@media (max-width: 768px) {
  .search-input {
    min-width: 100%;
    flex: 1 1 100%;
  }
  
  .filter-select {
    flex: 1;
    min-width: 0;
  }
  
  .filter-group button {
    width: 100%;
  }
}
</style>
