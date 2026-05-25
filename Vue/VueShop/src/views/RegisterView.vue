<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

async function handleRegister() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await response.json()
    if (response.ok) {
      router.push('/login')
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
      <h1 class="text-3xl font-serif font-bold text-[#2C1E15] text-center mb-6">Create Account</h1>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-[#4A3525] mb-1">Email Address</label>
          <input v-model="email" type="email" required class="w-full px-4 py-2 border border-[#EADBC8] rounded-lg focus:outline-none focus:border-[#4A3525]" />
        </div>
        <div>
          <label class="block text-sm font-medium text-[#4A3525] mb-1">Password</label>
          <input v-model="password" type="password" required class="w-full px-4 py-2 border border-[#EADBC8] rounded-lg focus:outline-none focus:border-[#4A3525]" />
        </div>
        <div v-if="errorMsg" class="text-red-500 text-sm font-medium">{{ errorMsg }}</div>
        <button type="submit" class="w-full bg-[#6F4E37] text-white py-3 rounded-xl font-bold hover:bg-[#4A3525] transition">Register</button>
      </form>
      <div class="mt-6 text-center text-sm text-gray-600">
        Already have an account? 
        <RouterLink to="/login" class="text-[#6F4E37] font-bold hover:underline">Sign in</RouterLink>
      </div>
    </div>
  </div>
</template>