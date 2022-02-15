# Databricks notebook source
from utils.lineage import add_lineage
from utils.paths import *
# from utils.images import *
from pyspark.sql.functions import col

# COMMAND ----------

import io
from PIL import Image
import pandas as pd
from pyspark.sql.functions import pandas_udf


def extract_size(content):
  """Extract image size from its raw content."""
  image = Image.open(io.BytesIO(content))
  return image.size
 
@pandas_udf("width: int, height: int")
def extract_size_udf(content_series):
  sizes = content_series.apply(extract_size)
  return pd.DataFrame(list(sizes))

# COMMAND ----------

add_lineage(spark.read.csv(ingestion_path() + 'articles/', header = True)).write.save(raw_path() + 'articles/')

# COMMAND ----------

add_lineage(spark.read.csv(ingestion_path() + 'customers/', header = True)).write.save(raw_path() + 'customers/')

# COMMAND ----------

add_lineage(spark.read.csv(ingestion_path() + 'transactions/', header = True)).write.save(raw_path() + 'transactions/')

# COMMAND ----------

# add_lineage(spark.read.format("image").load(ingestion_path() + 'images/*/')).write.save(raw_path() + 'images/')

# COMMAND ----------

spark.read.format("binaryFile").load(ingestion_path() + 'images/*/').select(
  col("path"),
  extract_size_udf(col("content")).alias("size"),
  col("content")).write.save(raw_path() + 'images/')
