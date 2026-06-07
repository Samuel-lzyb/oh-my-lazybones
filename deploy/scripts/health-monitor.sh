#!/bin/bash
# Health check monitor — run every 5 minutes via cron
# Reports failures to Hermes for notification

set -e

LOG="/var/log/lazybones-monitor.log"
REPORT=""

# 1. API health
if ! curl -sf -o /dev/null -m 5 http://127.0.0.1:8000/api/v1/health; then
    REPORT+="[CRIT] API health check FAILED\n"
fi

# 2. MySQL
if ! docker exec lazybones-mysql mysqladmin ping -h localhost --silent 2>/dev/null; then
    REPORT+="[CRIT] MySQL ping FAILED\n"
fi

# 3. Meilisearch
if ! curl -sf -o /dev/null -m 3 http://127.0.0.1:7700/health; then
    REPORT+="[WARN] Meilisearch health check FAILED\n"
fi

# 4. Disk space (< 10% free)
DISK_PCT=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_PCT" -gt 90 ]; then
    REPORT+="[CRIT] Disk usage at ${DISK_PCT}%\n"
fi

# 5. Memory (< 256MB free)
MEM_FREE=$(free -m | awk 'NR==2 {print $7}')
if [ "$MEM_FREE" -lt 256 ]; then
    REPORT+="[WARN] Memory free: ${MEM_FREE}MB\n"
fi

# Report only on failures
if [ -n "$REPORT" ]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] HEALTH CHECK FAILED:" | tee -a "$LOG"
    echo -e "$REPORT" | tee -a "$LOG"
    exit 1
fi
