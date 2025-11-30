import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Listings from '../views/Listings.vue'
import CreateListing from '../views/CreateListing.vue'
import Messages from '../views/Messages.vue'
import UserProfile from '../views/UserProfile.vue'
import authService from '../services/auth'


const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },
    {
        path: '/listings',
        name: 'Listings',
        component: Listings
    },
    {
        path: '/listings/create',
        name: 'CreateListing',
        component: CreateListing,
        meta: { requiresAuth: true }
    },
    {
        path: '/messages',
        name: 'Messages',
        component: Messages,
        meta: { requiresAuth: true }
    },
    {
        path: '/profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})


router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !authService.isAuthenticated()) {
        next({ name: 'Login', query: { next: to.fullPath } })
    } else {
        next()
    }
})


export default router