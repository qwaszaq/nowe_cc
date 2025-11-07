#!/bin/bash
# ============================================
# START DEVELOPMENT ENVIRONMENT
# ============================================
# Uruchamia czyste środowisko development
# Różne porty od investigation
# ============================================

set -e  # Exit on error

echo "🚀 Starting Destiny Development Environment..."
echo ""

# Check if investigation containers are running
echo "📊 Checking investigation containers..."
if docker ps | grep -q "sms-postgres"; then
    echo "   ✅ sms-postgres (5432) - running"
else
    echo "   ⚠️  sms-postgres not running"
fi

if docker ps | grep -q "sms-qdrant"; then
    echo "   ✅ sms-qdrant (6333) - running"
else
    echo "   ⚠️  sms-qdrant not running"
fi

echo ""

# Start development containers
echo "🔧 Starting development containers..."
docker-compose -f docker-compose-dev.yml up -d

echo ""
echo "⏳ Waiting for health checks..."
sleep 10

# Check status
echo ""
echo "📊 Development Environment Status:"
docker-compose -f docker-compose-dev.yml ps

echo ""
echo "✅ Development environment ready!"
echo ""
echo "Development ports:"
echo "  - PostgreSQL: 5434"
echo "  - Qdrant: 6335"
echo "  - Neo4j: 7475"
echo "  - Elasticsearch: 9201"
echo ""
echo "Investigation ports (untouched):"
echo "  - PostgreSQL: 5432, 5433"
echo "  - Qdrant: 6333"
echo "  - Neo4j: 7474"
echo "  - Elasticsearch: 9200"
echo ""
echo "🎯 Ready to develop!"
echo ""
echo "Usage:"
echo "  export ENV_FILE=.env.development"
echo "  python3 profound_test.py"
