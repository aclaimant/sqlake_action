#!/bin/sh -l
set -e

time=$(date)
echo ::set-output name=time::$time

## read API token from input and add it to the CLI configuration file
echo "token=${INPUT_API_KEY}" >> /config

if [ ! -z "${INPUT_PATH_TO_SQL}" ]
then 
  ## execute script with worksheet path
  python3 /executeworksheet.py -w ${INPUT_PATH_TO_SQL} -o ${GITHUB_WORKSPACE}
elif [ ! -z "${INPUT_FILE_LIST}" ]
then
  ## execute script with worksheet path
  python3 /executeworksheet.py -f ${INPUT_FILE_LIST} -o ${GITHUB_WORKSPACE}
fi

#echo "::set-output name=query_results::$results"
