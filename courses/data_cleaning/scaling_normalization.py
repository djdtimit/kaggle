# Databricks notebook source
import databricks.koalas as ks
import numpy as np
from scipy import stats
from mlxtend.preprocessing import minmax_scaling
import seaborn as sns
import matplotlib.pyplot as plt

# COMMAND ----------

dbutils.fs.ls('/mnt/kaggle/courses/scaling_normalization/')

# COMMAND ----------

# MAGIC %md
# MAGIC To practice scaling and normalization, we're going to use a dataset of Kickstarter campaigns. (Kickstarter is a website where people can ask people to invest in various projects and concept products.)

# COMMAND ----------

kickstarters_2017 = ks.read_csv("/mnt/kaggle/courses/scaling_normalization/ks-projects-201801.csv")


# COMMAND ----------

np.random.seed(0)

# COMMAND ----------

original_data.display()

# COMMAND ----------

original_data.to_pandas()

# COMMAND ----------

# select the usd_goal_real column
original_data = ks.DataFrame(kickstarters_2017.usd_goal_real).to_pandas()
original_data = original_data[original_data['usd_goal_real'] != 'US']

# scale the goals from 0 to 1
scaled_data = minmax_scaling(original_data, columns=['usd_goal_real'])

# plot the original & scaled data together to compare
fig, ax=plt.subplots(1,2,figsize=(15,3))
sns.distplot(original_data, ax=ax[0])
ax[0].set_title("Original Data")
sns.distplot(scaled_data, ax=ax[1])
ax[1].set_title("Scaled data")

# COMMAND ----------

print('Original data\nPreview:\n', original_data.head())
print('Minimum value:', float(original_data.min()),
      '\nMaximum value:', float(original_data.max()))
print('_'*30)

print('\nScaled data\nPreview:\n', scaled_data.head())
print('Minimum value:', float(scaled_data.min()),
      '\nMaximum value:', float(scaled_data.max()))

# COMMAND ----------

original_data['usd_goal_real'].min()

# COMMAND ----------

original_data['usd_goal_real'].val

# COMMAND ----------


