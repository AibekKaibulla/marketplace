<template>
  <div class="container container-sm">
    <h1 class="page-title mb-xl">{{ $t('edit.title') }}</h1>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>{{ $t('listings.loading') }}</p>
    </div>
    
    <!-- Error Message -->
    <div v-else-if="error" class="error-banner mb-lg">
      <p>{{ error }}</p>
      <router-link to="/profile" class="btn btn-secondary mt-md">{{ $t('card.view_details') }}</router-link>
    </div>
    
    <div v-else class="card">
      <form @submit.prevent="handleSubmit">
        <!-- Current Photos -->
        <div class="form-group">
          <label class="form-label">{{ $t('create.form.images') }}</label>
          <div class="photo-upload-area">
            <div 
              v-for="photo in existingPhotos" 
              :key="photo.photo_id"
              class="photo-preview"
            >
              <img :src="getImageUrl(photo.url)" :alt="photo.alt_text" />
              <button 
                type="button" 
                class="remove-photo" 
                @click="removeExistingPhoto(photo)"
              >×</button>
            </div>
            
            <!-- New Photos -->
            <div 
              v-for="(photo, index) in newPhotos" 
              :key="`new-${index}`"
              class="photo-preview new"
            >
              <img :src="photo.preview" :alt="`New Photo ${index + 1}`" />
              <button 
                type="button" 
                class="remove-photo" 
                @click="removeNewPhoto(index)"
              >×</button>
            </div>
            
            <!-- Upload Button -->
            <label v-if="totalPhotos < 5" class="photo-upload-btn">
              <input 
                type="file" 
                accept="image/*" 
                multiple 
                @change="handleFileSelect"
                hidden
              />
              <span class="upload-icon">📷</span>
              <span>{{ $t('create.form.add_photo') }}</span>
            </label>
          </div>
          <p class="form-hint">Add up to 5 photos. First photo will be the cover.</p>
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ $t('create.form.title') }} *</label>
          <input 
            type="text" 
            class="form-input"
            :placeholder="$t('create.placeholders.title')"
            v-model="formData.title"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ $t('create.form.category') }} *</label>
          <select class="form-select" v-model="formData.category_id" required>
            <option value="">{{ $t('create.form.category') }}...</option>
            <option 
              v-for="cat in categories" 
              :key="cat.category_id" 
              :value="cat.category_id"
            >
              {{ cat.icon }} {{ cat.name }}
            </option>
          </select>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">{{ $t('create.form.price') }} *</label>
            <input 
              type="number" 
              class="form-input"
              :placeholder="$t('create.placeholders.price')"
              step="1"
              min="0"
              v-model="formData.price"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">{{ $t('create.form.quantity') }}</label>
            <input 
              type="number" 
              class="form-input"
              min="1"
              v-model="formData.quantity"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ $t('create.form.condition') }}</label>
          <div class="condition-selector">
            <label 
              v-for="cond in conditions" 
              :key="cond.value"
              :class="['condition-option', { active: formData.condition === cond.value }]"
            >
              <input 
                type="radio" 
                :value="cond.value" 
                v-model="formData.condition"
                hidden
              />
              {{ cond.label }}
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ $t('status.label') }}</label>
          <div class="status-selector">
            <label 
              v-for="st in statuses" 
              :key="st.value"
              :class="['status-option', { active: formData.status === st.value }]"
            >
              <input 
                type="radio" 
                :value="st.value" 
                v-model="formData.status"
                hidden
              />
              {{ st.label }}
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label">{{ $t('create.form.description') }} *</label>
          <textarea 
            class="form-textarea"
            :placeholder="$t('create.placeholders.description')"
            v-model="formData.description"
            rows="5"
            required
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button 
            type="submit" 
            class="btn btn-primary btn-lg"
            :disabled="submitting"
          >
            {{ submitting ? 'Saving...' : $t('edit.save') }}
          </button>
          <router-link 
            :to="`/listings/${listingId}`"
            class="btn btn-ghost btn-lg"
          >
            {{ $t('edit.cancel') }}
          </router-link>
        </div>
      </form>
      
      <!-- Danger Zone -->
      <div class="danger-zone mt-xl">
        <h3>{{ $t('edit.danger_zone') }}</h3>
        <p class="text-secondary">{{ $t('edit.delete_warning') }}</p>
        <button 
          class="btn btn-danger" 
          @click="handleDelete"
          :disabled="deleting"
        >
          {{ deleting ? 'Deleting...' : $t('edit.delete_btn') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import listingsService from '../services/listings'
import categoriesService from '../services/categories'
import api from '../services/api'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const { t } = useI18n()

const listingId = computed(() => route.params.id)
const categories = ref([])
const loading = ref(true)
const submitting = ref(false)
const deleting = ref(false)
const error = ref(null)
const existingPhotos = ref([])
const newPhotos = ref([])
const photosToDelete = ref([])

const conditions = computed(() => [
  { value: 'brand-new', label: t('listings.condition.new') },
  { value: 'like-new', label: t('listings.condition.like_new') },
  { value: 'good', label: t('listings.condition.good') },
  { value: 'fair', label: t('listings.condition.fair') },
  { value: 'poor', label: t('listings.condition.poor') }
])

const statuses = computed(() => [
  { value: 'published', label: t('status.published') },
  { value: 'draft', label: t('status.draft') },
  { value: 'sold', label: t('status.sold') }
])

const formData = ref({
  title: '',
  category_id: '',
  price: '',
  description: '',
  condition: 'good',
  quantity: 1,
  status: 'published'
})

const totalPhotos = computed(() => existingPhotos.value.length + newPhotos.value.length)

function getImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

async function fetchListing() {
  loading.value = true
  error.value = null
  
  try {
    const listing = await listingsService.getListing(listingId.value)
    
    formData.value = {
      title: listing.title,
      category_id: listing.category_id || '',
      price: parseFloat(listing.price),
      description: listing.description || '',
      condition: listing.condition || 'good',
      quantity: listing.quantity || 1,
      status: listing.status || 'published'
    }
    
    existingPhotos.value = listing.photos || []
  } catch (err) {
    console.error('Error fetching listing:', err)
    error.value = 'Failed to load listing. You may not have permission to edit it.'
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    categories.value = await categoriesService.getCategories()
  } catch (err) {
    console.error('Error fetching categories:', err)
  }
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files)
  const maxPhotos = 5 - totalPhotos.value
  
  files.slice(0, maxPhotos).forEach(file => {
    const reader = new FileReader()
    reader.onload = (e) => {
      newPhotos.value.push({
        file: file,
        preview: e.target.result
      })
    }
    reader.readAsDataURL(file)
  })
  
  event.target.value = ''
}

function removeExistingPhoto(photo) {
  existingPhotos.value = existingPhotos.value.filter(p => p.photo_id !== photo.photo_id)
  photosToDelete.value.push(photo.photo_id)
}

function removeNewPhoto(index) {
  newPhotos.value.splice(index, 1)
}

async function uploadNewPhotos() {
  for (const photo of newPhotos.value) {
    const formDataUpload = new FormData()
    formDataUpload.append('file', photo.file)
    
    try {
      await api.post(`/api/photos/listing/${listingId.value}`, formDataUpload, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } catch (err) {
      console.error('Error uploading photo:', err)
    }
  }
}

async function deletePhotos() {
  for (const photoId of photosToDelete.value) {
    try {
      await api.delete(`/api/photos/${photoId}`)
    } catch (err) {
      console.error('Error deleting photo:', err)
    }
  }
}

const handleSubmit = async () => {
  submitting.value = true
  
  try {
    const payload = {
      ...formData.value,
      category_id: formData.value.category_id || null,
      price: parseFloat(formData.value.price)
    }
    
    await listingsService.updateListing(listingId.value, payload)
    
    // Handle photo changes
    await deletePhotos()
    await uploadNewPhotos()
    
    toast.success('Listing updated successfully!')
    router.push(`/listings/${listingId.value}`)
  } catch (err) {
    console.error('Error updating listing:', err)
    toast.error(err.response?.data?.detail || 'Failed to update listing')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this listing? This action cannot be undone.')) {
    return
  }
  
  deleting.value = true
  
  try {
    await listingsService.deleteListing(listingId.value)
    toast.success('Listing deleted')
    router.push('/profile')
  } catch (err) {
    console.error('Error deleting listing:', err)
    toast.error('Failed to delete listing')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchListing()
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

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  text-align: center;
}

.photo-upload-area {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.photo-preview {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px solid var(--color-border);
}

.photo-preview.new {
  border-color: var(--color-primary);
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-photo {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-upload-btn {
  width: 120px;
  height: 120px;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: all var(--transition-base);
  color: var(--color-text-tertiary);
}

.photo-upload-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.upload-icon {
  font-size: 2rem;
}

.form-hint {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-xs);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.condition-selector,
.status-selector {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.condition-option,
.status-option {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--font-weight-medium);
}

.condition-option:hover,
.status-option:hover {
  border-color: var(--color-primary);
}

.condition-option.active,
.status-option.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.form-actions > * {
  flex: 1;
  text-align: center;
}

.danger-zone {
  border-top: 1px solid var(--color-border);
  padding-top: var(--spacing-xl);
}

.danger-zone h3 {
  color: #dc2626;
  margin-bottom: var(--spacing-sm);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
}

.btn-danger:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
