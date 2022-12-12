#!/bin/sh -l
set -e

time=$(date)
echo name=time::$time >> $GITHUB_OUTPUT

## read API token and endpoint from input and add it to the CLI configuration file
echo "token=${INPUT_API_KEY}" >> /config
echo "base_url=${INPUT_API_ENDPOINT}" >> /config

if [ "${INPUT_PATH_TO_SQL}" ]
then 
  ## execute script with a path of a location where SQL files are stored
  python3 /executeworksheet.py -w ${INPUT_PATH_TO_SQL} -o ${GITHUB_WORKSPACE}
elif [ "${INPUT_FILE_LIST}" ]
then
  ## execute script with a list of SQL files to execute
  python3 /executeworksheet.py -f ${INPUT_FILE_LIST} -o ${GITHUB_WORKSPACE}
fi

#echo "::set-output name=query_results::$results"
