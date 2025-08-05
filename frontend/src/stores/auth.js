import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  
  // 计算属性
  const isLoggedIn = computed(() => !!user.value)
  
  // 方法
  const login = async (credentials) => {
    try {
      const response = await axios.post('/api/auth/login/', credentials)
      const { user: userData, token: authToken } = response.data
      
      user.value = userData
      token.value = authToken
      
      // 设置axios默认headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`
      
      // 保存到localStorage
      localStorage.setItem('user', JSON.stringify(userData))
      localStorage.setItem('token', authToken)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.message || '登录失败' 
      }
    }
  }
  
  const register = async (userData) => {
    try {
      const response = await axios.post('/api/auth/register/', userData)
      const { user: newUser, token: authToken } = response.data
      
      user.value = newUser
      token.value = authToken
      
      // 设置axios默认headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`
      
      // 保存到localStorage
      localStorage.setItem('user', JSON.stringify(newUser))
      localStorage.setItem('token', authToken)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.message || '注册失败' 
      }
    }
  }
  
  const logout = () => {
    user.value = null
    token.value = null
    
    // 清除axios默认headers
    delete axios.defaults.headers.common['Authorization']
    
    // 清除localStorage
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }
  
  const checkAuth = () => {
    const savedUser = localStorage.getItem('user')
    const savedToken = localStorage.getItem('token')
    
    if (savedUser && savedToken) {
      user.value = JSON.parse(savedUser)
      token.value = savedToken
      axios.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`
    }
  }
  
  return {
    user,
    token,
    isLoggedIn,
    login,
    register,
    logout,
    checkAuth
  }
}) 