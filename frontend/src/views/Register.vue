<template>
  <div class="auth-container">
    <div class="auth-card card">
      <div class="auth-icon">✨</div>
      <h2>Join Us Today!</h2>
      <p class="auth-subtitle text-secondary">Create your account to get started</p>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">Username *</label>
          <input 
            type="text" 
            class="form-input"
            placeholder="Choose a username"
            v-model="formData.username"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Email *</label>
          <input 
            type="email" 
            class="form-input"
            placeholder="your.email@university.edu"
            v-model="formData.email"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Display Name</label>
          <input 
            type="text" 
            class="form-input"
            placeholder="How should others see you?"
            v-model="formData.displayName"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">I want to *</label>
          <select class="form-select" v-model="formData.role" required>
            <option value="buyer">Buy items</option>
            <option value="seller">Sell items</option>
            <option value="both">Both buy and sell</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Password *</label>
          <input 
            type="password" 
            class="form-input"
            placeholder="Create a strong password"
            v-model="formData.password"
            required
          />
        </div>
        
        <button type="submit" class="btn btn-primary btn-block btn-lg">
          Create Account
        </button>
      </form>
      
      <div class="divider">
        <span>OR</span>
      </div>
      
      <p class="text-center text-secondary mb-md">Already have an account?</p>
      <router-link to="/login">
        <button class="btn btn-secondary btn-block">Sign In</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/auth'

const router = useRouter()
const formData = ref({
  username: '',
  email: '',
  displayName: '',
  role: 'buyer',
  password: ''
})

const handleRegister = async () => {
  try {
    await authService.register(formData.value)
    router.push('/')
  } catch (error) {
    alert('Registration failed: ' + error.message)
  }
}
</script>

<style scoped>
.auth-container {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-hero);
  padding: var(--spacing-xl);
}

.auth-card {
  max-width: 450px;
  width: 100%;
  box-shadow: var(--shadow-2xl);
}

.auth-icon {
  font-size: 4rem;
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.auth-card h2 {
  text-align: center;
  margin-bottom: var(--spacing-sm);
}

.auth-subtitle {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}
</style>