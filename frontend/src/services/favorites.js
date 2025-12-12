import api from './api'

/**
 * Favorites API Service
 */

async function getFavorites() {
    const res = await api.get('/api/favorites')
    return res.data
}

async function addFavorite(listingId) {
    const res = await api.post('/api/favorites', { listing_id: listingId })
    return res.data
}

async function removeFavorite(listingId) {
    await api.delete(`/api/favorites/${listingId}`)
}

async function checkFavorite(listingId) {
    const res = await api.get(`/api/favorites/check/${listingId}`)
    return res.data.is_favorite
}

export default {
    getFavorites,
    addFavorite,
    removeFavorite,
    checkFavorite
}
