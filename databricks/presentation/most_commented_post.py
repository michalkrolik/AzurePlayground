# Databricks notebook source
# MAGIC %run ../config/adls_access

# COMMAND ----------

# MAGIC %run ../config/unity_catalog

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rank
from pyspark.sql.window import Window

# COMMAND ----------

df_posts = spark.read.format("delta").load(f"{path}/silver/posts")

# COMMAND ----------

df_comments = spark.read.format("delta").load(f"{path}/silver/comments")

# COMMAND ----------

windowSpec = Window.orderBy(col("post_comments").desc())

# COMMAND ----------

df_most_commented_post = df_posts.withColumn("rank", rank().over(windowSpec)).filter(col("rank") == 1).drop("rank")

# COMMAND ----------

df_comments_of_most_commented_post = df_comments.join(df_most_commented_post, df_comments["post_id"] == df_most_commented_post["id"], "inner").select ( \
    df_most_commented_post["id"].alias("post_id"), \
    df_most_commented_post["created_date"].alias("post_created_date"), \
    df_most_commented_post["media"], \
    df_most_commented_post["media_url"], \
    df_most_commented_post["video_viewers_count"], \
    df_most_commented_post["caption"].alias("post_text"), \
    df_most_commented_post["likes"].alias("post_likes"), \
    df_most_commented_post["created_date"].alias("comment_created_date"), \
    df_comments["comment_id"], \
    df_comments["author"], \
    df_comments["text"].alias("comment") \
    )

# COMMAND ----------

df_comments_of_most_commented_post.write.mode("overwrite").format("delta").save(f"{path}/gold/most_commented_post")

# COMMAND ----------

f_saveAsTable(df_comments_of_most_commented_post, "comments_of_most_commented_post", 0)
