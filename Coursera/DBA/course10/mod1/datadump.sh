DB_PASSWD="nwDmvNqVnsceBcDGiNtzeRGO"
DB_USER="root"
DB_HOST="172.21.194.101"
DB_PORT="3306"

DATABASE="sales"
TABLE="sales_data"

DSTN_NAME="sales_data.sql"

mysqldump --hostname=$DB_HOST --user=$DB_USER --port=$DB_PORT ${DB_PASSWD:+-p"$DB_PASSWD"} \
        $DATABASE $TABLE > $DSTN_NAME