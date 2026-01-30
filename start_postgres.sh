#!/bin/bash

echo "🐘 Starting PostgreSQL Docker container..."

# Stop any existing container
docker stop wealthy_postgres 2>/dev/null || true
docker rm wealthy_postgres 2>/dev/null || true

# Start fresh container
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if it's running
if docker ps | grep -q wealthy_postgres; then
    echo "✅ PostgreSQL is running on port 5433"
    echo ""
    echo "Connection details:"
    echo "  Host: localhost"
    echo "  Port: 5433"
    echo "  User: postgres"
    echo "  Password: postgres"
    echo "  Database: wealthy_dashboard"
    echo ""
    echo "Test connection:"
    echo "  docker exec -it wealthy_postgres psql -U postgres -d wealthy_dashboard"
else
    echo "❌ Failed to start PostgreSQL"
    docker-compose logs
fi
