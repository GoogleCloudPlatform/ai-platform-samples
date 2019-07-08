#!/bin/bash

if lspci -vnn | grep NVIDIA > /dev/null 2>&1; then
  # Nvidia card found, need to check if driver is up
  if ! nvidia-smi > /dev/null 2>&1; then
    echo "Installing driver"
    /opt/deeplearning/install-driver.sh
  fi
fi

if [[ ! -z $(command -v conda) ]]; then
  source /opt/anaconda3/bin/activate base
  sudo /opt/anaconda3/bin/pip install -U papermill==0.19.1
fi

readonly INPUT_NOTEBOOK_GCS_FILE=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/input_notebook -H "Metadata-Flavor: Google")
readonly OUTPUT_NOTEBOOK_GCS_FOLDER=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/output_notebook -H "Metadata-Flavor: Google")
readonly PARAMETERS_GCS_FILE=$(curl --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/parameters_file -H "Metadata-Flavor: Google")

readonly TEMPORARY_NOTEBOOK_FOLDER="/tmp/notebook"
mkdir "${TEMPORARY_NOTEBOOK_FOLDER}"

readonly OUTPUT_NOTEBOOK_NAME=$(basename ${INPUT_NOTEBOOK_GCS_FILE})
readonly OUTPUT_NOTEBOOK_CLEAN_NAME="${OUTPUT_NOTEBOOK_NAME%.ipynb}-clean"
readonly TEMPORARY_NOTEBOOK_PATH="${TEMPORARY_NOTEBOOK_FOLDER}/${OUTPUT_NOTEBOOK_NAME}"
# For backward compitability.
readonly LEGACY_NOTEBOOK_PATH="${TEMPORARY_NOTEBOOK_FOLDER}/notebook.ipynb"

PAPERMILL_EXIT_CODE=0
if [[ -z "${PARAMETERS_GCS_FILE}" ]]; then
  echo "No input parameters present"
  papermill "${INPUT_NOTEBOOK_GCS_FILE}" "${TEMPORARY_NOTEBOOK_PATH}" --log-output || PAPERMILL_EXIT_CODE=1
else
  echo "input parameters present"
  echo "GCS file with parameters: ${PARAMETERS_GCS_FILE}"
  gsutil cp "${PARAMETERS_GCS_FILE}" params.yaml
  papermill "${INPUT_NOTEBOOK_GCS_FILE}" "${TEMPORARY_NOTEBOOK_PATH}" -f params.yaml --log-output || PAPERMILL_EXIT_CODE=1
fi

echo "Papermill exit code is: ${PAPERMILL_EXIT_CODE}"

if [[ "${PAPERMILL_EXIT_CODE}" -ne 0 ]]; then
  echo "Unable to execute notebook. Exit code: ${PAPERMILL_EXIT_CODE}"
  touch "${TEMPORARY_NOTEBOOK_FOLDER}/FAILED"
else
  cd "${TEMPORARY_NOTEBOOK_FOLDER}"
  jupyter nbconvert "${TEMPORARY_NOTEBOOK_PATH}"
  jupyter nbconvert "${TEMPORARY_NOTEBOOK_PATH}" --output "${OUTPUT_NOTEBOOK_CLEAN_NAME}" --TemplateExporter.exclude_input=True
fi

# For backward compitability.
cp "${TEMPORARY_NOTEBOOK_PATH}" "${LEGACY_NOTEBOOK_PATH}"
gsutil rsync -r "${TEMPORARY_NOTEBOOK_FOLDER}" "${OUTPUT_NOTEBOOK_GCS_FOLDER}"

readonly INSTANCE_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/instance/name -H "Metadata-Flavor: Google")
INSTANCE_ZONE="/"$(curl http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google")
INSTANCE_ZONE="${INSTANCE_ZONE##/*/}"
readonly INSTANCE_PROJECT_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/project/project-id -H "Metadata-Flavor: Google")
gcloud --quiet compute instances delete "${INSTANCE_NAME}" --zone "${INSTANCE_ZONE}" --project "${INSTANCE_PROJECT_NAME}"
