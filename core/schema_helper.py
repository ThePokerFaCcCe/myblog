from typing import Any


RESPONSE_DEFAULT_PAGINATED = {
    'name': 'Response Paginated',
    'response_only': True,
}
RESPONSE_DEFAULT_RETRIEVE = {
    'name': 'Response Retrieve',
    'response_only': True,
}
RESPONSE_DEFAULT_LIST = {
    'name': 'Response List',
    'response_only': True,
}
REQUEST_DEFAULT = {
    'name': 'Request',
    'request_only': True,
}


def convert_type_to_value(vtype) -> Any:
    if isinstance(vtype, type):
        if issubclass(vtype, bool):
            return True
        if issubclass(vtype, int):
            return 0
        if issubclass(vtype, float):
            return 0.0
        if issubclass(vtype, str):
            return 'string'
        if issubclass(vtype, (list, tuple, set)):
            return []

    else:
        if isinstance(vtype, str):
            if vtype == '+int':
                return 4294967295
            if vtype == 'datetime':
                return "2000-12-29T00:00:00.000Z"
            if vtype == 'date':
                return "2000-12-29"
            if vtype == 'email':
                return "user@example.com"
            if vtype == 'uuid':
                return "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            if vtype == 'country':
                return "IR"

    return vtype


def convert_list(data: list):
    converted_items = []
    for item in data:
        if isinstance(item, dict):
            converted = schema_generator(item)
        elif isinstance(item, (list, tuple, set)):
            converted = convert_list(item)
        else:
            converted = convert_type_to_value(item)
        converted_items.append(converted)
    return converted_items


def schema_generator(data: dict):
    for k, v in data.items():

        if isinstance(v, dict):
            data[k] = schema_generator(v)

        elif isinstance(v, (list, tuple, set)):
            data[k] = convert_list(v)

        else:
            data[k] = convert_type_to_value(v)

    return data


PAGINATION_DEFAULT = schema_generator({
    "count": int,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
})
