<script setup>
import Navbar from '../components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white">
    
    <Navbar />

    <header class="relative h-screen flex items-center justify-center overflow-hidden">
      <img src="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=2000&auto=format&fit=crop" alt="Coffee Shop Interior" class="absolute inset-0 w-full h-full object-cover scale-105" />
      <div class="absolute inset-0 bg-gradient-to-t from-[#1A1A1A]/80 via-[#1A1A1A]/40 to-transparent z-10"></div>
      
      <div class="relative z-20 text-center text-white px-4 flex flex-col items-center mt-20">
        <span class="text-[#D4C3B3] font-medium tracking-[0.3em] mb-6 uppercase text-xs">Curated Coffee Experience</span>
        <h2 class="text-5xl md:text-7xl font-serif font-light mb-8 tracking-tight drop-shadow-sm">The Art of<br>Perfect Brew</h2>
        <p class="text-base md:text-lg max-w-xl mx-auto mb-12 text-gray-300 font-light leading-relaxed">
          Discover a symphony of flavors crafted for the modern palate. Ethically sourced, expertly roasted, and poured with passion.
        </p>
        <RouterLink to="/products" class="group flex items-center space-x-3 bg-white text-[#1A1A1A] px-8 py-4 rounded-full font-medium text-sm tracking-wide hover:bg-[#1A1A1A] hover:text-white transition-all duration-500 shadow-xl">
          <span>VIEW COLLECTION</span>
          <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
        </RouterLink>
      </div>
    </header>
  </div>
</template>