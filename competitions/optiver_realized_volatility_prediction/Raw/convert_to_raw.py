# Databricks notebook source
dbutils.fs.ls('mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/')

# COMMAND ----------

df_book_test = spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/book_test.parquet')

# COMMAND ----------

df_book_train = spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/book_train.parquet')

# COMMAND ----------

df_trade_test = spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/trade_test.parquet')

# COMMAND ----------

df_trade_train = spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/trade_train.parquet')

# COMMAND ----------


