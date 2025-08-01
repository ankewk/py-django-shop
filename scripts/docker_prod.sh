#!/bin/bash

# Docker生产环境运行脚本

ENVIRONMENT=${1:-prod}

if [ "$ENVIRONMENT" = "uat" ]; then
    ENV_FILE="env.uat"
    COMPOSE_FILE="docker-compose.prod.yml"
elif [ "$ENVIRONMENT" = "prod" ]; then
    ENV_FILE="env.prod"
    COMPOSE_FILE="docker-compose.prod.yml"
else
    echo "错误: 无效的环境参数. 使用 'uat' 或 'prod'"
    exit 1
fi

echo "启动Docker生产环境: $ENVIRONMENT"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未找到Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未找到Docker Compose"
    exit 1
fi

# 检查环境文件
if [ ! -f "$ENV_FILE" ]; then
    echo "错误: 环境文件 $ENV_FILE 不存在"
    exit 1
fi

# 加载环境变量
export $(cat $ENV_FILE | xargs)

# 停止现有容器
echo "停止现有容器..."
docker-compose -f $COMPOSE_FILE down

# 构建镜像
echo "构建Docker镜像..."
docker-compose -f $COMPOSE_FILE build

# 启动服务
echo "启动服务..."
docker-compose -f $COMPOSE_FILE up -d

# 等待数据库启动
echo "等待数据库启动..."
sleep 15

# 运行数据库迁移
echo "运行数据库迁移..."
docker-compose -f $COMPOSE_FILE exec web python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
docker-compose -f $COMPOSE_FILE exec web python manage.py collectstatic --noinput

echo "Docker生产环境启动完成!"
echo "环境: $ENVIRONMENT"
echo "访问地址: http://localhost"
echo "管理后台: http://localhost/admin"
echo "API文档: http://localhost/api/"
echo ""
echo "查看日志: docker-compose -f $COMPOSE_FILE logs -f"
echo "停止服务: docker-compose -f $COMPOSE_FILE down" 