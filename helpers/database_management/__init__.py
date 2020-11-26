import psycopg2
import psycopg2.extras

from config import config


def sql_delete_query(sql_command, parameters=[], mogrify=False):
    try:
        config_info = config("postgresql")
        conn = psycopg2.connect(**config_info)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if mogrify:
            return cursor.mogrify(sql_command, parameters).decode('utf-8')
        cursor.execute(sql_command, parameters)
        rows_deleted = cursor.rowcount
        conn.commit()
    except psycopg2.OperationalError as error:
        raise ConnectionError("Operational error: Check database connection.")
    except psycopg2.Error as error:
        raise psycopg2.Error(f"QUERY: {sql_command} Parameters: {parameters} Error: {error.args}")
    cursor.close()
    conn.close()  # Terminate the connection
    return rows_deleted


def sql_update_query(sql_command, parameters=[], row_num=None, return_value=False, mogrify=False):
    try:
        config_info = config("postgresql")
        conn = psycopg2.connect(**config_info)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if mogrify:
            return cursor.mogrify(sql_command, parameters).decode('utf-8')
        cursor.execute(sql_command, parameters)
        if return_value:
            response = cursor.fetchall()
        else:
            response = cursor.rowcount
        conn.commit()
    except psycopg2.OperationalError as error:
        raise ConnectionError("Operational error: Check database connection.")
    except psycopg2.Error as error:
        raise psycopg2.Error(f"QUERY: {sql_command} Parameters: {parameters} Error: {error.args}")
    cursor.close()
    conn.close()  # Terminate the connection
    return response


def sql_select_query(sql_command, parameters=[], row_num=None, mogrify=False):
    try:
        config_info = config("postgresql")
        conn = psycopg2.connect(**config_info)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if mogrify:
            return cursor.mogrify(sql_command, parameters).decode('utf-8')
        cursor.execute(sql_command, parameters)
        if row_num is None:
            response = cursor.fetchall()
        elif isinstance(row_num, int):
            response = cursor.fetchmany(row_num)
        else:
            raise TypeError
    except TypeError as error:
        raise TypeError("row_num parameter must be an integer value or left empty")
    except psycopg2.OperationalError as error:
        raise ConnectionError("Operational error: Check database connection.")
    except psycopg2.Error as error:
        raise psycopg2.Error(f"QUERY: {sql_command} Parameters: {parameters} Error: {error.args}")
    cursor.close()
    conn.close()  # Terminate the connection
    return response


def sql_insert_query(sql_command, parameters, mogrify=False):
    try:
        config_info = config("postgresql")
        conn = psycopg2.connect(**config_info)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if mogrify:
            return cursor.mogrify(sql_command, parameters).decode('utf-8')
        cursor.execute(sql_command, parameters)  # Return number of affected rows
        try:
            response = cursor.fetchall()
        except:
            response = None
        conn.commit()  # Save changes
    except psycopg2.Error as error:
        raise psycopg2.Error(f"QUERY: {sql_command} Parameters: {parameters} Error: {error.args}")

    cursor.close()
    conn.close()  # Terminate the connection
    return response


def sql_insert_dict_list(table_name, insert_dict_list, return_tuple=False):
    try:
        config_info = config("postgresql")
        conn = psycopg2.connect(**config_info)
        cursor = conn.cursor()
        columns = insert_dict_list[0].keys()
        sql_query = f"Insert into {table_name} ({','.join(columns)}) values %s on conflict do nothing RETURNING {return_tuple}"
        values = [tuple([value for value in insert_dict.values()]) for insert_dict in insert_dict_list]
        response = psycopg2.extras.execute_values(cursor, sql_query, values, template=None, page_size=100)
        conn.commit()  # Save changes
        cursor.close()
        conn.close()  # Terminate the connection

    except psycopg2.Error as error:
        raise error
        # raise psycopg2.Error(f"Error inserting into {ta} : \n {values_tuples} \n into {columns}")

    return response


def sql_tuple_string_from_list(sql_list):
    sql_tuple_string = "','".join(sql_list)
    # sql_tuple_string = "'" + sql_tuple_string.replace(",", "','") + "'"
    return sql_tuple_string


def placeholders(_value):
    def recur_placeholders(value, _placeholder_list=None):
        if _placeholder_list is None:
            placeholder_list = []
        else:
            placeholder_list = _placeholder_list
        if isinstance(value, list) or isinstance(value, tuple):
            placeholder_list.append('(')
            for val in value:
                recur_placeholders(val, placeholder_list)
                placeholder_list.append(',')
            placeholder_list[-1] = ')'
        else:
            placeholder_list.append('%s')
        return placeholder_list

    return ''.join(recur_placeholders(_value))


def insert_placeholders(value):
    return placeholders(value)[1:-1]


if __name__ == "__main__":
    test_sql_query = """
    """

    response = sql_select_query(test_sql_query)
    print(response)
