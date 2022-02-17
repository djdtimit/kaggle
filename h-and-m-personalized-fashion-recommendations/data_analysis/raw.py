# Databricks notebook source
# MAGIC %md
# MAGIC # H&M Personalized Fashion Recommendations

# COMMAND ----------

# MAGIC %md
# MAGIC In this competition, H&M Group invites you to develop product recommendations based on data from previous transactions, as well as from customer and product meta data. The available meta data spans from simple data, such as garment type and customer age, to text data from product descriptions, to image data from garment images.

# COMMAND ----------

# MAGIC %md
# MAGIC For this challenge you are given the purchase history of customers across time, along with supporting metadata. Your challenge is to predict what articles each customer will purchase in the 7-day period immediately after the training data ends. Customer who did not make any purchase during that time are excluded from the scoring.

# COMMAND ----------

# MAGIC %md
# MAGIC **Files**
# MAGIC - images/ - a folder of images corresponding to each article_id; images are placed in subfolders starting with the first three digits of the article_id; note, not all article_id values have a corresponding image.
# MAGIC 
# MAGIC - articles.csv - detailed metadata for each article_id available for purchase
# MAGIC 
# MAGIC - customers.csv - metadata for each customer_id in dataset
# MAGIC 
# MAGIC - sample_submission.csv - a sample submission file in the correct format
# MAGIC 
# MAGIC - transactions_train.csv - the training data, consisting of the purchases each customer for each date, as well as additional information. Duplicate rows correspond to multiple purchases of the same item. Your task is to predict the article_ids each customer will purchase during the 7-day period immediately after the training data period.
# MAGIC 
# MAGIC **NOTE**: You must make predictions for all customer_id values found in the sample submission. All customers who made purchases during the test period are scored, regardless of whether they had purchase history in the training data.

# COMMAND ----------

from utils.paths import *
import pyspark.pandas as ps

# COMMAND ----------

# MAGIC %md
# MAGIC **images**

# COMMAND ----------

df_images = ps.read_delta(raw_path() + 'images/')
df_images.head()

# COMMAND ----------

# MAGIC %md
# MAGIC => extract article_id from path

# COMMAND ----------

# MAGIC %md
# MAGIC **articles**

# COMMAND ----------

df_articles = ps.read_delta(raw_path() + 'articles/')
df_articles.head()

# COMMAND ----------

df_articles['_loadDate'] = df_articles['_loadDate'].astype('datetime64')

# COMMAND ----------

df_articles.info()

# COMMAND ----------

display(df_articles)

# COMMAND ----------

# MAGIC %md
# MAGIC **customers**

# COMMAND ----------

df_customers = ps.read_delta(raw_path() + 'customers/')
df_customers.head()

# COMMAND ----------

df_customers['age'] = df_customers['age'].astype('int')
df_customers['_loadDate'] = df_customers['_loadDate'].astype('datetime64')

# COMMAND ----------

df_customers.info()

# COMMAND ----------

display(df_customers)

# COMMAND ----------

# MAGIC %md
# MAGIC **transactions_train**

# COMMAND ----------

df_transactions = ps.read_delta(raw_path() + 'transactions/')
df_transactions.head()

# COMMAND ----------

df_transactions['t_dat'] = df_transactions['t_dat'].astype('datetime64')
df_transactions['price'] = df_transactions['price'].astype('float64')
df_transactions['_loadDate'] = df_transactions['_loadDate'].astype('datetime64')

# COMMAND ----------

df_transactions.info()

# COMMAND ----------

display(df_transactions)

# COMMAND ----------


