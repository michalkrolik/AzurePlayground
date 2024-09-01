# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

# MAGIC %run ../config/unity_catalog

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rank
from pyspark.sql.window import Window

# COMMAND ----------

windowSpec = Window.orderBy(col("likes").desc())

# COMMAND ----------

df_posts = spark.read.format("delta").load(f"{path}/silver/posts")

# COMMAND ----------

df_most_liked_post = df_posts.withColumn("rank", rank().over(windowSpec)).filter(col("rank") == 1).drop("rank")

# COMMAND ----------

df_most_liked_post.write.mode("overwrite").format("delta").save(f"{path}/gold/most_liked_post")

# COMMAND ----------

f_saveAsTable(df_most_liked_post, "most_liked_post", 0)
