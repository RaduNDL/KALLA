<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import Navbar from '../components/Navbar.vue'

const authStore = useAuthStore()

const name = ref('')
const email = ref('')
const password = ref('')
const message = ref('')
const errorMsg = ref('')
const isProcessing = ref(false)

onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const base64Url = token.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      }).join(''))
      
      const decoded = JSON.parse(jsonPayload)
      if (decoded) {
        email.value = decoded.sub || ''
        name.value = decoded.name || ''
      }
    } catch (e) {
    }
  }
})

async function handleUpdate() {
  isProcessing.value = true
  message.value = ''
  errorMsg.value = ''

  const token = localStorage.getItem('token')

  try {
    const response = await fetch('http://127.0.0.1:8000/api/user/settings', {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        new_name: name.value,
        new_email: email.value,
        new_password: password.value ? password.value : null
      })
    })

    const data = await response.json()
    if (response.ok) {
      authStore.setToken(data.access_token)
      message.value = 'Account configuration updated successfully.'
      password.value = ''
    } else {
      errorMsg.value = data.detail
    }
  } catch (e) {
    errorMsg.value = 'Server connection failed.'
  } finally {
    isProcessing.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    
    <Navbar />

    <main class="max-w-xl mx-auto px-8 py-12">
      <div class="mb-12">
        <h2 class="text-3xl font-serif font-light mb-2">Settings</h2>
        <p class="text-sm text-[#666666] font-light">Update your credential entries and system configuration.</p>
      </div>

      <div class="bg-white border border-[#EAE5DF] p-8 rounded-sm shadow-sm">
        <form @submit.prevent="handleUpdate" class="space-y-6">
          <div class="space-y-2">
            <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Full Name</label>
            <input v-model="name" type="text" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A] transition-colors" />
          </div>

          <div class="space-y-2">
            <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Email Address</label>
            <input v-model="email" type="email" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A] transition-colors" />
          </div>

          <div class="space-y-2">
            <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">New Password</label>
            <input v-model="password" type="password" placeholder="Leave blank to keep current password" class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A] transition-colors" />
          </div>

          <div v-if="message" class="text-green-600 text-xs font-medium">{{ message }}</div>
          <div v-if="errorMsg" class="text-red-500 text-xs font-medium">{{ errorMsg }}</div>

          <button type="submit" :disabled="isProcessing" class="w-full bg-[#1A1A1A] text-white py-4 text-xs font-semibold tracking-[0.2em] uppercase hover:bg-[#A68A6D] transition-colors duration-300 disabled:opacity-50">
            <span v-if="isProcessing">Saving configuration...</span>
            <span v-else>Update Settings</span>
          </button>
        </form>
      </div>
    </main>
  </div>
</template>