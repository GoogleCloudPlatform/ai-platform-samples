import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import os
import errno
from RemoveNoExecuteCells import RemoveNoExecuteCells

# This script is used to execute a notebook and write out the output notebook.
# The nbconvert command-line doesn't write the output notebook correctly when there are errors.

# Retrieve arguments
notebook_file_path = sys.argv[1]

file_name = os.path.basename(os.path.normpath(notebook_file_path))
output_file_folder = sys.argv[2]

print(f"Executing {notebook_file_path}")

# Read notebook
with open(notebook_file_path) as f:
    nb = nbformat.read(f, as_version=4)

has_error = False

# Execute notebook
try:
    # Create preprocessors
    remove_no_execute_cells_preprocessor = RemoveNoExecuteCells()
    execute_preprocessor = ExecutePreprocessor(timeout=-1, kernel_name="python3")

    # Use no-execute preprocessor
    (
        nb_no_execute_cells_removed,
        resources_no_execute_cells_removed,
    ) = remove_no_execute_cells_preprocessor.preprocess(nb)

    # Execute notebook
    out = execute_preprocessor.preprocess(
        nb_no_execute_cells_removed, resources_no_execute_cells_removed
    )

    has_error = True
except CellExecutionError as error:
    out = None
    print(f"Error executing the notebook {notebook_file_path}.\n\n")
    print(error)

    # # Re-raise exception so return code is non-zero
    # raise
except Exception as error:
    out = None
    print(f"Error executing the notebook {notebook_file_path}.\n\n")
    print(error)
finally:
    output_file_path = os.path.join(
        output_file_folder, "success" if has_error else "error", file_name
    )

    # Create directories if they don't exist
    if not os.path.exists(os.path.dirname(output_file_path)):
        try:
            os.makedirs(os.path.dirname(output_file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    print(f"Writing output to {output_file_path}")
    with open(output_file_path, mode="w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    # print(f"Checking contents of {output_file_folder}")
    # print(os.listdir(output_file_folder))