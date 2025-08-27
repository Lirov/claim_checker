#!/bin/bash

echo "🚀 Deploying Claim-Checker System"
echo "=================================="

# Default values
GITHUB_REPOSITORY=${GITHUB_REPOSITORY:-"lirov/claim_checker"}
JWT_SECRET=${JWT_SECRET:-"change-me-in-production"}

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
echo "📦 Using Docker images from: ghcr.io/$GITHUB_REPOSITORY"

# Create .env file for production
cat > .env << EOF
GITHUB_REPOSITORY=$GITHUB_REPOSITORY
JWT_SECRET=$JWT_SECRET
EOF

echo "📝 Created .env file with configuration"

# Pull and start services
echo "🔨 Pulling and starting services..."
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

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
echo "🎉 Deployment complete!"
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
echo "   curl -X POST http://localhost:8080/auth/login \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"email\":\"test@example.com\",\"password\":\"password\"}'"
echo ""
echo "🛑 To stop the system:"
echo "   docker-compose -f docker-compose.prod.yml down"
echo ""
echo "📊 To view logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
