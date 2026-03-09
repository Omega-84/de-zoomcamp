import pyspark
from pyspark.sql import SparkSession
from warnings import filterwarnings
filterwarnings("ignore")

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")


print(f"Spark version: {spark.version}")

df = spark.range(10)
df.show()

spark.stop()