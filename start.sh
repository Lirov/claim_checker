#!/bin/bash

echo "🚀 Starting Claim-Checker System"
echo "================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🏥 Checking service health..."

# Check gateway
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Gateway service is running"
else
    echo "❌ Gateway service is not responding"
fi

# Check evidence service
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Evidence service is running"
else
    echo "❌ Evidence service is not responding"
fi

echo ""
echo "🎉 System startup complete!"
echo ""
echo "📋 Available endpoints:"
echo "   Gateway: http://localhost:8080"
echo "   Evidence: http://localhost:8000"
echo "   Database: localhost:5432"
echo ""
echo "📖 API Documentation:"
echo "   Gateway API: http://localhost:8080/docs"
echo "   Evidence API: http://localhost:8000/docs"
echo ""
echo "🧪 Test the system:"
echo "   python test_local.py"
echo ""
echo "🛑 To stop the system:"
echo "   docker-compose down"
