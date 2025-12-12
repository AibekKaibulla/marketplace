import api from './api'

/**
 * Messages API Service
 */

async function getConversations() {
    const res = await api.get('/api/messages/conversations')
    return res.data
}

async function getConversationMessages(userId, listingId = null) {
    const params = listingId ? `?listing_id=${listingId}` : ''
    const res = await api.get(`/api/messages/conversation/${userId}${params}`)
    return res.data
}

async function sendMessage(receiverId, body, listingId = null) {
    const payload = {
        receiver_id: receiverId,
        body: body  // Match backend field name
    }
    if (listingId) {
        payload.listing_id = listingId
    }
    const res = await api.post('/api/messages', payload)
    return res.data
}

async function markAsRead(messageId) {
    const res = await api.put(`/api/messages/${messageId}/read`)
    return res.data
}

export default {
    getConversations,
    getConversationMessages,
    sendMessage,
    markAsRead
}
