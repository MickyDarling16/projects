 #!/bin/bash

DATABASE='sales'
BACKUP_DIR=/home/theia/backups
RETENTION_DAYS=10

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE=backup_sales_${TIMESTAMP}.gz
TEMP_SQL_FILE=${BACKUP_DIR}/temp_sales_${TIMESTAMP}.sql

# Create backup directory if it doesn't exist
if ! mkdir -p $BACKUP_DIR; then
    echo Error: Failed to create backup directory $BACKUP_DIR
    exit 1
fi

# Check if database exists
if ! mysql -e USE $DATABASE 2>/dev/null; then
    echo Error: Database '$DATABASE' does not exist
    exit 1
fi

# Create database backup
if mysqldump $DATABASE > $TEMP_SQL_FILE; then
    echo Database dump created successfully
    
    # Compress the backup
    if gzip -c $TEMP_SQL_FILE > ${BACKUP_DIR}/${BACKUP_FILE}; then
        echo Backup compressed successfully: $BACKUP_FILE
        rm $TEMP_SQL_FILE
    else
        echo Error: Failed to compress backup
        rm $TEMP_SQL_FILE
        exit 1
    fi
else
    echo Error: Failed to create database backup
    exit 1
fi

# Clean up old backups (older than retention period)
echo Cleaning up backups older than $RETENTION_DAYS days...
find $BACKUP_DIR -name backup_sales_*.gz -mtime +$RETENTION_DAYS -delete











* * * * * /home/project/backup_automation.sh
# Start the cron service
if systemctl is-active cron >/dev/null 2>&1; then
    echo Cron service is already running
else
    if sudo service cron start; then
        echo Cron service started successfully
    else
        echo Error: Failed to start cron service
        exit 1
    fi
fi
# Wait for 3 minutes
sleep 180

# Print contents of backup directory
echo Contents of $BACKUP_DIR:
ls -l $BACKUP_DIR