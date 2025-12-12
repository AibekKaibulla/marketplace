<template>
 <div class="container container-sm">
    <!-- Profile Header -->
    <div class="profile-header card text-center mb-xl">
      <UserAvatar :username="user.username" size="xl" />
      <h2 class="mt-lg">{{ user.display_name || user.username }}</h2>
      <p class="text-secondary">@{{ user.username }}</p>
      <span class="badge badge-primary">{{ user.role }}</span>
      <div class="profile-meta mt-lg text-secondary">
        <p>{{ user.email }}</p>
        <p>Member since {{ formatDate(user.created_at) }}</p>
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
        <p class="text-secondary">Rating</p>
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
        <div v-if="loadingListings" class="loading-state">
          <p class="text-secondary">{{ $t('listings.loading') }}</p>
        </div>
        
        <div v-else-if="myListings.length > 0" class="grid grid-auto-fit">
          <div v-for="listing in myListings" :key="listing.listing_id" class="listing-item card">
            <div class="listing-header">
              <h4>{{ listing.title }}</h4>
              <span :class="['status-badge', `status-${listing.status}`]">{{ $t('status.' + listing.status) }}</span>
            </div>
            <p class="text-secondary">{{ listing.price }} ₸</p>
            <div class="listing-actions mt-md">
              <button class="btn btn-secondary btn-sm" @click="editListing(listing)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="deleteListing(listing)">Delete</button>
            </div>
          </div>
        </div>
        
        <EmptyState 
          v-else
          icon="📦"
          title="No Listings Yet"
          description="Start selling by creating your first listing!"
          :buttonText="$t('home.create_listing.btn')"
          @action="goToCreateListing"
        />
      </div>
      
      <!-- Favorites Tab -->
      <div v-if="activeTab === 'favorites'">
        <div v-if="loadingFavorites" class="loading-state">
          <p class="text-secondary">{{ $t('listings.loading') }}</p>
        </div>
        
        <div v-else-if="favorites.length > 0" class="grid grid-auto-fit">
          <ListingCard 
            v-for="fav in favorites" 
            :key="fav.favorite_id"
            :listing="formatListing(fav.listing)"
          />
        </div>
        
        <EmptyState 
          v-else
          icon="⭐"
          title="No Favorites"
          description="Browse listings and save your favorites for later"
          :buttonText="$t('home.browse.btn')"
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
      <div v-if="activeTab === 'settings'" class="settings-container">
        <!-- Profile Settings Card -->
        <div class="card">
          <h3 class="settings-title">{{ $t('profile.edit_profile') }}</h3>
          
          <div v-if="settingsError" class="error-banner mb-lg">
            <p>{{ settingsError }}</p>
          </div>
          
          <div v-if="settingsSuccess" class="success-banner mb-lg">
            <p>{{ settingsSuccess }}</p>
          </div>
          
          <div class="form-group">
            <label class="form-label">{{ $t('auth.full_name') }}</label>
            <input type="text" class="form-input" v-model="settingsForm.display_name" />
          </div>
          <div class="form-group">
            <label class="form-label">{{ $t('auth.email') }}</label>
            <input type="email" class="form-input" v-model="settingsForm.email" />
          </div>
          <div class="form-group">
            <label class="form-label">Role</label>
            <select class="form-select" v-model="settingsForm.role">
              <option value="buyer">Buyer</option>
              <option value="seller">Seller</option>
              <option value="both">Both</option>
            </select>
          </div>
          <button 
            class="btn btn-primary" 
            @click="saveSettings"
            :disabled="savingSettings"
          >
            {{ savingSettings ? 'Saving...' : $t('profile.save') }}
          </button>
        </div>
        
        <!-- Password Change Card -->
        <div class="card">
          <h3 class="settings-title">{{ $t('profile.change_password') }}</h3>
          
          <div v-if="passwordError" class="error-banner mb-lg">
            <p>{{ passwordError }}</p>
          </div>
          
          <div v-if="passwordSuccess" class="success-banner mb-lg">
            <p>{{ passwordSuccess }}</p>
          </div>
          
          <div class="form-group">
            <label class="form-label">{{ $t('auth.password') }}</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="passwordForm.currentPassword" 
              placeholder="Enter current password"
            />
          </div>
          <div class="form-group">
            <label class="form-label">New {{ $t('auth.password') }}</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="passwordForm.newPassword" 
              placeholder="Enter new password (min 6 characters)"
            />
          </div>
          <div class="form-group">
            <label class="form-label">Confirm New {{ $t('auth.password') }}</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="passwordForm.confirmPassword" 
              placeholder="Confirm new password"
            />
          </div>
          <button 
            class="btn btn-primary" 
            @click="changePassword"
            :disabled="changingPassword"
          >
            {{ changingPassword ? 'Updating...' : $t('profile.change_password') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import UserAvatar from '../components/UserAvatar.vue'
import EmptyState from '../components/EmptyState.vue'
import ListingCard from '../components/ListingCard.vue'
import authService from '../services/auth'
import listingsService from '../services/listings'
import favoritesService from '../services/favorites'
import api from '../services/api'

const router = useRouter()
const { t } = useI18n()

const user = ref(authService.getCurrentUser() || {
  username: 'user',
  display_name: 'User',
  email: 'user@example.com',
  role: 'buyer',
  created_at: new Date().toISOString()
})

const stats = ref({
  activeListings: 0,
  completedSales: 0,
  rating: 5.0
})

const myListings = ref([])
const favorites = ref([])
const loadingListings = ref(false)
const loadingFavorites = ref(false)

const settingsForm = ref({
  display_name: user.value.display_name || '',
  email: user.value.email || '',
  role: user.value.role || 'buyer'
})
const savingSettings = ref(false)
const settingsError = ref(null)
const settingsSuccess = ref(null)

// Password change state
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const changingPassword = ref(false)
const passwordError = ref(null)
const passwordSuccess = ref(null)

const tabs = computed(() => [
  { id: 'listings', label: t('profile.tabs.listings') },
  { id: 'favorites', label: t('profile.tabs.favorites') },
  { id: 'reviews', label: 'Reviews' },
  { id: 'settings', label: t('profile.tabs.settings') }
])

const activeTab = ref('listings')

async function fetchMyListings() {
  loadingListings.value = true
  try {
    myListings.value = await listingsService.getMyListings()
    stats.value.activeListings = myListings.value.filter(l => l.status === 'published').length
    stats.value.completedSales = myListings.value.filter(l => l.status === 'sold').length
  } catch (err) {
    console.error('Error fetching listings:', err)
  } finally {
    loadingListings.value = false
  }
}

async function fetchFavorites() {
  loadingFavorites.value = true
  try {
    favorites.value = await favoritesService.getFavorites()
  } catch (err) {
    console.error('Error fetching favorites:', err)
  } finally {
    loadingFavorites.value = false
  }
}

async function saveSettings() {
  savingSettings.value = true
  settingsError.value = null
  settingsSuccess.value = null
  
  try {
    const res = await api.put('/api/auth/me', settingsForm.value)
    // Update local user data
    authService.saveAuth(authService.getToken(), res.data)
    user.value = res.data
    settingsSuccess.value = 'Settings saved successfully!'
  } catch (err) {
    console.error('Error saving settings:', err)
    settingsError.value = err.response?.data?.detail || 'Failed to save settings'
  } finally {
    savingSettings.value = false
  }
}

async function changePassword() {
  passwordError.value = null
  passwordSuccess.value = null
  
  // Validate
  if (!passwordForm.value.currentPassword) {
    passwordError.value = 'Please enter your current password'
    return
  }
  
  if (passwordForm.value.newPassword.length < 6) {
    passwordError.value = 'New password must be at least 6 characters'
    return
  }
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = 'New passwords do not match'
    return
  }
  
  changingPassword.value = true
  
  try {
    await api.put('/api/auth/me/password', {
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword
    })
    
    passwordSuccess.value = 'Password updated successfully!'
    
    // Clear form
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (err) {
    console.error('Error changing password:', err)
    passwordError.value = err.response?.data?.detail || 'Failed to change password'
  } finally {
    changingPassword.value = false
  }
}

async function deleteListing(listing) {
  if (!confirm('Are you sure you want to delete this listing?')) return
  
  try {
    await listingsService.deleteListing(listing.listing_id)
    myListings.value = myListings.value.filter(l => l.listing_id !== listing.listing_id)
    stats.value.activeListings = myListings.value.filter(l => l.status === 'published').length
  } catch (err) {
    console.error('Error deleting listing:', err)
    alert('Failed to delete listing')
  }
}

function editListing(listing) {
  // TODO: Implement edit functionality
  router.push(`/listings/${listing.listing_id}/edit`)
}

function formatListing(listing) {
  return {
    id: listing.listing_id,
    title: listing.title,
    description: listing.description,
    price: parseFloat(listing.price),
    category: listing.category?.name || 'Other',
    image: listing.photos && listing.photos.length > 0 ? listing.photos[0].url : null,
    viewCount: listing.view_count || 0,
    sellerId: listing.seller_id,
    seller: {
      user_id: listing.seller?.user_id || listing.seller_id,
      username: listing.seller?.username || 'unknown',
      displayName: listing.seller?.display_name || listing.seller?.username
    }
  }
}

function formatDate(dateStr) {
  if (!dateStr) return 'Unknown'
  return new Date(dateStr).toLocaleDateString('en-US', { 
    month: 'long', 
    year: 'numeric' 
  })
}

const goToCreateListing = () => {
  router.push('/listings/create')
}

const goToListings = () => {
  router.push('/listings')
}

onMounted(() => {
  fetchMyListings()
  fetchFavorites()
})
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

.listing-item {
  padding: var(--spacing-lg);
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.listing-header h4 {
  margin: 0;
}

.status-badge {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: capitalize;
}

.status-published {
  background: #dcfce7;
  color: #16a34a;
}

.status-draft {
  background: #fef3c7;
  color: #d97706;
}

.status-sold {
  background: #dbeafe;
  color: #2563eb;
}

.listing-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.loading-state {
  text-align: center;
  padding: var(--spacing-xl);
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
}

.success-banner {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
}

.settings-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
}

.settings-title {
  margin: 0 0 var(--spacing-lg);
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
}

@media (max-width: 900px) {
  .settings-container {
    grid-template-columns: 1fr;
  }
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
