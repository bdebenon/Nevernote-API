import jsonschema
import psycopg2

from helpers.http import http_response
from helpers.database_management import sql_select_query
from helpers.validation import load_validation_data


def validate(input_dict):
    schema = {
        "type": "object",
        "properties": {
            "query_type": load_validation_data()["query_type"],
            "query": load_validation_data()["query"],
            },
        "required": ["query_type", "query"]
        }
    jsonschema.validate(instance=input_dict, schema=schema)


def notes_get(**kwargs):
    """
    # RAML START #
    description: Query notes stored in Nevernote
    queryParameters:
        query_type:
            displayName: Query Type
            type: string
            description: Query by 'note_id'
            example: "note_id"
            required: true
        query:
            displayName: Query
            type: integer
            description: Query term - what is the 'node_id' you are looking up?
            example: 43
            required: true
    # RAML END #
    """
    try:
        validate(kwargs)
    except jsonschema.exceptions.ValidationError as e:
        return http_response.http_failure_response(
            400, http_response.InternalResponseCode.invalid_dict_parameters, f"Error validating input: {e.args[0]}"
            )

    # Attempt to create new accounts
    query_type = kwargs["query_type"]
    query = kwargs["query"]

    # Construct search_string based on query_type
    if query_type == "note_id":
        search_string = "notes.id"
    else:
        return http_response.http_failure_response(
            400, http_response.InternalResponseCode.invalid_dict_parameters, "Invalid 'query_type' specified"
            )

    try:
        sql_command = f"""
        SELECT notes.id as note_id, notes.title as note_title, notes.body as note_body,
               to_char(created, 'YYYY-MM-DD HH24:MI:SS') as created,
               to_char(last_modified, 'YYYY-MM-DD HH24:MI:SS') as last_modified, tag
        FROM notes
        JOIN junction_notes_tags ON notes.id = junction_notes_tags.note_id
        WHERE {search_string} = %s;
        """
        query_result = sql_select_query(sql_command, [query])

        response = query_result

    except psycopg2.DatabaseError:
        return http_response.http_failure_response(
            500, http_response.InternalResponseCode.database_error, "Database could not fulfil request"
            )
    except KeyError:
        return http_response.http_failure_response(
            404, http_response.InternalResponseCode.basic_info_empty, "Resource not found"
            )
    return http_response.http_success_response(200, response)
