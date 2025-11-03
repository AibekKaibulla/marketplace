<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="card auth-card">
        <div class="card-header text-center">
          <div class="auth-icon">✨</div>
          <h2>Join Us Today!</h2>
          <p style="color: var(--gray)">Create your account to get started</p>
        </div>

        <form @submit.prevent="doRegister">
          <div class="form-group">
            <label for="username">Username *</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="Choose a username"
              required
              minlength="3"
              :disabled="isLoading"
            />
            <small style="color: var(--gray)">At least 3 characters</small>
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="your.email@university.edu"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label for="display_name">Display Name</label>
            <input
              id="display_name"
              v-model="display_name"
              type="text"
              placeholder="How should others see you?"
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label for="role">I want to *</label>
            <select id="role" v-model="role" :disabled="isLoading">
              <option value="buyer">Buy items</option>
              <option value="seller">Sell items</option>
              <option value="both">Both buy and sell</option>
            </select>
          </div>

          <div class="form-group">
            <label for="password">Password *</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Create a strong password"
              required
              minlength="8"
              :disabled="isLoading"
            />
            <small style="color: var(--gray)">Minimum 8 characters</small>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password *</label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              placeholder="Re-enter your password"
              required
              :disabled="isLoading"
            />
          </div>

          <div v-if="passwordMismatch" class="alert alert-warning">
            <span>⚠️</span>
            Passwords do not match!
          </div>

          <button 
            type="submit" 
            class="btn btn-primary btn-block" 
            :disabled="isLoading || passwordMismatch"
          >
            <span v-if="isLoading" class="spinner"></span>
            {{ isLoading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <div v-if="error" class="alert alert-error mt-3">
          <span>⚠️</span>
          {{ error }}
        </div>

        <div v-if="success" class="alert alert-success mt-3">
          <span>✅</span>
          {{ success }}
        </div>

        <div class="divider">
          <span>OR</span>
        </div>

        <div class="text-center">
          <p style="color: var(--gray)">Already have an account?</p>
          <router-link to="/login" class="btn btn-outline btn-block mt-2">
            Sign In
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import auth from '../services/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const display_name = ref('')
const role = ref('buyer')
const password = ref('')
const confirmPassword = ref('')
const error = ref(null)
const success = ref(null)
const isLoading = ref(false)
const router = useRouter()

const passwordMismatch = computed(() => {
  return password.value && confirmPassword.value && 
         password.value !== confirmPassword.value
})

async function doRegister() {
  error.value = null
  success.value = null
  
  if (passwordMismatch.value) {
    error.value = 'Passwords do not match!'
    return
  }
  
  isLoading.value = true
  
  try {
    await auth.register({ 
      username: username.value, 
      email: email.value, 
      display_name: display_name.value || username.value, 
      role: role.value, 
      password: password.value 
    })
    
    success.value = 'Account created successfully! Redirecting...'
    
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (err) {
    console.error('Registration error:', err)
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.auth-container {
  width: 100%;
  max-width: 500px;
}

.auth-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.auth-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  animation: rotate 3s ease-in-out infinite;
}

@keyframes rotate {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(10deg); }
}

.divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 1px;
  background: var(--border);
}

.divider span {
  position: relative;
  background: white;
  padding: 0 1rem;
  color: var(--gray);
  font-weight: 600;
  font-size: 0.875rem;
}

small {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
}

@media (max-width: 640px) {
  .auth-page {
    padding: 1rem;
  }
  
  .auth-card {
    padding: 1.5rem;
  }
}
</style>