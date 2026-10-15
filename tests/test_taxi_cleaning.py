from datetime import datetime

import pytest
from pyspark.sql import SparkSession

from src.etl.taxi_cleaning import (
    prepare_taxi_data,
    add_advanced_quality_flags,
    filter_taxi_2024,
)


@pytest.fixture(scope="module")
def spark():
    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("test_taxi_cleaning")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_taxi_quality_pipeline(spark):

    schema = """
        tpep_pickup_datetime timestamp,
        tpep_dropoff_datetime timestamp,
        trip_distance double,
        PULocationID int,
        DOLocationID int,
        payment_type int,
        source_month string,
        fare_amount double,
        total_amount double,
        tip_amount double
    """

    data = [
        # Viaje válido, Flex Fare, tarifa negativa
        (
            datetime(2024, 1, 1, 10),
            datetime(2024, 1, 1, 10, 10),
            2.0, 1, 2, 0, "2024-01",
            -5.0, 10.0, 0.0
        ),

        # Velocidad extrema: 10 millas en un minuto
        (
            datetime(2024, 1, 2, 10),
            datetime(2024, 1, 2, 10, 1),
            10.0, 1, 2, 1, "2024-01",
            20.0, 25.0, 5.0
        ),

        # Registro fuera de 2024 y duración negativa
        (
            datetime(2023, 12, 31, 10),
            datetime(2023, 12, 31, 9),
            0.0, 1, 2, 2, "2024-01",
            8.0, 10.0, 0.0
        ),
    ]

    df = spark.createDataFrame(data, schema)

    prepared = prepare_taxi_data(df)
    prepared = add_advanced_quality_flags(prepared)

    # Este DataFrame es pequeño: collect es seguro aquí.
    rows = {
        row["payment_type"]: row
        for row in prepared.collect()
    }

    assert rows[0]["is_flex_fare"]
    assert rows[0]["flag_negative_fare"]
    assert rows[0]["is_mobility_core"]

    assert rows[1]["flag_speed_over_80"]
    assert not rows[1]["is_mobility_core"]

    assert rows[2]["flag_out_of_year"]
    assert rows[2]["flag_invalid_duration"]

    silver = filter_taxi_2024(prepared)

    assert silver.count() == 2