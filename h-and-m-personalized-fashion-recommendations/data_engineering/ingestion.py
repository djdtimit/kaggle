# Databricks notebook source
from utils.lineage import add_lineage
from utils.paths import *

# COMMAND ----------

add_lineage(spark.read.csv(ingestion_path() + 'articles/', header = True)).write.save(raw_path() + 'articles/')

# COMMAND ----------

add_lineage(spark.read.csv(ingestion_path() + 'customers/', header = True)).write.save(raw_path() + 'customers/')

# COMMAND ----------

add_lineage(spark.read.csv(ingestion_path() + 'transactions/', header = True)).write.save(raw_path() + 'transactions/')

# COMMAND ----------

add_lineage(spark.read.format("image").load(ingestion_path() + 'images/*/').write.save(raw_path() + 'images/')

# COMMAND ----------

# df = spark.read.format("image").load(ingestion_path() + 'images/*/')

# COMMAND ----------

# df.display()

# COMMAND ----------


