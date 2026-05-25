import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  const totalItems = computed(() => {
    return items.value.reduce((total, item) => total + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return items.value.reduce((total, item) => total + (item.price * item.quantity), 0)
  })

  function generateCartItemId(productId, customizations) {
    if (!customizations || Object.keys(customizations).length === 0) {
      return String(productId)
    }
    return `${productId}-${btoa(JSON.stringify(customizations))}`
  }

  function addToCart(product, customizations = {}) {
    const cartItemId = generateCartItemId(product.id, customizations)
    const existingItem = items.value.find(item => item.cartItemId === cartItemId)
    
    if (existingItem) {
      existingItem.quantity++
    } else {
      items.value.push({ 
        ...product, 
        cartItemId,
        customizations,
        quantity: 1 
      })
    }
  }

  function removeFromCart(cartItemId) {
    const index = items.value.findIndex(item => item.cartItemId === cartItemId)
    if (index !== -1) {
      items.value.splice(index, 1)
    }
  }

  function updateQuantity(cartItemId, quantity) {
    const item = items.value.find(item => item.cartItemId === cartItemId)
    if (item) {
      item.quantity = quantity
      if (item.quantity <= 0) {
        removeFromCart(cartItemId)
      }
    }
  }

  function clearCart() {
    items.value = []
  }

  return {
    items,
    totalItems,
    totalPrice,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart
  }
})