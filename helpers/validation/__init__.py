from os.path import join, dirname
import jsonref


def load_validation_data():
    """ Loads the given schema file """

    absolute_path = join(dirname(__file__), "validation_data.json")

    base_path = dirname(absolute_path)
    base_uri = 'file://{}/'.format(base_path)

    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)
