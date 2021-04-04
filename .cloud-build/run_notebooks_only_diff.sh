#!/bin/bash
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -eo pipefail

get_date () {
    # Return current date.
    CURRENT_DATE=$(date +%Y%m%d_%H%M%S)
    echo "${CURRENT_DATE}"
}

update_value () {
    # replace variable in notebook in-line. example:
    # "PROJECT_ID = '[your-project-id]' -> "PROJECT_ID = 'gcp-project'
    sed -i -E "s/(\"$1.*\=.*)\[.*\](.*)/\1$2\2/" "$3"
}

update_notebook_install () {
  # remove --user as install already happening inside virtual environment
  PIP_INSTALL_USER='\--user'
  if grep -q "$PIP_INSTALL_USER" "$1"; then
    sed -i 's/--user//g' "$1"
  fi
}

update_notebook_variables () {
    # replace variables inside .ipynb files
    # looking for this format inside notebooks:
    # VARIABLE_NAME = '[description]'
    update_value "PROJECT_ID" "${PROJECT_ID}" "$notebook"
    update_value "REGION" "${REGION}" "$notebook"
    update_value "BUCKET_NAME" "${BUCKET_NAME}" "$notebook"
    update_value "OUTPUT_DIR" "$(get_date)" "$notebook"
    update_value "USER" "${NOTEBOOKS_USER}" "$notebook"
    # update pip installation settings
    update_notebook_install "$notebook"
}

run_tests() {
    # Switch to 'fail at end' to allow all tests to complete before exiting.
    set +e

    # Use RTN to return a non-zero value if the test fails.
    RTN=0

    if eval "$(git rev-parse --is-shallow-repository)"; then
        echo "Fetching branch: ${BASE_BRANCH}"
        git fetch origin "${BASE_BRANCH}":refs/remotes/origin/"${BASE_BRANCH}"
    else
        echo "Skipping fetch: ${BASE_BRANCH}"
    fi

    # Get the repo's root directory
    root_folder=$(git rev-parse --show-toplevel)

    echo "Root folder:  ${root_folder}"

    # Get the file that defines the folders to test
    test_folders_file="$root_folder/.kokoro/notebooks/test_folders.txt"

    # Read each test folder into a variable
    test_folders=()
    while read -r line || [ -n "$line" ]
    do
        # Combine the root directory and relative directory
        test_folders+=("$root_folder/$line")
    done < "$test_folders_file"

    if [ ${#test_folders[@]} -eq 0 ]; then
        echo "No test folders provided."
        exit "0"
    fi

    echo "Checking folders: ${test_folders[*]}"

    # Only check notebooks in test folders modified in this pull request.
    # Note: Use process substitution to persist the data in the array
    notebooks=()
    while read -r file || [ -n "$line" ]; 
    do
        notebooks+=("$file")
        echo "file: $file"
    done < <(git diff --name-only origin/"${BASE_BRANCH}" "${test_folders[@]}" | sed "s,^,$root_folder/," | grep '\.ipynb$')
    
    cd .cloud-build
    
    ARTIFACTS_PATH="${root_folder}/${ARTIFACTS_FOLDER}"
    mkdir -p "${ARTIFACTS_PATH}"
    mkdir -p "${ARTIFACTS_PATH}/success"
    mkdir -p "${ARTIFACTS_PATH}/error"
    
    if [ ${#notebooks[@]} -gt 0 ]; then
        echo "Found modified notebooks: ${notebooks[*]}"

        for notebook in "${notebooks[@]}"
        do
            update_notebook_variables "$notebook"
            echo "Running notebook: ${notebook}"
            
            # TODO: Handle cases where multiple notebooks have the same name
            python3 execute_notebook.py "$notebook" "$ARTIFACTS_PATH"
            
            NOTEBOOK_RTN=$?
            echo "Notebook finished with return code = $NOTEBOOK_RTN"
            if [ "$NOTEBOOK_RTN" != "0" ]
            then                                
                RTN=$NOTEBOOK_RTN                
            fi

            # cp "$notebook" "$ARTIFACTS_PATH"
        done
    else
        echo "No notebooks modified in this pull request."
    fi

    # echo "Finding files"
    # find . -type f -name '*.nbconvert.ipynb'
    
    # echo "Copying files to ${ARTIFACTS_FOLDER}"
    # mkdir ${ARTIFACTS_FOLDER}
    # find . -type f -name '*.nbconvert.ipynb' -exec cp '{}' "${ARTIFACTS_FOLDER}" ';'
    
    # echo "Finding files in ${ARTIFACTS_PATH}"
    # ls "${ARTIFACTS_PATH}"

    echo "All tests finished. Exiting with return code = $RTN"
    exit "$RTN"
}

main(){
    run_tests
}

main