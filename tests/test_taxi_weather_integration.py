from datetime import date

import pytest
from pyspark.sql import SparkSession

from src.etl.taxi_weather_integration import (
    integrate_taxi_weather
)


@pytest.fixture(scope="module")
def spark():
    """Sesión Spark utilizada por las pruebas."""

    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("test_taxi_weather_integration")
        .getOrCreate()
    )

    yield session
    session.stop()


def test_taxi_weather_integration(spark):
    """
    Verifica:
    - Conservación de los viajes.
    - Correcta asociación por fecha.
    - Identificación de AWND faltante.
    - Identificación de fechas sin correspondencia.
    """

    # Datos artificiales de taxi
    taxi_data = [
        (1, date(2024, 1, 1)),
        (2, date(2024, 1, 1)),
        (3, date(2024, 1, 2)),
        (4, date(2024, 1, 3)),
    ]

    df_taxi = spark.createDataFrame(
        taxi_data,
        "trip_id int, pickup_date date"
    )

    # Datos meteorológicos artificiales:
    # El segundo día tiene AWND faltante.
    # El tercer día no aparece en NOAA.
    weather_data = [
        (date(2024, 1, 1), 2.5, 5.0),
        (date(2024, 1, 2), None, 0.0),
    ]

    df_weather = spark.createDataFrame(
        weather_data,
        """
        weather_date date,
        awnd_mps double,
        prcp_mm double
        """
    )

    # Aplicar integración
    result = integrate_taxi_weather(
        df_taxi,
        df_weather
    )

    rows = {
        row["trip_id"]: row
        for row in result.collect()
    }

    # Se conservan todos los viajes.
    assert len(rows) == 4

    # Dos viajes del mismo día reciben el mismo clima.
    assert rows[1]["awnd_mps"] == 2.5
    assert rows[2]["awnd_mps"] == 2.5

    # Fecha encontrada, pero AWND faltante.
    assert rows[3]["flag_weather_missing_awnd"]
    assert not rows[3]["flag_weather_not_matched"]

    # Fecha sin observación meteorológica.
    assert rows[4]["flag_weather_not_matched"]
    assert not rows[4]["flag_weather_missing_awnd"]