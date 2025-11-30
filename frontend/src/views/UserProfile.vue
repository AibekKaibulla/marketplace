<template>
  <div class="container container-sm">
    <!-- Profile Header -->
    <div class="profile-header card text-center mb-xl">
      <UserAvatar :username="user.username" size="xl" />
      <h2 class="mt-lg">{{ user.displayName }}</h2>
      <p class="text-secondary">@{{ user.username }}</p>
      <span class="badge badge-primary">{{ user.role }}</span>
      <div class="profile-meta mt-lg text-secondary">
        <p>📧 {{ user.email }}</p>
        <p>📅 Member since {{ user.memberSince }}</p>
      </div>
    </div>
    
    <!-- Stats -->
    <div class="grid grid-cols-3 mb-xl">
      <div class="card text-center">
        <div class="stat-value text-primary">{{ stats.activeListings }}</div>
        <p class="text-secondary">Active Listings</p>
      </div>
      <div class="card text-center">
        <div class="stat-value text-success">{{ stats.completedSales }}</div>
        <p class="text-secondary">Completed Sales</p>
      </div>
      <div class="card text-center">
        <div class="stat-value text-warning">{{ stats.rating }}</div>
        <p class="text-secondary">⭐ Rating</p>
      </div>
    </div>
    
    <!-- Tabs -->
    <div class="tabs-container mb-xl">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>
    
    <!-- Tab Content -->
    <div class="tab-content">
      <!-- My Listings Tab -->
      <div v-if="activeTab === 'listings'">
        <EmptyState 
          icon="📦"
          title="No Listings Yet"
          description="Start selling by creating your first listing!"
          buttonText="Create Listing"
          @action="goToCreateListing"
        />
      </div>
      
      <!-- Favorites Tab -->
      <div v-if="activeTab === 'favorites'">
        <EmptyState 
          icon="⭐"
          title="No Favorites"
          description="Browse listings and save your favorites for later"
          buttonText="Browse Listings"
          @action="goToListings"
        />
      </div>
      
      <!-- Reviews Tab -->
      <div v-if="activeTab === 'reviews'">
        <EmptyState 
          icon="💭"
          title="No Reviews Yet"
          description="Complete some transactions to receive reviews from other users"
        />
      </div>
      
      <!-- Settings Tab -->
      <div v-if="activeTab === 'settings'" class="card">
        <h3 class="mb-lg">Account Settings</h3>
        <div class="form-group">
          <label class="form-label">Display Name</label>
          <input type="text" class="form-input" v-model="user.displayName" />
        </div>
        <div class="form-group">
          <label class="form-label">Email</label>
          <input type="email" class="form-input" v-model="user.email" />
        </div>
        <div class="form-group">
          <label class="form-label">Role</label>
          <select class="form-select" v-model="user.role">
            <option value="buyer">Buyer</option>
            <option value="seller">Seller</option>
            <option value="both">Both</option>
          </select>
        </div>
        <button class="btn btn-primary">Save Changes</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import UserAvatar from '../components/UserAvatar.vue'
import EmptyState from '../components/EmptyState.vue'
import authService from '../services/auth'

const router = useRouter()

const user = ref(authService.getCurrentUser() || {
  username: 'username123',
  displayName: 'Aibek',
  email: 'username123@university.edu',
  role: 'buyer',
  memberSince: 'November 2025'
})

const stats = ref({
  activeListings: 0,
  completedSales: 0,
  rating: 5.0
})

const tabs = [
  { id: 'listings', label: 'My Listings' },
  { id: 'favorites', label: 'Favorites' },
  { id: 'reviews', label: 'Reviews' },
  { id: 'settings', label: 'Settings' }
]

const activeTab = ref('listings')

const goToCreateListing = () => {
  router.push('/listings/create')
}

const goToListings = () => {
  router.push('/listings')
}
</script>

<style scoped>
.profile-header {
  padding: var(--spacing-3xl);
}

.profile-meta {
  color: var(--color-text-secondary);
}

.profile-meta p {
  margin: var(--spacing-xs) 0;
}

.stat-value {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--spacing-sm);
}

.tabs-container {
  border-bottom: 2px solid var(--color-border);
}

.tabs {
  display: flex;
  gap: var(--spacing-xl);
}

.tab {
  padding: var(--spacing-md) 0;
  border: none;
  background: none;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all var(--transition-base);
}

.tab:hover {
  color: var(--color-primary);
}

.tab.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

@media (max-width: 768px) {
  .grid-cols-3 {
    grid-template-columns: 1fr;
  }
  
  .tabs {
    gap: var(--spacing-md);
    overflow-x: auto;
  }
  
  .tab {
    white-space: nowrap;
  }
}
</style>
