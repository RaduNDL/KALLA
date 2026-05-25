<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import Navbar from '../components/Navbar.vue'

const cartStore = useCartStore()
const router = useRouter()

const fullName = ref('')
const address = ref('')
const city = ref('')
const cardNumber = ref('')
const expiry = ref('')
const cvc = ref('')
const isProcessing = ref(false)

const errors = ref({})
const touched = ref({
  fullName: false,
  address: false,
  city: false,
  cardNumber: false,
  expiry: false,
  cvc: false
})

const digitsOnly = (v) => (v || '').replace(/\D/g, '')
const cleanCard = computed(() => digitsOnly(cardNumber.value))
const expDigits = computed(() => digitsOnly(expiry.value))

const cardType = computed(() => {
  const d = cleanCard.value
  if (/^4/.test(d)) return 'visa'
  if (/^(34|37)/.test(d)) return 'amex'
  if (/^(5[1-5])/.test(d) || /^(222[1-9]|22[3-9]\d|2[3-6]\d{2}|27[01]\d|2720)/.test(d)) return 'mastercard'
  if (/^(6011|65|64[4-9]|622)/.test(d)) return 'discover'
  if (/^35/.test(d)) return 'jcb'
  return 'unknown'
})

const maxCardLen = computed(() => (cardType.value === 'amex' ? 15 : 19))

function formatCardNumber(digits) {
  if (cardType.value === 'amex') {
    const p1 = digits.slice(0, 4)
    const p2 = digits.slice(4, 10)
    const p3 = digits.slice(10, 15)
    return [p1, p2, p3].filter(Boolean).join(' ')
  }
  return digits.replace(/(.{4})/g, '$1 ').trim()
}

function formatExpiryMMYY(digits) {
  const mm = digits.slice(0, 2)
  const yy = digits.slice(2, 4)
  if (digits.length <= 2) return mm
  return `${mm} / ${yy}`
}

function setFieldError(field, msg) {
  const next = { ...errors.value }
  if (msg) next[field] = msg
  else delete next[field]
  errors.value = next
}

function validateField(field) {
  if (field === 'fullName') {
    setFieldError('fullName', fullName.value.trim() ? '' : 'Full name is required')
    return
  }
  if (field === 'address') {
    setFieldError('address', address.value.trim() ? '' : 'Street address is required')
    return
  }
  if (field === 'city') {
    setFieldError('city', city.value.trim() ? '' : 'City is required')
    return
  }
  if (field === 'cardNumber') {
    const d = cleanCard.value
    if (!/^\d{13,19}$/.test(d)) {
      setFieldError('cardNumber', 'Card number must be 13–19 digits')
      return
    }
    if (cardType.value === 'unknown') {
      setFieldError('cardNumber', 'Unknown card type')
      return
    }
    if (cardType.value === 'amex' && d.length !== 15) {
      setFieldError('cardNumber', 'AMEX must be 15 digits')
      return
    }
    if (cardType.value !== 'amex' && d.length !== 16 && d.length !== 19 && !(cardType.value === 'visa' && d.length === 13)) {
      setFieldError('cardNumber', 'Invalid card length')
      return
    }
    setFieldError('cardNumber', '')
    return
  }
  if (field === 'expiry') {
    const d = expDigits.value
    if (!/^\d{4}$/.test(d)) {
      setFieldError('expiry', 'Expiry must be in MM / YY format')
      return
    }
    const month = parseInt(d.slice(0, 2), 10)
    const year = parseInt(`20${d.slice(2, 4)}`, 10)
    if (month < 1 || month > 12) {
      setFieldError('expiry', 'Invalid month')
      return
    }
    const now = new Date()
    const currentMonth = now.getMonth() + 1
    const currentYear = now.getFullYear()
    if (year < currentYear || (year === currentYear && month < currentMonth)) {
      setFieldError('expiry', 'Card has expired')
      return
    }
    setFieldError('expiry', '')
    return
  }
  if (field === 'cvc') {
    const d = digitsOnly(cvc.value)
    const need = cardType.value === 'amex' ? 4 : 3
    if (!/^\d{3,4}$/.test(d)) {
      setFieldError('cvc', 'CVC must be 3 or 4 digits')
      return
    }
    if (d.length !== need) {
      setFieldError('cvc', `CVC must be ${need} digits`)
      return
    }
    setFieldError('cvc', '')
    return
  }
}

function validateForm() {
  ;['fullName', 'address', 'city', 'cardNumber', 'expiry', 'cvc'].forEach((f) => {
    touched.value[f] = true
    validateField(f)
  })
  return Object.keys(errors.value).length === 0
}

function onBlur(field) {
  touched.value[field] = true
  validateField(field)
}

function onCardInput(e) {
  const digits = digitsOnly(e.target.value).slice(0, maxCardLen.value)
  cardNumber.value = formatCardNumber(digits)
  touched.value.cardNumber = true
  validateField('cardNumber')
}

function onExpiryInput(e) {
  const digits = digitsOnly(e.target.value).slice(0, 4)
  expiry.value = formatExpiryMMYY(digits)
  touched.value.expiry = true
  validateField('expiry')
}

function onCvcInput(e) {
  const max = cardType.value === 'amex' ? 4 : 3
  const digits = digitsOnly(e.target.value).slice(0, max)
  cvc.value = digits
  touched.value.cvc = true
  validateField('cvc')
}

watch(fullName, () => touched.value.fullName && validateField('fullName'))
watch(address, () => touched.value.address && validateField('address'))
watch(city, () => touched.value.city && validateField('city'))
watch(cleanCard, () => touched.value.cardNumber && validateField('cardNumber'))
watch(expDigits, () => touched.value.expiry && validateField('expiry'))
watch(cvc, () => touched.value.cvc && validateField('cvc'))

async function handlePayment() {
  if (cartStore.items.length === 0) return
  if (!validateForm()) return

  isProcessing.value = true

  const payload = {
    full_name: fullName.value.trim(),
    address: address.value.trim(),
    city: city.value.trim(),
    total_amount: parseFloat((cartStore.totalPrice * 1.09).toFixed(2)),
    items: cartStore.items.map((item) => ({
      product_id: item.id,
      price: parseFloat(item.price),
      quantity: item.quantity
    }))
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      cartStore.clearCart()
      router.push('/history')
    } else {
      alert('Failed to process order.')
    }
  } catch (error) {
    console.error(error)
    alert('Network error. Please try again.')
  } finally {
    isProcessing.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#FAFAF8] text-[#1A1A1A] font-sans selection:bg-[#D4C3B3] selection:text-white pt-24">
    
    <Navbar />

    <main class="max-w-6xl mx-auto px-8 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
        <div class="lg:col-span-7 space-y-12">
          <div>
            <h2 class="text-3xl font-serif font-light mb-2">Checkout</h2>
            <p class="text-sm text-[#666666] font-light">Please enter your shipping and payment details below.</p>
          </div>

          <form @submit.prevent="handlePayment" class="space-y-8" novalidate>
            <div class="space-y-4">
              <h3 class="text-xs font-semibold tracking-wider uppercase text-[#666666]">Shipping Information</h3>
              <div class="space-y-4">
                <div>
                  <input v-model="fullName" @blur="onBlur('fullName')" type="text" autocomplete="name" placeholder="Full Name" :class="['w-full bg-white border px-5 py-4 text-sm focus:outline-none transition-colors', touched.fullName && errors.fullName ? 'border-red-500 text-red-500' : 'border-[#EAE5DF] focus:border-[#1A1A1A]']" />
                  <span v-if="touched.fullName && errors.fullName" class="text-xs text-red-500 block mt-1">{{ errors.fullName }}</span>
                </div>
                <div>
                  <input v-model="address" @blur="onBlur('address')" type="text" autocomplete="street-address" placeholder="Street Address" :class="['w-full bg-white border px-5 py-4 text-sm focus:outline-none transition-colors', touched.address && errors.address ? 'border-red-500 text-red-500' : 'border-[#EAE5DF] focus:border-[#1A1A1A]']" />
                  <span v-if="touched.address && errors.address" class="text-xs text-red-500 block mt-1">{{ errors.address }}</span>
                </div>
                <div>
                  <input v-model="city" @blur="onBlur('city')" type="text" autocomplete="address-level2" placeholder="City" :class="['w-full bg-white border px-5 py-4 text-sm focus:outline-none transition-colors', touched.city && errors.city ? 'border-red-500 text-red-500' : 'border-[#EAE5DF] focus:border-[#1A1A1A]']" />
                  <span v-if="touched.city && errors.city" class="text-xs text-red-500 block mt-1">{{ errors.city }}</span>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <h3 class="text-xs font-semibold tracking-wider uppercase text-[#666666]">Payment Method</h3>
              <div class="space-y-4">
                <div>
                  <input :value="cardNumber" @input="onCardInput" @blur="onBlur('cardNumber')" name="cardNumber" inputmode="numeric" autocomplete="cc-number" placeholder="Card Number" :class="['w-full bg-white border px-5 py-4 text-sm focus:outline-none transition-colors', touched.cardNumber && errors.cardNumber ? 'border-red-500 text-red-500' : 'border-[#EAE5DF] focus:border-[#1A1A1A]']" />
                  <span v-if="touched.cardNumber && errors.cardNumber" class="text-xs text-red-500 block mt-1">{{ errors.cardNumber }}</span>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <input :value="expiry" @input="onExpiryInput" @blur="onBlur('expiry')" name="expiry" inputmode="numeric" autocomplete="cc-exp" placeholder="MM / YY" :class="['w-full bg-white border px-5 py-4 text-sm focus:outline-none transition-colors', touched.expiry && errors.expiry ? 'border-red-500 text-red-500' : 'border-[#EAE5DF] focus:border-[#1A1A1A]']" />
                    <span v-if="touched.expiry && errors.expiry" class="text-xs text-red-500 block mt-1">{{ errors.expiry }}</span>
                  </div>
                  <div>
                    <input :value="cvc" @input="onCvcInput" @blur="onBlur('cvc')" name="cvc" inputmode="numeric" autocomplete="cc-csc" placeholder="CVC" :class="['w-full bg-white border px-5 py-4 text-sm focus:outline-none transition-colors', touched.cvc && errors.cvc ? 'border-red-500 text-red-500' : 'border-[#EAE5DF] focus:border-[#1A1A1A]']" />
                    <span v-if="touched.cvc && errors.cvc" class="text-xs text-red-500 block mt-1">{{ errors.cvc }}</span>
                  </div>
                </div>
              </div>
            </div>

            <button type="submit" :disabled="isProcessing || cartStore.items.length === 0" class="w-full bg-[#1A1A1A] text-white py-5 text-xs font-semibold tracking-[0.2em] uppercase hover:bg-[#A68A6D] transition-colors duration-300 disabled:opacity-50 disabled:hover:bg-[#1A1A1A]">
              <span v-if="isProcessing">Processing Payment...</span>
              <span v-else>Authorize Payment — ${{ (cartStore.totalPrice * 1.09).toFixed(2) }}</span>
            </button>
          </form>
        </div>

        <div class="lg:col-span-5 bg-white border border-[#EAE5DF] p-8">
          <h3 class="text-lg font-serif font-medium mb-6">Order Summary</h3>

          <div class="divide-y divide-[#EAE5DF] overflow-y-auto max-h-[350px] pr-2 mb-6">
            <div v-for="item in cartStore.items" :key="item.cartItemId" class="py-4 flex gap-4 first:pt-0 last:pb-0">
              <img :src="item.image_url" class="w-16 h-20 object-cover bg-[#EAE5DF]" />
              <div class="flex-1 flex flex-col justify-between py-0.5">
                <div>
                  <h4 class="font-serif text-sm font-medium text-[#1A1A1A]">{{ item.name }}</h4>
                  
                  <div v-if="item.customizations && Object.keys(item.customizations).length" class="text-[11px] text-[#666666] mt-1 space-y-0.5">
                    <div v-for="(val, key) in item.customizations" :key="key">
                      <span v-if="val !== 'None'" class="capitalize font-medium">{{ key }}: <span class="font-light">{{ val }}</span></span>
                    </div>
                  </div>

                  <p class="text-xs text-[#666666] font-light mt-1">Qty: {{ item.quantity }}</p>
                </div>
                <span class="text-sm font-medium">${{ (Number(item.price) * item.quantity).toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <div class="space-y-4 text-sm border-t border-[#EAE5DF] pt-6">
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
              <span class="font-medium text-[#1A1A1A]">Total Amount</span>
              <span class="text-2xl font-serif font-medium text-[#1A1A1A]">${{ (cartStore.totalPrice * 1.09).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>