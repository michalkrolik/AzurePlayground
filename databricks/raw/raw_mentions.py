# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col, explode

# COMMAND ----------

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------

df_posts = spark.read.format("delta").load(f"{path}/bronze")

# COMMAND ----------

df_mentions = df_posts.select( \
    col("results.id").alias("post_id"),
    explode("results.mentions").alias("mentions")
)

# COMMAND ----------

df_mentions.write.mode("overwrite").format("delta").option("overwriteSchema", "true").save(f"{path}/silver/mentions")

# COMMAND ----------


