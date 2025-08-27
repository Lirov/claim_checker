@echo off
echo 🚀 Deploying Claim-Checker System
echo ==================================

REM Default values
set GITHUB_REPOSITORY_OWNER=%GITHUB_REPOSITORY_OWNER%
if "%GITHUB_REPOSITORY_OWNER%"=="" set GITHUB_REPOSITORY_OWNER=yourusername

set JWT_SECRET=%JWT_SECRET%
if "%JWT_SECRET%"=="" set JWT_SECRET=change-me-in-production

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
echo 📦 Using Docker images from: ghcr.io/%GITHUB_REPOSITORY_OWNER%

REM Create .env file for production
echo GITHUB_REPOSITORY_OWNER=%GITHUB_REPOSITORY_OWNER% > .env
echo JWT_SECRET=%JWT_SECRET% >> .env

echo 📝 Created .env file with configuration

REM Pull and start services
echo 🔨 Pulling and starting services...
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

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
echo 🎉 Deployment complete!
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
echo    curl -X POST http://localhost:8080/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password\"}"
echo.
echo 🛑 To stop the system:
echo    docker-compose -f docker-compose.prod.yml down
echo.
echo 📊 To view logs:
echo    docker-compose -f docker-compose.prod.yml logs -f
echo.
pause
