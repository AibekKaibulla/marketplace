<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Welcome to Student Marketplace</h1>
        <p class="hero-subtitle">
          <template v-if="isLoggedIn">
            Hello, <strong>{{ currentUser.displayName || currentUser.username }}</strong>!
            <span class="badge badge-primary">{{ currentUser.role }}</span>
          </template>
          <template v-else>
            Your campus community for buying, selling, and trading
          </template>
        </p>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container">
      <!-- Guest View -->
      <template v-if="!isLoggedIn">
        <div class="grid grid-auto-fit">
          <div class="card text-center">
            <div class="feature-icon">🎓</div>
            <h3>For Students, By Students</h3>
            <p class="text-secondary">
              Join thousands of students buying and selling safely within your campus community
            </p>
          </div>
          <div class="card text-center">
            <div class="feature-icon">💰</div>
            <h3>Save Money</h3>
            <p class="text-secondary">
              Find textbooks, furniture, and electronics at student-friendly prices
            </p>
          </div>
          <div class="card text-center">
            <div class="feature-icon">🤝</div>
            <h3>Meet & Trade</h3>
            <p class="text-secondary">
              Safe campus meetups with verified student sellers
            </p>
          </div>
          <div class="card text-center">
            <div class="feature-icon">🔒</div>
            <h3>Secure Platform</h3>
            <p class="text-secondary">
              Verified accounts and secure messaging keep your transactions safe
            </p>
          </div>
        </div>
      </template>

      <!-- Logged In View -->
      <template v-else>
        <div class="grid grid-auto-fit">
          <div class="card text-center">
            <div class="feature-icon">📝</div>
            <h3>Create Listing</h3>
            <p class="text-secondary mb-lg">
              List items you want to sell or services you offer to other students
            </p>
            <router-link to="/listings/create">
              <button class="btn btn-primary btn-block">New Listing</button>
            </router-link>
          </div>
          
          <div class="card text-center">
            <div class="feature-icon">🔍</div>
            <h3>Browse Items</h3>
            <p class="text-secondary mb-lg">
              Discover great deals on textbooks, electronics, furniture, and more
            </p>
            <router-link to="/listings">
              <button class="btn btn-secondary btn-block">Start Shopping</button>
            </router-link>
          </div>
          
          <div class="card text-center">
            <div class="feature-icon">💬</div>
            <h3>Messages</h3>
            <p class="text-secondary mb-lg">
              Chat with buyers and sellers to negotiate deals and arrange meetups
            </p>
            <router-link to="/messages">
              <button class="btn btn-secondary btn-block">View Messages</button>
            </router-link>
          </div>
          
          <div class="card text-center">
            <div class="feature-icon">⭐</div>
            <h3>Your Profile</h3>
            <p class="text-secondary mb-lg">
              Manage your listings, favorites, and account settings
            </p>
            <router-link to="/profile">
              <button class="btn btn-secondary btn-block">My Profile</button>
            </router-link>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import authService from '../services/auth'

const isLoggedIn = computed(() => authService.isAuthenticated())
const currentUser = computed(() => authService.getCurrentUser() || {})
</script>

<style scoped>
.hero {
  background: var(--gradient-hero);
  color: var(--color-white);
  padding: var(--spacing-3xl) var(--spacing-xl);
  text-align: center;
  margin-bottom: var(--spacing-3xl);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: var(--font-size-5xl);
  margin-bottom: var(--spacing-lg);
  color: var(--color-white);
}

.hero-subtitle {
  font-size: var(--font-size-xl);
  opacity: 0.95;
}

.hero-subtitle .badge {
  margin-left: var(--spacing-sm);
  background: rgba(255, 255, 255, 0.2);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-lg);
}

@media (max-width: 768px) {
  .hero {
    padding: var(--spacing-2xl) var(--spacing-lg);
  }
  
  .hero-title {
    font-size: var(--font-size-3xl);
  }
  
  .hero-subtitle {
    font-size: var(--font-size-lg);
  }
}
</style>