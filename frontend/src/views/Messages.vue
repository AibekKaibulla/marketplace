<template>
  <div class="messages-container">
    <div class="messages-layout">
      <!-- Conversations List -->
      <div class="conversations-panel">
        <div class="conversations-header">
          <h2>{{ $t('messages.title') }}</h2>
          <input 
            type="text" 
            class="form-input"
            :placeholder="$t('listings.filter.search_placeholder')"
            v-model="searchQuery"
          />
        </div>
        
        <div v-if="loadingConversations" class="loading-state">
          <p class="text-secondary">{{ $t('listings.loading') }}</p>
        </div>
        
        <div v-else class="conversations-list">
          <div 
            v-for="conv in filteredConversations" 
            :key="`${conv.user.user_id}-${conv.listing?.listing_id || 'none'}`"
            class="conversation-item"
            :class="{ active: isActiveConversation(conv) }"
            @click="selectConversation(conv)"
          >
            <UserAvatar :username="conv.user.username" size="lg" />
            <div class="conversation-info">
              <div class="conversation-header-row">
                <strong>{{ conv.user.display_name || conv.user.username }}</strong>
                <span class="conversation-time">{{ formatTime(conv.last_message?.sent_at) }}</span>
              </div>
              <p class="conversation-preview">{{ conv.last_message?.body || 'No messages yet' }}</p>
              <span v-if="conv.listing" class="badge badge-secondary">{{ conv.listing.title }}</span>
              <span v-if="conv.unread_count > 0" class="unread-badge">{{ conv.unread_count }}</span>
            </div>
          </div>
          
          <EmptyState 
            v-if="conversations.length === 0"
            icon="💬"
            :title="$t('messages.title')"
            :description="$t('messages.contacts')"
          />
        </div>
      </div>
      
      <!-- Chat Area -->
      <div class="chat-panel">
        <div v-if="activeConversation" class="chat-container">
          <!-- Chat Header -->
          <div class="chat-header">
            <div class="flex items-center gap-md">
              <UserAvatar :username="activeConversation.user.username" size="lg" />
              <div>
                <strong>{{ activeConversation.user.display_name || activeConversation.user.username }}</strong>
                <div class="text-secondary text-sm" v-if="activeConversation.listing">
                  Re: {{ activeConversation.listing.title }}
                </div>
              </div>
            </div>
            <router-link 
              v-if="activeConversation.listing" 
              :to="`/listings/${activeConversation.listing.listing_id}`"
              class="btn btn-secondary"
            >
              {{ $t('card.view_details') }}
            </router-link>
          </div>
          
          <!-- Messages -->
          <div class="messages-area" ref="messagesArea">
            <div v-if="loadingMessages" class="loading-state">
              <p class="text-secondary">{{ $t('listings.loading') }}</p>
            </div>
            
            <div 
              v-for="message in messages" 
              :key="message.message_id"
              :class="['message', isSentByMe(message) ? 'message-sent' : 'message-received']"
            >
              <UserAvatar 
                v-if="!isSentByMe(message)" 
                :username="activeConversation.user.username" 
                size="sm" 
              />
              <div class="message-content">
                <div class="message-bubble">
                  <p>{{ message.body }}</p>
                </div>
                <span class="message-time">{{ formatTime(message.sent_at) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Message Input -->
          <div class="message-input-container">
            <input 
              type="text" 
              class="form-input"
              :placeholder="$t('messages.type_message')"
              v-model="newMessage"
              @keyup.enter="sendMessage"
              :disabled="sendingMessage"
            />
            <button 
              class="btn btn-primary" 
              @click="sendMessage"
              :disabled="sendingMessage || !newMessage.trim()"
            >
              {{ sendingMessage ? '...' : $t('messages.send') }}
            </button>
          </div>
        </div>
        
        <EmptyState 
          v-else
          icon="💬"
          :title="$t('messages.no_chat_selected')"
          :description="$t('messages.contacts')"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import UserAvatar from '../components/UserAvatar.vue'
import EmptyState from '../components/EmptyState.vue'
import messagesService from '../services/messages'
import listingsService from '../services/listings'
import api from '../services/api'
import authService from '../services/auth'

const { t } = useI18n()

const route = useRoute()

const searchQuery = ref('')
const conversations = ref([])
const messages = ref([])
const activeConversation = ref(null)
const newMessage = ref('')
const loadingConversations = ref(true)
const loadingMessages = ref(false)
const sendingMessage = ref(false)
const messagesArea = ref(null)

const currentUser = authService.currentUser

// Fetch conversations from API
async function fetchConversations() {
  loadingConversations.value = true
  try {
    conversations.value = await messagesService.getConversations()
  } catch (err) {
    console.error('Error fetching conversations:', err)
  } finally {
    loadingConversations.value = false
  }
}

// Fetch messages for a conversation
async function fetchMessages() {
  if (!activeConversation.value) return
  
  loadingMessages.value = true
  try {
    messages.value = await messagesService.getConversationMessages(
      activeConversation.value.user.user_id,
      activeConversation.value.listing?.listing_id
    )
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Error fetching messages:', err)
  } finally {
    loadingMessages.value = false
  }
}

// Send a message
async function sendMessage() {
  if (!newMessage.value.trim() || !activeConversation.value) return
  
  sendingMessage.value = true
  try {
    const sentMessage = await messagesService.sendMessage(
      activeConversation.value.user.user_id,
      newMessage.value,
      activeConversation.value.listing?.listing_id
    )
    messages.value.push(sentMessage)
    newMessage.value = ''
    await nextTick()
    scrollToBottom()
    
    // Refresh conversations to update last message
    fetchConversations()
  } catch (err) {
    console.error('Error sending message:', err)
  } finally {
    sendingMessage.value = false
  }
}

function selectConversation(conv) {
  activeConversation.value = conv
  fetchMessages()
}

function isActiveConversation(conv) {
  if (!activeConversation.value) return false
  return activeConversation.value.user.user_id === conv.user.user_id &&
         activeConversation.value.listing?.listing_id === conv.listing?.listing_id
}

function isSentByMe(message) {
  return message.sender_id === currentUser.value?.user_id
}

function scrollToBottom() {
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight
  }
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  const query = searchQuery.value.toLowerCase()
  return conversations.value.filter(conv => 
    conv.user.username.toLowerCase().includes(query) ||
    conv.user.display_name?.toLowerCase().includes(query) ||
    conv.listing?.title.toLowerCase().includes(query)
  )
})

// Handle deep links from listing detail (e.g., /messages?to=5&listing=10)
async function handleDeepLink() {
  const toUserId = route.query.to
  const listingId = route.query.listing
  
  if (toUserId) {
    try {
      // Get user info
      const userRes = await api.get(`/api/auth/user/${toUserId}`)
      const user = userRes.data
      
      // Get listing info if provided
      let listing = null
      if (listingId) {
        listing = await listingsService.getListing(listingId)
      }
      
      // Create a new conversation object
      activeConversation.value = {
        user: {
          user_id: parseInt(toUserId),
          username: user.username,
          display_name: user.display_name
        },
        listing: listing ? {
          listing_id: listing.listing_id,
          title: listing.title,
          price: listing.price
        } : null,
        last_message: null,
        unread_count: 0
      }
      
      // Fetch existing messages if any
      fetchMessages()
    } catch (err) {
      console.error('Error handling deep link:', err)
    }
  }
}

onMounted(async () => {
  await fetchConversations()
  
  // Check for deep link params
  if (route.query.to) {
    handleDeepLink()
  }
})

// Watch for route changes
watch(() => route.query, (newQuery) => {
  if (newQuery.to) {
    handleDeepLink()
  }
})
</script>

<style scoped>
.messages-container {
  padding: 0;
}

.messages-layout {
  display: grid;
  grid-template-columns: 350px 1fr;
  height: calc(100vh - 100px);
  background: var(--color-white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.conversations-panel {
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
}

.conversations-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
}

.conversations-header h2 {
  margin-bottom: var(--spacing-md);
  color: var(--color-text-primary);
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background var(--transition-base);
  position: relative;
}

.conversation-item:hover {
  background: var(--color-gray-50);
}

.conversation-item.active {
  background: var(--color-gray-100);
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-xs);
}

.conversation-time {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
}

.conversation-preview {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-xs);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.unread-badge {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-lg);
  background: var(--color-primary);
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
}

.chat-panel {
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
}

.messages-area {
  flex: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
  background: var(--color-gray-50);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.message {
  display: flex;
  gap: var(--spacing-sm);
}

.message-sent {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 400px;
}

.message-sent .message-content {
  align-items: flex-end;
  display: flex;
  flex-direction: column;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.message-received .message-bubble {
  background: var(--color-white);
  color: var(--color-text-primary);
}

.message-sent .message-bubble {
  background: var(--color-primary);
  color: var(--color-white);
}

.message-bubble p {
  margin: 0;
}

.message-time {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
  margin-top: var(--spacing-xs);
  display: block;
}

.message-input-container {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  background: var(--color-white);
}

.loading-state {
  text-align: center;
  padding: var(--spacing-xl);
}

@media (max-width: 768px) {
  .messages-layout {
    grid-template-columns: 1fr;
  }
  
  .conversations-panel {
    display: none;
  }
  
  .conversations-panel.mobile-show {
    display: flex;
  }
  
  .chat-panel.mobile-hide {
    display: none;
  }
}
</style>
