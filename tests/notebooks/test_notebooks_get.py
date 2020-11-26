import json

from routes.notebooks.get import notebooks_get
from tests.notebooks.test_notebooks_post import create as create_notebook, delete as delete_notebook
from tests.notes.test_notes_post import create as create_note, delete as delete_note
from tests.functions import send_get_request_with_params_dict

# Setup
endpoint = "/notebooks"


def evaluate_results(results):
    # Ensure expected fields/values were returned
    assert 'message' in results
    content = results['message']


# Functions for test cases
def query_by_id(notebook_id):
    parameters = {'query_type': 'notebook_id', 'query': notebook_id}
    response, response_code = notebooks_get(**parameters)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    return True


def query_by_id_and_tag(notebook_id, tag):
    parameters = {'query_type': 'notebook_id', 'query': notebook_id, 'tag': tag}
    response, response_code = notebooks_get(**parameters)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    return True


def query_by_id_http(notebook_id):
    parameters = {'query_type': 'notebook_id', 'query': notebook_id}
    response = send_get_request_with_params_dict(endpoint, parameters)
    assert response.status_code == 200
    response_dict = response.json()
    evaluate_results(response_dict)
    return True


# Test cases
def test_notebooks_get_by_id():
    notebook_id = create_notebook()
    note_id = create_note(notebook_id)
    query_by_id(notebook_id)
    delete_note(note_id)
    delete_notebook(notebook_id)


def test_notebooks_get_by_id_and_tag():
    notebook_id = create_notebook()
    note_id = create_note(notebook_id)
    query_by_id_and_tag(notebook_id, tag="funny")
    delete_note(note_id)
    delete_notebook(notebook_id)


def test_notebooks_get_by_id_http():
    notebook_id = create_notebook()
    note_id = create_note(notebook_id)
    query_by_id_http(notebook_id)
    delete_note(note_id)
    delete_notebook(notebook_id)


if __name__ == "__main__":
    test_notebooks_get_by_id()
    test_notebooks_get_by_id_and_tag()
    test_notebooks_get_by_id_http()
