<script setup>
import { ref, onMounted } from 'vue'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'

const cartStore = useCartStore()
const authStore = useAuthStore()

const isDropdownOpen = ref(false)
const isCartOpen = ref(false)
const userName = ref('Customer')
const userRole = ref('customer')

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
        if (decoded.name) userName.value = decoded.name
        else if (decoded.sub) {
          const namePart = decoded.sub.split('@')[0]
          userName.value = namePart.charAt(0).toUpperCase() + namePart.slice(1)
        }
        if (decoded.role) userRole.value = decoded.role
      }
    } catch (e) {
    }
  }
})
</script>

<template>
  <nav class="fixed w-full top-0 z-40 bg-[#FAFAF8]/90 backdrop-blur-md border-b border-[#EAE5DF] transition-all duration-300">
    <div class="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
      <RouterLink to="/" class="flex items-center space-x-3 group">
        <svg class="w-8 h-8 text-[#1A1A1A] group-hover:text-[#A68A6D] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 8a3 3 0 100-6 3 3 0 000 6zM5 8a3 3 0 100-6 3 3 0 000 6zM5 14h14a2 2 0 012 2v1a5 5 0 01-5 5H8a5 5 0 01-5-5v-1a2 2 0 012-2z"></path>
        </svg>
        <h1 class="text-xl font-serif font-semibold tracking-widest uppercase">KÄLLA</h1>
      </RouterLink>
      
      <div class="hidden md:flex items-center space-x-12 text-xs font-semibold tracking-[0.2em] text-[#666666]">
        <RouterLink to="/" class="hover:text-[#1A1A1A] hover:border-b-2 border-transparent hover:border-[#EAE5DF] pb-1 transition-all">HOME</RouterLink>
        <RouterLink to="/about" class="hover:text-[#1A1A1A] hover:border-b-2 border-transparent hover:border-[#EAE5DF] pb-1 transition-all">ABOUT</RouterLink>
        <RouterLink to="/products" class="hover:text-[#1A1A1A] hover:border-b-2 border-transparent hover:border-[#EAE5DF] pb-1 transition-all">OUR MENU</RouterLink>
        <button @click="isCartOpen = true" class="relative hover:text-[#1A1A1A] hover:border-b-2 border-transparent hover:border-[#EAE5DF] pb-1 transition-all">
          CART
          <span v-if="cartStore.totalItems > 0" class="absolute -top-2 -right-4 bg-[#1A1A1A] text-white text-[9px] font-bold w-4 h-4 rounded-full flex items-center justify-center tracking-normal">
            {{ cartStore.totalItems }}
          </span>
        </button>
      </div>

      <div class="flex items-center relative">
        <div class="relative">
          <button @click="isDropdownOpen = !isDropdownOpen" class="flex items-center focus:outline-none group rounded-full ring-2 ring-transparent hover:ring-[#EAE5DF] transition-all">
            <img :src="'https://ui-avatars.com/api/?name=' + userName + '&background=EAE5DF&color=1A1A1A'" alt="Profile" class="w-9 h-9 rounded-full object-cover border border-[#EAE5DF]" />
          </button>
          
          <div v-if="isDropdownOpen" class="absolute right-0 mt-4 w-56 bg-white border border-[#EAE5DF] shadow-xl flex flex-col z-50">
            <RouterLink v-if="userRole === 'employee'" to="/employee" @click="isDropdownOpen = false" class="px-6 py-4 text-xs font-semibold tracking-wider uppercase text-[#A68A6D] hover:bg-[#FAFAF8] transition-colors">Employee Portal</RouterLink>
            <RouterLink to="/profile" @click="isDropdownOpen = false" class="px-6 py-4 text-xs font-semibold tracking-wider uppercase text-[#1A1A1A] hover:bg-[#FAFAF8] border-t border-[#EAE5DF] transition-colors">Profile</RouterLink>
            <RouterLink to="/history" @click="isDropdownOpen = false" class="px-6 py-4 text-xs font-semibold tracking-wider uppercase text-[#1A1A1A] hover:bg-[#FAFAF8] border-t border-[#EAE5DF] transition-colors">Order History</RouterLink>
            <RouterLink to="/settings" @click="isDropdownOpen = false" class="px-6 py-4 text-xs font-semibold tracking-wider uppercase text-[#1A1A1A] hover:bg-[#FAFAF8] border-t border-[#EAE5DF] transition-colors">Settings</RouterLink>
            <button @click="authStore.logout" class="px-6 py-4 text-xs font-semibold tracking-wider uppercase text-red-600 hover:bg-red-50 border-t border-[#EAE5DF] transition-colors text-left">Sign Out</button>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <div v-if="isDropdownOpen" @click="isDropdownOpen = false" class="fixed inset-0 z-30"></div>

  <div v-if="isCartOpen" class="fixed inset-0 z-50 overflow-hidden">
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity" @click="isCartOpen = false"></div>
    
    <div class="absolute inset-y-0 right-0 max-w-md w-full bg-[#FAFAF8] shadow-2xl flex flex-col transform transition-transform duration-500 ease-in-out translate-x-0 border-l border-[#EAE5DF]">
      <div class="px-8 py-6 flex justify-between items-center border-b border-[#EAE5DF]">
        <h2 class="text-lg font-serif font-medium tracking-wide text-[#1A1A1A]">Shopping Cart</h2>
        <button @click="isCartOpen = false" class="text-[#666666] hover:text-[#1A1A1A] transition-colors p-2">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-8 space-y-6">
        <div v-if="cartStore.items.length === 0" class="h-full flex flex-col items-center justify-center text-center space-y-6">
          <svg class="w-16 h-16 text-[#EAE5DF]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
          <p class="font-serif text-[#666666] text-lg">Your cart is currently empty.</p>
          <button @click="isCartOpen = false" class="text-xs font-semibold tracking-wider uppercase text-[#1A1A1A] border-b border-[#1A1A1A] pb-1 hover:text-[#A68A6D] hover:border-[#A68A6D] transition-colors">Continue Shopping</button>
        </div>

        <div v-for="item in cartStore.items" :key="item.cartItemId" class="flex gap-6 items-center">
          <img :src="item.image_url" class="w-24 h-32 object-cover bg-[#EAE5DF]" />
          <div class="flex-1 flex flex-col justify-between h-32 py-1">
            <div>
              <div class="flex justify-between items-start mb-1">
                <h4 class="font-serif font-medium text-[#1A1A1A]">{{ item.name }}</h4>
                <button @click="cartStore.removeFromCart(item.cartItemId)" class="text-xs text-[#999999] hover:text-red-500 transition-colors">Remove</button>
              </div>
              
              <div v-if="item.customizations && Object.keys(item.customizations).length" class="text-[11px] text-[#666666] mb-1 space-y-0.5">
                <div v-for="(val, key) in item.customizations" :key="key">
                  <span v-if="val !== 'None'" class="capitalize font-medium">{{ key }}: <span class="font-light">{{ val }}</span></span>
                </div>
              </div>

              <p class="text-sm text-[#1A1A1A] mt-1">${{ Number(item.price).toFixed(2) }}</p>
            </div>
            
            <div class="flex items-center space-x-4 border border-[#EAE5DF] w-fit px-3 py-1.5">
              <button @click="cartStore.updateQuantity(item.cartItemId, item.quantity - 1)" class="text-[#666666] hover:text-[#1A1A1A] px-1 transition-colors">-</button>
              <span class="w-4 text-center font-medium text-sm text-[#1A1A1A]">{{ item.quantity }}</span>
              <button @click="cartStore.updateQuantity(item.cartItemId, item.quantity + 1)" class="text-[#666666] hover:text-[#1A1A1A] px-1 transition-colors">+</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="cartStore.items.length > 0" class="p-8 border-t border-[#EAE5DF] bg-white">
        <div class="space-y-4 mb-8 text-sm">
          <div class="flex justify-between text-[#666666]">
            <span>Subtotal</span>
            <span class="text-[#1A1A1A]">${{ cartStore.totalPrice.toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-[#666666]">
            <span>Estimated Tax</span>
            <span class="text-[#1A1A1A]">${{ (cartStore.totalPrice * 0.09).toFixed(2) }}</span>
          </div>
          <div class="w-full h-px bg-[#EAE5DF] my-2"></div>
          <div class="flex justify-between items-end">
            <span class="font-medium text-[#1A1A1A]">Total</span>
            <span class="text-xl font-serif font-medium text-[#1A1A1A]">${{ (cartStore.totalPrice * 1.09).toFixed(2) }}</span>
          </div>
        </div>
        <RouterLink to="/checkout" @click="isCartOpen = false" class="w-full bg-[#1A1A1A] text-white py-4 text-xs font-semibold tracking-[0.2em] uppercase hover:bg-[#A68A6D] transition-colors duration-300 flex justify-center items-center">
          Proceed to Checkout
        </RouterLink>
      </div>
    </div>
  </div>
</template>