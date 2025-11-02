<template>
    <div class="card">
        <h2>Login</h2>

        <form @submit.prevent="doLogin">
            <label>Username</label>
            <input v-model="username" required />

            <label>Password</label>
            <input v-model="password" type="password" required />

            <button type="submit">Login</button>
        </form>

        <p class="error" v-if="error">{{ error }}</p>
    </div>
</template>


<script setup>
import { ref } from 'vue'
import auth from '../services/auth'
import { useRouter, useRoute } from 'vue-router'


const username = ref('')
const password = ref('')
const error = ref(null)
const router = useRouter()
const route = useRoute()


async function doLogin() {
    error.value = null
    try {
        await auth.login({ username: username.value, password: password.value })
        const next = route.query.next || '/'
        router.push(next)
    } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
            error.value = err.response.data.detail
        } else {
            error.value = 'Login failed'
        }
    }
}
</script>


<style scoped>
.card { padding:16px; border:1px solid #eee; border-radius:6px; max-width:400px }
label { display:block; margin-top:12px }
input { width:100%; padding:8px; margin-top:6px }
button { margin-top:12px; padding:8px 12px }
.error { color:crimson; margin-top:12px }
</style>