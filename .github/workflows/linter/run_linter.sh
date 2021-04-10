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

# This script automatically formats and lints all notebooks that have changed from the head of the master branch.
#
# Options:
# -t: Test-mode. Only test if format and linting are required but make no changes to files.
#
# Returns:
# This script will return 0 if linting was successful/unneeded and 1 if there were any errors.

# `+e` enables the script to continue even when a command fails
set +e

# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -o pipefail

# Use RTN to return a non-zero value if the test fails.
RTN=0

is_test=false

# Process all options supplied on the command line 
while getopts 'tc' arg; do
    case $arg in
        't')
            is_test=true
            ;;
        *)
            echo "Unimplemented flag"
            exit 1
            ;;
    esac
done

echo "Test mode: $is_test"

# Only check notebooks in test folders modified in this pull request.
# Note: Use process substitution to persist the data in the array
notebooks=()
while read -r file || [ -n "$line" ]; 
do
    notebooks+=("$file")
done < <(git diff --name-only master | grep '\.ipynb$')

if [ ${#notebooks[@]} -gt 0 ]; then
    for notebook in "${notebooks[@]}"
    do    
        if [ -f "$notebook" ]; then
            echo "Checking notebook: ${notebook}"

            if [ "$is_test" = true ] ; then
                echo "Running nbfmt..."
                python3 -m tensorflow_docs.tools.nbfmt --test "$notebook"
                echo "Running black..."
                python3 -m nbqa black "$notebook" --check
                echo "Running pyupgrade..."
                python3 -m nbqa pyupgrade "$notebook"
                echo "Running isort..."
                python3 -m nbqa isort "$notebook" --check
                echo "Running flake8..."
                python3 -m nbqa flake8 "$notebook" --show-source --ignore=W391,E501,F821,E402,F404
            else
                echo "Running nbfmt..."
                python3 -m tensorflow_docs.tools.nbfmt "$notebook"
                echo "Running black..."
                python3 -m nbqa black "$notebook" --nbqa-mutate
                echo "Running pyupgrade..."
                python3 -m nbqa pyupgrade "$notebook" --nbqa-mutate
                echo "Running isort..."
                python3 -m nbqa isort "$notebook" --nbqa-mutate
                echo "Running flake8..."
                python3 -m nbqa flake8 "$notebook" --show-source --ignore=W391,E501,F821,E402,F404 --nbqa-mutate
            fi

            FLAKE8_RTN=$?
            echo "flake8 finished with return code = $FLAKE8_RTN"
            echo ""
            if [ "$FLAKE8_RTN" != "0" ]
            then                                
                RTN=$FLAKE8_RTN                
            fi
        fi
    done
else
    echo "No notebooks modified in this pull request."
fi

echo "All tests finished. Exiting with return code = $RTN"
exit "$RTN"
