<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()
const authStore = useAuthStore()

async function handleLogin() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await response.json()
    if (response.ok) {
      authStore.setToken(data.access_token)
      router.push('/')
    } else {
      errorMsg.value = data.detail
    }
  } catch (e) {
    errorMsg.value = 'Server connection failed'
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#FDFBF7] flex items-center justify-center p-4">
    <div class="bg-white p-8 rounded-2xl shadow-lg border border-[#F5E6D3] w-full max-w-md">
      <h1 class="text-3xl font-serif font-bold text-[#2C1E15] text-center mb-6">Welcome Back</h1>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-[#4A3525] mb-1">Email Address</label>
          <input v-model="email" type="email" required class="w-full px-4 py-2 border border-[#EADBC8] rounded-lg focus:outline-none focus:border-[#4A3525]" />
        </div>
        <div>
          <label class="block text-sm font-medium text-[#4A3525] mb-1">Password</label>
          <input v-model="password" type="password" required class="w-full px-4 py-2 border border-[#EADBC8] rounded-lg focus:outline-none focus:border-[#4A3525]" />
        </div>
        <div v-if="errorMsg" class="text-red-500 text-sm font-medium">{{ errorMsg }}</div>
        <button type="submit" class="w-full bg-[#4A3525] text-white py-3 rounded-xl font-bold hover:bg-[#2C1E15] transition">Sign In</button>
      </form>
      <div class="mt-6 text-center text-sm text-gray-600">
        Don't have an account? 
        <RouterLink to="/register" class="text-[#6F4E37] font-bold hover:underline">Register here</RouterLink>
      </div>
    </div>
  </div>
</template>