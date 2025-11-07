#!/bin/bash

# Master Database Initialization Script
# Initializes all 4 databases for Destiny Analytical System

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Database Stack Initialization                               ║"
echo "║  Destiny Analytical System                                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load .env if exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "📝 Loading configuration from .env..."
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
    echo -e "${GREEN}✅ Configuration loaded${NC}"
    echo ""
fi

# Step 1: PostgreSQL
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  1/4: PostgreSQL Setup${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -f "$SCRIPT_DIR/init_postgres.sh" ]; then
    bash "$SCRIPT_DIR/init_postgres.sh"
else
    echo -e "${RED}❌ PostgreSQL setup script not found!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ PostgreSQL setup complete${NC}"
echo ""
sleep 2

# Step 2: Docker Compose (Qdrant, Elasticsearch, Neo4j, Redis)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  2/4: Docker Services (Qdrant, Elasticsearch, Neo4j, Redis)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if docker-compose exists
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found!${NC}"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Use 'docker compose' (new) or 'docker-compose' (old)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "🐳 Starting Docker services..."
cd "$PROJECT_ROOT"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml not found!${NC}"
    exit 1
fi

# Start services
$DOCKER_COMPOSE up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check service health
echo ""
echo "🔍 Checking service health..."

# Qdrant
if curl -s http://localhost:6333/healthz &> /dev/null; then
    echo -e "  Qdrant:         ${GREEN}✅ Healthy${NC}"
else
    echo -e "  Qdrant:         ${YELLOW}⚠️  Not responding${NC}"
fi

# Elasticsearch
if curl -s http://localhost:9200/_cluster/health &> /dev/null; then
    echo -e "  Elasticsearch:  ${GREEN}✅ Healthy${NC}"
else
    echo -e "  Elasticsearch:  ${YELLOW}⚠️  Not responding (may still be starting)${NC}"
fi

# Neo4j
if curl -s http://localhost:7474 &> /dev/null; then
    echo -e "  Neo4j:          ${GREEN}✅ Healthy${NC}"
else
    echo -e "  Neo4j:          ${YELLOW}⚠️  Not responding${NC}"
fi

# Redis
if redis-cli -h localhost -p 6379 ping &> /dev/null; then
    echo -e "  Redis:          ${GREEN}✅ Healthy${NC}"
else
    echo -e "  Redis:          ${YELLOW}⚠️  Not responding${NC}"
fi

echo ""
echo -e "${GREEN}✅ Docker services started${NC}"
echo ""
sleep 2

# Step 3: Run Health Check Script
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  3/4: System Health Check${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -f "$PROJECT_ROOT/health_check.py" ]; then
    python3 "$PROJECT_ROOT/health_check.py"
else
    echo -e "${YELLOW}⚠️  Health check script not found, skipping${NC}"
fi

echo ""
sleep 2

# Step 4: Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  4/4: Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cat <<EOF
╔══════════════════════════════════════════════════════════════╗
║  ✅ Database Stack Initialization Complete!                  ║
╚══════════════════════════════════════════════════════════════╝

Database Endpoints:
  📊 PostgreSQL:      localhost:5432 (destiny_analytical)
  🔍 Qdrant:          http://localhost:6333
  📄 Elasticsearch:   http://localhost:9200
  🕸️  Neo4j:          http://localhost:7474
  💾 Redis:           localhost:6379

Web Interfaces:
  📊 Qdrant:          http://localhost:6333/dashboard
  📄 Elasticsearch:   http://localhost:9200
  🕸️  Neo4j Browser:  http://localhost:7474 (neo4j / destiny_dev_2024)

Useful Commands:
  View logs:          $DOCKER_COMPOSE logs -f
  Stop services:      $DOCKER_COMPOSE down
  Restart services:   $DOCKER_COMPOSE restart
  Check status:       $DOCKER_COMPOSE ps

Next Steps:
  1. Run integration tests: python3 tests/integration/test_end_to_end.py
  2. Try demo system:       python3 demo.py
  3. Check documentation:   cat GETTING_STARTED.md

EOF
