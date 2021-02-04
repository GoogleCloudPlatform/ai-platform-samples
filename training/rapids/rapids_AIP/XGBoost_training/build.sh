#!/usr/bin/env bash
# Build the Rapids-based custom container with the XGboost training code
## Change the gcr.io path to your own repository!

docker build -t gcr.io/[PROJECT_NAME]/[IMAGE]:[VERSION] .

docker push gcr.io/[PROJECT_NAME]/[IMAGE]:[VERSION]

