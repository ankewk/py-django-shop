<template>
  <div class="products">
    <!-- 筛选栏 -->
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchQuery"
            placeholder="搜索商品"
            prefix-icon="Search"
            @input="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="categoryFilter" placeholder="选择分类" @change="handleFilter">
            <el-option label="全部分类" value="" />
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="sortBy" placeholder="排序方式" @change="handleSort">
            <el-option label="默认排序" value="" />
            <el-option label="价格从低到高" value="price_asc" />
            <el-option label="价格从高到低" value="price_desc" />
            <el-option label="最新上架" value="created_desc" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="clearFilter">清除</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 商品列表 -->
    <el-row :gutter="20">
      <el-col :span="6" v-for="product in products" :key="product.id">
        <div class="product-card" @click="goToProduct(product.id)">
          <div class="product-image">
            <img :src="product.image || 'https://via.placeholder.com/300x300'" :alt="product.name">
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-description">{{ product.description }}</p>
            <div class="product-price">¥{{ product.price }}</div>
            <div class="product-actions">
              <el-button type="primary" size="small" @click.stop="addToCart(product)">
                加入购物车
              </el-button>
              <el-button type="text" size="small" @click.stop="goToProduct(product.id)">
                查看详情
              </el-button>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 分页 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 48, 96]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { Search } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Products',
  components: {
    Search
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const cartStore = useCartStore()

    const products = ref([])
    const categories = ref([])
    const searchQuery = ref('')
    const categoryFilter = ref('')
    const sortBy = ref('')
    const currentPage = ref(1)
    const pageSize = ref(12)
    const total = ref(0)
    const loading = ref(false)

    const loadProducts = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchQuery.value,
          category: categoryFilter.value,
          ordering: sortBy.value
        }

        const response = await axios.get('/api/products/', { params })
        products.value = response.data.results || response.data
        total.value = response.data.count || products.value.length
      } catch (error) {
        console.error('加载商品失败:', error)
        // 使用模拟数据
        products.value = [
          { id: 1, name: 'iPhone 15', price: 5999, description: '最新款iPhone', image: 'https://via.placeholder.com/300x300/ff6b6b/ffffff?text=iPhone' },
          { id: 2, name: 'MacBook Pro', price: 12999, description: '专业级笔记本', image: 'https://via.placeholder.com/300x300/4ecdc4/ffffff?text=MacBook' },
          { id: 3, name: 'AirPods Pro', price: 1999, description: '无线降噪耳机', image: 'https://via.placeholder.com/300x300/45b7d1/ffffff?text=AirPods' },
          { id: 4, name: 'iPad Air', price: 4599, description: '轻薄平板电脑', image: 'https://via.placeholder.com/300x300/96ceb4/ffffff?text=iPad' }
        ]
        total.value = products.value.length
      } finally {
        loading.value = false
      }
    }

    const loadCategories = async () => {
      try {
        const response = await axios.get('/api/categories/')
        categories.value = response.data.results || response.data
      } catch (error) {
        console.error('加载分类失败:', error)
        categories.value = [
          { id: 1, name: '电子产品' },
          { id: 2, name: '服装鞋包' },
          { id: 3, name: '家居用品' },
          { id: 4, name: '手机数码' }
        ]
      }
    }

    const handleSearch = () => {
      currentPage.value = 1
      loadProducts()
    }

    const handleFilter = () => {
      currentPage.value = 1
      loadProducts()
    }

    const handleSort = () => {
      currentPage.value = 1
      loadProducts()
    }

    const clearFilter = () => {
      searchQuery.value = ''
      categoryFilter.value = ''
      sortBy.value = ''
      currentPage.value = 1
      loadProducts()
    }

    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
      loadProducts()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadProducts()
    }

    const goToProduct = (productId) => {
      router.push(`/products/${productId}`)
    }

    const addToCart = (product) => {
      cartStore.addToCart(product)
      ElMessage.success('已添加到购物车')
    }

    // 监听路由参数变化
    watch(() => route.query.category, (newCategory) => {
      if (newCategory) {
        categoryFilter.value = newCategory
        loadProducts()
      }
    })

    onMounted(() => {
      loadCategories()
      loadProducts()
    })

    return {
      products,
      categories,
      searchQuery,
      categoryFilter,
      sortBy,
      currentPage,
      pageSize,
      total,
      loading,
      handleSearch,
      handleFilter,
      handleSort,
      clearFilter,
      handleSizeChange,
      handleCurrentChange,
      goToProduct,
      addToCart
    }
  }
}
</script>

<style scoped>
.products {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 20px;
}

.product-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.product-image {
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.product-description {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
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

.product-actions {
  display: flex;
  gap: 10px;
}

.pagination-wrapper {
  margin-top: 30px;
  text-align: center;
}
</style> 