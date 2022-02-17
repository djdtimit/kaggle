# Databricks notebook source
from utils.paths import *

# COMMAND ----------

spark.sql("""CREATE SCHEMA IF NOT EXISTS hmraw""")

# COMMAND ----------

spark.sql(f"""CREATE TABLE IF NOT EXISTS  hmraw.articles (
article_id                     STRING    
, product_code                   STRING    
, prod_name                      STRING    
, product_type_no                STRING    
, product_type_name              STRING    
, product_group_name             STRING    
, graphical_appearance_no        STRING    
, graphical_appearance_name      STRING    
, colour_group_code              STRING    
, colour_group_name              STRING    
, perceived_colour_value_id      STRING    
, perceived_colour_value_name    STRING    
, perceived_colour_master_id     STRING    
, perceived_colour_master_name   STRING    
, department_no                  STRING    
, department_name                STRING    
, index_code                     STRING    
, index_name                     STRING    
, index_group_no                 STRING    
, index_group_name               STRING    
, section_no                     STRING    
, section_name                   STRING    
, garment_group_no               STRING    
, garment_group_name             STRING    
, detail_desc                    STRING    
, _loadDate                      timestamp
, _source                        STRING    
)
USING DELTA
LOCATION '{raw_path() + 'articles/'}'""")

# COMMAND ----------

spark.sql(f"""CREATE TABLE IF NOT EXISTS hmraw.customers (
customer_id             STRING
,FN                     STRING 
,Active                 STRING 
,club_member_status      STRING
,fashion_news_frequency  STRING
,age                     STRING
,postal_code             STRING
,_loadDate               TIMESTAMP
,_source                STRING
)
USING
DELTA
LOCATION '{raw_path() + 'customers/'}'""")

# COMMAND ----------

spark.sql(f"""CREATE TABLE IF NOT EXISTS hmraw.transactions (
t_dat              STRING
,customer_id        STRING    
,article_id         STRING    
,price              STRING   
,sales_channel_id   STRING    
,_loadDate          TIMESTAMP
,_source            STRING 
)
USING DELTA
LOCATION '{raw_path() + 'transactions/'}'""")

# COMMAND ----------

spark.sql(f"""CREATE TABLE IF NOT EXISTS hmraw.images 
USING DELTA
LOCATION '{raw_path() + 'images/'}'""")

# COMMAND ----------

spark.sql(f"""VACUUM delta.`{raw_path() + 'images/'}` RETAIN 24 HOURS""")
