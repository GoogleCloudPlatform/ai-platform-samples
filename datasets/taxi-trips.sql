/*
 *    Copyright 2019 Google LLC
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License.
 *
 *    This script downloads datasets from GCS to local drive.
 */

SELECT
    IF(tips / fare >= 0.2, 1, 0) AS tip, --Generate label
    trip_miles,
    trip_seconds,
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
    CAST(pickup_community_area AS string) AS pickup_community_area,
    CAST(dropoff_community_area AS string) AS dropoff_community_area,
    CAST(pickup_census_tract AS string) AS pickup_census_tract,
    CAST(dropoff_census_tract AS string) AS dropoff_census_tract,
    pickup_latitude,
    pickup_longitude,
    dropoff_latitude,
    dropoff_longitude,
    payment_type,
    company
FROM
    `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE
    tips IS NOT NULL
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