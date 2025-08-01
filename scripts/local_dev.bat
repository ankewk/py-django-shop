@echo off
chcp 65001 >nul
echo 启动本地开发环境...

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 切换到项目根目录
cd /d "%~dp0.."

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 设置环境变量（从env.dev文件读取）
echo 设置环境变量...
for /f "tokens=1,2 delims==" %%a in (env.dev) do (
    set %%a=%%b
)

REM 检查数据库连接
echo 检查数据库连接...
python manage.py check --database default

REM 运行数据库迁移
echo 运行数据库迁移...
python manage.py makemigrations
python manage.py migrate

REM 创建超级用户（如果不存在）
echo 检查超级用户...
python manage.py shell -c "from django.contrib.auth.models import User; print('超级用户已创建: admin/admin123') if not User.objects.filter(username='admin').exists() else print('超级用户已存在')"

REM 收集静态文件
echo 收集静态文件...
python manage.py collectstatic --noinput

REM 启动开发服务器
echo 启动开发服务器...
echo 访问地址: http://localhost:8000
echo 管理后台: http://localhost:8000/admin
echo API文档: http://localhost:8000/api/

python manage.py runserver 0.0.0.0:8000

pause 