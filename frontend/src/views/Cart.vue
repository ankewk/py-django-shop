<template>
  <div class="cart">
    <h1>购物车</h1>
    
    <div v-if="cartItems.length === 0" class="empty-cart">
      <el-empty description="购物车是空的">
        <el-button type="primary" @click="$router.push('/products')">
          去购物
        </el-button>
      </el-empty>
    </div>
    
    <div v-else>
      <!-- 购物车商品列表 -->
      <el-card class="cart-items">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <div class="item-image">
            <img :src="item.image || 'https://via.placeholder.com/100x100'" :alt="item.name">
          </div>
          <div class="item-info">
            <h3>{{ item.name }}</h3>
            <p class="item-price">¥{{ item.price }}</p>
          </div>
          <div class="item-quantity">
            <el-input-number
              v-model="item.quantity"
              :min="1"
              :max="99"
              size="small"
              @change="updateQuantity(item.id, $event)"
            />
          </div>
          <div class="item-total">
            ¥{{ (item.price * item.quantity).toFixed(2) }}
          </div>
          <div class="item-actions">
            <el-button type="danger" size="small" @click="removeItem(item.id)">
              删除
            </el-button>
          </div>
        </div>
      </el-card>
      
      <!-- 购物车总结 -->
      <el-card class="cart-summary">
        <div class="summary-row">
          <span>商品总数:</span>
          <span>{{ totalItems }} 件</span>
        </div>
        <div class="summary-row">
          <span>商品总价:</span>
          <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
        </div>
        <div class="summary-actions">
          <el-button @click="clearCart">清空购物车</el-button>
          <el-button type="primary" @click="goToCheckout">去结算</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'

export default {
  name: 'Cart',
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    
    const cartItems = computed(() => cartStore.items)
    const totalItems = computed(() => cartStore.totalItems)
    const totalPrice = computed(() => cartStore.totalPrice)
    
    const updateQuantity = (productId, quantity) => {
      cartStore.updateQuantity(productId, quantity)
    }
    
    const removeItem = (productId) => {
      cartStore.removeFromCart(productId)
    }
    
    const clearCart = () => {
      cartStore.clearCart()
    }
    
    const goToCheckout = () => {
      router.push('/checkout')
    }
    
    return {
      cartItems,
      totalItems,
      totalPrice,
      updateQuantity,
      removeItem,
      clearCart,
      goToCheckout
    }
  }
}
</script>

<style scoped>
.cart {
  max-width: 1200px;
  margin: 0 auto;
}

.cart h1 {
  margin-bottom: 30px;
  color: #333;
}

.empty-cart {
  text-align: center;
  padding: 60px 0;
}

.cart-items {
  margin-bottom: 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  margin-right: 20px;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.item-info {
  flex: 1;
  margin-right: 20px;
}

.item-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.item-price {
  margin: 0;
  color: #e60012;
  font-weight: bold;
}

.item-quantity {
  margin-right: 20px;
}

.item-total {
  font-weight: bold;
  color: #e60012;
  margin-right: 20px;
  min-width: 80px;
  text-align: right;
}

.item-actions {
  margin-left: auto;
}

.cart-summary {
  background: #f8f9fa;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.summary-row:last-child {
  border-bottom: none;
}

.total-price {
  font-size: 20px;
  font-weight: bold;
  color: #e60012;
}

.summary-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style> 