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


PROJECT_ID = "python-docs-samples-tests"
BUCKET_ID = "python-docs-samples-tests--ivan"
BUCKET_NAME = f"gs://{BUCKET_ID}"
REGION = "us-central1"


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

                ## ! gcloud auth application-default login
                cell.source = re.sub(
                    r"!\s*?gcloud auth application-default login",
                    "# ! gcloud auth application-default login",
                    cell.source,
                )

                cell.source = re.sub(r"YOUR-PROJECT-ID", PROJECT_ID, cell.source)

                cell.source = re.sub(r"gs://YOUR-BUCKET-NAME", BUCKET_NAME, cell.source)

                # <PROJECT_ID>
                cell.source = re.sub(
                    r"<PROJECT_ID>",
                    PROJECT_ID,
                    cell.source,
                )

                # <YOUR_PROJECT_ID>
                cell.source = re.sub(
                    r"<YOUR_PROJECT_ID>",
                    PROJECT_ID,
                    cell.source,
                )

                # <YOUR_BUCKET_ID>
                cell.source = re.sub(
                    r"<YOUR_BUCKET_ID>",
                    PROJECT_ID,
                    cell.source,
                )

                # <REGION>
                cell.source = re.sub(
                    r"<REGION>",
                    REGION,
                    cell.source,
                )

                # <BUCKET_NAME>
                cell.source = re.sub(
                    r"<BUCKET_NAME>",
                    BUCKET_ID,
                    cell.source,
                )

                # <BUCKET_ID>
                cell.source = re.sub(
                    r"<BUCKET_ID>",
                    BUCKET_ID,
                    cell.source,
                )

                cell.source = re.sub(
                    r"%env PROJECT_ID PROJECT_ID",
                    f"%env PROJECT_ID {PROJECT_ID}",
                    cell.source,
                )
                cell.source = re.sub(
                    r"%env BUCKET_ID BUCKET_ID",
                    f"%env BUCKET_ID {BUCKET_ID}",
                    cell.source,
                )
                cell.source = re.sub(
                    r"gs://BUCKET_ID/", f"gs://{BUCKET_ID}/", cell.source
                )

                cell.source = re.sub(
                    rf"^print\s+?(.+)",
                    rf"print(\1)",
                    cell.source,
                    flags=re.M,
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
