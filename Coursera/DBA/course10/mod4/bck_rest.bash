mysqldump --host=mysql --port=3306 --user=root --password sales FactSales  > sales_backup.sql

# Display tables in sales database
mysql --host=mysql --port=3306 --user=root --password sales -e "show tables;"