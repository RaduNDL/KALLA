<script setup>
import Navbar from '../components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    <Navbar />

    <main class="max-w-5xl mx-auto px-8 py-12">
      <div class="text-center mb-16">
        <span class="text-xs font-semibold tracking-[0.2em] text-[#666666] uppercase mb-4 block">Our Story</span>
        <h1 class="text-5xl md:text-6xl font-serif font-light mb-6">KÄLLA</h1>
        <div class="w-12 h-px bg-[#A68A6D] mx-auto"></div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-16 items-center mb-24">
        <div class="aspect-[4/5] bg-[#EAE5DF] overflow-hidden">
          <img src="https://images.unsplash.com/photo-1442512595331-e89e73853f31?q=80&w=1000&auto=format&fit=crop" alt="Pour over coffee" class="w-full h-full object-cover hover:scale-105 transition-transform duration-1000 ease-out" />
        </div>
        <div class="space-y-6">
          <h2 class="text-3xl font-serif font-light">Rooted in Tradition,<br>Brewed for Tomorrow.</h2>
          <p class="text-[#666666] font-light leading-relaxed">
            KÄLLA started with a simple belief: coffee is more than just a morning routine. It is a ritual, a moment of pause in a chaotic world. We source our beans directly from sustainable farms across the globe, ensuring that every cup respects both the environment and the farmers who cultivate it.
          </p>
          <p class="text-[#666666] font-light leading-relaxed">
            Our roasting process is meticulous. We do not mass-produce; we micro-roast in small batches to bring out the unique flavor profile of each origin. From the earthy notes of Sumatra to the bright acidity of Ethiopian Yirgacheffe, we celebrate diversity in every pour.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center border-t border-[#EAE5DF] pt-16">
        <div class="p-6">
          <h3 class="text-lg font-serif font-medium mb-3">Ethical Sourcing</h3>
          <p class="text-sm text-[#666666] font-light leading-relaxed">Direct trade relationships ensuring fair compensation and sustainable agricultural practices.</p>
        </div>
        <div class="p-6">
          <h3 class="text-lg font-serif font-medium mb-3">Artisan Roasting</h3>
          <p class="text-sm text-[#666666] font-light leading-relaxed">Small-batch roasting techniques designed to maximize clarity, sweetness, and complex aromas.</p>
        </div>
        <div class="p-6">
          <h3 class="text-lg font-serif font-medium mb-3">Expert Extraction</h3>
          <p class="text-sm text-[#666666] font-light leading-relaxed">Precision brewing methods handled by trained baristas to deliver the perfect cup, every time.</p>
        </div>
      </div>
    </main>
  </div>
</template>