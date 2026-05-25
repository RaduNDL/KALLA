import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ProductView from '../views/ProductView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import OrderHistoryView from '../views/OrderHistoryView.vue'
import ProfileView from '../views/ProfileView.vue'
import SettingsView from '../views/SettingsView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import EmployeeDashboardView from '../views/EmployeeDashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/about', name: 'about', component: AboutView },
    { path: '/products', name: 'products', component: ProductView },
    { path: '/product/:id', name: 'product-detail', component: ProductDetailView },
    { path: '/checkout', name: 'checkout', component: CheckoutView },
    { path: '/history', name: 'history', component: OrderHistoryView },
    { path: '/profile', name: 'profile', component: ProfileView },
    { path: '/settings', name: 'settings', component: SettingsView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/employee', name: 'employee', component: EmployeeDashboardView }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.name !== 'login' && to.name !== 'register' && to.name !== 'home' && to.name !== 'about' && !token) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router