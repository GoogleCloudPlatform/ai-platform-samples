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
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict
import pathlib
from typing import Dict, List
import UpdateNotebookVariables
import ExecuteNotebook
import argparse


def get_date():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def update_notebook_variables(notebook_file_path: str, replacement_map: Dict[str, str]):
    # replace variables inside .ipynb files
    # looking for this format inside notebooks:
    # VARIABLE_NAME = '[description]'

    for variable_name, variable_value in replacement_map.items():
        UpdateNotebookVariables.update_value_in_notebook(
            notebook_file_path=notebook_file_path,
            variable_name=variable_name,
            variable_value=variable_value,
        )


def run_changed_notebooks(
    allowed_folders_file: str,
    base_branch: str,
    output_folder: str,
    variable_project_id: str,
    variable_bucket_name: str,
):
    """
    Run the notebooks that exist under the folders defined in the allowed_folders_file.
    It only runs notebooks that have differences from the Git base_branch.

    The executed notebooks are saved in the output_folder.

    Variables are also injected into the notebooks such as the variable_project_id and variable_bucket_name.
    """
    test_folders = []
    with open(allowed_folders_file) as file:
        test_folders = [folder.strip() for folder in file.readlines()]
        test_folders = [folder for folder in test_folders if len(folder) > 0]

    if len(test_folders) == 0:
        raise RuntimeError("No test folders found")

    print(f"Checking folders: {test_folders}")

    # Find notebooks
    notebooks = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base_branch}"] + test_folders
    )
    notebooks = notebooks.decode("utf-8").split("\n")
    notebooks = [notebook for notebook in notebooks if notebook.endswith(".ipynb")]
    notebooks = [notebook for notebook in notebooks if len(notebook) > 0]

    # Create paths
    artifacts_path = Path(output_folder)
    artifacts_path.mkdir(parents=True, exist_ok=True)
    artifacts_path.joinpath("success").mkdir(parents=True, exist_ok=True)
    artifacts_path.joinpath("failure").mkdir(parents=True, exist_ok=True)

    passed_notebooks: List[str] = []
    failed_notebooks: List[str] = []

    if len(notebooks) > 0:
        print(f"Found {len(notebooks)} modified notebooks: {notebooks}")

        for notebook in notebooks:
            print(f"Updating notebook variables: {notebook}")
            update_notebook_variables(
                notebook_file_path=notebook,
                replacement_map={
                    "PROJECT_ID": variable_project_id,
                    "BUCKET_NAME": variable_bucket_name,
                    "OUTPUT_DIR": get_date(),
                },
            )

            print(f"Running notebook: {notebook}")

            # TODO: Handle cases where multiple notebooks have the same name
            try:
                ExecuteNotebook.execute_notebook(
                    notebook_file_path=notebook, output_file_folder=artifacts_path
                )
                print(f"Notebook finished successfully.")
                passed_notebooks.append(notebook)
            except Exception as error:
                print(f"Notebook finished with failure: {error}")
                failed_notebooks.append(notebook)
    else:
        print("No notebooks modified in this pull request.")

    if len(failed_notebooks) > 0:
        print(f"{len(failed_notebooks)} notebooks failed:")
        print(failed_notebooks)
        print(f"{len(passed_notebooks)} notebooks passed:")
        print(passed_notebooks)
    else:
        print("All notebooks executed successfully:")
        print(passed_notebooks)


parser = argparse.ArgumentParser(description="Run changed notebooks.")
parser.add_argument(
    "--allowed_folders_file",
    type=pathlib.Path,
    help="The path to the file that has newline-limited folders of notebooks that should be tested.",
    required=True,
)
parser.add_argument(
    "--base_branch",
    help="The base git branch to diff against to find changed files.",
    required=True,
)
parser.add_argument(
    "--output_folder",
    type=pathlib.Path,
    help="The path to the folder to store executed notebooks.",
    required=True,
)
parser.add_argument(
    "--variable_project_id",
    type=pathlib.Path,
    help="The GCP project id. This is used to inject a variable value into the notebook before running.",
    required=True,
)
parser.add_argument(
    "--variable_bucket_name",
    type=pathlib.Path,
    help="The GCP bucket name. This is used to inject a variable value into the notebook before running.",
    required=True,
)

args = parser.parse_args()
run_changed_notebooks(
    allowed_folders_file=args.allowed_folders_file,
    base_branch=args.base_branch,
    output_folder=args.output_folder,
    variable_project_id=args.variable_project_id,
    variable_bucket_name=args.variable_bucket_name,
)
