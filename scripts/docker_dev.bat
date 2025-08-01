@echo off
chcp 65001 >nul
echo 启动Docker开发环境...

REM 检查Docker是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Docker，请先安装Docker Desktop
    pause
    exit /b 1
)

REM 检查Docker Compose是否安装
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Docker Compose
    pause
    exit /b 1
)

REM 切换到项目根目录
cd /d "%~dp0.."

REM 停止现有容器
echo 停止现有容器...
docker-compose down

REM 构建镜像
echo 构建Docker镜像...
docker-compose build

REM 启动服务
echo 启动服务...
docker-compose up -d

REM 等待数据库启动
echo 等待数据库启动...
timeout /t 10 /nobreak >nul

REM 运行数据库迁移
echo 运行数据库迁移...
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

REM 创建超级用户
echo 创建超级用户...
docker-compose exec web python manage.py shell -c "from django.contrib.auth.models import User; print('超级用户已创建: admin/admin123') if not User.objects.filter(username='admin').exists() else print('超级用户已存在')"

REM 收集静态文件
echo 收集静态文件...
docker-compose exec web python manage.py collectstatic --noinput

echo.
echo ========================================
echo Docker开发环境启动完成!
echo ========================================
echo 访问地址: http://localhost:8000
echo 管理后台: http://localhost:8000/admin
echo API文档: http://localhost:8000/api/
echo.
echo 常用命令:
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
echo 重启服务: docker-compose restart
echo ========================================
echo.
pause 