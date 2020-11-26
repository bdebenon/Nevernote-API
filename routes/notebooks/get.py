import jsonschema
import psycopg2

from helpers.http import http_response
from helpers.database_management import sql_select_query
from helpers.validation import load_validation_data


def validate(input_dict):
    schema = {
        "type": "object",
        "properties":
            {
                "query_type": load_validation_data()["query_type"],
                "query": load_validation_data()["query"],
                "tag": load_validation_data()["tag"],
                },
        "required": ["query_type", "query"]
        }
    jsonschema.validate(instance=input_dict, schema=schema)


def notebooks_get(**kwargs):
    """
    # RAML START #
    description: Returns a list of job applications the user has already submitted.
    queryParameters:
        query_type:
            displayName: Query Type
            type: string
            description: Query by 'notebook_id' or 'notebook_title'
            example: "notebook_id"
            required: true
        query:
            displayName: Query
            type: string or integer
            description: Query term
            example: "grocery_notebook" or 2"
            required: true
        tag:
            displayName: Tag
            type: string
            description: Filter by a 'tag' value
            example: "funny"
            required: false
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
    if query_type == "notebook_id":
        search_string = "notebooks.id"
    elif query_type == "notebook_title":
        search_string = "notebooks.title"
    else:
        return http_response.http_failure_response(
            400, http_response.InternalResponseCode.invalid_dict_parameters, "Invalid 'query_type' specified"
            )

    # Add extra logic if filtering by tags
    tag_sql_string = ""
    if 'tag' in kwargs:
        tag_sql_string = """
        JOIN 
        """

    try:
        sql_command = f"""
        SELECT notebook_id, notes.id as note_id, notebooks.title as notebook_title, notes.title as note_title, 
           to_char(created, 'YYYY-MM-DD HH24:MI:SS') as created,
           to_char(last_modified, 'YYYY-MM-DD HH24:MI:SS') as last_modified, tag
        FROM notebooks
        JOIN junction_notebooks_notes ON junction_notebooks_notes.notebook_id = notebooks.id
        JOIN notes ON junction_notebooks_notes.note_id = notes.id
        JOIN junction_notes_tags on notes.id = junction_notes_tags.note_id
        WHERE {search_string} = %s;
        """
        query_result = sql_select_query(sql_command, [query])

        if 'tag' in kwargs:
            tag = kwargs['tag'].lower()
            filtered_results = []
            for result in query_result:
                if result['tag'] == tag:
                    filtered_results.append(result)
            query_result = filtered_results

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
