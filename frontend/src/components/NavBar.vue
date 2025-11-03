<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="brand">
        <span class="brand-text">Student Marketplace</span>
      </router-link>
      
      <div class="nav-links">
        <router-link to="/" class="nav-link">
          Home
        </router-link>
        
        <template v-if="!user">
          <router-link to="/login" class="nav-link">
            Login
          </router-link>
          <router-link to="/register" class="nav-link btn-register">
            Register
          </router-link>
        </template>
        
        <template v-else>
          <div class="user-menu">
            <div class="user-info">
              <div class="user-avatar">{{ userInitial }}</div>
              <div class="user-details">
                <div class="user-name">{{ user.display_name || user.username }}</div>
                <div class="user-role">{{ user.role }}</div>
              </div>
            </div>
            <button @click="logout" class="btn-logout">
              <span class="link-icon">🚪</span>
              Logout
            </button>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import auth from '../services/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = auth.currentUser // Use reactive ref from auth service

const userInitial = computed(() => {
  if (!user.value) return ''
  const name = user.value.display_name || user.value.username
  return name.charAt(0).toUpperCase()
})

function logout() {
  if (confirm('Are you sure you want to logout?')) {
    auth.clearAuth()
    router.push('/')
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
  transition: transform 0.2s;
}

.brand:hover {
  transform: scale(1.05);
}

.brand-icon {
  font-size: 1.75rem;
}

.brand-text {
  display: none;
}

@media (min-width: 640px) {
  .brand-text {
    display: inline;
  }
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  color: var(--gray);
  text-decoration: none;
  transition: all 0.2s;
}

.nav-link:hover {
  background: var(--gray-light);
  color: var(--primary);
}

.nav-link.router-link-active {
  color: var(--primary);
  background: rgba(99, 102, 241, 0.1);
}

.link-icon {
  font-size: 1.1rem;
}

.btn-register {
  background: var(--primary);
  color: white;
}

.btn-register:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 6px;
  background: var(--gray-light);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
}

.user-details {
  display: none;
}

@media (min-width: 640px) {
  .user-details {
    display: block;
  }
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--dark);
}

.user-role {
  font-size: 0.75rem;
  color: var(--gray);
  text-transform: capitalize;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: 2px solid var(--danger);
  color: var(--danger);
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: var(--danger);
  color: white;
  transform: translateY(-1px);
}

@media (max-width: 640px) {
  .nav-container {
    padding: 0.75rem 1rem;
  }
  
  .nav-links {
    gap: 0.25rem;
  }
  
  .nav-link {
    padding: 0.5rem;
  }
  
  .link-icon {
    font-size: 1.25rem;
  }
  
  .nav-link span:not(.link-icon) {
    display: none;
  }
}
</style>