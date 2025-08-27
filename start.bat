@echo off
echo 🚀 Starting Claim-Checker System
echo ================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available

REM Build and start services
echo 🔨 Building and starting services...
docker-compose up --build -d

echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check service health
echo 🏥 Checking service health...

REM Check gateway
curl -s http://localhost:8080/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Gateway service is running
) else (
    echo ❌ Gateway service is not responding
)

REM Check evidence service
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Evidence service is running
) else (
    echo ❌ Evidence service is not responding
)

echo.
echo 🎉 System startup complete!
echo.
echo 📋 Available endpoints:
echo    Gateway: http://localhost:8080
echo    Evidence: http://localhost:8000
echo    Database: localhost:5432
echo.
echo 📖 API Documentation:
echo    Gateway API: http://localhost:8080/docs
echo    Evidence API: http://localhost:8000/docs
echo.
echo 🧪 Test the system:
echo    python test_local.py
echo.
echo 🛑 To stop the system:
echo    docker-compose down
echo.
pause
