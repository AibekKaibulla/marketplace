<template>
  <div class="messages-container">
    <div class="messages-layout">
      <!-- Conversations List -->
      <div class="conversations-panel">
        <div class="conversations-header">
          <h2>Messages</h2>
          <input 
            type="text" 
            class="form-input"
            placeholder="Search conversations..."
            v-model="searchQuery"
          />
        </div>
        
        <div class="conversations-list">
          <div 
            v-for="conv in conversations" 
            :key="conv.id"
            class="conversation-item"
            :class="{ active: activeConversation === conv.id }"
            @click="selectConversation(conv.id)"
          >
            <UserAvatar :username="conv.user.username" size="lg" />
            <div class="conversation-info">
              <div class="conversation-header-row">
                <strong>{{ conv.user.name }}</strong>
                <span class="conversation-time">{{ conv.lastMessage.time }}</span>
              </div>
              <p class="conversation-preview">{{ conv.lastMessage.text }}</p>
              <span class="badge badge-secondary">{{ conv.listing.title }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Chat Area -->
      <div class="chat-panel">
        <div v-if="activeConversation" class="chat-container">
          <!-- Chat Header -->
          <div class="chat-header">
            <div class="flex items-center gap-md">
              <UserAvatar :username="selectedConversation.user.username" size="lg" />
              <div>
                <strong>{{ selectedConversation.user.name }}</strong>
                <div class="text-success text-sm">● Online</div>
              </div>
            </div>
            <button class="btn btn-secondary">View Listing</button>
          </div>
          
          <!-- Messages -->
          <div class="messages-area">
            <div 
              v-for="message in selectedConversation.messages" 
              :key="message.id"
              :class="['message', message.sent ? 'message-sent' : 'message-received']"
            >
              <UserAvatar 
                v-if="!message.sent" 
                :username="selectedConversation.user.username" 
                size="sm" 
              />
              <div class="message-content">
                <div class="message-bubble">
                  <p>{{ message.text }}</p>
                </div>
                <span class="message-time">{{ message.time }}</span>
              </div>
            </div>
          </div>
          
          <!-- Message Input -->
          <div class="message-input-container">
            <input 
              type="text" 
              class="form-input"
              placeholder="Type a message..."
              v-model="newMessage"
              @keyup.enter="sendMessage"
            />
            <button class="btn btn-primary" @click="sendMessage">Send</button>
          </div>
        </div>
        
        <EmptyState 
          v-else
          icon="💬"
          title="Select a Conversation"
          description="Choose a conversation from the left to start messaging"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import UserAvatar from '../components/UserAvatar.vue'
import EmptyState from '../components/EmptyState.vue'

const searchQuery = ref('')
const activeConversation = ref(1)
const newMessage = ref('')

// Mock conversations data
const conversations = ref([
  {
    id: 1,
    user: { username: 'johnd', name: 'John D.' },
    listing: { title: 'Calculus Textbook' },
    lastMessage: { text: 'Sure! When can we meet?', time: '2m ago' },
    messages: [
      { id: 1, text: "Hi! I'm interested in the Calculus textbook. Is it still available?", sent: false, time: '10:30 AM' },
      { id: 2, text: "Yes, it's still available! It's in excellent condition.", sent: true, time: '10:32 AM' },
      { id: 3, text: 'Great! Would you accept $40?', sent: false, time: '10:35 AM' },
      { id: 4, text: "How about $42? That's my lowest price.", sent: true, time: '10:38 AM' },
      { id: 5, text: 'Sure! When can we meet?', sent: false, time: 'Just now' }
    ]
  },
  {
    id: 2,
    user: { username: 'sarahm', name: 'Sarah M.' },
    listing: { title: 'MacBook Pro' },
    lastMessage: { text: 'Is the laptop still available?', time: '1h ago' },
    messages: [
      { id: 1, text: 'Is the laptop still available?', sent: false, time: '9:15 AM' }
    ]
  },
  {
    id: 3,
    user: { username: 'miker', name: 'Mike R.' },
    listing: { title: 'Desk Chair' },
    lastMessage: { text: 'Thanks for the quick response!', time: '3h ago' },
    messages: [
      { id: 1, text: 'Thanks for the quick response!', sent: false, time: '7:20 AM' }
    ]
  }
])

const selectedConversation = computed(() => {
  return conversations.value.find(c => c.id === activeConversation.value)
})

const selectConversation = (id) => {
  activeConversation.value = id
}

const sendMessage = () => {
  if (newMessage.value.trim() && selectedConversation.value) {
    selectedConversation.value.messages.push({
      id: Date.now(),
      text: newMessage.value,
      sent: true,
      time: 'Just now'
    })
    newMessage.value = ''
  }
}
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
