#!/bin/bash -u

source gcp-notebook-executor/utils.sh

readonly BUILD_TIME=$(date +%s)
readonly DEFAULT_NOTEBOOK_EXECUTOR_INSTANCE_NAME="notebookexecutor-${BUILD_TIME}"

TESTING_MODE="false"
PARAM_FILE=""
OUTPUT_DATE=""

while getopts ":tp:o:" opt; do
  case ${opt} in
    t )
      TESTING_MODE="true"
      ;;
    p )
      PARAM_FILE=$OPTARG
      ;;
    o )
      OUTPUT_DATE=$OPTARG
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      ;;
  esac
done
shift $((OPTIND -1))

function output_for_mode() {
    local TESTING_MODE=$1
    local GCS_LOCATION=$2
    local OUTPUT_DATE=$3
    if [[ "${TESTING_MODE}" == "true" ]]; then
        echo "${GCS_LOCATION}/results/${BUILD_TIME}"
    else
        echo "${GCS_LOCATION}/versions/${OUTPUT_DATE}"
    fi
}

INPUT_NOTEBOOK="demo.ipynb"
NOTEBOOK_NAME=$(basename ${INPUT_NOTEBOOK})
GCS_LOCATION="gs://dl-platform-temp/notebook-ci-showcase"
INPUT_NOTEBOOK_GCS_PATH="${GCS_LOCATION}/staging/${BUILD_TIME}/${NOTEBOOK_NAME}"
PARAM_METADATA=""
if [[ ! -z ${PARAM_FILE} ]]; then
    INPUT_PARAM_GCS_PATH="${GCS_LOCATION}/staging/${BUILD_TIME}/params.yaml"
    gsutil cp "${PARAM_FILE}" "${INPUT_PARAM_GCS_PATH}"
    PARAM_METADATA=",parameters_file=${INPUT_PARAM_GCS_PATH}"
fi
OUTPUT_NOTEBOOK_GCS_FOLDER=$(output_for_mode "${TESTING_MODE}" "${GCS_LOCATION}" "${OUTPUT_DATE}")
OUTPUT_NOTEBOOK_GCS_PATH="${OUTPUT_NOTEBOOK_GCS_FOLDER}/${NOTEBOOK_NAME}"

# This is in order to remove new line at the end of the string.
API_KEY=`echo "${API_KEY}"`

echo "Going to execute the following command"
echo "execute_notebook -i ./${INPUT_NOTEBOOK} -o ${INPUT_NOTEBOOK_GCS_PATH} -m api_key=${API_KEY}${PARAM_METADATA:-} -g t4 -c 1"
execute_notebook -i "./${INPUT_NOTEBOOK}" -o "${INPUT_NOTEBOOK_GCS_PATH}" -m "api_key=${API_KEY}${PARAM_METADATA:-}" -g t4 -c 1
