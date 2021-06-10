from nbconvert.preprocessors import Preprocessor
import re


class RemoveNoExecuteCells(Preprocessor):
    def preprocess(self, notebook, resources=None):
        executable_cells = []
        for cell in notebook.cells:
            if cell.metadata.get("tags"):
                if "no_execute" in cell.metadata.get("tags"):
                    continue
            executable_cells.append(cell)
        notebook.cells = executable_cells
        return notebook, resources


class RemoveInvalidCellContents(Preprocessor):
    def preprocess(self, notebook, resources=None):
        executable_cells = []
        for cell in notebook.cells:
            if cell.cell_type == "code":
                # Comment out

                ## version
                cell.source = re.sub(r"^version", "# version", cell.source)

                ## ! gcloud auth login
                cell.source = re.sub(
                    r"!\s*?gcloud auth login", "# ! gcloud auth login", cell.source
                )

                executable_cells.append(cell)
            else:
                executable_cells.append(cell)
            # if cell.metadata.get("tags"):
            #     if "no_execute" in cell.metadata.get("tags"):
            #         continue
            # executable_cells.append(cell)
            # cell.
            pass
        notebook.cells = executable_cells
        return notebook, resources
