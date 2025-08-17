DATABASE='sakila'
backupfolder=/home/theia/backups
sqlfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).sql
zipfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).gz

echo "Pulling Database: This may take a few minutes"

keep_day=0.00183888889 # Keep for 2mins

if [ mysqldump $DATABASE > $sqlfile ] # Create database backup file
then
    echo 'Sql dump (backup file) created'

    # Compress back file
    if [ gzip -c $sqlfile > $zipfile ]
    then
        echo 'The database file backup was successfully compressed'
    else
        echo 'Error: The database file backup was not compressed'
        exit 1
    fi

    # Remove the uncompressed backup file
    rm $sqlfile
else
    echo 'Error: The database file backup was not created'
    exit 1
fi

# Delete backup files older than keep_day days
find $backupfolder -mtime +$keep_day -delete