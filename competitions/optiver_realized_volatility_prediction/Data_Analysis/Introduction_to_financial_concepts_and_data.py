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
import pandas as pd
from pyspark.sql.functions import log, lit, col, lag
from databricks.koalas.config import set_option, reset_option

from sklearn.metrics import r2_score
from pyspark.sql.window import Window

# COMMAND ----------

train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/train/'

book_train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/book_train/stock_id=0'

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

# COMMAND ----------

stock_id = '0'
book_example = book_example[book_example['time_id']==5]
book_example.loc[:,'stock_id'] = stock_id
trade_example = trade_example[trade_example['time_id']==5]
trade_example.loc[:,'stock_id'] = stock_id

# COMMAND ----------

# MAGIC %md
# MAGIC ### book data snapshot

# COMMAND ----------

book_example.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ### trade date snapshot

# COMMAND ----------

trade_example.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Realized volatility calculation in python

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
# MAGIC ### The WAP of the stock is plotted below

# COMMAND ----------

fig = px.line(book_example.to_pandas(), x="seconds_in_bucket", y="wap", title='WAP of stock_id_0, time_id_5')
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC To compute the log return, we can simply take the logarithm of the ratio between two consecutive WAP. The first row will have an empty return as the previous book update is unknown, therefore the empty return data point will be dropped.

# COMMAND ----------

set_option("compute.ops_on_diff_frames", True)

# COMMAND ----------

book_example['log_return'] = book_example['wap'].spark.transform(lambda scol: log(scol)).diff()

# COMMAND ----------

reset_option("compute.ops_on_diff_frames")

# COMMAND ----------

book_example = book_example[~book_example['log_return'].isnull()]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Let's plot the tick-to-tick return of this instrument over this time bucket

# COMMAND ----------

fig = px.line(book_example.to_pandas(), x="seconds_in_bucket", y="log_return", title='Log return of stock_id_0, time_id_5')
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC The realized vol of stock 0 in this feature bucket, will be:

# COMMAND ----------

# realized_vol = book_example['log_return'].spark.transform(lambda scol: scol**2).sum()**(1/2)

# COMMAND ----------

realized_vol = (book_example['log_return']**2).sum()**(1/2)

# COMMAND ----------

print(f'Realized volatility for stock_id 0 on time_id 5 is {realized_vol}')

# COMMAND ----------

# MAGIC %md
# MAGIC # Naive prediction: using past realized volatility as target

# COMMAND ----------

# MAGIC %md
# MAGIC A commonly known fact about volatility is that it tends to be autocorrelated. We can use this property to implement a naive model that just "predicts" realized volatility by using whatever the realized volatility was in the initial 10 minutes.

# COMMAND ----------

train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/train/'

book_train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/book_train'
trade_train_path = '/mnt/kaggle/competitions/optiver_realized_volatility_prediction/Raw/trade_train'

# COMMAND ----------

windowSpec  = Window.partitionBy(["stock_id","time_id"]).orderBy("seconds_in_bucket")

# COMMAND ----------

df_book_data = spark.read.format('delta').load(book_train_path)
df_book_data = (df_book_data
                .withColumn('wap', (col('bid_price1') * col('ask_size1') + col('ask_price1') * col('bid_size1')) / (col('bid_size1') + col('ask_size1')) )
                .withColumn('log_wap', log(col('wap')))
                .withColumn("wap_lag",lag("wap",1).over(windowSpec))
                .withColumn("log_wap_lag",log(col('wap_lag')))
                .withColumn("log_return",col('log_wap') - col('log_wap_lag'))
                .withColumn('log_return_squared', col('log_return')**2)
               )

df_book_data = df_book_data.where(col('log_return').isNotNull())


# COMMAND ----------

df_realized_vol_per_stock = df_book_data.groupBy(['stock_id', 'time_id']).sum('log_return_squared')

# COMMAND ----------

df_realized_vol_per_stock = (df_realized_vol_per_stock
                             .withColumn('realized_volatility', col('sum(log_return_squared)')**(1/2)))

# COMMAND ----------

df_past_realized_train = (df_realized_vol_per_stock.withColumnRenamed('realized_volatility', 'pred')
                          .select('stock_id', 'time_id', 'pred'))

# COMMAND ----------

train = spark.read.format('delta').load(train_path)

# COMMAND ----------

df_joined = (df_past_realized_train.join(train, on = ['stock_id', 'time_id'], how = 'left')).toPandas()
df_joined['target'] = df_joined['target'].astype('float')

# COMMAND ----------

from sklearn.metrics import r2_score
def rmspe(y_true, y_pred):
    return  (np.sqrt(np.mean(np.square((y_true - y_pred) / y_true))))
R2 = round(r2_score(y_true = df_joined['target'], y_pred = df_joined['pred']),3)
RMSPE = round(rmspe(y_true = df_joined['target'], y_pred = df_joined['pred']),3)
print(f'Performance of the naive prediction: R2 score: {R2}, RMSPE: {RMSPE}')

# COMMAND ----------

df_joined['row_id'] = df_joined['stock_id'].astype(str) + '-' +  df_joined['time_id'].astype(str)

# COMMAND ----------

df_joined = df_joined.sort_values(by=['stock_id', 'time_id'])[['row_id','target', 'pred']]

# COMMAND ----------

df_joined

# COMMAND ----------


