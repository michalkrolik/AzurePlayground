# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col, explode, from_unixtime

# COMMAND ----------

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------

#posts_schema = StructType(fields=[
#    StructField("_rid", StringType(), False),
#    StructField("_ts", StringType(), True),
#    StructField("id", StringType(), True),
#    StructField("results", StructType(fields=[
#        StructField("id", StringType(), True),
#        StructField("date", StringType(), True),
#        StructField("media", StringType(), True),
#        StructField("media_url", StringType(), True),
#        StructField("video_viewers_count", IntegerType(), True),
#        StructField("caption", StringType(), True),
#        StructField("likes", IntegerType(), True),
#        StructField("hashtags", ArrayType(StringType()), True),
#        StructField("mentions", ArrayType(StringType()), True),
#        StructField("post_comments", IntegerType(), True),
#        StructField("comments", ArrayType(StringType()), True),
#        StructField("ingestion_date", StringType(), True)
#    ])),
#    StructField("_etag", StringType(), True),
#    StructField("__usr_opType", StringType(), True)
#])

# COMMAND ----------

df_posts = spark.read.format("delta").load(f"{path}/bronze")

# COMMAND ----------

df_posts_pre = df_posts.select( \
    col("results.id").alias("id"),
    col("results.date").alias("date"),
    col("results.media").alias("media"),
    col("results.media_url").alias("media_url"),
    col("results.video_viewers_count").alias("video_viewers_count"),
    col("results.caption").alias("caption"),
    col("results.likes").alias("likes"),
    col("results.post_comments").alias("post_comments"),
    col("results.ingestion_date").alias("ingestion_date")
)

# COMMAND ----------

df_posts = df_post_pre.withColumn(
    "created_date", from_unixtime(col("date")
))

# COMMAND ----------

df_posts_final = df_post.select(
    "id", "created_date", "media", "media_url", "video_viewers_count", "caption", "likes", "post_comments", "ingestion_date"
)

# COMMAND ----------

df_posts_final.write.mode("overwrite").format("delta").save(f"{path}/silver/posts")
