from operator import contains
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.functions import when

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "/home/emre/spark-3.0.1-bin-hadoop2.7/jars/postgresql-42.3.1.jar") \
    .getOrCreate()

comments = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/yemeksepetidb") \
    .option("dbtable", "restaurant_comments") \
    .option("user", "postgres") \
    .option("password", "Pa55w.rd") \
    .option("driver", "org.postgresql.Driver") \
    .load()

# comments.printSchema()


commentswordcount=comments \
          .withColumn('word',f.explode(f.split(f.col('comment'), ' '))) \
          .groupBy('restaurant_name','word') \
          .count() \
          .sort('count',ascending=False) 

commentswordcount_cswhen= commentswordcount \
          .withColumn('IsTesekkurler',when(f.column('word').contains('teşekkür'),1).otherwise(0)) \
          .withColumn('IsKotu',when(f.column('word').contains('kötü'),1).otherwise(0)) \
          .withColumn('IsMuthesem',when(f.column('word').contains('mutheşem'),1).otherwise(0)) \
          .withColumn('IsBerbat',when(f.column('word').contains('berbat'),1).otherwise(0))  \
          .withColumn('IsZehir',when(f.column('word').contains('zehir'),1).otherwise(0)) \
          .withColumn('IsAfiyet',when(f.column('word').contains('Afiyet'),1).otherwise(0)) \
          .withColumn('IsAfiyet',when(f.column('word').contains('layık'),1).otherwise(0)) 

 
commentstotalbyrest=comments \
          .groupBy('restaurant_name') \
          .count() \
          .sort('count',ascending=False) 


mode = "overwrite"
url = "jdbc:postgresql://localhost:5432/yemeksepetidb"
properties = {"user": "postgres","password": "Pa55w.rd","driver": "org.postgresql.Driver"}
table1="commentstotalbyrest"
table2="commentswordcount_cswhen"

commentstotalbyrest \
    .write \
    .jdbc(url=url, table=table1, mode=mode, properties=properties)

commentswordcount_cswhen \
    .write \
    .jdbc(url=url, table=table2, mode=mode, properties=properties)