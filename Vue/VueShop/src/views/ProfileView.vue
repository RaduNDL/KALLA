<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'

const userEmail = ref('user@example.com')
const userName = ref('Customer')

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
        userEmail.value = decoded.sub || ''
        userName.value = decoded.name || 'Customer'
      }
    } catch (e) {
    }
  }
})
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    
    <Navbar />

    <main class="max-w-4xl mx-auto px-8 py-12">
      <div class="mb-16 border-b border-[#EAE5DF] pb-8">
        <h2 class="text-4xl font-serif font-light mb-2">Account Overview</h2>
        <p class="text-sm text-[#666666] font-light">Manage your profile, active sessions, and provisions archive.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-12">
        <div class="md:col-span-4 bg-white border border-[#EAE5DF] p-8 flex flex-col items-center text-center h-fit">
          <img :src="'https://ui-avatars.com/api/?name=' + userName + '&background=EAE5DF&color=1A1A1A&size=128'" alt="Profile" class="w-24 h-24 rounded-full object-cover border border-[#EAE5DF] mb-4" />
          
          <h3 class="text-sm font-semibold tracking-wider text-[#666666] uppercase mb-1">NAME</h3>
          <p class="text-base text-[#1A1A1A] font-medium mb-4">{{ userName }}</p>

          <h3 class="text-sm font-semibold tracking-wider text-[#666666] uppercase mb-1">EMAIL</h3>
          <p class="text-xs text-[#1A1A1A] font-mono break-all">{{ userEmail }}</p>
        </div>

        <div class="md:col-span-8 space-y-8">
          <h4 class="text-xs font-semibold tracking-wider uppercase text-[#666666]">Quick Actions</h4>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <RouterLink to="/history" class="group bg-white border border-[#EAE5DF] p-6 hover:border-[#1A1A1A] transition-all duration-300 flex flex-col justify-between h-40">
              <div class="text-2xl">📦</div>
              <div>
                <h5 class="font-serif font-medium text-base group-hover:text-[#A68A6D] transition-colors mb-1">Order History</h5>
                <p class="text-xs text-[#666666] font-light">Track statuses and details of all purchases.</p>
              </div>
            </RouterLink>

            <RouterLink to="/settings" class="group bg-white border border-[#EAE5DF] p-6 hover:border-[#1A1A1A] transition-all duration-300 flex flex-col justify-between h-40">
              <div class="text-2xl">⚙️</div>
              <div>
                <h5 class="font-serif font-medium text-base group-hover:text-[#A68A6D] transition-colors mb-1">Settings</h5>
                <p class="text-xs text-[#666666] font-light">Configure interface and security fields.</p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>