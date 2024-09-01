# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col, explode, to_timestamp

# COMMAND ----------

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------

df_posts = spark.read.format("delta").load(f"{path}/bronze")

# COMMAND ----------

df_comments_pre = df_posts.select( \
    col("results.id").alias("id"),
    explode("results.comments").alias("comments")
)

# COMMAND ----------

df_comments = df_comments_pre.select(
    col("id").alias("post_id"),
    col("comments.comment_id").alias("comment_id"),
    col("comments.author").alias("author"),
    col("comments.date").alias("date"),
    col("comments.text").alias("text"),
    col("comments.likes").alias("likes")
).withColumn("created_date", to_timestamp("date", "yyyy-MM-dd HH:mm:ss")) \
 .drop("date")

# COMMAND ----------

df_comments.write.mode("overwrite").format("delta").option("overwriteSchema", "true").save(f"{path}/silver/comments")
