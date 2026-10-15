from datetime import date

import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from src.etl.weather_cleaning import transform_weather_daily


@pytest.fixture(scope="module")
def spark():
    """
    Crea una sesión Spark para las pruebas
    y la cierra al finalizar el módulo.
    """
    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("test_weather_cleaning")
        .getOrCreate()
    )

    yield session
    session.stop()


def test_weather_daily_transformation(spark):
    """
    Verifica:
    1. Calendario completo de 2024.
    2. Transformación pivot.
    3. Variables derivadas.
    4. Conservación de valores faltantes.
    5. Identificación de anomalías físicas.
    """

    station = "GHCND:USW00094728"

    # Datos artificiales.
    # El segundo día presenta una anomalía de temperatura,
    # precipitación negativa y ausencia de AWND.
    data = [
        (station, date(2024, 1, 1), "TMAX", 8.3),
        (station, date(2024, 1, 1), "TMIN", 1.7),
        (station, date(2024, 1, 1), "PRCP", 0.8),
        (station, date(2024, 1, 1), "SNOW", 0.0),
        (station, date(2024, 1, 1), "AWND", 1.5),

        (station, date(2024, 1, 2), "TMAX", 3.0),
        (station, date(2024, 1, 2), "TMIN", 4.0),
        (station, date(2024, 1, 2), "PRCP", -1.0),
        (station, date(2024, 1, 2), "SNOW", 0.0),
    ]

    schema = """
        station string,
        weather_date date,
        datatype string,
        value double
    """

    df = spark.createDataFrame(data, schema)

    # Aplicar transformación
    result = transform_weather_daily(
        df=df,
        spark=spark,
        year=2024,
        station_id=station
    )

    # El calendario debe contener todos los días de 2024.
    assert result.count() == 366

    assert (
        result.select("weather_date").distinct().count()
        == 366
    )

    # Recuperar únicamente las dos fechas de prueba.
    rows = {
        row["weather_date"]: row
        for row in result.filter(
            F.col("weather_date").isin(
                date(2024, 1, 1),
                date(2024, 1, 2)
            )
        ).collect()
    }

    # -----------------------------------------------
    # Día 1: valores correctos
    # -----------------------------------------------

    day1 = rows[date(2024, 1, 1)]

    assert day1["tmax_c"] == 8.3
    assert day1["temperature_midpoint_c"] == pytest.approx(5.0)
    assert day1["has_precipitation"]
    assert not day1["flag_invalid_temperature"]

    # -----------------------------------------------
    # Día 2: anomalías y faltantes
    # -----------------------------------------------

    day2 = rows[date(2024, 1, 2)]

    assert day2["awnd_mps"] is None
    assert day2["flag_missing_awnd"]
    assert day2["flag_invalid_temperature"]
    assert day2["flag_negative_precipitation"]

    # Día sin observaciones: calendario conservado.
    day3 = result.filter(
        F.col("weather_date") == date(2024, 1, 3)
    ).first()

    assert day3["tmax_c"] is None

    print("Pruebas de transformación NOAA correctas.")