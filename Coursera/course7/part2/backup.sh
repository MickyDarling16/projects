#!/bin/sh

# backup.sh - A simple script to back up files

BACKUP_BASE_DIR="/tmp/mysqldump"
BACKUP_FILE="all-databases-backup.sql"

if mysqldump --all-databases --user="root" > all-databases-backup.sql
then 
    echo 'Backup Successful'
else
    echo 'Backup Failed'
    exit 1
fi

# Create backup folder
CURRENT_DATE=$(date +%Y%m%d)
BACKUP_DIR="${BACKUP_BASE_DIR}/${CURRENT_DATE}"

if mkdir -p $BACKUP_DIR
then
    echo "Created $BACKUP_DIR"
else
    echo "Failed to create $BACKUP_DIR"
    exit 1
fi

mv $BACKUP_FILE $BACKUP_DIR/$BACKUP_FILE