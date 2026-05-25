<script setup>
import { ref, onMounted, computed } from 'vue'
import { useCartStore } from '../stores/cart'
import Navbar from '../components/Navbar.vue'

const cartStore = useCartStore()
const products = ref([])
const selectedCategory = ref('All')

const categories = ['All', 'Coffee', 'Tea', 'Pastries']

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/products')
    products.value = await response.json()
  } catch (error) {
  }
})

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'All') return products.value
  return products.value.filter(p => p.category === selectedCategory.value)
})
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    
    <Navbar />

    <main class="max-w-7xl mx-auto px-8 py-12">
      <div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
        <div>
          <h2 class="text-4xl md:text-5xl font-serif font-light mb-4 text-[#1A1A1A]">Menu Collection</h2>
          <p class="text-[#666666] font-light max-w-md text-sm leading-relaxed">Carefully curated beverages and pastries designed to elevate your daily ritual.</p>
        </div>
        
        <div class="flex space-x-6 overflow-x-auto pb-2 scrollbar-hide">
          <button 
            v-for="cat in categories" 
            :key="cat"
            @click="selectedCategory = cat"
            :class="['text-xs font-semibold tracking-[0.15em] uppercase pb-2 whitespace-nowrap transition-all duration-300 border-b-2', selectedCategory === cat ? 'border-[#1A1A1A] text-[#1A1A1A]' : 'border-transparent text-[#999999] hover:text-[#1A1A1A]']"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-16">
        <div v-for="product in filteredProducts" :key="product.id" class="group flex flex-col">
          <RouterLink :to="'/product/' + product.id" class="relative overflow-hidden aspect-[4/5] bg-[#EAE5DF] mb-6 block">
            <img :src="product.image_url" :alt="product.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" />
            <div class="absolute inset-0 bg-black/5 group-hover:bg-transparent transition-colors duration-500"></div>
            
            <button @click.prevent="cartStore.addToCart(product)" class="absolute bottom-6 left-1/2 -translate-x-1/2 translate-y-16 group-hover:translate-y-0 opacity-0 group-hover:opacity-100 bg-white/90 backdrop-blur-sm text-[#1A1A1A] px-8 py-3 text-xs font-semibold tracking-wider uppercase transition-all duration-300 hover:bg-[#1A1A1A] hover:text-white flex items-center space-x-2">
              <span>Add to Bag</span>
            </button>
          </RouterLink>
          
          <div class="flex justify-between items-start">
            <div>
              <RouterLink :to="'/product/' + product.id">
                <h3 class="text-lg font-serif font-medium text-[#1A1A1A] mb-1 hover:text-[#A68A6D] transition-colors">{{ product.name }}</h3>
              </RouterLink>
              <p class="text-xs text-[#666666] font-light max-w-[200px] line-clamp-2">{{ product.description }}</p>
              <p class="text-xs text-[#999999] font-light max-w-[200px] mt-1 line-clamp-1 italic">{{ product.details }}</p>
            </div>
            <span class="text-sm font-medium text-[#1A1A1A]">${{ Number(product.price).toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>