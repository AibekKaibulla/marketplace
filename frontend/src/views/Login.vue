<template>
  <div class="auth-container">
    <div class="auth-card card">
      <div class="auth-icon">🔐</div>
      <h2>Welcome Back!</h2>
      <p class="auth-subtitle text-secondary">Sign in to your account</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">Username</label>
          <input 
            type="text" 
            class="form-input"
            placeholder="Enter your username"
            v-model="username"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Password</label>
          <input 
            type="password" 
            class="form-input"
            placeholder="Enter your password"
            v-model="password"
            required
          />
        </div>
        
        <button type="submit" class="btn btn-primary btn-block btn-lg">
          Sign In
        </button>
      </form>
      
      <div class="divider">
        <span>OR</span>
      </div>
      
      <p class="text-center text-secondary mb-md">Don't have an account?</p>
      <router-link to="/register">
        <button class="btn btn-secondary btn-block">Create Account</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/auth'

const router = useRouter()
const username = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    await authService.login(username.value, password.value)
    router.push('/')
  } catch (error) {
    alert('Login failed: ' + error.message)
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