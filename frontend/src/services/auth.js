import api, { setAuthHeader } from './api'
import { ref } from 'vue'

const TOKEN_KEY = 'sm_access_token'
const USER_KEY = 'sm_user'

const currentUser = ref(null)

function initAuth() {
    const token = localStorage.getItem(TOKEN_KEY)
    const userStr = localStorage.getItem(USER_KEY)

    if (token && userStr) {
        try {
            currentUser.value = JSON.parse(userStr)
            setAuthHeader(token)
        } catch (e) {
            clearAuth()
        }
    }
}

initAuth()

function saveAuth(token, user) {
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(USER_KEY, JSON.stringify(user))
    setAuthHeader(token)
    currentUser.value = user
}

function clearAuth() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setAuthHeader(null)
    currentUser.value = null
}

function getToken() {
    return localStorage.getItem(TOKEN_KEY)
}

function getUser() {
    return currentUser.value
}

function getCurrentUser() {
    return currentUser.value
}

async function register({ username, email, password, displayName, role = 'buyer' }) {
    const payload = {
        username,
        email,
        password,
        display_name: displayName,  // Backend expects snake_case
        role
    }
    const res = await api.post('/api/auth/register', payload)
    const { access_token, user } = res.data
    saveAuth(access_token, user)
    return res.data
}

async function login(username, password) {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)

    const res = await api.post('/api/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    const { access_token, user } = res.data
    saveAuth(access_token, user)
    return res.data
}

async function fetchCurrentUser() {
    const res = await api.get('/api/auth/me')
    currentUser.value = res.data
    saveAuth(getToken(), res.data)
    return res.data
}

function isAuthenticated() {
    return !!getToken()
}

function logout() {
    clearAuth()
}

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // Token expired or invalid
            clearAuth()
            // Optionally redirect to login
            if (window.location.pathname !== '/login') {
                window.location.href = '/login'
            }
        }
        return Promise.reject(error)
    }
)

export default {
    register,
    login,
    logout,
    fetchCurrentUser,
    getCurrentUser,
    saveAuth,
    clearAuth,
    getToken,
    getUser,
    isAuthenticated,
    currentUser // Export reactive ref for components
}