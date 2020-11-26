import json

from routes.notes.post import notes_post
from tests.functions import send_post_request_with_json
from tests.notebooks.test_notebooks_post import create as create_notebook, delete as delete_notebook

# Setup
endpoint = "/notes"


def evaluate_results(results):
    # Ensure expected fields/values were returned
    assert 'message' in results
    content = results['message']


# Functions for test cases
def create(notebook_id):
    # Create a test note
    parameters_create = {
        'action': 'create',
        'title': 'my first note',
        'body': 'this is the body of my first note!',
        'tags': ['funny', 'kevin'],
        'notebook_id': notebook_id,
        }
    response, response_code = notes_post(**parameters_create)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    note_id = response_dict['message']['note_id']
    return note_id


def delete(note_id):
    # Delete the test note
    parameters_delete = {'action': 'delete', 'note_id': note_id}
    response, response_code = notes_post(**parameters_delete)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    return True


def update(note_id, body=None, tags=None):
    # Update the test note
    parameters_update = {'action': 'update', 'note_id': note_id}
    if body is not None:
        parameters_update['body'] = body
    if tags is not None:
        parameters_update['tags'] = tags
    response, response_code = notes_post(**parameters_update)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    return True


def create_http(notebook_id):
    # Create a test note
    parameters_create = {
        'action': 'create',
        'title': 'my first note',
        'body': 'this is the body of my first note!',
        'tags': ['funny', 'kevin'],
        'notebook_id': notebook_id,
        }
    response = send_post_request_with_json(endpoint, parameters_create)
    assert response.status_code == 200
    response_dict = response.json()
    evaluate_results(response_dict)
    note_id = response_dict['message']['note_id']
    return note_id


def delete_http(note_id):
    # Delete the test note
    parameters_delete = {'action': 'delete', 'note_id': note_id}
    response = send_post_request_with_json(endpoint, parameters_delete)
    assert response.status_code == 200
    response_dict = response.json()
    evaluate_results(response_dict)
    return True


# Test cases
def test_notes_post_create_and_delete():
    notebook_id = create_notebook()
    note_id = create(notebook_id)
    assert delete(note_id)
    assert delete_notebook(notebook_id)


def test_notes_post_create_and_delete_http():
    notebook_id = create_notebook()
    note_id = create_http(notebook_id)
    assert delete_http(note_id)
    assert delete_notebook(notebook_id)


def test_notes_post_update():
    notebook_id = create_notebook()
    note_id = create(notebook_id)
    assert update(note_id, body="This is an updated note!", tags=['updated_funny', 'updated_kevin'])
    assert delete(note_id)
    assert delete_notebook(notebook_id)


if __name__ == "__main__":
    test_notes_post_create_and_delete()
    test_notes_post_create_and_delete_http()
    test_notes_post_update()
