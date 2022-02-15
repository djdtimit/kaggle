from pyspark.sql.functions import lit, input_file_name()
from datetime import datetime

def add_lineage(df):
    df = df.withColumn("_loadDate", lit(datetime.now())).withColumn("_source", input_file_name())
    return df