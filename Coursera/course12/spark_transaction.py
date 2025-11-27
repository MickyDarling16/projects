import findspark
findspark.init()

from pyspark.sql import SparkSession

configs = {
    "spark.executor.memory": "1g",
    "spark.driver.memory": "1g"
}

# Create a Spark session 
# Standard practice is to call .config(key, value) iteratively or chain them
builder = SparkSession.builder.appName("transactions").master("local[3]")

# Apply configurations
for key, value in configs.items():
    builder = builder.config(key, value)
    
spark = builder.getOrCreate()

# Load data 
# FIXED: Added leading slash to the WSL path to ensure absolute referencing
data = spark.read.csv("/mnt/c/Users/micha/Desktop/Book2.csv", header=True, inferSchema=True) 

# Perform operations 
# FIXED: Removed trailing whitespace from the column name "name "
result = data.groupBy("Account").agg({"Net Amount": "sum"})

# Show result 
result.show()
# Stop the Spark session
spark.stop()