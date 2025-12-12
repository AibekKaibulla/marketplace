import api from './api'

/**
 * Categories API Service
 */

async function getCategories() {
    const res = await api.get('/api/categories')
    return res.data
}

async function getCategory(categoryId) {
    const res = await api.get(`/api/categories/${categoryId}`)
    return res.data
}

export default {
    getCategories,
    getCategory
}
