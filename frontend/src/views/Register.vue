<template>
    <div class="card">
        <h2>Register</h2>

        <form @submit.prevent="doRegister">
            <label>Username</label>
            <input v-model="username" required minlength="3" />

            <label>Email</label>
            <input v-model="email" type="email" required />

            <label>Display Name (optional)</label>
            <input v-model="display_name" />

            <label>Role</label>
            <select v-model="role">
                <option value="buyer">Buyer</option>
                <option value="seller">Seller</option>
                <option value="both">Both</option>
            </select>

            <label>Password</label>
            <input v-model="password" type="password" required minlength="8" />

            <button type="submit">Register</button>
        </form>

        <p class="error" v-if="error">{{ error }}</p>
    </div>
</template>


<script setup>
import { ref } from 'vue'
import auth from '../services/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const display_name = ref('')
const role = ref('buyer')
const password = ref('')
const error = ref(null)
const router = useRouter()

async function doRegister() {
    error.value = null
    try {
        await auth.register({ username: username.value, email: email.value, display_name: display_name.value, role: role.value, password: password.value })
        router.push('/')
    } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
            error.value = err.response.data.detail
        } else {
            error.value = 'Registration failed'
        }
    }
}
</script>


<style scoped>
.card { padding:16px; border:1px solid #eee; border-radius:6px; max-width:500px }
label { display:block; margin-top:12px }
input, select { width:100%; padding:8px; margin-top:6px }
button { margin-top:12px; padding:8px 12px }
.error { color:crimson; margin-top:12px }
</style>