import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
    function addToast(message, type = 'info', duration = 4000) {
        const id = ++toastId
        toasts.value.push({ id, message, type })

        if (duration > 0) {
            setTimeout(() => removeToast(id), duration)
        }

        return id
    }

    function removeToast(id) {
        const index = toasts.value.findIndex(t => t.id === id)
        if (index > -1) {
            toasts.value.splice(index, 1)
        }
    }

    return {
        toasts,
        success: (msg) => addToast(msg, 'success'),
        error: (msg) => addToast(msg, 'error'),
        warning: (msg) => addToast(msg, 'warning'),
        info: (msg) => addToast(msg, 'info'),
        remove: removeToast
    }
}
