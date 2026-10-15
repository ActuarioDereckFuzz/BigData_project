from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def prepare_taxi_data(df: DataFrame) -> DataFrame:
    """
    Prepara los registros de NYC Taxi para su validación.

    Operaciones:
    1. Genera variables temporales.
    2. Calcula la duración de los viajes.
    3. Identifica viajes Flex Fare.
    4. Construye indicadores de calidad.
    5. Define elegibilidad analítica preliminar.

    No elimina registros ni imputa valores faltantes.

    Parameters
    ----------
    df : DataFrame
        Datos originales de NYC Taxi, incluyendo source_month.

    Returns
    -------
    DataFrame
        Datos enriquecidos con indicadores y variables derivadas.
    """

    # --------------------------------------------------
    # 1. Variables temporales
    # --------------------------------------------------

    df = (
        df
        .withColumn(
            "pickup_date",
            F.to_date("tpep_pickup_datetime")
        )
        .withColumn(
            "pickup_month",
            F.date_format("pickup_date", "yyyy-MM")
        )
        .withColumn(
            "pickup_hour",
            F.hour("tpep_pickup_datetime")
        )
        .withColumn(
            "pickup_dayofweek",
            F.dayofweek("pickup_date")
        )
        .withColumn(
            "is_weekend",
            F.dayofweek("pickup_date").isin(1, 7)
        )
    )

    # --------------------------------------------------
    # 2. Duración y modalidad del viaje
    # --------------------------------------------------

    df = (
        df
        .withColumn(
            "duration_seconds",
            F.unix_timestamp("tpep_dropoff_datetime")
            - F.unix_timestamp("tpep_pickup_datetime")
        )
        .withColumn(
            "is_flex_fare",
            F.coalesce(
                F.col("payment_type") == 0,
                F.lit(False)
            )
        )
    )

    # --------------------------------------------------
    # 3. Indicadores de calidad
    # --------------------------------------------------

    df = (
        df
        .withColumn(
            "flag_out_of_year",
            F.col("pickup_date").isNull()
            | (F.year("pickup_date") != 2024)
        )
        .withColumn(
            "flag_month_mismatch",
            ~F.col("pickup_month").eqNullSafe(
                F.col("source_month")
            )
        )
        .withColumn(
            "flag_invalid_duration",
            F.col("duration_seconds").isNull()
            | (F.col("duration_seconds") <= 0)
        )
        .withColumn(
            "flag_zero_distance",
            F.coalesce(
                F.col("trip_distance") == 0,
                F.lit(False)
            )
        )
        .withColumn(
            "flag_missing_or_negative_distance",
            F.col("trip_distance").isNull()
            | F.isnan("trip_distance")
            | (F.col("trip_distance") < 0)
        )
        .withColumn(
            "flag_missing_location",
            F.col("PULocationID").isNull()
            | F.col("DOLocationID").isNull()
        )
        .withColumn(
            "flag_nonpositive_location_id",
            (F.col("PULocationID") <= 0)
            | (F.col("DOLocationID") <= 0)
        )
    )

    # --------------------------------------------------
    # 4. Elegibilidad analítica
    # --------------------------------------------------

    df = (
        df
        .withColumn(
            "is_eligible_for_daily_volume",
            ~F.col("flag_out_of_year")
        )
        .withColumn(
            "is_candidate_mobility",
            (~F.col("flag_out_of_year"))
            & (~F.col("flag_invalid_duration"))
            & (~F.col("flag_missing_or_negative_distance"))
            & (F.col("trip_distance") > 0)
            & (~F.col("flag_missing_location"))
        )
    )

    return df


def filter_taxi_2024(df: DataFrame) -> DataFrame:
    """
    Genera el dataset Silver para el periodo 2024.

    Conserva los registros cuya fecha de inicio pertenece
    a 2024 y mantiene los indicadores de calidad.
    """

    return df.filter(
        ~F.col("flag_out_of_year")
    )


def add_advanced_quality_flags(df: DataFrame) -> DataFrame:
    """
    Incorpora indicadores de anomalías físicas y monetarias.

    Los umbrales de 80 mph y 4 horas son criterios
    exploratorios para seleccionar viajes de movilidad.

    No elimina registros.
    """

    df = (
        df
        # Velocidad promedio: millas por hora
        .withColumn(
            "speed_mph",
            F.when(
                F.col("is_candidate_mobility"),
                F.col("trip_distance") * 3600.0
                / F.col("duration_seconds")
            )
        )

        # Velocidad superior al umbral
        .withColumn(
            "flag_speed_over_80",
            F.coalesce(
                F.col("speed_mph") > 80,
                F.lit(False)
            )
        )

        # Duración superior a cuatro horas
        .withColumn(
            "flag_duration_over_4h",
            F.coalesce(
                F.col("duration_seconds") > 14400,
                F.lit(False)
            )
        )

        # Anomalías monetarias
        .withColumn(
            "flag_negative_fare",
            F.coalesce(
                F.col("fare_amount") < 0,
                F.lit(False)
            )
        )
        .withColumn(
            "flag_negative_total",
            F.coalesce(
                F.col("total_amount") < 0,
                F.lit(False)
            )
        )
        .withColumn(
            "flag_negative_tip",
            F.coalesce(
                F.col("tip_amount") < 0,
                F.lit(False)
            )
        )
    )

    # Selección más estricta para análisis de movilidad.
    # Los viajes excluidos siguen presentes en Silver.
    df = df.withColumn(
        "is_mobility_core",
        F.col("is_candidate_mobility")
        & (~F.col("flag_speed_over_80"))
        & (~F.col("flag_duration_over_4h"))
    )

    return df

