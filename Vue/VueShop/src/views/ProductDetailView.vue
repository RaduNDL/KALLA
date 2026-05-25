<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import Navbar from '../components/Navbar.vue'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()

const product = ref(null)
const quantity = ref(1)

const customizations = ref({
  sugar: 'Regular',
  milk: 'None',
  flavor: 'None'
})

onMounted(async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/products/${route.params.id}`)
    if (response.ok) {
      product.value = await response.json()
    } else {
      router.push('/products')
    }
  } catch (error) {
    router.push('/products')
  }
})

function handleAddToCart() {
  if (product.value) {
    for (let i = 0; i < quantity.value; i++) {
      cartStore.addToCart(product.value, { ...customizations.value })
    }
    quantity.value = 1
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    <Navbar />

    <main class="max-w-6xl mx-auto px-8 py-12" v-if="product">
      <div class="mb-8">
        <RouterLink to="/products" class="text-xs font-semibold tracking-[0.15em] uppercase hover:text-[#A68A6D] transition-colors flex items-center space-x-2 w-fit">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          <span>Back to Menu</span>
        </RouterLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-16">
        <div class="bg-[#EAE5DF] aspect-[4/5] overflow-hidden">
          <img :src="product.image_url" :alt="product.name" class="w-full h-full object-cover" />
        </div>
        
        <div class="flex flex-col justify-center">
          <div class="mb-8">
            <span class="text-xs font-semibold tracking-[0.2em] text-[#666666] uppercase mb-4 block">{{ product.category }}</span>
            <h1 class="text-4xl md:text-5xl font-serif font-light mb-4">{{ product.name }}</h1>
            <p class="text-2xl font-medium mb-8">${{ Number(product.price).toFixed(2) }}</p>
            <p class="text-[#666666] font-light leading-relaxed mb-6">{{ product.description }}</p>
            <p class="text-sm text-[#1A1A1A] font-light leading-relaxed">{{ product.details }}</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider text-[#666666] uppercase">Sugar</label>
              <select v-model="customizations.sugar" class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]">
                <option value="None">None</option>
                <option value="Less Sugar">Less Sugar</option>
                <option value="Regular">Regular</option>
                <option value="Extra Sugar">Extra Sugar</option>
              </select>
            </div>

            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider text-[#666666] uppercase">Milk</label>
              <select v-model="customizations.milk" class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]">
                <option value="None">None</option>
                <option value="Whole Milk">Whole Milk</option>
                <option value="Oat Milk">Oat Milk</option>
                <option value="Almond Milk">Almond Milk</option>
              </select>
            </div>

            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider text-[#666666] uppercase">Flavor</label>
              <select v-model="customizations.flavor" class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]">
                <option value="None">None</option>
                <option value="Vanilla">Vanilla</option>
                <option value="Caramel">Caramel</option>
                <option value="Hazelnut">Hazelnut</option>
              </select>
            </div>
          </div>
          
          <div class="mb-10">
            <p class="text-xs font-semibold tracking-wider text-[#666666] uppercase mb-3">Availability</p>
            <p class="text-sm font-medium" :class="product.stock > 0 ? 'text-green-600' : 'text-red-500'">
              {{ product.stock > 0 ? product.stock + ' In Stock' : 'Out of Stock' }}
            </p>
          </div>

          <div class="flex items-center space-x-6 border-t border-[#EAE5DF] pt-8">
            <div class="flex items-center border border-[#EAE5DF] px-4 py-4 bg-white">
              <button @click="quantity > 1 && quantity--" class="text-[#666666] hover:text-[#1A1A1A] px-3 transition-colors">-</button>
              <span class="w-10 text-center font-medium">{{ quantity }}</span>
              <button @click="quantity < product.stock && quantity++" class="text-[#666666] hover:text-[#1A1A1A] px-3 transition-colors">+</button>
            </div>
            
            <button @click="handleAddToCart" :disabled="product.stock === 0" class="flex-1 bg-[#1A1A1A] text-white py-5 text-xs font-semibold tracking-[0.2em] uppercase hover:bg-[#A68A6D] transition-colors disabled:opacity-50 disabled:hover:bg-[#1A1A1A]">
              Add to Bag
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>