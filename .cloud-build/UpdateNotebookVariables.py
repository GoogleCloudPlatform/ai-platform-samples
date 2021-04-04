import re


def update_value_in_notebook(
    notebook_file_path: str, variable_name: str, variable_value: str
):
    content_new = None
    with open(notebook_file_path, "r") as file:
        content = file.read()
        content_new = get_updated_value(
            content=content, variable_name=variable_name, variable_value=variable_value
        )

    if content_new:
        with open(notebook_file_path, "w") as file:
            file.write(content_new)


def get_updated_value(content: str, variable_name: str, variable_value: str):
    return re.sub(
        rf"({variable_name}.*?=.*?\\[\",\'])\[.+?\](\\[\",\'].*?)",
        # rf"({variable_name}.*?=.*?[\", \'])\[.+?\]([\",\'].*?)",
        rf"\1{variable_value}\2",
        content,
        flags=re.M,
    )


def test_update_value():
    new_content = get_updated_value(
        content='asdf\nPROJECT_ID = \\"[your-project-id]\\" #@param {type:"string"} \nasdf',
        variable_name="PROJECT_ID",
        variable_value="sample-project",
    )
    assert (
        new_content
        == 'asdf\nPROJECT_ID = \\"sample-project\\" #@param {type:"string"} \nasdf'
    )


def test_update_value_single_quotes():
    new_content = get_updated_value(
        content="PROJECT_ID = \\'[your-project-id]\\'",
        variable_name="PROJECT_ID",
        variable_value="sample-project",
    )
    assert new_content == "PROJECT_ID = \\'sample-project\\'"


def test_update_value_avoidance():
    new_content = get_updated_value(
        content="PROJECT_ID = shell_output[0] ",
        variable_name="PROJECT_ID",
        variable_value="sample-project",
    )
    assert new_content == "PROJECT_ID = shell_output[0] "
