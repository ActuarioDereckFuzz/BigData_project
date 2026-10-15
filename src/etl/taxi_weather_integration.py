from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def integrate_taxi_weather(
    df_taxi: DataFrame,
    df_weather: DataFrame
) -> DataFrame:
    """
    Integra viajes de NYC Taxi con observaciones diarias NOAA.

    Parámetros
    ----------
    df_taxi : DataFrame
        Dataset Silver de NYC Taxi. Debe contener pickup_date.

    df_weather : DataFrame
        Dataset Silver de NOAA. Debe contener weather_date
        y una única observación por fecha.

    Retorna
    -------
    DataFrame
        Viajes enriquecidos con variables meteorológicas.

    Consideraciones
    ---------------
    - LEFT JOIN: conserva todos los viajes de taxi.
    - Broadcast: distribuye la tabla meteorológica.
    - Distingue fechas sin correspondencia de AWND faltante.
    - No imputa, elimina ni modifica registros de taxi.
    - La unicidad de weather_date debe validarse previamente.
    """

    # --------------------------------------------------
    # 1. Integración muchos-a-uno
    # --------------------------------------------------

    df_integrated = df_taxi.join(
        F.broadcast(df_weather),

        on=(
            df_taxi["pickup_date"]
            == df_weather["weather_date"]
        ),

        how="left"
    )

    # --------------------------------------------------
    # 2. Indicadores de integración
    # --------------------------------------------------

    df_integrated = (
        df_integrated

        # Fecha sin correspondencia en NOAA
        .withColumn(
            "flag_weather_not_matched",
            F.col("weather_date").isNull()
        )

        # AWND faltante, pero fecha meteorológica presente
        .withColumn(
            "flag_weather_missing_awnd",
            F.col("weather_date").isNotNull()
            & F.col("awnd_mps").isNull()
        )

        # Conservar pickup_date como clave de integración
        .drop("weather_date")
    )

    return df_integrated