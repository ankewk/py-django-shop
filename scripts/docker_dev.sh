#!/bin/bash

# Docker开发环境运行脚本

echo "启动Docker开发环境..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未找到Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未找到Docker Compose"
    exit 1
fi

# 停止现有容器
echo "停止现有容器..."
docker-compose down

# 构建镜像
echo "构建Docker镜像..."
docker-compose build

# 启动服务
echo "启动服务..."
docker-compose up -d

# 等待数据库启动
echo "等待数据库启动..."
sleep 10

# 运行数据库迁移
echo "运行数据库迁移..."
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# 创建超级用户
echo "创建超级用户..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('超级用户已创建: admin/admin123')
else:
    print('超级用户已存在')
"

# 收集静态文件
echo "收集静态文件..."
docker-compose exec web python manage.py collectstatic --noinput

echo "Docker开发环境启动完成!"
echo "访问地址: http://localhost:8000"
echo "管理后台: http://localhost:8000/admin"
echo "API文档: http://localhost:8000/api/"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down" 