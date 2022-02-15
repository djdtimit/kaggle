from pyspark.sql.functions import lit
from datetime import datetime

def add_lineage(df):
    df = df.withColumn("_loadDate", lit(datetime.now()))
    return df