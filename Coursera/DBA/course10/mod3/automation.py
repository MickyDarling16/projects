# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to DB2
import ibm_db

# Connect to MySQL
connection = mysql.connector.connect(user='root', password='zdzYMFpcp9x77L76DAGVBJaA',host='172.21.81.100',database='sales')

# create cursor

cursor = connection.cursor()

# Connect to DB2
# connectction details
dsn_hostname = "" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = ""
dsn_pwd = ""      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = ""                # e.g. "50000" 
dsn_database = ""            # i.e. "BLUDB"
dsn_driver = "" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = ""            # i.e. "TCPIP"
dsn_security = ""              # i.e. "SSL"

#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)
#  Create connection
conn = ibm_db.connect(dsn, "", "")


# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
	SQL = """
		SELECT
			rowid
		FROM sales_data
		ORDER BY rowid DESC
		LIMIT 1
	"""

	stmt = ibm_db.exec_immediate(conn, SQL)
	tuple = ibm_db.fetch_tuple(stmt)
	if tuple != False:
		return tuple[0]
	

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
	SQL = """
		SELECT
			*
		FROM sales_data
		WHERE rowid > %s
	"""
	cursor.execute(SQL, (rowid,))
	records = cursor.fetchall()
	if records:
		print(records[-1])
		return records

	

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
	SQL = """
		INSERT INTO sales_data(rowid,product_id,customer_id,quantity) VALUES(?,?,?,?,?,?)
	"""
	stmt = ibm_db.prepare(conn, SQL)
	for record in records:
		ibm_db.execute(stmt, record)


insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()
# disconnect from DB2 data warehouse 
ibm_db.close(conn)

# End of program