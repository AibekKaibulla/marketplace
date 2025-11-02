import api, { setAuthHeader } from './api'

const TOKEN_KEY = 'sm_access_token'
const USER_KEY = 'sm_user'

function saveAuth(token, user) {
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(USER_KEY, JSON.stringify(user))
    setAuthHeader(token)
}

function clearAuth() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setAuthHeader(null)
}

function getToken() {
    return localStorage.getItem(TOKEN_KEY)
}
function getUser() {
    const u = localStorage.getItem(USER_KEY)
    return u ? JSON.parse(u) : null
}

async function register({ username, email, password, display_name, role = 'buyer' }) {
    const payload = { username, email, password, display_name, role }
    const res = await api.post('/api/auth/register', payload)
    const { access_token, user } = res.data
    saveAuth(access_token, user)
    return res.data
}


async function login({ username, password }) {
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
    return res.data
}


function isAuthenticated() {
return !!getToken()
}


export default {
    register,
    login,
    fetchCurrentUser,
    saveAuth,
    clearAuth,
    getToken,
    getUser,
    isAuthenticated
}