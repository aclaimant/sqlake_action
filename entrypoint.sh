#!/bin/sh -l
set -e

time=$(date)
echo ::set-output name=time::$time

## read API token from input and add it to the CLI configuration file
echo "token=${INPUT_API_KEY}" >> /config

## execute script with worksheet path
echo "worksheet: ${INPUT_WORKSHEET_PATH}"
echo "env: ${ENV_GITHUB_WORKSPACE}"

python3 /executeworksheet.py -w ${INPUT_WORKSHEET_PATH} -o ${ENV_GITHUB_WORKSPACE}

#echo "::set-output name=query_results::$results"
