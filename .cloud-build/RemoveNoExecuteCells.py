from nbconvert.preprocessors import Preprocessor


class RemoveNoExecuteCells(Preprocessor):
    def preprocess(self, notebook, resources=None):
        executable_cells = []
        for cell in notebook.cells:
            if cell.metadata.get("tags"):
                if "no_execute" in cell.metadata.get("tags"):
                    continue
            executable_cells.append(cell)
        notebook.cells = executable_cells
<<<<<<< HEAD
<<<<<<< HEAD
        return notebook, resources
=======
        return notebook, resources
>>>>>>> Added cloud build notebook testing (#261)
=======
        return notebook, resources
>>>>>>> Added Python version of cloud-build notebook test script (#262)
