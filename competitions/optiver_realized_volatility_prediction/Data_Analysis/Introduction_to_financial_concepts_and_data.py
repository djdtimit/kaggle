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

book_train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/book_train/'

trade_train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/trade_train/stock_id=0'

# COMMAND ----------

train = ks.read_delta(train_path)

# COMMAND ----------

train.head()

# COMMAND ----------

# MAGIC %md
# MAGIC Taking the first row of data, it implies that the realized vol of the **target bucket** for time_id 5, stock_id 0 is 0.004136. How does the book and trade data in **feature bucket** look like for us to build signals?

# COMMAND ----------

book_example = ks.read_delta(book_train_path)
trade_example =  ks.read_delta(trade_train_path)
stock_id = '0'
book_example = book_example[book_example['time_id']==5]
book_example.loc[:,'stock_id'] = stock_id
trade_example = trade_example[trade_example['time_id']==5]
trade_example.loc[:,'stock_id'] = stock_id

# COMMAND ----------

# MAGIC %md
# MAGIC ### book data snapshot

# COMMAND ----------

book_example.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### trade date snapshot

# COMMAND ----------

trade_example.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Realized volatility calculation in python

# COMMAND ----------

# MAGIC %md
# MAGIC In this competition, our target is to predict short-term realized volatility. Although the order book and trade data for the target cannot be shared, we can still present the realized volatility calculation using the feature data we provided.
# MAGIC 
# MAGIC As realized volatility is a statistical measure of price changes on a given stock, to calculate the price change we first need to have a stock valuation at the fixed interval (1 second). We will use weighted averaged price, or WAP, of the order book data we provided.

# COMMAND ----------

book_example['wap'] = (book_example['bid_price1'] * book_example['ask_size1'] +
                                book_example['ask_price1'] * book_example['bid_size1']) / (
                                       book_example['bid_size1']+ book_example['ask_size1'])

# COMMAND ----------

# MAGIC %md
# MAGIC The WAP of the stock is plotted below

# COMMAND ----------

fig = px.line(book_example.to_pandas(), x="seconds_in_bucket", y="wap", title='WAP of stock_id_0, time_id_5')
fig.show()

# COMMAND ----------


