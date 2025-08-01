@echo off
chcp 65001 >nul
echo 启动简化版Django商城...

REM 切换到项目根目录
cd /d "%~dp0.."

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 创建简化的settings文件
echo 创建简化配置...
copy shop\settings.py shop\settings_simple.py >nul

REM 运行数据库迁移
echo 运行数据库迁移...
python manage.py makemigrations
python manage.py migrate

REM 创建超级用户
echo 创建超级用户...
python manage.py shell -c "from django.contrib.auth.models import User; print('超级用户已创建: admin/admin123') if not User.objects.filter(username='admin').exists() else print('超级用户已存在')"

REM 收集静态文件
echo 收集静态文件...
python manage.py collectstatic --noinput

REM 启动开发服务器
echo 启动开发服务器...
echo 访问地址: http://localhost:8000
echo 管理后台: http://localhost:8000/admin

python manage.py runserver 0.0.0.0:8000

pause 