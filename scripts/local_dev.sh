#!/bin/bash

# 本地开发环境运行脚本

echo "启动本地开发环境..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 设置环境变量
export $(cat env.dev | xargs)

# 检查数据库连接
echo "检查数据库连接..."
python manage.py check --database default

# 运行数据库迁移
echo "运行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（如果不存在）
echo "检查超级用户..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('超级用户已创建: admin/admin123')
else:
    print('超级用户已存在')
"

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 启动开发服务器
echo "启动开发服务器..."
echo "访问地址: http://localhost:8000"
echo "管理后台: http://localhost:8000/admin"
echo "API文档: http://localhost:8000/api/"

python manage.py runserver 0.0.0.0:8000 