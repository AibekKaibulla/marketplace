<template>
    <nav class="nav">
        <div class="brand">Student Marketplace</div>
        <div class="links">
            <router-link to="/">Home</router-link>
            <router-link v-if="!user" to="/login">Login</router-link>
            <router-link v-if="!user" to="/register">Register</router-link>
            <a v-if="user" @click.prevent="logout" href="#">Logout ({{ user.username }})</a>
        </div>
    </nav>
</template>

<script setup>
import { ref } from 'vue'
import auth from '../services/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(auth.getUser())

function logout() {
    auth.clearAuth()
    user.value = null
    router.push({ name: 'Home' })
}
</script>


<style scoped>
.nav { display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #eee }
.brand { font-weight:700 }
.links > * { margin-left:12px }
</style>