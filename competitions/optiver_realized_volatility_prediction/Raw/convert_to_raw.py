# Databricks notebook source
spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/book_test.parquet').write.partitionBy('stock_id').save('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/book_test/')

# COMMAND ----------

spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/book_train.parquet').write.partitionBy('stock_id').save('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/book_train/')

# COMMAND ----------

spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/trade_test.parquet').write.partitionBy('stock_id').save('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/trade_test/')

# COMMAND ----------

spark.read.parquet('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Ingestion/trade_train.parquet').write.partitionBy('stock_id').save('/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/trade_train/')
