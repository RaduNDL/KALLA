<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'

const activeTab = ref('products')
const products = ref([])
const orders = ref([])
const isModalOpen = ref(false)
const editingId = ref(null)

const form = ref({
  name: '',
  category: 'Coffee',
  price: 0,
  stock: 0,
  image_url: '',
  description: '',
  details: ''
})

const fetchProducts = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/products')
    products.value = await response.json()
  } catch (e) {
  }
}

const fetchOrders = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/orders/history')
    orders.value = await response.json()
  } catch (e) {
  }
}

onMounted(() => {
  fetchProducts()
  fetchOrders()
})

const openAddModal = () => {
  editingId.value = null
  form.value = { name: '', category: 'Coffee', price: 0, stock: 100, image_url: '', description: '', details: '' }
  isModalOpen.value = true
}

const openEditModal = (p) => {
  editingId.value = p.id
  form.value = { ...p }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const saveProduct = async () => {
  const token = localStorage.getItem('token')
  const method = editingId.value ? 'PUT' : 'POST'
  const url = editingId.value 
    ? `http://127.0.0.1:8000/api/admin/products/${editingId.value}` 
    : 'http://127.0.0.1:8000/api/admin/products'

  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    })
    if (response.ok) {
      closeModal()
      fetchProducts()
    } else {
      alert('Failed to save product')
    }
  } catch (e) {
    alert('Error saving product')
  }
}

const deleteProduct = async (id) => {
  if (!confirm('Are you sure you want to delete this product?')) return
  const token = localStorage.getItem('token')
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/admin/products/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.ok) {
      fetchProducts()
    } else {
      alert('Failed to delete product')
    }
  } catch (e) {
    alert('Error deleting product')
  }
}

const updateOrderStatus = async (orderId, newStatus) => {
  const token = localStorage.getItem('token') // Preia token-ul curent exact acum
  
  if (!token) {
    alert('Session expired. Please log in again.')
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/admin/orders/${orderId}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` 
      },
      body: JSON.stringify({ status: newStatus })
    })
    
    if (response.ok) {
      await fetchOrders() 
    } else {
      const errorData = await response.json()
      console.error('API Error:', errorData)
      alert('Failed to update order status: ' + (errorData.detail || 'Unknown error'))
    }
  } catch (e) {
    alert('Server connection failed')
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    
    <Navbar />

    <main class="max-w-7xl mx-auto px-8 py-12">
      <div class="mb-12 border-b border-[#EAE5DF] pb-8">
        <h2 class="text-4xl font-serif font-light mb-2">Employee Portal</h2>
        <p class="text-sm text-[#666666] font-light">Manage catalog inventory and monitor active provisions.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        <div class="lg:col-span-3">
          <div class="flex flex-col space-y-2 sticky top-32">
            <button @click="activeTab = 'products'" :class="['text-left px-6 py-4 text-xs font-semibold tracking-wider uppercase transition-colors border-l-2', activeTab === 'products' ? 'border-[#1A1A1A] bg-white text-[#1A1A1A] shadow-sm' : 'border-transparent text-[#666666] hover:bg-white hover:text-[#1A1A1A]']">
              Manage Products
            </button>
            <button @click="activeTab = 'orders'" :class="['text-left px-6 py-4 text-xs font-semibold tracking-wider uppercase transition-colors border-l-2', activeTab === 'orders' ? 'border-[#1A1A1A] bg-white text-[#1A1A1A] shadow-sm' : 'border-transparent text-[#666666] hover:bg-white hover:text-[#1A1A1A]']">
              Manage Orders
            </button>
          </div>
        </div>

        <div class="lg:col-span-9">
          <div v-if="activeTab === 'products'" class="bg-white border border-[#EAE5DF] p-8 shadow-sm">
            <div class="flex justify-between items-center mb-8">
              <h3 class="text-lg font-serif font-medium">Products Database</h3>
              <button @click="openAddModal" class="bg-[#1A1A1A] text-white px-6 py-3 text-xs font-semibold tracking-wider uppercase hover:bg-[#A68A6D] transition-colors">
                Add New Product
              </button>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse min-w-[700px]">
                <thead>
                  <tr class="bg-[#FAFAF8] border-b border-[#EAE5DF] text-xs font-semibold tracking-wider text-[#666666] uppercase">
                    <th class="py-4 px-4">Image</th>
                    <th class="py-4 px-4">Name</th>
                    <th class="py-4 px-4">Category</th>
                    <th class="py-4 px-4">Price</th>
                    <th class="py-4 px-4">Stock</th>
                    <th class="py-4 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#EAE5DF] text-sm">
                  <tr v-for="product in products" :key="product.id" class="hover:bg-[#FAFAF8]/50">
                    <td class="py-4 px-4">
                      <img :src="product.image_url" class="w-12 h-12 object-cover border border-[#EAE5DF]" />
                    </td>
                    <td class="py-4 px-4 font-medium">{{ product.name }}</td>
                    <td class="py-4 px-4 text-[#666666]">{{ product.category }}</td>
                    <td class="py-4 px-4">${{ Number(product.price).toFixed(2) }}</td>
                    <td class="py-4 px-4">
                      <span :class="product.stock > 0 ? 'text-green-600' : 'text-red-500'">{{ product.stock }}</span>
                    </td>
                    <td class="py-4 px-4 text-right space-x-4">
                      <button @click="openEditModal(product)" class="text-xs font-semibold uppercase tracking-wider text-[#1A1A1A] hover:text-[#A68A6D] transition-colors">Edit</button>
                      <button @click="deleteProduct(product.id)" class="text-xs font-semibold uppercase tracking-wider text-red-500 hover:text-red-700 transition-colors">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'orders'" class="bg-white border border-[#EAE5DF] p-8 shadow-sm">
            <h3 class="text-lg font-serif font-medium mb-8">Active Orders</h3>
            
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse min-w-[700px]">
                <thead>
                  <tr class="bg-[#FAFAF8] border-b border-[#EAE5DF] text-xs font-semibold tracking-wider text-[#666666] uppercase">
                    <th class="py-4 px-4">Order ID</th>
                    <th class="py-4 px-4">Date</th>
                    <th class="py-4 px-4">Customer</th>
                    <th class="py-4 px-4">Total</th>
                    <th class="py-4 px-4">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#EAE5DF] text-sm">
                  <tr v-for="order in orders" :key="order.id" class="hover:bg-[#FAFAF8]/50">
                    <td class="py-4 px-4 font-mono text-xs text-[#666666]">#{{ order.id }}</td>
                    <td class="py-4 px-4 text-[#666666]">{{ formatDate(order.created_at) }}</td>
                    <td class="py-4 px-4 font-medium">{{ order.full_name }}</td>
                    <td class="py-4 px-4">${{ Number(order.total_amount).toFixed(2) }}</td>
                    <td class="py-4 px-4">
                      <select 
                        :value="order.status" 
                        @change="updateOrderStatus(order.id, $event.target.value)" 
                        class="bg-white border border-[#EAE5DF] px-3 py-1.5 text-xs font-medium focus:outline-none focus:border-[#1A1A1A] uppercase tracking-wider cursor-pointer"
                      >
                        <option value="Pending">Pending</option>
                        <option value="Processing">Processing</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="closeModal"></div>
      <div class="relative bg-white w-full max-w-2xl max-h-[90vh] overflow-y-auto border border-[#EAE5DF] p-8">
        <div class="flex justify-between items-center mb-8 border-b border-[#EAE5DF] pb-4">
          <h3 class="text-xl font-serif font-medium">{{ editingId ? 'Edit Product' : 'Add New Product' }}</h3>
          <button @click="closeModal" class="text-[#666666] hover:text-[#1A1A1A]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <form @submit.prevent="saveProduct" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Product Name</label>
              <input v-model="form.name" type="text" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]" />
            </div>
            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Category</label>
              <select v-model="form.category" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]">
                <option value="Coffee">Coffee</option>
                <option value="Tea">Tea</option>
                <option value="Pastries">Pastries</option>
              </select>
            </div>
            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Price ($)</label>
              <input v-model.number="form.price" type="number" step="0.01" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]" />
            </div>
            <div class="space-y-2">
              <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Stock Quantity</label>
              <input v-model.number="form.stock" type="number" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]" />
            </div>
          </div>
          
          <div class="space-y-2">
            <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Image URL</label>
            <input v-model="form.image_url" type="url" required class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]" />
          </div>

          <div class="space-y-2">
            <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Short Description</label>
            <textarea v-model="form.description" required rows="2" class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]"></textarea>
          </div>

          <div class="space-y-2">
            <label class="block text-xs font-semibold tracking-wider uppercase text-[#666666]">Full Details</label>
            <textarea v-model="form.details" required rows="4" class="w-full bg-[#FAFAF8] border border-[#EAE5DF] px-4 py-3 text-sm focus:outline-none focus:border-[#1A1A1A]"></textarea>
          </div>

          <div class="pt-4 flex justify-end space-x-4">
            <button type="button" @click="closeModal" class="px-6 py-3 text-xs font-semibold tracking-wider uppercase text-[#666666] hover:text-[#1A1A1A]">Cancel</button>
            <button type="submit" class="bg-[#1A1A1A] text-white px-8 py-3 text-xs font-semibold tracking-wider uppercase hover:bg-[#A68A6D] transition-colors">
              {{ editingId ? 'Save Changes' : 'Create Product' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>