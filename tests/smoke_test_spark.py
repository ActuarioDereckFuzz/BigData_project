from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("bigdata-smoke-test")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print("\n" + "=" * 60)
    print("PRUEBA DEL ENTORNO SPARK")
    print("=" * 60)

    print(f"Spark version: {spark.version}")

    java_version = (
        spark.sparkContext
        ._jvm.java.lang.System
        .getProperty("java.version")
    )

    print(f"Java version: {java_version}")

    hadoop_version = (
        spark.sparkContext
        ._jvm.org.apache.hadoop.util.VersionInfo
        .getVersion()
    )

    print(f"Hadoop version: {hadoop_version}")

    print("\nDataFrame de prueba:")

    df = spark.range(5)

    df.show()

    assert df.count() == 5

    print("\n" + "=" * 60)
    print("PRUEBA DE ESCRITURA Y LECTURA")
    print("=" * 60)

    output_path = "/workspace/data/_smoke_test/parquet"

    df.write \
        .mode("overwrite") \
        .parquet(output_path)

    print(f"Datos escritos en: {output_path}")

    df_read = spark.read.parquet(output_path)

    print("\nDatos leídos nuevamente:")

    df_read.show()

    assert df_read.count() == 5

    print("Escritura y lectura Parquet correctas.")

    print("Prueba completada correctamente.")

    spark.stop()


if __name__ == "__main__":
    main()