# cp-access-log.sh
# This script downloads the file 'web-server-access-log.txt.gz'
# from "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/".

# The script then extracts the .txt file using gunzip.

# The .txt file contains the timestamp, latitude, longitude 
# and visitor id apart from other data.

# Transforms the text delimeter from "#" to "," and saves to a csv file.
# Loads the data from the CSV file into the table 'access_log' in PostgreSQL database.

# Extracting phase
echo 'Extracting data'

# Load web-server-access-log.txt data into extracted-data.txt
gawk -F"#" '{print $1"#"$2"#"$3"#"$4}' web-server-access-log.txt > extracted-data.txt


# Transformation phase
echo "Transforming data"

# read the extracted data and replace the colons with commas and
# write it to a csv file
tr "#" "," < extracted-data.txt > transformed-data.csv


export PGPASSWORD=QvlycFFxRCyjMZG3hLy1WD6m;
echo "\c template1;\COPY access_log  FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=postgres


echo "SELECT * FROM access_log LIMIT 6;" | psql --username=postgres --host=postgres template1