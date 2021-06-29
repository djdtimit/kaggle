# Databricks notebook source
# MAGIC %md
# MAGIC #Competition data

# COMMAND ----------

# MAGIC %md
# MAGIC In this competition, Kagglers are challenged to generate a series of short-term signals from the book and trade data of a fixed 10-minute window to predict the realized volatility of the next 10-minute window. The target, which is given in train/test.csv, can be linked with the raw order book/trade data by the same **time_id** and **stock_id**. There is no overlap between the feature and target window.

# COMMAND ----------

import databricks.koalas as ks
import numpy as np
import plotly.express as px

# COMMAND ----------

train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/train/'

# COMMAND ----------

train = ks.read_delta(train_path)

# COMMAND ----------

train.head()

# COMMAND ----------

# MAGIC %md
# MAGIC Taking the first row of data, it implies that the realized vol of the **target bucket** for time_id 5, stock_id 0 is 0.004136. How does the book and trade data in **feature bucket** look like for us to build signals?

# COMMAND ----------


