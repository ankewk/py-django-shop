<template>
  <div id="app">
    <!-- 导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <router-link to="/">
            <h1>Django商城</h1>
          </router-link>
        </div>
        
        <div class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/products" class="nav-item">商品</router-link>
          <router-link to="/orders" class="nav-item">订单</router-link>
        </div>
        
        <div class="header-right">
          <router-link to="/cart" class="cart-icon">
            <el-badge :value="cartCount" :hidden="cartCount === 0">
              <el-icon><ShoppingCart /></el-icon>
            </el-badge>
          </router-link>
          
          <div v-if="!isLoggedIn" class="auth-buttons">
            <router-link to="/login">
              <el-button type="text">登录</el-button>
            </router-link>
            <router-link to="/register">
              <el-button type="primary">注册</el-button>
            </router-link>
          </div>
          
          <el-dropdown v-else @command="handleUserCommand">
            <span class="user-dropdown">
              {{ username }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="orders">我的订单</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>
    
    <!-- 主内容区域 -->
    <el-main class="main-content">
      <router-view />
    </el-main>
    
    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="footer-content">
        <p>&copy; 2025 Django商城. 保留所有权利.</p>
      </div>
    </el-footer>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingCart, ArrowDown } from '@element-plus/icons-vue'
import { useCartStore } from './stores/cart'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  components: {
    ShoppingCart,
    ArrowDown
  },
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    const authStore = useAuthStore()
    
    const cartCount = computed(() => cartStore.totalItems)
    const isLoggedIn = computed(() => authStore.isLoggedIn)
    const username = computed(() => authStore.user?.username || '用户')
    
    const handleUserCommand = (command) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'orders':
          router.push('/orders')
          break
        case 'logout':
          authStore.logout()
          router.push('/')
          break
      }
    }
    
    onMounted(() => {
      // 初始化购物车和用户状态
      cartStore.loadFromStorage()
      authStore.checkAuth()
    })
    
    return {
      cartCount,
      isLoggedIn,
      username,
      handleUserCommand
    }
  }
}
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
}

.logo a {
  text-decoration: none;
  color: #e60012;
}

.logo h1 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-item {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #e60012;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.cart-icon {
  text-decoration: none;
  color: #333;
  font-size: 20px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.main-content {
  margin-top: 60px;
  min-height: calc(100vh - 120px);
  padding: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.footer {
  background: #f5f5f5;
  text-align: center;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 