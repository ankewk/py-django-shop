@echo off
echo ========================================
echo Django商城 - 前后端分离启动脚本
echo ========================================

echo.
echo 正在启动后端服务...
echo.

REM 激活虚拟环境并启动后端
call venv\Scripts\activate
start "Django Backend" cmd /k "python manage.py runserver --settings=shop.settings_mysql"

echo 后端服务已启动在 http://127.0.0.1:8000
echo.

echo 正在启动前端服务...
echo.

REM 启动前端服务
cd frontend
start "Vue Frontend" cmd /k "npm run dev"

echo 前端服务已启动在 http://localhost:3000
echo.

echo ========================================
echo 服务启动完成！
echo ========================================
echo 后端API: http://127.0.0.1:8000
echo 前端页面: http://localhost:3000
echo 管理后台: http://127.0.0.1:8000/admin
echo API文档: http://127.0.0.1:8000/api/v1/swagger/
echo ========================================

pause 