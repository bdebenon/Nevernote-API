import jsonschema
import psycopg2

from datetime import datetime
from time import time

from helpers.database_management import sql_insert_query, sql_delete_query, sql_update_query, insert_placeholders
from helpers.http import http_response
from helpers.validation import load_validation_data


def validate(input_dict):
    schema = {
        "type": "object",
        "properties":
            {
                "action": load_validation_data()["action"],
                "note_id": load_validation_data()["note_id"],
                "title": load_validation_data()["title"],
                "body": load_validation_data()["body"],
                "tags": load_validation_data()["tags"],
                "notebook_id": load_validation_data()["notebook_id"],
                },
        "required": ["action"]
        }
    jsonschema.validate(instance=input_dict, schema=schema)


def notes_post(**kwargs):
    """
    # RAML START #
    description: Create, Delete, or Update notes
    queryParameters:
        action:
            displayName: Action
            type: string
            description: The action you would like to perform: "create", "delete", or "update"
            example: "create"
            required: true
        note_id:
            displayName: Note ID
            type: integer
            description: ID of the note you would like to perform operations on. Required for "delete" and "update" actions.
            example: 43
            required: false
        title:
            displayName: Note Title
            type: string
            description: Title of the note you are performing actions with. Required for "create" action.
            example: "Shopping List"
            required: false
        body:
            displayName: Note Body
            type: string
            description: Text body of the note you are performing actions with. Required for "create" action.
            example: "Need to buy: eggs, cheeseburgers, coffee, soup."
            required: false
        tags:
            displayName: Tags
            type: array
            items:
                type: string
            description: List of tags (strings) to associate with the note. Required for "create" action
            example: "bdebenon"
            required: false
        notebook_id:
            displayName: Notebook ID
            type: integer
            description: Notebook ID of the note you are associating a note with. Required for "create" action.
            example: 32
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

        # Create a note and return a note id
        if action == "create":
            # Ensure we have all the inputs we need
            required_params = ['title', 'body', 'tags', 'notebook_id']
            if not all(param in kwargs for param in required_params):
                return http_response.http_failure_response(
                    400, http_response.InternalResponseCode.invalid_dict_parameters,
                    f"Required parameters missing. Need: {required_params}"
                    )
            title = kwargs['title']
            body = kwargs['body']
            tags = kwargs['tags']
            notebook_id = kwargs['notebook_id']

            # Get timestamp
            time_stamp = time()
            time_stamp = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

            # Add note to db
            sql_command = """
            INSERT INTO notes(title, body, created, last_modified)
            VALUES (%s, %s, %s, %s)
            RETURNING id; 
            """
            sql_params = [title, body, time_stamp, time_stamp]
            result = sql_insert_query(sql_command, sql_params)
            note_id = result[0]['id']
            response = {'note_id': note_id}

            # Add junction between note and notebook
            sql_command = f"""
            INSERT INTO junction_notebooks_notes(notebook_id, note_id) 
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
            """
            sql_params = [notebook_id, note_id]
            result = sql_insert_query(sql_command, sql_params)

            # Add each tag to db
            sql_command = f"""
            INSERT INTO tags(tag)
            VALUES {insert_placeholders([[tag.lower()] for tag in tags])}
            ON CONFLICT DO NOTHING;
            """
            sql_params = [tag.lower() for tag in tags]
            result = sql_insert_query(sql_command, sql_params)

            # Add junction between tags and note_id
            node_id_tag_pairs = [(note_id, tag.lower()) for tag in tags]
            sql_command = f"""
            INSERT INTO junction_notes_tags(note_id, tag) 
            VALUES {insert_placeholders(node_id_tag_pairs)}
            ON CONFLICT DO NOTHING;
            """
            sql_params = [item for sublist in node_id_tag_pairs for item in sublist]
            result = sql_insert_query(sql_command, sql_params)

        # Delete a note by note id
        elif action == "delete":
            required_params = ['note_id']
            if not all(param in kwargs for param in required_params):
                return http_response.http_failure_response(
                    400, http_response.InternalResponseCode.invalid_dict_parameters,
                    f"Required parameters missing. Need: {required_params}"
                    )
            note_id = kwargs['note_id']

            sql_command = """
            DELETE FROM notes
            WHERE id = %s;
            """
            sql_params = [note_id]
            rows_deleted = sql_delete_query(sql_command, sql_params)
            if rows_deleted != 1:
                raise ValueError(f"Anticipated 'rows_deleted' to equal '1'. Got '{rows_deleted}' instead.")
            response = {}

        # Update a note by id
        elif action == "update":
            required_params = ['note_id']
            if not all(param in kwargs for param in required_params):
                return http_response.http_failure_response(
                    400, http_response.InternalResponseCode.invalid_dict_parameters,
                    f"Required parameters missing. Need: {required_params}"
                    )
            note_id = kwargs['note_id']

            any_required_params = ['body', 'tags']
            if not any(param in kwargs for param in any_required_params):
                return http_response.http_failure_response(
                    400, http_response.InternalResponseCode.invalid_dict_parameters,
                    f"Required parameters missing. Need at least one of the following: {any_required_params}"
                    )
            body = (kwargs['body'] if 'body' in kwargs else None)
            tags = (kwargs['tags'] if 'tags' in kwargs else None)

            # Update 'body' if needed
            if body:
                sql_command = """
                UPDATE notes
                SET body = %s
                WHERE id = %s;
                """
                sql_params = [body, note_id]
                result = sql_update_query(sql_command, sql_params)

            # Update 'tags' if needed
            if tags:
                node_id_tag_pairs = [(note_id, tag.lower()) for tag in tags]
                sql_command = f"""
                -- Delete old tags from junction table                 
                DELETE FROM junction_notes_tags
                WHERE note_id = %s;
                
                -- Create new tags if not already present
                INSERT INTO tags(tag)
                VALUES {insert_placeholders([[tag.lower()] for tag in tags])}
                ON CONFLICT DO NOTHING;

                -- Create links in junction table between tag and note_id
                INSERT INTO junction_notes_tags(note_id, tag) 
                VALUES {insert_placeholders(node_id_tag_pairs)}
                ON CONFLICT DO NOTHING;
                """
                sql_params = [note_id]  # note to delete
                sql_params.extend([tag.lower() for tag in tags])  # tags list
                sql_params.extend([x for sub in node_id_tag_pairs for x in sub])  # flattened pairs list
                result = sql_update_query(sql_command, sql_params)

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
