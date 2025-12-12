<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="brand">Student Marketplace</router-link>
      
      <div class="nav-menu" :class="{ 'active': mobileMenuOpen }">
        <router-link to="/" class="nav-link" @click="closeMobileMenu">{{ $t('nav.home') }}</router-link>
        
        <template v-if="isLoggedIn">
          <router-link to="/listings" class="nav-link" @click="closeMobileMenu">{{ $t('nav.browse') }}</router-link>
          <router-link to="/listings/create" class="nav-link" @click="closeMobileMenu">{{ $t('nav.sell') }}</router-link>
          <router-link to="/messages" class="nav-link" @click="closeMobileMenu">{{ $t('nav.messages') }}</router-link>
          
          <div class="nav-actions">
            <router-link to="/profile" @click="closeMobileMenu">
              <UserAvatar :username="currentUser?.username || 'User'" size="md" />
            </router-link>
            <button class="btn btn-danger btn-sm" @click="handleLogout">{{ $t('nav.logout') }}</button>
            <LanguageSwitcher />
          </div>
        </template>
        
        <template v-else>
          <div class="nav-actions">
            <router-link to="/login" class="nav-link" @click="closeMobileMenu">{{ $t('nav.login') }}</router-link>
            <router-link to="/register" @click="closeMobileMenu">
              <button class="btn btn-primary btn-sm">{{ $t('nav.register') }}</button>
            </router-link>
            <LanguageSwitcher />
          </div>
        </template>
      </div>
      
      <button class="mobile-toggle" @click="toggleMobileMenu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/auth'
import UserAvatar from './UserAvatar.vue'
import LanguageSwitcher from './LanguageSwitcher.vue'

const router = useRouter()
const mobileMenuOpen = ref(false)

// Use the reactive currentUser ref directly from auth service
// This will automatically update when user logs in/out
const currentUser = authService.currentUser
const isLoggedIn = computed(() => !!currentUser.value)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const handleLogout = () => {
  authService.logout()
  closeMobileMenu()
  router.push('/')
}
</script>

<style scoped>
.navbar {
  background: var(--color-white);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-lg) var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-base);
}

.brand:hover {
  color: var(--color-primary-hover);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

.nav-link:hover {
  background: var(--color-gray-50);
  color: var(--color-primary);
}

.nav-link.router-link-active {
  color: var(--color-primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--spacing-sm);
}

.mobile-toggle span {
  width: 24px;
  height: 2px;
  background: var(--color-text-primary);
  transition: all var(--transition-base);
}

@media (max-width: 768px) {
  .navbar-container {
    padding: var(--spacing-md) var(--spacing-lg);
  }
  
  .mobile-toggle {
    display: flex;
  }
  
  .nav-menu {
    position: fixed;
    top: 65px;
    right: -100%;
    width: 100%;
    max-width: 300px;
    height: calc(100vh - 65px);
    background: var(--color-white);
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-xl);
    transition: right var(--transition-slow);
  }
  
  .nav-menu.active {
    right: 0;
  }
  
  .nav-link {
    padding: var(--spacing-md);
  }
  
  .nav-actions {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--color-border);
  }
  
  .nav-actions button {
    width: 100%;
  }
}
</style>