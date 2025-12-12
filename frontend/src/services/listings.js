import api from './api'

/**
 * Listings API Service
 */

async function getListings(filters = {}) {
    const params = new URLSearchParams()

    if (filters.search) params.append('search', filters.search)
    if (filters.category_id) params.append('category_id', filters.category_id)
    if (filters.min_price) params.append('min_price', filters.min_price)
    if (filters.max_price) params.append('max_price', filters.max_price)
    if (filters.condition) params.append('condition', filters.condition)
    if (filters.status) params.append('status', filters.status)
    if (filters.sort_by) params.append('sort_by', filters.sort_by)
    if (filters.limit) params.append('limit', filters.limit)
    if (filters.offset) params.append('offset', filters.offset)

    const res = await api.get(`/api/listings?${params.toString()}`)
    return res.data
}

async function getListing(listingId) {
    const res = await api.get(`/api/listings/${listingId}`)
    return res.data
}

async function createListing(listingData) {
    const res = await api.post('/api/listings', listingData)
    return res.data
}

async function updateListing(listingId, updateData) {
    const res = await api.put(`/api/listings/${listingId}`, updateData)
    return res.data
}

async function deleteListing(listingId) {
    await api.delete(`/api/listings/${listingId}`)
}

async function getMyListings(status = null) {
    const params = status ? `?status=${status}` : ''
    const res = await api.get(`/api/listings/me/listings${params}`)
    return res.data
}

async function getUserListings(userId, status = null) {
    const params = status ? `?status=${status}` : ''
    const res = await api.get(`/api/listings/user/${userId}${params}`)
    return res.data
}

export default {
    getListings,
    getListing,
    createListing,
    updateListing,
    deleteListing,
    getMyListings,
    getUserListings
}
