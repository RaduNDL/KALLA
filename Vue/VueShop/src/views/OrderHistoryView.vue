<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'

const orders = ref([])

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/orders/history')
    orders.value = await response.json()
  } catch (error) {
  }
})

function getStatusClass(status) {
  if (status === 'Pending') return 'bg-yellow-50 text-yellow-700 border-yellow-200'
  if (status === 'Completed') return 'bg-green-50 text-green-700 border-green-200'
  return 'bg-gray-50 text-gray-700 border-gray-200'
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    
    <Navbar />

    <main class="max-w-5xl mx-auto px-8 py-12">
      <div class="mb-12">
        <h2 class="text-3xl font-serif font-light mb-2">Order History</h2>
        <p class="text-sm text-[#666666] font-light">Track the status of your past laboratory coffee provisions.</p>
      </div>

      <div v-if="orders.length === 0" class="bg-white border border-[#EAE5DF] p-16 text-center rounded-sm">
        <p class="text-sm text-[#666666] font-light">No orders found in your archive.</p>
      </div>

      <div v-else class="bg-white border border-[#EAE5DF] overflow-hidden rounded-sm shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-[#FAFAF8] border-b border-[#EAE5DF] text-xs font-semibold tracking-wider text-[#666666] uppercase">
                <th class="py-4 px-6">Order ID</th>
                <th class="py-4 px-6">Date & Time</th>
                <th class="py-4 px-6">Recipient</th>
                <th class="py-4 px-6">Total</th>
                <th class="py-4 px-6 text-center">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[#EAE5DF] text-sm font-light">
              <tr v-for="order in orders" :key="order.id" class="hover:bg-[#FAFAF8]/50 transition-colors">
                <td class="py-5 px-6 font-mono text-xs text-[#666666]">#{{ order.id }}</td>
                <td class="py-5 px-6 text-[#666666]">{{ formatDate(order.created_at) }}</td>
                <td class="py-5 px-6 font-medium">{{ order.full_name }}</td>
                <td class="py-5 px-6 font-medium">${{ Number(order.total_amount).toFixed(2) }}</td>
                <td class="py-5 px-6 text-center">
                  <span :class="['inline-block px-3 py-1 text-xs font-medium border rounded-full uppercase tracking-wider', getStatusClass(order.status)]">
                    {{ order.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>