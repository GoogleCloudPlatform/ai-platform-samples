#!/bin/bash
# Copyright 2021 Google LLC
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

# Use RTN to return a non-zero value if the test fails.
RTN=0

# Only check notebooks in test folders modified in this pull request.
# Note: Use process substitution to persist the data in the array
notebooks=()
while read -r file || [ -n "$line" ]; 
do
    notebooks+=("$file")
    echo "file: $file"
done < <(git diff --name-only master | grep '\.ipynb$')

if [ ${#notebooks[@]} -gt 0 ]; then
    for notebook in "${notebooks[@]}"
    do    
        echo "Checking notebook: ${notebook}"
        echo "Running black..."
        python3 -m nbqa black "$notebook" --check
        echo "Running pyupgrade..."
        python3 -m nbqa pyupgrade "$notebook"
        echo "Running isort..."
        python3 -m nbqa isort "$notebook" --check
        echo "Running flake8..."
        python3 -m nbqa flake8 "$notebook" --show-source --ignore=W391,E501,F821,E402,F404

        NOTEBOOK_RTN=$?
        echo "Notebook finished with return code = $NOTEBOOK_RTN"
        if [ "$NOTEBOOK_RTN" != "0" ]
        then                                
            RTN=$NOTEBOOK_RTN                
        fi
    done
else
    echo "No notebooks modified in this pull request."
fi

echo "All tests finished. Exiting with return code = $RTN"
exit "$RTN"
