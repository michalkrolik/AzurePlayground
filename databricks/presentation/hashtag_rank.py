# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

# MAGIC %run ../config/unity_catalog

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rank
from pyspark.sql.window import Window

# COMMAND ----------

df_hashtags = spark.read.format("delta").load((f"{path}/silver/hashtags"))

# COMMAND ----------

df_hashtag_rank = df_hashtags.groupBy("hashtags").count().orderBy(col("count").desc())

# COMMAND ----------

df_hashtag_rank.write.mode("overwrite").format("delta").save(f"{path}/gold/hashtag_rank")

# COMMAND ----------

f_saveAsTable(df_hashtag_rank, "hashtag_rank", 0)

# COMMAND ----------


