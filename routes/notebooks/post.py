import jsonschema
import psycopg2

from helpers.database_management import sql_insert_query, sql_delete_query
from helpers.http import http_response
from helpers.validation import load_validation_data


def validate(input_dict):
    schema = {
        "type": "object",
        "properties":
            {
                "action": load_validation_data()["action"],
                "notebook_id": load_validation_data()["notebook_id"],
                "title": load_validation_data()["title"],
                },
        "required": ["action"]
        }
    jsonschema.validate(instance=input_dict, schema=schema)


def notebooks_post(**kwargs):
    """
    # RAML START #
    description: Create or Delete notebooks
    queryParameters:
        action:
            displayName: Action
            type: string
            description: User ID for the user whom made the click.
            example: "create"
            required: true
        notebook_id:
            displayName: Notebook ID
            type: integer
            description: ID of the notebook you would like to perform operations on. Required for 'delete' action.
            example: "25"
            required: false
        title:
            displayName: Notebook Title
            type: string
            description: Title of the notebook you would like to perform operations on. Required for 'create' action.
            example: "Shopping Lists"
            required: false
    # RAML END #
    """

    try:
        validate(kwargs)
    except jsonschema.exceptions.ValidationError as e:
        return http_response.http_failure_response(
            400, http_response.InternalResponseCode.invalid_dict_parameters, f"Error validating input: {e.args[0]}"
            )

    try:
        action = kwargs['action']

        # Create a notebook and return a notebook id
        if action == "create":
            if 'title' not in kwargs:
                return http_response.http_failure_response(
                    400, http_response.InternalResponseCode.invalid_dict_parameters, "'title' not specified"
                    )
            title = kwargs['title']

            sql_command = """
            INSERT INTO notebooks(title)
            VALUES (%s)
            RETURNING id; 
            """
            sql_params = [title]
            result = sql_insert_query(sql_command, sql_params)
            notebook_id = result[0]['id']
            response = {'notebook_id': notebook_id}

        # Delete a notebook by notebook id
        elif action == "delete":
            # Ensure we have all the params we need
            required_params = ['notebook_id']
            if not all(param in kwargs for param in required_params):
                return http_response.http_failure_response(
                    400, http_response.InternalResponseCode.invalid_dict_parameters,
                    f"Required parameters missing. Need: {required_params}"
                    )
            notebook_id = kwargs['notebook_id']

            sql_command = """
            DELETE FROM notebooks
            WHERE id = %s;
            """
            sql_params = [notebook_id]
            rows_deleted = sql_delete_query(sql_command, sql_params)
            if rows_deleted != 1:
                raise ValueError(f"Anticipated 'rows_deleted' to equal '1'. Got '{rows_deleted}' instead.")
            response = {}

        # Invalid action specified
        else:
            return http_response.http_failure_response(
                400, http_response.InternalResponseCode.invalid_dict_parameters, "Invalid 'action' specified"
                )
    except (IndexError, KeyError, ValueError):
        return http_response.http_failure_response(
            500, http_response.InternalResponseCode.invalid_database_response, "Invalid result returned from database"
            )
    except psycopg2.DatabaseError:
        return http_response.http_failure_response(
            500, http_response.InternalResponseCode.database_error, "Database could not fulfil request"
            )

    return http_response.http_success_response(200, response)
