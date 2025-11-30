<template>
  <div class="container container-sm">
    <h1 class="page-title mb-xl">Create New Listing</h1>
    
    <div class="card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">Title *</label>
          <input 
            type="text" 
            class="form-input"
            placeholder="e.g., Calculus Textbook - 9th Edition"
            v-model="formData.title"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Category *</label>
          <select class="form-select" v-model="formData.category" required>
            <option value="">Select a category...</option>
            <option value="Textbooks">Textbooks</option>
            <option value="Electronics">Electronics</option>
            <option value="Furniture">Furniture</option>
            <option value="Clothing">Clothing</option>
            <option value="Gaming">Gaming</option>
            <option value="Musical Instruments">Musical Instruments</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Price ($) *</label>
          <input 
            type="number" 
            class="form-input"
            placeholder="0.00"
            step="0.01"
            min="0"
            v-model="formData.price"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Description *</label>
          <textarea 
            class="form-textarea"
            placeholder="Describe your item in detail..."
            v-model="formData.description"
            required
          ></textarea>
        </div>
        
        <div class="form-group">
          <label class="form-label">Condition</label>
          <select class="form-select" v-model="formData.condition">
            <option value="brand-new">Brand New</option>
            <option value="like-new">Like New</option>
            <option value="good">Good</option>
            <option value="fair">Fair</option>
            <option value="poor">Poor</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Quantity</label>
          <input 
            type="number" 
            class="form-input"
            min="1"
            v-model="formData.quantity"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Photos</label>
          <div class="upload-area">
            <div class="upload-icon">📷</div>
            <p class="text-secondary">Click to upload photos or drag and drop</p>
            <p class="text-tertiary text-sm">PNG, JPG up to 10MB</p>
            <input type="file" multiple accept="image/*" class="file-input" />
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-lg">Publish Listing</button>
          <button type="button" class="btn btn-ghost btn-lg" @click="saveDraft">Save as Draft</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = ref({
  title: '',
  category: '',
  price: 0,
  description: '',
  condition: 'good',
  quantity: 1
})

const handleSubmit = () => {
  // TODO: Implement API call to create listing
  console.log('Creating listing:', formData.value)
  alert('Listing created successfully!')
  router.push('/listings')
}

const saveDraft = () => {
  // TODO: Implement save as draft
  console.log('Saving draft:', formData.value)
  alert('Draft saved!')
}
</script>

<style scoped>
.page-title {
  color: var(--color-text-primary);
}

.upload-area {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-3xl) var(--spacing-lg);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
}

.upload-area:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.form-actions button {
  flex: 1;
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions button {
    width: 100%;
  }
}
</style>
