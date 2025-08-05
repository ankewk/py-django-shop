<template>
  <div class="product-detail">
    <div v-if="loading" class="loading">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="product" class="product-content">
      <el-row :gutter="40">
        <!-- 商品图片 -->
        <el-col :span="12">
          <div class="product-images">
            <el-image
              :src="product.image || 'https://via.placeholder.com/500x500'"
              :preview-src-list="[product.image || 'https://via.placeholder.com/500x500']"
              fit="cover"
              class="main-image"
            />
          </div>
        </el-col>
        
        <!-- 商品信息 -->
        <el-col :span="12">
          <div class="product-info">
            <h1 class="product-title">{{ product.name }}</h1>
            <div class="product-category">
              分类: {{ product.category?.name || '未分类' }}
            </div>
            <div class="product-price">
              <span class="price">¥{{ product.price }}</span>
              <span class="original-price" v-if="product.original_price">
                ¥{{ product.original_price }}
              </span>
            </div>
            <div class="product-stock">
              库存: <el-tag :type="getStockType(product.stock)">{{ product.stock }} 件</el-tag>
            </div>
            <div class="product-description">
              <h3>商品描述</h3>
              <p>{{ product.description || '暂无描述' }}</p>
            </div>
            
            <!-- 购买操作 -->
            <div class="purchase-actions">
              <div class="quantity-selector">
                <span>数量:</span>
                <el-input-number
                  v-model="quantity"
                  :min="1"
                  :max="product.stock"
                  size="large"
                />
              </div>
              
              <div class="action-buttons">
                <el-button
                  type="primary"
                  size="large"
                  :disabled="product.stock <= 0"
                  @click="addToCart"
                >
                  加入购物车
                </el-button>
                <el-button
                  type="danger"
                  size="large"
                  :disabled="product.stock <= 0"
                  @click="buyNow"
                >
                  立即购买
                </el-button>
              </div>
            </div>
            
            <!-- 商品属性 -->
            <div class="product-attributes" v-if="product.attributes">
              <h3>商品属性</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item
                  v-for="(value, key) in product.attributes"
                  :key="key"
                  :label="key"
                >
                  {{ value }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- 商品详情 -->
      <div class="product-details">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="商品详情" name="details">
            <div v-html="product.details || '暂无详细信息'"></div>
          </el-tab-pane>
          <el-tab-pane label="规格参数" name="specs">
            <el-descriptions :column="2" border>
              <el-descriptions-item
                v-for="(value, key) in product.specifications || {}"
                :key="key"
                :label="key"
              >
                {{ value }}
              </el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          <el-tab-pane label="用户评价" name="reviews">
            <div class="reviews-section">
              <p>暂无用户评价</p>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
    
    <div v-else class="not-found">
      <el-empty description="商品不存在">
        <el-button type="primary" @click="$router.push('/products')">
          返回商品列表
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import axios from 'axios'

export default {
  name: 'ProductDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const cartStore = useCartStore()
    
    const product = ref(null)
    const loading = ref(true)
    const quantity = ref(1)
    const activeTab = ref('details')
    
    const loadProduct = async () => {
      try {
        const response = await axios.get(`/api/products/${route.params.id}/`)
        product.value = response.data
      } catch (error) {
        console.error('加载商品详情失败:', error)
        product.value = null
      } finally {
        loading.value = false
      }
    }
    
    const getStockType = (stock) => {
      if (stock <= 0) return 'danger'
      if (stock <= 10) return 'warning'
      return 'success'
    }
    
    const addToCart = () => {
      if (product.value) {
        const cartItem = {
          ...product.value,
          quantity: quantity.value
        }
        cartStore.addToCart(cartItem)
        ElMessage.success('已添加到购物车')
      }
    }
    
    const buyNow = () => {
      if (product.value) {
        const cartItem = {
          ...product.value,
          quantity: quantity.value
        }
        cartStore.clearCart()
        cartStore.addToCart(cartItem)
        router.push('/checkout')
      }
    }
    
    onMounted(() => {
      loadProduct()
    })
    
    return {
      product,
      loading,
      quantity,
      activeTab,
      getStockType,
      addToCart,
      buyNow
    }
  }
}
</script>

<style scoped>
.product-detail {
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  padding: 40px;
}

.product-content {
  margin-top: 20px;
}

.product-images {
  text-align: center;
}

.main-image {
  width: 100%;
  max-width: 500px;
  height: 500px;
  border-radius: 8px;
}

.product-info {
  padding: 20px;
}

.product-title {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #333;
}

.product-category {
  color: #666;
  margin-bottom: 15px;
}

.product-price {
  margin-bottom: 20px;
}

.price {
  font-size: 28px;
  font-weight: bold;
  color: #e60012;
  margin-right: 10px;
}

.original-price {
  font-size: 16px;
  color: #999;
  text-decoration: line-through;
}

.product-stock {
  margin-bottom: 20px;
  color: #666;
}

.product-description {
  margin-bottom: 30px;
}

.product-description h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.product-description p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.purchase-actions {
  margin-bottom: 30px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.product-attributes {
  margin-bottom: 30px;
}

.product-attributes h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.product-details {
  margin-top: 40px;
}

.reviews-section {
  text-align: center;
  padding: 40px;
  color: #666;
}

.not-found {
  text-align: center;
  padding: 60px 0;
}
</style> 