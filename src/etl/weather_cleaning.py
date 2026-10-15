from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


# Variables meteorológicas que esperamos encontrar.
WEATHER_TYPES = ["AWND", "PRCP", "SNOW", "TMAX", "TMIN"]


def transform_weather_daily(
    df: DataFrame,
    spark: SparkSession,
    year: int = 2024,
    station_id: str = "GHCND:USW00094728"
) -> DataFrame:
    """
    Transforma observaciones NOAA de formato largo a diario.

    Parámetros
    ----------
    df : DataFrame
        Observaciones con columnas:
        station, weather_date, datatype y value.

    spark : SparkSession
        Sesión activa de Spark.

    year : int
        Año de referencia.

    station_id : str
        Identificador de la estación NOAA.

    Retorna
    -------
    DataFrame
        Una fila por día, con las variables
        meteorológicas como columnas.

    Consideraciones
    ---------------
    - No imputa valores faltantes.
    - No elimina días sin observaciones.
    - Requiere validar previamente la ausencia de
      duplicados por estación, fecha y datatype.
    """

    # --------------------------------------------------
    # 1. Seleccionar estación y año de interés
    # --------------------------------------------------

    df_filtered = df.filter(
        (F.col("station") == station_id)
        & (F.year("weather_date") == year)
        & F.col("datatype").isin(WEATHER_TYPES)
    )

    # --------------------------------------------------
    # 2. Transformar formato largo a ancho
    # --------------------------------------------------

    df_wide = (
        df_filtered
        .groupBy("weather_date")
        .pivot("datatype", WEATHER_TYPES)
        .agg(F.first("value"))
    )

    # Renombrar columnas con unidades explícitas
    df_wide = (
        df_wide
        .withColumnRenamed("AWND", "awnd_mps")
        .withColumnRenamed("PRCP", "prcp_mm")
        .withColumnRenamed("SNOW", "snow_mm")
        .withColumnRenamed("TMAX", "tmax_c")
        .withColumnRenamed("TMIN", "tmin_c")
    )

    # --------------------------------------------------
    # 3. Construir calendario completo
    # --------------------------------------------------

    # Generamos todas las fechas del año para evitar
    # perder días sin observaciones meteorológicas.

    start_date = F.to_date(F.lit(f"{year}-01-01"))
    end_date = F.to_date(F.lit(f"{year}-12-31"))

    df_calendar = (
        spark.range(1)
        .select(
            F.explode(
                F.sequence(start_date, end_date)
            ).alias("weather_date")
        )
    )

    # LEFT JOIN: conserva todas las fechas del calendario.
    df_daily = df_calendar.join(
        df_wide,
        on="weather_date",
        how="left"
    )

    # --------------------------------------------------
    # 4. Variables derivadas
    # --------------------------------------------------

    df_daily = (
        df_daily

        # Identificador de la estación
        .withColumn(
            "station",
            F.lit(station_id)
        )

        # Punto medio de temperaturas máxima y mínima.
        # No equivale necesariamente a la media diaria
        # obtenida de observaciones horarias.
        .withColumn(
            "temperature_midpoint_c",
            (
                F.col("tmax_c") + F.col("tmin_c")
            ) / 2
        )

        # Amplitud térmica diaria
        .withColumn(
            "temperature_range_c",
            F.col("tmax_c") - F.col("tmin_c")
        )

        # Indicadores meteorológicos
        .withColumn(
            "has_precipitation",
            F.col("prcp_mm") > 0
        )
        .withColumn(
            "has_snow",
            F.col("snow_mm") > 0
        )

        # Indicador explícito de viento faltante
        .withColumn(
            "flag_missing_awnd",
            F.col("awnd_mps").isNull()
        )

        # Anomalías físicas básicas
        .withColumn(
            "flag_invalid_temperature",
            F.coalesce(
                F.col("tmax_c") < F.col("tmin_c"),
                F.lit(False)
            )
        )

        .withColumn(
            "flag_negative_precipitation",
            F.coalesce(
                F.col("prcp_mm") < 0,
                F.lit(False)
            )
        )

        .withColumn(
            "flag_negative_snow",
            F.coalesce(
                F.col("snow_mm") < 0,
                F.lit(False)
            )
        )
    )

    return df_daily.orderBy("weather_date")