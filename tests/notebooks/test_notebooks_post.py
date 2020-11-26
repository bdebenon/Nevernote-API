import json

from routes.notebooks.post import notebooks_post
from tests.functions import send_post_request_with_json

# Setup
endpoint = "/notebooks"


def evaluate_results(results):
    # Ensure expected fields/values were returned
    assert 'message' in results
    content = results['message']


# Functions for test cases
def create():
    # Create a test notebook
    parameters_create = {'action': 'create', 'title': 'my first notebook'}
    response, response_code = notebooks_post(**parameters_create)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    notebook_id = response_dict['message']['notebook_id']
    return notebook_id


def delete(notebook_id):
    # Delete the test notebook
    parameters_delete = {'action': 'delete', 'notebook_id': notebook_id}
    response, response_code = notebooks_post(**parameters_delete)
    assert response_code == 200
    response_dict = json.loads(response)
    evaluate_results(response_dict)
    return True


def create_http():
    # Create a test notebook
    parameters_create = {'action': 'create', 'title': 'my first notebook'}
    response = send_post_request_with_json(endpoint, parameters_create)
    assert response.status_code == 200
    response_dict = response.json()
    evaluate_results(response_dict)
    notebook_id = response_dict['message']['notebook_id']
    return notebook_id


def delete_http(notebook_id):
    # Delete the test notebook
    parameters_delete = {'action': 'delete', 'notebook_id': notebook_id}
    response = send_post_request_with_json(endpoint, parameters_delete)
    assert response.status_code == 200
    response_dict = response.json()
    evaluate_results(response_dict)
    return True


# Test cases
def test_notebooks_post_create_and_delete():
    notebook_id = create()
    assert delete(notebook_id)


def test_notebooks_post_create_and_delete_http():
    notebook_id = create_http()
    assert delete_http(notebook_id)


if __name__ == "__main__":
    test_notebooks_post_create_and_delete()
    test_notebooks_post_create_and_delete_http()
