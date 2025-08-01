# Django 商城项目

一个基于Django的现代化电商平台，支持商品管理、订单处理、用户系统等功能。

## 功能特性

- 🛍️ 商品管理：分类、商品、图片管理
- 📦 订单系统：订单创建、状态管理、支付流程
- 👤 用户系统：注册、登录、个人资料管理
- 🔐 权限控制：基于Token的API认证
- 📱 RESTful API：完整的API接口
- 🐳 Docker支持：本地开发和生产环境部署
- 🌍 多环境配置：开发、UAT、生产环境

## 技术栈

- **后端框架**: Django 4.2.7
- **API框架**: Django REST Framework
- **数据库**: PostgreSQL
- **缓存**: Redis
- **任务队列**: Celery
- **Web服务器**: Gunicorn + Nginx
- **容器化**: Docker + Docker Compose

## 项目结构

```
py-django-shop/
├── shop/                 # Django项目配置
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 主URL配置
│   └── wsgi.py          # WSGI配置
├── products/            # 商品应用
│   ├── models.py        # 商品数据模型
│   ├── views.py         # 商品视图
│   ├── serializers.py   # 序列化器
│   └── urls.py          # URL配置
├── orders/              # 订单应用
│   ├── models.py        # 订单数据模型
│   ├── views.py         # 订单视图
│   ├── serializers.py   # 序列化器
│   └── urls.py          # URL配置
├── users/               # 用户应用
│   ├── views.py         # 用户视图
│   ├── serializers.py   # 序列化器
│   └── urls.py          # URL配置
├── scripts/             # 运行脚本
│   ├── local_dev.sh     # 本地开发脚本
│   ├── docker_dev.sh    # Docker开发脚本
│   └── docker_prod.sh   # Docker生产脚本
├── env.dev              # 开发环境配置
├── env.uat              # UAT环境配置
├── env.prod             # 生产环境配置
├── docker-compose.yml   # Docker开发配置
├── docker-compose.prod.yml # Docker生产配置
├── Dockerfile           # Docker镜像构建
├── nginx.conf           # Nginx配置
└── requirements.txt     # Python依赖
```

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (可选)

### 本地开发

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd py-django-shop
   ```

2. **运行本地开发环境**
   ```bash
   # 使用脚本（推荐）
   chmod +x scripts/local_dev.sh
   ./scripts/local_dev.sh
   
   # 或手动运行
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   export $(cat env.dev | xargs)
   python manage.py migrate
   python manage.py runserver
   ```

3. **访问应用**
   - 主页: http://localhost:8000
   - 管理后台: http://localhost:8000/admin
   - API文档: http://localhost:8000/api/

### Docker 开发环境

1. **启动Docker开发环境**
   ```bash
   chmod +x scripts/docker_dev.sh
   ./scripts/docker_dev.sh
   ```

2. **访问应用**
   - 主页: http://localhost:8000
   - 管理后台: http://localhost:8000/admin

### Docker 生产环境

1. **启动UAT环境**
   ```bash
   chmod +x scripts/docker_prod.sh
   ./scripts/docker_prod.sh uat
   ```

2. **启动生产环境**
   ```bash
   ./scripts/docker_prod.sh prod
   ```

## API 接口

### 认证接口
- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `GET /api/auth/profile/` - 获取用户信息
- `PUT /api/auth/profile/update/` - 更新用户信息

### 商品接口
- `GET /api/categories/` - 获取商品分类
- `GET /api/products/` - 获取商品列表
- `GET /api/products/{id}/` - 获取商品详情
- `GET /api/products/featured/` - 获取推荐商品
- `GET /api/products/by_category/` - 按分类获取商品

### 订单接口
- `GET /api/orders/` - 获取订单列表
- `POST /api/orders/` - 创建订单
- `GET /api/orders/{id}/` - 获取订单详情
- `POST /api/orders/{id}/pay/` - 支付订单
- `POST /api/orders/{id}/cancel/` - 取消订单

## 环境配置

### 开发环境 (env.dev)
- DEBUG=True
- 本地数据库和Redis
- 开发服务器

### UAT环境 (env.uat)
- DEBUG=False
- UAT数据库和Redis
- 生产配置

### 生产环境 (env.prod)
- DEBUG=False
- 生产数据库和Redis
- 完整生产配置

## 管理后台

访问 http://localhost:8000/admin 使用以下账号登录：
- 用户名: admin
- 密码: admin123

## 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

## 静态文件

```bash
# 收集静态文件
python manage.py collectstatic

# 或使用Docker
docker-compose exec web python manage.py collectstatic
```

## 常用命令

### 本地开发
```bash
# 启动开发服务器
python manage.py runserver

# 运行测试
python manage.py test

# 创建迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### Docker 命令
```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重建镜像
docker-compose build --no-cache

# 进入容器
docker-compose exec web bash
```

## 部署说明

### 生产环境部署

1. **配置环境变量**
   - 复制 `env.prod` 并根据实际情况修改
   - 设置安全的 `SECRET_KEY`
   - 配置数据库连接信息

2. **使用Docker部署**
   ```bash
   ./scripts/docker_prod.sh prod
   ```

3. **配置域名和SSL**
   - 修改 `nginx.conf` 中的域名配置
   - 配置SSL证书

### 性能优化

- 启用Redis缓存
- 配置CDN加速静态文件
- 使用数据库连接池
- 启用Gzip压缩

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。 