mysqldump --host=172.21.143.142 --port=3306 --user=root --password sales FactSales  > sales_backup.sql

# Display tables in sales database
mysql --host=172.21.143.142 --port=3306 --user=root --password sales -e "show tables;"