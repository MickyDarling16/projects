DATABASE='sales'

# Dis-enable foreign key checks
if ! mysql -e "SET FOREIGN_KEY_CHECKS=0;" "$DATABASE"; then
    echo Database "$DATABASE" does not exist
    exit 1
fi

#  Get list of table(s) in the database
TABLES=$(mysql -Ne "SHOW TABLES;" "$DATABASE")
if [ -z "$TABLES" ]; then
    echo Database "$DATABASE" is empty
    exit 1
else
    echo Truncating tables in database "$DATABASE"...

    # Truncate table(s) found in the database
    for TABEL in $TABLES; do
        if ! mysql -e "TRUNCATE TABLE $TABEL" "$DATABASE"; then
        echo Failed to truncate table $TABEL. Terminating process
        exit 1
        fi
    done
    echo All tables in database "$DATABASE" have been truncated successfully
fi

# Re-enable foreign key checks
mysql -e "SET FOREIGN_KEY_CHECKS=1" "$DATABASE"







gzip -cd backups/backup_sales_20250818_004201.gz > ./sales_db.sql