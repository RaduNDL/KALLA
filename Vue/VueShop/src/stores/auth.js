import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const router = useRouter()

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function clearToken() {
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user_role')
  }

  function logout() {
    clearToken()
    router.push('/login')
  }

  return { token, setToken, clearToken, logout }
})