<template>
  <div class="orders">
    <h1>我的订单</h1>
    
    <div v-if="!isLoggedIn" class="not-logged-in">
      <el-empty description="请先登录">
        <el-button type="primary" @click="$router.push('/login')">
          去登录
        </el-button>
      </el-empty>
    </div>
    
    <div v-else>
      <!-- 订单筛选 -->
      <el-card class="filter-card">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-select v-model="statusFilter" placeholder="订单状态" @change="loadOrders">
              <el-option label="全部订单" value="" />
              <el-option label="待付款" value="pending" />
              <el-option label="已付款" value="paid" />
              <el-option label="已发货" value="shipped" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="loadOrders"
            />
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="loadOrders">筛选</el-button>
            <el-button @click="clearFilter">清除</el-button>
          </el-col>
        </el-row>
      </el-card>
      
      <!-- 订单列表 -->
      <div v-if="loading" class="loading">
        <el-skeleton :rows="5" animated />
      </div>
      
      <div v-else-if="orders.length === 0" class="empty-orders">
        <el-empty description="暂无订单">
          <el-button type="primary" @click="$router.push('/products')">
            去购物
          </el-button>
        </el-empty>
      </div>
      
      <div v-else class="orders-list">
        <el-card v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <div class="order-info">
              <span class="order-number">订单号: {{ order.order_number }}</span>
              <span class="order-date">{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="order-status">
              <el-tag :type="getStatusType(order.status)">
                {{ getStatusText(order.status) }}
              </el-tag>
            </div>
          </div>
          
          <div class="order-items">
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <img :src="item.product?.image || 'https://via.placeholder.com/80x80'" :alt="item.product?.name">
              <div class="item-info">
                <h4>{{ item.product?.name }}</h4>
                <p>¥{{ item.price }} × {{ item.quantity }}</p>
              </div>
              <div class="item-total">
                ¥{{ (item.price * item.quantity).toFixed(2) }}
              </div>
            </div>
          </div>
          
          <div class="order-footer">
            <div class="order-total">
              总计: <span class="total-price">¥{{ order.total_amount }}</span>
            </div>
            <div class="order-actions">
              <el-button size="small" @click="viewOrderDetail(order.id)">
                查看详情
              </el-button>
              <el-button
                v-if="order.status === 'pending'"
                type="primary"
                size="small"
                @click="payOrder(order.id)"
              >
                立即付款
              </el-button>
              <el-button
                v-if="order.status === 'shipped'"
                type="success"
                size="small"
                @click="confirmReceived(order.id)"
              >
                确认收货
              </el-button>
              <el-button
                v-if="order.status === 'pending'"
                type="danger"
                size="small"
                @click="cancelOrder(order.id)"
              >
                取消订单
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
      
      <!-- 分页 -->
      <div v-if="total > 0" class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'Orders',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const orders = ref([])
    const loading = ref(false)
    const statusFilter = ref('')
    const dateRange = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    
    const isLoggedIn = computed(() => authStore.isLoggedIn)
    
    const loadOrders = async () => {
      if (!isLoggedIn.value) return
      
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          status: statusFilter.value
        }
        
        if (dateRange.value && dateRange.value.length === 2) {
          params.start_date = dateRange.value[0]
          params.end_date = dateRange.value[1]
        }
        
        const response = await axios.get('/api/orders/', { params })
        orders.value = response.data.results || response.data
        total.value = response.data.count || orders.value.length
      } catch (error) {
        console.error('加载订单失败:', error)
        ElMessage.error('加载订单失败')
      } finally {
        loading.value = false
      }
    }
    
    const clearFilter = () => {
      statusFilter.value = ''
      dateRange.value = []
      currentPage.value = 1
      loadOrders()
    }
    
    const getStatusType = (status) => {
      const statusMap = {
        pending: 'warning',
        paid: 'primary',
        shipped: 'info',
        completed: 'success',
        cancelled: 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        pending: '待付款',
        paid: '已付款',
        shipped: '已发货',
        completed: '已完成',
        cancelled: '已取消'
      }
      return statusMap[status] || '未知'
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }
    
    const viewOrderDetail = (orderId) => {
      router.push(`/orders/${orderId}`)
    }
    
    const payOrder = (orderId) => {
      ElMessage.info('支付功能开发中...')
    }
    
    const confirmReceived = async (orderId) => {
      try {
        await axios.patch(`/api/orders/${orderId}/`, { status: 'completed' })
        ElMessage.success('确认收货成功')
        loadOrders()
      } catch (error) {
        ElMessage.error('确认收货失败')
      }
    }
    
    const cancelOrder = async (orderId) => {
      try {
        await axios.patch(`/api/orders/${orderId}/`, { status: 'cancelled' })
        ElMessage.success('取消订单成功')
        loadOrders()
      } catch (error) {
        ElMessage.error('取消订单失败')
      }
    }
    
    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
      loadOrders()
    }
    
    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadOrders()
    }
    
    onMounted(() => {
      if (isLoggedIn.value) {
        loadOrders()
      }
    })
    
    return {
      orders,
      loading,
      statusFilter,
      dateRange,
      currentPage,
      pageSize,
      total,
      isLoggedIn,
      loadOrders,
      clearFilter,
      getStatusType,
      getStatusText,
      formatDate,
      viewOrderDetail,
      payOrder,
      confirmReceived,
      cancelOrder,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.orders {
  max-width: 1200px;
  margin: 0 auto;
}

.orders h1 {
  margin-bottom: 30px;
  color: #333;
}

.not-logged-in {
  text-align: center;
  padding: 60px 0;
}

.filter-card {
  margin-bottom: 20px;
}

.loading {
  padding: 40px;
}

.empty-orders {
  text-align: center;
  padding: 60px 0;
}

.order-card {
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.order-number {
  font-weight: bold;
  color: #333;
}

.order-date {
  font-size: 12px;
  color: #666;
}

.order-items {
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f5f5f5;
}

.order-item:last-child {
  border-bottom: none;
}

.order-item img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 15px;
}

.item-info {
  flex: 1;
}

.item-info h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: #333;
}

.item-info p {
  margin: 0;
  font-size: 12px;
  color: #666;
}

.item-total {
  font-weight: bold;
  color: #e60012;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.order-total {
  font-size: 16px;
  color: #333;
}

.total-price {
  font-weight: bold;
  color: #e60012;
  font-size: 18px;
}

.order-actions {
  display: flex;
  gap: 10px;
}

.pagination-wrapper {
  margin-top: 30px;
  text-align: center;
}
</style> 