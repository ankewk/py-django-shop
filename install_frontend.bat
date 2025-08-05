@echo off
echo ========================================
echo 安装前端依赖
echo ========================================

echo.
echo 正在进入前端目录...
cd frontend

echo.
echo 正在安装npm依赖...
npm install

echo.
echo 依赖安装完成！
echo.
echo 现在可以运行以下命令启动前端：
echo npm run dev
echo.
echo 或者运行 start_frontend_backend.bat 启动前后端服务
echo ========================================

pause 