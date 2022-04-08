# pkg_list=com.databricks:spark-avro_2.11:4.0.0,org.apache.hadoop:hadoop-aws:2.7.1
# pyspark --packages $pkg_list --executor-memory 39g --num-executors 29 --executor-cores 5 --conf "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version=2"
import pyspark.sql.functions as F
import sys
from pyspark.sql import SparkSession

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
spark = SparkSession.builder.appName("Optmyzy").getOrCreate()
df = spark.read.json('Data_path')
df.printSchema()
# root
#  |-- annotations: array (nullable = true)
#  |    |-- element: struct (containsNull = true)
#  |    |    |-- offset: long (nullable = true)
#  |    |    |-- surface_form: string (nullable = true)
#  |    |    |-- uri: string (nullable = true)
#  |-- categories: array (nullable = true)
#  |    |-- element: string (containsNull = true)
#  |-- id: long (nullable = true)
#  |-- infobox_types: array (nullable = true)
#  |    |-- element: string (containsNull = true)
#  |-- text: string (nullable = true)
#  |-- url: string (nullable = true)


df1=df.select('annotations')
df1.printSchema()
# root
#  |-- annotations: array (nullable = true)
#  |    |-- element: struct (containsNull = true)
#  |    |    |-- offset: long (nullable = true)
#  |    |    |-- surface_form: string (nullable = true)
#  |    |    |-- uri: string (nullable = true)

df1=df.select('annotations',F.explode('annotations')).alias('opt')
df1.printSchema()
# root
#  |-- annotations: array (nullable = true)
#  |    |-- element: struct (containsNull = true)
#  |    |    |-- offset: long (nullable = true)
#  |    |    |-- surface_form: string (nullable = true)
#  |    |    |-- uri: string (nullable = true)
#  |-- opt: struct (nullable = true)
#  |    |-- offset: long (nullable = true)
#  |    |-- surface_form: string (nullable = true)
#  |    |-- uri: string (nullable = true)

df2 = df1.select('opt.surface_form', 'opt.uri')
df2.printSchema()
# root
#  |-- surface_form: string (nullable = true)

df3=df2.groupBy('surface_form','uri').count()
df3.show()
# +--------------------+--------------------+-----+
# |        surface_form|                 uri|count|
# +--------------------+--------------------+-----+
# |       Clark Gillies|       Clark_Gillies|    2|
# |       Randy Carlyle|       Randy_Carlyle|    1|
# |    Balkan Peninsula|    Balkan_Peninsula|    8|
# |       Enlightenment|Age_of_Enlightenment|   22|
# |           Ro Khanna|           Ro_Khanna|    3|
# |          Adam McKay|          Adam_McKay|    7|
# |   2020 primary race|2020_Democratic_P...|    1|
# |     Great Awakening|     Great_Awakening|    2|
# |      Moral Majority|      Moral_Majority|    1|
# |                pact|                Pact|    4|
# |        insular area|        Insular_area|    1|
# |institution of sl...|Slavery_in_the_Un...|    1|
# |             tornado|             Tornado|   79|
# |United States Con...|United_States_Con...|  144|
# |                Neil|         Neil_Reagan|    1|
# |       welfare queen|       Welfare_queen|    2|
# |         institution|         Institution|   64|
# |             cholera|             Cholera|   41|
# |4th (Aoba) Infant...|     Aoba_Detachment|    1|
# | William Halsey, Jr.|William_Halsey%2C...|    1|
# +--------------------+--------------------+-----+

path = 'your_path'
df3.coalesce(1).write.csv(path + "output", mode='overwrite', header=True)