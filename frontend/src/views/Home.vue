<template>
    <div>
        <h1>Welcome to Student Marketplace</h1>
        <p v-if="user">Logged in as: <strong>{{ user.display_name || user.username }}</strong> ({{ user.role }})</p>
        <p v-else>Please login or register to continue.</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import auth from '../services/auth'

const user = ref(auth.getUser())

onMounted(async () => {
    if (auth.isAuthenticated() && !user.value) {
        try {
            const data = await auth.fetchCurrentUser()
            user.value = data
            auth.saveAuth(auth.getToken(), data)
        } catch (err) {
        // token invalid -> clear
            auth.clearAuth()
        }
    }
})
</script>