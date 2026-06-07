#!/bin/bash
# Daily backup of lazybones MySQL database
# Run: /etc/cron.daily/lazybones-backup

BACKUP_DIR="/var/backups/lazybones"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MYSQL_PW=$(grep MYSQL_ROOT_PASSWORD /home/hermes/oh-my-lazybones/deploy/.env | cut -d= -f2)

mkdir -p "$BACKUP_DIR"

# Dump the database
docker exec lazybones-mysql mysqldump \
  --single-transaction --quick --lock-tables=false \
  -u root -p"$MYSQL_PW" lazybones \
  > "$BACKUP_DIR/lazybones_$TIMESTAMP.sql"

# Compress
gzip "$BACKUP_DIR/lazybones_$TIMESTAMP.sql"

# Rotate: keep only last N days
find "$BACKUP_DIR" -name "lazybones_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "$(date): Backup completed. Size: $(ls -lh "$BACKUP_DIR" | tail -1 | awk '{print $5}')"

# Verify the dump is not empty
if [ ! -s "$BACKUP_DIR/lazybones_$TIMESTAMP.sql.gz" ]; then
    echo "FATAL: Backup file is empty!" >&2
    exit 1
fi
