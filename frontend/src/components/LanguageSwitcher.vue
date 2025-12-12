<template>
  <div class="language-switcher">
    <select v-model="currentLocale" @change="changeLocale" class="lang-select">
      <option value="en">English</option>
      <option value="ru">Русский</option>
      <option value="kk">Қазақша</option>
    </select>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

// Computed property for v-model binding
const currentLocale = computed({
  get: () => locale.value,
  set: (val) => {
    locale.value = val
    // Persist preference if desired (e.g., localStorage)
    localStorage.setItem('user-locale', val)
  }
})

// Initialize from storage if available
const storedLocale = localStorage.getItem('user-locale')
if (storedLocale) {
  locale.value = storedLocale
}

const changeLocale = () => {
  // Action is handled by the setter of computed property
}
</script>

<style scoped>
.lang-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background-color: var(--color-white);
  color: var(--color-text-primary);
  font-size: 0.9rem;
  cursor: pointer;
  outline: none;
}

.lang-select:focus {
  border-color: var(--color-primary);
}
</style>
