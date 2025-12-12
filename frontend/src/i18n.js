import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import ru from './locales/ru.json'
import kk from './locales/kk.json'

const i18n = createI18n({
    legacy: false, // Composition API mode
    locale: 'en', // Default locale
    fallbackLocale: 'en',
    messages: {
        en,
        ru,
        kk
    }
})

export default i18n
