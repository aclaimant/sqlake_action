#!/bin/sh -l
set -e

time=$(date)
echo ::set-output name=time::$time

echo "token=${INPUT_API_KEY}" >> /config

results=`upsolver -c /config catalogs ls`

echo "::set-output name=query_results::$results"
