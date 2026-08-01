#!/bin/bash
set -e

# Configuration
DB_HOST=${DB_HOST:-postgres}
DB_USER=${DB_USER:-carscope_user}
DB_NAME=${DB_NAME:-carscope}
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/db_backup_$DATE.sql.gz"

echo "Starting database backup at $DATE..."

# Ensure directory exists
mkdir -p $BACKUP_DIR

# Run pg_dump and gzip
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $BACKUP_FILE

echo "Backup completed successfully: $BACKUP_FILE"

# Upload to S3 (Uncomment and configure in production)
# aws s3 cp $BACKUP_FILE s3://carscope-backups/postgres/

# Retention Policy: Keep last 7 days locally
find $BACKUP_DIR -type f -name "*.sql.gz" -mtime +7 -delete

echo "Retention policy applied."
