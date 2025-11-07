#!/bin/bash

# PostgreSQL Initialization Script for Destiny Analytical System
# Creates user, database, and runs schema initialization

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  PostgreSQL Setup - Destiny Analytical System               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
POSTGRES_USER="${POSTGRES_USER:-destiny}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-destiny_dev_2024}"
POSTGRES_DB="${POSTGRES_DB:-destiny_analytical}"
POSTGRES_HOST="${POSTGRES_HOST:-localhost}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Configuration:"
echo "  Host: $POSTGRES_HOST"
echo "  Port: $POSTGRES_PORT"
echo "  Database: $POSTGRES_DB"
echo "  User: $POSTGRES_USER"
echo ""

# Function to run SQL as postgres superuser
run_as_superuser() {
    local sql="$1"
    echo "$sql" | psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U postgres -w
}

# Function to run SQL as destiny user
run_as_user() {
    local sql="$1"
    echo "$sql" | psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -w
}

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL connectivity..."
if ! psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U postgres -c "SELECT version();" &> /dev/null; then
    echo -e "${RED}❌ Error: Cannot connect to PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT${NC}"
    echo ""
    echo "Please ensure PostgreSQL is running and you can connect as 'postgres' user."
    echo "You may need to:"
    echo "  1. Start PostgreSQL: brew services start postgresql"
    echo "  2. Set PGPASSWORD for postgres user, or configure pg_hba.conf for trust authentication"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL is accessible${NC}"
echo ""

# Check if user already exists
echo "🔍 Checking if user '$POSTGRES_USER' exists..."
USER_EXISTS=$(psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'")

if [ "$USER_EXISTS" = "1" ]; then
    echo -e "${YELLOW}⚠️  User '$POSTGRES_USER' already exists${NC}"
    read -p "Do you want to reset the password? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Resetting password for user '$POSTGRES_USER'..."
        run_as_superuser "ALTER USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
        echo -e "${GREEN}✅ Password reset${NC}"
    fi
else
    echo "👤 Creating user '$POSTGRES_USER'..."
    run_as_superuser "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
    echo -e "${GREEN}✅ User created${NC}"
fi
echo ""

# Check if database already exists
echo "🔍 Checking if database '$POSTGRES_DB' exists..."
DB_EXISTS=$(psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")

if [ "$DB_EXISTS" = "1" ]; then
    echo -e "${YELLOW}⚠️  Database '$POSTGRES_DB' already exists${NC}"
    read -p "Do you want to drop and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Dropping database '$POSTGRES_DB'..."
        run_as_superuser "DROP DATABASE $POSTGRES_DB;"
        echo "🗄️  Creating database '$POSTGRES_DB'..."
        run_as_superuser "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"
        echo -e "${GREEN}✅ Database recreated${NC}"
    fi
else
    echo "🗄️  Creating database '$POSTGRES_DB'..."
    run_as_superuser "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"
    echo -e "${GREEN}✅ Database created${NC}"
fi
echo ""

# Grant privileges
echo "🔑 Granting privileges..."
run_as_superuser "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"
echo -e "${GREEN}✅ Privileges granted${NC}"
echo ""

# Enable pgvector extension
echo "🔌 Enabling pgvector extension..."
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS vector;" || {
    echo -e "${YELLOW}⚠️  Warning: Could not enable pgvector extension${NC}"
    echo "You may need to install it first:"
    echo "  brew install pgvector  # macOS"
    echo "  or follow instructions at: https://github.com/pgvector/pgvector"
}
echo ""

# Run schema initialization
SCHEMA_FILE="$(dirname "$0")/../sql/init/01_create_tables.sql"
if [ -f "$SCHEMA_FILE" ]; then
    echo "📋 Running schema initialization from $SCHEMA_FILE..."
    PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$SCHEMA_FILE"
    echo -e "${GREEN}✅ Schema initialized${NC}"
else
    echo -e "${YELLOW}⚠️  Schema file not found: $SCHEMA_FILE${NC}"
    echo "Skipping schema initialization."
fi
echo ""

# Verify setup
echo "🧪 Verifying setup..."
TABLES=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")
echo "  Tables created: $TABLES"

VECTOR_ENABLED=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT COUNT(*) FROM pg_extension WHERE extname='vector';")
if [ "$VECTOR_ENABLED" = "1" ]; then
    echo -e "  pgvector: ${GREEN}✅ Enabled${NC}"
else
    echo -e "  pgvector: ${RED}❌ Not enabled${NC}"
fi
echo ""

# Create .env file if it doesn't exist
ENV_FILE="$(dirname "$0")/../.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "📝 Creating .env file..."
    cat > "$ENV_FILE" <<EOF
# PostgreSQL Configuration
POSTGRES_HOST=$POSTGRES_HOST
POSTGRES_PORT=$POSTGRES_PORT
POSTGRES_DB=$POSTGRES_DB
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD

# LMStudio Configuration
LMSTUDIO_BASE_URL=http://192.168.200.226:1234/v1
LMSTUDIO_LLM_MODEL=openai/gpt-oss-20b
LMSTUDIO_EMBED_MODEL_GENERAL=text-embedding-multilingual-e5-large-instruct
LMSTUDIO_EMBED_MODEL_FINANCIAL=jina-embeddings-v4-text-retrieval

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Elasticsearch Configuration
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Neo4j Configuration
NEO4J_HOST=localhost
NEO4J_PORT=7474
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=destiny_dev_2024

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Claude API (for supervision)
# ANTHROPIC_API_KEY=your_key_here

# Feature Flags
ENABLE_CLAUDE_SUPERVISION=false
SUPERVISION_MODE=spot_check

# Logging
LOG_LEVEL=INFO
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
    echo "  Please update with your actual configuration."
else
    echo -e "${YELLOW}⚠️  .env file already exists, not overwriting${NC}"
fi
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ PostgreSQL Setup Complete!                               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Connection string:"
echo "  postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
echo ""
echo "Test connection:"
echo "  psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB"
echo ""
