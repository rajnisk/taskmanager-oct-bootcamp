
<template>
  <router-view />

  <!-- Global Toast Container -->
  <div
    class="toast-container position-fixed top-0 end-0 p-3"
    style="z-index: 1100"
  >
    <div
      v-for="item in toastState.messages"
      :key="item.id"
      class="toast show border-0 mb-2"
      :class="'text-bg-' + item.type"
      role="alert"
      aria-live="polite"
      aria-atomic="true"
    >
      <div class="d-flex">
        <div class="toast-body">
          <strong>
            {{ titles[item.type] }}:
          </strong>
          {{ item.message }}
        </div>

        <button
          type="button"
          class="btn-close me-2 m-auto"
          :class="{ 'btn-close-white': item.type !== 'warning' && item.type !== 'info' }"
          aria-label="Close"
          @click="$toast.remove(item.id)"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
import { toastState } from './toast'

export default {
  data() {
    return {
      toastState,
      titles: {
        success: 'Success',
        danger: 'Error',
        warning: 'Warning',
        info: 'Info'
      }
    }
  }
}
</script>
