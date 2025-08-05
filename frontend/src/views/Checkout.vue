<template>
  <div class="checkout">
    <h1>订单结算</h1>
    
    <div v-if="cartItems.length === 0" class="empty-cart">
      <el-empty description="购物车是空的">
        <el-button type="primary" @click="$router.push('/products')">
          去购物
        </el-button>
      </el-empty>
    </div>
    
    <div v-else>
      <el-row :gutter="40">
        <!-- 订单信息 -->
        <el-col :span="16">
          <el-card class="order-info">
            <template #header>
              <span>订单信息</span>
            </template>
            
            <!-- 收货地址 -->
            <div class="section">
              <h3>收货地址</h3>
              <el-form :model="addressForm" label-width="80px">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="收货人">
                      <el-input v-model="addressForm.receiver" placeholder="请输入收货人姓名" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="手机号">
                      <el-input v-model="addressForm.phone" placeholder="请输入手机号" />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item label="详细地址">
                  <el-input
                    v-model="addressForm.address"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入详细地址"
                  />
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 支付方式 -->
            <div class="section">
              <h3>支付方式</h3>
              <el-radio-group v-model="paymentMethod">
                <el-radio label="alipay">支付宝</el-radio>
                <el-radio label="wechat">微信支付</el-radio>
                <el-radio label="card">银行卡</el-radio>
              </el-radio-group>
            </div>
            
            <!-- 订单备注 -->
            <div class="section">
              <h3>订单备注</h3>
              <el-input
                v-model="orderNote"
                type="textarea"
                :rows="3"
                placeholder="请输入订单备注（可选）"
              />
            </div>
          </el-card>
        </el-col>
        
        <!-- 订单总结 -->
        <el-col :span="8">
          <el-card class="order-summary">
            <template #header>
              <span>订单总结</span>
            </template>
            
            <!-- 商品列表 -->
            <div class="order-items">
              <div v-for="item in cartItems" :key="item.id" class="order-item">
                <div class="item-info">
                  <img :src="item.image || 'https://via.placeholder.com/60x60'" :alt="item.name">
                  <div class="item-details">
                    <h4>{{ item.name }}</h4>
                    <p>¥{{ item.price }} × {{ item.quantity }}</p>
                  </div>
                </div>
                <div class="item-total">
                  ¥{{ (item.price * item.quantity).toFixed(2) }}
                </div>
              </div>
            </div>
            
            <!-- 费用明细 -->
            <div class="cost-breakdown">
              <div class="cost-item">
                <span>商品总价:</span>
                <span>¥{{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="cost-item">
                <span>运费:</span>
                <span>¥{{ shipping.toFixed(2) }}</span>
              </div>
              <div class="cost-item total">
                <span>应付总额:</span>
                <span class="total-price">¥{{ total.toFixed(2) }}</span>
              </div>
            </div>
            
            <!-- 提交订单 -->
            <div class="submit-order">
              <el-button
                type="primary"
                size="large"
                :loading="submitting"
                @click="submitOrder"
                style="width: 100%"
              >
                提交订单
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'Checkout',
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    const authStore = useAuthStore()
    
    const cartItems = computed(() => cartStore.items)
    const subtotal = computed(() => cartStore.totalPrice)
    const shipping = ref(0)
    const total = computed(() => subtotal.value + shipping.value)
    
    const addressForm = reactive({
      receiver: '',
      phone: '',
      address: ''
    })
    
    const paymentMethod = ref('alipay')
    const orderNote = ref('')
    const submitting = ref(false)
    
    const submitOrder = async () => {
      if (!authStore.isLoggedIn) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      
      if (!addressForm.receiver || !addressForm.phone || !addressForm.address) {
        ElMessage.warning('请填写完整的收货信息')
        return
      }
      
      submitting.value = true
      
      try {
        const orderData = {
          items: cartItems.value.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price
          })),
          shipping_address: {
            receiver: addressForm.receiver,
            phone: addressForm.phone,
            address: addressForm.address
          },
          payment_method: paymentMethod.value,
          note: orderNote.value,
          total_amount: total.value
        }
        
        const response = await axios.post('/api/orders/', orderData)
        
        if (response.data) {
          ElMessage.success('订单提交成功')
          cartStore.clearCart()
          router.push(`/orders/${response.data.id}`)
        }
      } catch (error) {
        console.error('提交订单失败:', error)
        ElMessage.error('订单提交失败，请重试')
      } finally {
        submitting.value = false
      }
    }
    
    return {
      cartItems,
      subtotal,
      shipping,
      total,
      addressForm,
      paymentMethod,
      orderNote,
      submitting,
      submitOrder
    }
  }
}
</script>

<style scoped>
.checkout {
  max-width: 1200px;
  margin: 0 auto;
}

.checkout h1 {
  margin-bottom: 30px;
  color: #333;
}

.empty-cart {
  text-align: center;
  padding: 60px 0;
}

.order-info {
  margin-bottom: 20px;
}

.section {
  margin-bottom: 30px;
}

.section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
}

.order-summary {
  position: sticky;
  top: 20px;
}

.order-items {
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.item-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.item-info img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 15px;
}

.item-details h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: #333;
}

.item-details p {
  margin: 0;
  font-size: 12px;
  color: #666;
}

.item-total {
  font-weight: bold;
  color: #e60012;
}

.cost-breakdown {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.cost-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.cost-item.total {
  border-top: 1px solid #eee;
  padding-top: 10px;
  margin-top: 10px;
  font-weight: bold;
}

.total-price {
  color: #e60012;
  font-size: 18px;
}

.submit-order {
  margin-top: 20px;
}
</style> 