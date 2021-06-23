# Databricks notebook source
dbutils.fs.ls('/mnt/kaggle/courses/data_cleaning/Building_Permits.csv')

# COMMAND ----------

import databricks.koalas as ks
import numpy as np

# COMMAND ----------

# MAGIC %md
# MAGIC #Take a first look at the data

# COMMAND ----------

sf_permits = ks.read_csv('/mnt/kaggle/courses/data_cleaning/Building_Permits.csv')

# COMMAND ----------

sf_permits.head(5)

# COMMAND ----------

# MAGIC %md
# MAGIC # How many missing data points do we have?

# COMMAND ----------

missing_values_count  = sf_permits.isnull().sum()
missing_values_count

# COMMAND ----------

total_cells = np.product(sf_permits.shape)
total_missing = missing_values_count.sum()
percent_missing = (total_missing/total_cells) * 100
print(percent_missing)

# COMMAND ----------

# MAGIC %md
# MAGIC # Figure out why the data is missing

# COMMAND ----------

# MAGIC %md
# MAGIC **Is this value missing because it wasn't recorded or because it doesn't exist?**
# MAGIC 
# MAGIC If a value is missing becuase it doesn't exist (like the height of the oldest child of someone who doesn't have any children) then it doesn't make sense to try and guess what it might be. These values you probably do want to keep as NaN. On the other hand, if a value is missing because it wasn't recorded, then you can try to guess what it might have been based on the other values in that column and row. This is called imputation, and we'll learn how to do it next! :)
# MAGIC 
# MAGIC Look at the columns "Street Number Suffix" and "Zipcode" from the San Francisco Building Permits dataset. Both of these contain missing values.
# MAGIC 
# MAGIC - Which, if either, are missing because they don't exist?
# MAGIC - Which, if either, are missing because they weren't recorded?
# MAGIC 
# MAGIC => If a value in the "Street Number Suffix" column is missing, it is likely because it does not exist. If a value in the "Zipcode" column is missing, it was not recorded.

# COMMAND ----------

# MAGIC %md
# MAGIC # Drop missing values: rows

# COMMAND ----------

sf_permits.dropna()

# COMMAND ----------

# MAGIC %md
# MAGIC # Drop missing values: columns

# COMMAND ----------

sf_permits_with_na_dropped = sf_permits.dropna(axis=1)

# COMMAND ----------

sf_permits_with_na_dropped.head()

# COMMAND ----------

# MAGIC %md
# MAGIC # Fill in missing values automatically

# COMMAND ----------

sf_permits_with_na_imputed  = sf_permits.fillna(method='bfill', axis=0).fillna(0)

# COMMAND ----------

sf_permits_with_na_imputed.head()

# COMMAND ----------


