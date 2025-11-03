<template>
  <div class="home-wrapper">
    <!-- Hero Section -->
    <div class="hero">
      <div class="hero-content">
        <h1>👋 Welcome to Trinity</h1>
        <p class="hero-subtitle" v-if="user">
          Hello, <strong>{{ user.display_name || user.username }}</strong>! 
          You're logged in as <span class="role-badge">{{ user.role }}</span>
        </p>
        <p class="hero-subtitle" v-else>
          Your campus community for buying, selling, and trading
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-grid">
      <!-- User is logged in -->
      <template v-if="user">
        <div class="card feature-card">
          <div class="feature-icon">📝</div>
          <h3>Create Listing</h3>
          <p>List items you want to sell or services you offer to other students</p>
          <button class="btn btn-primary btn-block mt-3">
            <span>➕</span>
            New Listing
          </button>
        </div>

        <div class="card feature-card">
          <div class="feature-icon">🔍</div>
          <h3>Browse Items</h3>
          <p>Discover great deals on textbooks, electronics, furniture, and more</p>
          <button class="btn btn-outline btn-block mt-3">
            <span>🛍️</span>
            Start Shopping
          </button>
        </div>

        <div class="card feature-card">
          <div class="feature-icon">💬</div>
          <h3>Messages</h3>
          <p>Chat with buyers and sellers to negotiate deals and arrange meetups</p>
          <button class="btn btn-outline btn-block mt-3">
            <span>📨</span>
            View Messages
          </button>
        </div>

        <div class="card feature-card">
          <div class="feature-icon">⭐</div>
          <h3>Your Favorites</h3>
          <p>Keep track of items you're interested in and get notified of price changes</p>
          <button class="btn btn-outline btn-block mt-3">
            <span>❤️</span>
            My Favorites
          </button>
        </div>
      </template>

      <!-- User is not logged in -->
      <template v-else>
        <div class="card info-card">
          <div class="info-icon">🎓</div>
          <h3>For Students, By Students</h3>
          <p>Join thousands of students buying and selling safely within your campus community</p>
        </div>

        <div class="card info-card">
          <div class="info-icon">💰</div>
          <h3>Save Money</h3>
          <p>Find textbooks, furniture, and electronics at student-friendly prices</p>
        </div>

        <div class="card info-card">
          <div class="info-icon">🤝</div>
          <h3>Meet & Trade</h3>
          <p>Safe campus meetups with verified student sellers</p>
        </div>

        <div class="card info-card">
          <div class="info-icon">🔒</div>
          <h3>Secure Platform</h3>
          <p>Verified accounts and secure messaging keep your transactions safe</p>
        </div>
      </template>
    </div>

    <!-- CTA Section for non-logged in users -->
    <div v-if="!user" class="cta-section">
      <div class="card cta-card">
        <h2>Ready to Get Started?</h2>
        <p class="mb-4">Join our community today and start buying or selling!</p>
        <div class="cta-buttons">
          <router-link to="/register" class="btn btn-primary">
            Create Account
          </router-link>
          <router-link to="/login" class="btn btn-outline">
            Sign In
          </router-link>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner-large"></div>
      <p>Loading your dashboard...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import auth from '../services/auth'

const user = auth.currentUser // Use reactive ref from auth service
const loading = ref(false)

onMounted(async () => {
  if (auth.isAuthenticated() && !user.value) {
    loading.value = true
    try {
      await auth.fetchCurrentUser()
    } catch (err) {
      console.error('Failed to fetch user:', err)
      auth.clearAuth()
    } finally {
      loading.value = false
    }
  }
})
</script>

<style scoped>
.home-wrapper {
  min-height: calc(100vh - 80px);
  position: relative;
}

.hero {
  text-align: center;
  padding: 3rem 1rem;
  margin-bottom: 2rem;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  max-width: 600px;
  margin: 0 auto;
}

.role-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  text-transform: capitalize;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.feature-card, .info-card {
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover, .info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.feature-icon, .info-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.feature-card h3, .info-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  color: var(--dark);
}

.feature-card p, .info-card p {
  color: var(--gray);
  line-height: 1.6;
}

.cta-section {
  max-width: 600px;
  margin: 3rem auto;
}

.cta-card {
  text-align: center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
}

.cta-card h2 {
  color: var(--dark);
  margin-bottom: 0.5rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  color: white;
}

.spinner-large {
  width: 3rem;
  height: 3rem;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .cta-buttons .btn {
    width: 100%;
  }
}
</style>