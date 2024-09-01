# Databricks notebook source
#spark.sql("CREATE DATABASE instacandf")

# COMMAND ----------

def f_saveAsTable(df, table_name, force):
    spark.sql("USE instacandf")

    if force == 1:
        df.write.mode("overwrite").saveAsTable(table_name)
        message = "The table has been created (or overwritten if it already existed)."
    else:
        df.write.saveAsTable(table_name)
        message = "The table has been created"
    
    return message

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG my_new_catalog;

# COMMAND ----------


