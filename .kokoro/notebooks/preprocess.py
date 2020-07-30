from nbconvert.preprocessors import Preprocessor

class remove_no_execute_cells(Preprocessor):
    def preprocess(self, notebook, resources):
        executable_cells = []
        for cell in notebook.cells:
            if cell.metadata.get('tags'):
                if 'no_execute' in cell.metadata.get('tags'):
                    continue
            executable_cells.append(cell)
        notebook.cells = executable_cells
        return notebook, resources