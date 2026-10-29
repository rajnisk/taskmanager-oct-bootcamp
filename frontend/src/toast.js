
import { reactive } from 'vue'

export const toastState = reactive({
  messages: []
})

let nextId = 1

function show(type, message) {
  const id = nextId++

  const item = { id, type, message }
  toastState.messages.push(item)

  item.timer = setTimeout(() => {
    remove(id)
  }, 3000)
}

function remove(id) {
  const index = toastState.messages.findIndex(
    item => item.id === id
  )

  if (index !== -1) {
    clearTimeout(toastState.messages[index].timer)
    toastState.messages.splice(index, 1)
  }
}

export const toast = {
  success: message => show('success', message),
  error: message => show('danger', message),
  warning: message => show('warning', message),
  info: message => show('info', message),
  remove
}
