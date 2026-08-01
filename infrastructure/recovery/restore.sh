#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <backup_file.sql.gz>"
  exit 1
fi

BACKUP_FILE=$1
DB_HOST=${DB_HOST:-postgres}
DB_USER=${DB_USER:-carscope_user}
DB_NAME=${DB_NAME:-carscope}

echo "WARNING: This will overwrite the database '$DB_NAME' on host '$DB_HOST'."
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Restoring database from $BACKUP_FILE..."
    gunzip -c $BACKUP_FILE | PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME
    echo "Restore completed successfully."
else
    echo "Restore cancelled."
fi
