# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

# MAGIC %run ../config/unity_catalog

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rank
from pyspark.sql.window import Window

# COMMAND ----------

df_mentions = spark.read.format("delta").load(f"{path}/silver/mentions")

# COMMAND ----------

df_mention_rank = df_mentions.groupBy("mentions").count().orderBy(col("count").desc())

# COMMAND ----------

df_mention_rank.write.mode("overwrite").format("delta").save(f"{path}/gold/mention_rank")

# COMMAND ----------

f_saveAsTable(df_mention_rank, "mention_rank", 0)

# COMMAND ----------


