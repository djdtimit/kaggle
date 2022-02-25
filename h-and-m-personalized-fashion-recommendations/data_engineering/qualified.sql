-- Databricks notebook source
Create schema if not exists hmqualified

-- COMMAND ----------

CREATE VIEW IF NOT EXISTS hmqualified.articles
AS
SELECT 

hmraw.articles (
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
