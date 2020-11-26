import json


def params_to_dict(request_args):
    new_dict = {}
    args_copy = dict(request_args)

    # Determine which key-value pairs have a JSON string that must be converted to dict
    for key, value in args_copy.items():
        if "[]" in key:
            new_dict[key.strip("[]")] = request_args.getlist(key)
        else:
            try:
                new_dict[key] = json.loads(value)
            except (ValueError,TypeError):
                new_dict[key] = value
    return new_dict
