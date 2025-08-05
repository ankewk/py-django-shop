# Django商城 - 前后端分离架构

## 项目结构

```
py-django-shop/
├── frontend/                 # 前端项目 (Vue 3 + Vite)
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # Pinia状态管理
│   │   ├── App.vue          # 主应用组件
│   │   └── main.js          # 应用入口
│   ├── package.json         # 前端依赖配置
│   ├── vite.config.js       # Vite构建配置
│   └── index.html           # HTML模板
├── shop/                    # Django后端项目
│   ├── settings_mysql.py    # 数据库配置
│   ├── urls.py             # URL路由
│   └── api_urls.py         # API路由
├── products/                # 商品应用
├── orders/                  # 订单应用
├── users/                   # 用户应用
└── manage.py               # Django管理脚本
```

## 技术栈

### 前端 (Frontend)
- **Vue 3** - 渐进式JavaScript框架
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理库
- **Element Plus** - Vue 3组件库
- **Axios** - HTTP客户端
- **Vite** - 构建工具

### 后端 (Backend)
- **Django 4.2** - Python Web框架
- **Django REST Framework** - API框架
- **MySQL** - 数据库
- **django-cors-headers** - CORS支持
- **drf-yasg** - Swagger API文档

## 快速开始

### 1. 启动后端服务

```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动Django开发服务器
python manage.py runserver --settings=shop.settings_mysql
```

后端服务将在 http://127.0.0.1:8000 运行

### 2. 启动前端服务

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000 运行

## API接口

### 商品相关
- `GET /api/v1/products/` - 获取商品列表
- `GET /api/v1/products/{id}/` - 获取商品详情
- `GET /api/v1/categories/` - 获取分类列表

### 订单相关
- `GET /api/v1/orders/` - 获取订单列表
- `POST /api/v1/orders/` - 创建订单
- `GET /api/v1/orders/{id}/` - 获取订单详情

### 用户认证
- `POST /api/v1/auth/login/` - 用户登录
- `POST /api/v1/auth/register/` - 用户注册
- `POST /api/v1/auth/logout/` - 用户登出

## 前端页面

### 主要页面
- `/` - 首页 (京东风格布局)
- `/products` - 商品列表
- `/products/{id}` - 商品详情
- `/cart` - 购物车
- `/checkout` - 结算页面
- `/login` - 登录页面
- `/register` - 注册页面
- `/orders` - 订单列表

### 功能特性
- ✅ 响应式设计
- ✅ 购物车功能 (本地存储)
- ✅ 用户认证
- ✅ 商品搜索和筛选
- ✅ 分页功能
- ✅ 现代化UI (Element Plus)

## 开发说明

### 前端开发
1. 所有前端代码在 `frontend/` 目录
2. 使用Vue 3 Composition API
3. 状态管理使用Pinia
4. UI组件使用Element Plus
5. 路由使用Vue Router

### 后端开发
1. Django项目在根目录
2. API接口在 `shop/api_urls.py` 中定义
3. 数据库使用MySQL
4. 支持CORS跨域请求
5. 提供Swagger API文档

### 数据流
1. 前端通过Axios调用后端API
2. 后端返回JSON数据
3. 前端使用Pinia管理状态
4. 购物车数据存储在localStorage

## 部署说明

### 前端部署
```bash
cd frontend
npm run build
# 生成的dist目录可以部署到任何静态文件服务器
```

### 后端部署
```bash
# 使用生产环境设置
python manage.py collectstatic
python manage.py migrate --settings=shop.settings_prod
```

## 注意事项

1. **CORS配置**: 后端已配置CORS允许前端域名访问
2. **API版本**: 使用 `/api/v1/` 前缀
3. **认证**: 使用JWT Token认证
4. **数据库**: 使用MySQL，需要先创建数据库
5. **静态文件**: 前端构建后的文件需要配置静态文件服务

## 开发工具

- **前端**: VS Code + Volar插件
- **后端**: PyCharm或VS Code
- **数据库**: MySQL Workbench
- **API测试**: Postman或Swagger UI

## 常见问题

### Q: 前端无法访问后端API
A: 检查CORS配置和API地址是否正确

### Q: 购物车数据丢失
A: 购物车数据存储在localStorage中，清除浏览器数据会丢失

### Q: 数据库连接失败
A: 确保MySQL服务运行，检查数据库配置

### Q: 前端热更新不工作
A: 检查Vite配置和端口设置 