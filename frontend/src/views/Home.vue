<template>
  <div class="home">
    <!-- 轮播图 -->
    <el-carousel height="400px" class="banner">
      <el-carousel-item v-for="banner in banners" :key="banner.id">
        <img :src="banner.image" :alt="banner.title" class="banner-image">
        <div class="banner-content">
          <h2>{{ banner.title }}</h2>
          <p>{{ banner.description }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>
    
    <!-- 分类导航 -->
    <div class="categories">
      <el-row :gutter="20">
        <el-col :span="6" v-for="category in categories" :key="category.id">
          <div class="category-card" @click="goToCategory(category.id)">
            <div class="category-icon">
              <el-icon><component :is="category.icon" /></el-icon>
            </div>
            <div class="category-name">{{ category.name }}</div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <!-- 热门商品 -->
    <div class="section">
      <div class="section-header">
        <h2>热门商品</h2>
        <router-link to="/products" class="more-link">查看更多</router-link>
      </div>
      
      <el-row :gutter="20">
        <el-col :span="6" v-for="product in hotProducts" :key="product.id">
          <div class="product-card" @click="goToProduct(product.id)">
            <div class="product-image">
              <img :src="product.image" :alt="product.name">
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-price">¥{{ product.price }}</p>
              <el-button type="primary" size="small" @click.stop="addToCart(product)">
                加入购物车
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <!-- 新品推荐 -->
    <div class="section">
      <div class="section-header">
        <h2>新品推荐</h2>
        <router-link to="/products" class="more-link">查看更多</router-link>
      </div>
      
      <el-row :gutter="20">
        <el-col :span="6" v-for="product in newProducts" :key="product.id">
          <div class="product-card" @click="goToProduct(product.id)">
            <div class="product-image">
              <img :src="product.image" :alt="product.name">
              <div class="product-badge">新品</div>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-price">¥{{ product.price }}</p>
              <el-button type="primary" size="small" @click.stop="addToCart(product)">
                加入购物车
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { Goods, ShoppingBag, Mobile, Monitor } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    Goods,
    ShoppingBag,
    Mobile,
    Monitor
  },
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    
    const banners = ref([
      {
        id: 1,
        title: '新品上市',
        description: '最新商品等你来抢',
        image: 'https://via.placeholder.com/1200x400/ff6b6b/ffffff?text=新品上市'
      },
      {
        id: 2,
        title: '限时特价',
        description: '精选商品限时优惠',
        image: 'https://via.placeholder.com/1200x400/4ecdc4/ffffff?text=限时特价'
      },
      {
        id: 3,
        title: '品质保证',
        description: '正品保证，假一赔十',
        image: 'https://via.placeholder.com/1200x400/45b7d1/ffffff?text=品质保证'
      }
    ])
    
    const categories = ref([
      { id: 1, name: '电子产品', icon: 'Monitor' },
      { id: 2, name: '服装鞋包', icon: 'ShoppingBag' },
      { id: 3, name: '家居用品', icon: 'Goods' },
      { id: 4, name: '手机数码', icon: 'Mobile' }
    ])
    
    const hotProducts = ref([])
    const newProducts = ref([])
    
    const loadProducts = async () => {
      try {
        const response = await axios.get('/api/products/')
        const products = response.data.results || response.data
        
        // 模拟热门商品和新品
        hotProducts.value = products.slice(0, 4)
        newProducts.value = products.slice(4, 8)
      } catch (error) {
        console.error('加载商品失败:', error)
        // 使用模拟数据
        hotProducts.value = [
          { id: 1, name: 'iPhone 15', price: 5999, image: 'https://via.placeholder.com/300x300/ff6b6b/ffffff?text=iPhone' },
          { id: 2, name: 'MacBook Pro', price: 12999, image: 'https://via.placeholder.com/300x300/4ecdc4/ffffff?text=MacBook' },
          { id: 3, name: 'AirPods Pro', price: 1999, image: 'https://via.placeholder.com/300x300/45b7d1/ffffff?text=AirPods' },
          { id: 4, name: 'iPad Air', price: 4599, image: 'https://via.placeholder.com/300x300/96ceb4/ffffff?text=iPad' }
        ]
        newProducts.value = hotProducts.value
      }
    }
    
    const goToCategory = (categoryId) => {
      router.push(`/products?category=${categoryId}`)
    }
    
    const goToProduct = (productId) => {
      router.push(`/products/${productId}`)
    }
    
    const addToCart = (product) => {
      cartStore.addToCart(product)
      ElMessage.success('已添加到购物车')
    }
    
    onMounted(() => {
      loadProducts()
    })
    
    return {
      banners,
      categories,
      hotProducts,
      newProducts,
      goToCategory,
      goToProduct,
      addToCart
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.banner {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  color: white;
  padding: 20px;
}

.categories {
  margin-bottom: 40px;
}

.category-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.category-icon {
  font-size: 40px;
  color: #e60012;
  margin-bottom: 10px;
}

.category-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.more-link {
  color: #e60012;
  text-decoration: none;
  font-weight: 500;
}

.product-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: relative;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.product-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #e60012;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.product-info {
  padding: 15px;
}

.product-name {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  margin: 0 0 10px 0;
  font-size: 18px;
  font-weight: bold;
  color: #e60012;
}
</style> 