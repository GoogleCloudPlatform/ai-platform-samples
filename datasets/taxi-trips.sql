SELECT
    IF(tips/fare >= 0.2, 1, 0) AS tip,
    CAST(pickup_community_area AS string) AS pickup_community_area,
    CAST(dropoff_community_area AS string) AS dropoff_community_area,
    CAST(pickup_census_tract AS string) AS pickup_census_tract,
    CAST(dropoff_census_tract AS string) AS dropoff_census_tract,
    fare,
    EXTRACT(MONTH
      FROM
        trip_start_timestamp) AS trip_start_month,
    EXTRACT(HOUR
      FROM
        trip_start_timestamp) AS trip_start_hour,
    EXTRACT(DAYOFWEEK
      FROM
        trip_start_timestamp) AS trip_start_day,
    pickup_latitude,
    pickup_longitude,
    dropoff_latitude,
    dropoff_longitude,
    trip_miles,
    payment_type,
    company,
    trip_seconds
FROM
    `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE
    tip IS NOT NULL
    AND fare > 0
    AND (trip_miles > 0 AND trip_miles <= 50)
    AND (trip_seconds > 0 AND trip_seconds <= 3600)
    AND (pickup_community_area !=0 AND pickup_community_area IS NOT NULL)
    AND (dropoff_community_area !=0 AND dropoff_community_area IS NOT NULL)
    AND (pickup_latitude !=0 AND pickup_latitude IS NOT NULL)
    AND (pickup_longitude !=0 AND pickup_longitude IS NOT NULL)
    AND (dropoff_latitude !=0 AND dropoff_latitude IS NOT NULL)
    AND (dropoff_longitude !=0 AND dropoff_longitude IS NOT NULL)
    AND company IS NOT NULL
    AND pickup_census_tract IS NOT NULL
    AND dropoff_census_tract IS NOT NULL

LIMIT 2000000;