<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="card auth-card">
        <div class="card-header text-center">
          <div class="auth-icon">🔐</div>
          <h2>Welcome Back!</h2>
          <p style="color: var(--gray)">Sign in to your account</p>
        </div>

        <form @submit.prevent="doLogin">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="Enter your username"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
              required
              :disabled="isLoading"
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            {{ isLoading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div v-if="error" class="alert alert-error mt-3">
          <span>⚠️</span>
          {{ error }}
        </div>

        <div class="divider">
          <span>OR</span>
        </div>

        <div class="text-center">
          <p style="color: var(--gray)">Don't have an account?</p>
          <router-link to="/register" class="btn btn-outline btn-block mt-2">
            Create Account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import auth from '../services/auth'
import { useRouter, useRoute } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref(null)
const isLoading = ref(false)
const router = useRouter()
const route = useRoute()

async function doLogin() {
  error.value = null
  isLoading.value = true
  
  try {
    const result = await auth.login({ 
      username: username.value, 
      password: password.value 
    })
    
    // Navigate to next page or home
    const next = route.query.next || '/'
    router.push(next)
  } catch (err) {
    console.error('Login error:', err)
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Login failed. Please check your credentials.'
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
  max-width: 450px;
}

.auth-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.auth-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
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

@media (max-width: 640px) {
  .auth-page {
    padding: 1rem;
  }
  
  .auth-card {
    padding: 1.5rem;
  }
}
</style>