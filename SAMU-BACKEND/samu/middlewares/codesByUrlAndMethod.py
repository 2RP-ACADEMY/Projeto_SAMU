import re
from  samu.models.requestTypeModel import RequestType

# A dictionary mapping URL paths and HTTP methods to corresponding request names.
url_method_mapping = {
    "/users/": {
        "POST": 'create_user',
        "GET": 'list_user'
    },
    "/users/login/": {
        "POST": 'login_user'
    },
    "/users/\d+/": {
        "DELETE": 'delete_user',
        "GET": 'get_user',
        "PUT": 'update_user'
    },
    "/auth/login/": {
        "POST": 'get_token'
    },
    "/requests/": {
        "GET": 'list_request'
    },
    "/requests/\d+/": {
        "GET": 'get_request'
    },
    "/medicines/": {
        "POST": 'create_medicine',
        "GET": 'list_medicine'
    },
    "/medicines/\d+/": {
        "DELETE": 'delete_medicine',
        "GET": 'get_medicine',
        "PUT": 'update_medicine'
    },
    "/materials/": {
        "POST": 'create_material',
        "GET": 'list_material'
    },
    "/materials/\d+/": {
        "DELETE": 'delete_material',
        "GET": 'get_material',
        "PUT": 'update_material'
    },
    "/equipments/": {
        "POST": 'create_equipment',
        "GET": 'list_equipment'
    },
    "/equipments/\d+/": {
        "DELETE": 'delete_equipment',
        "GET": 'get_equipment',
        "PUT": 'update_equipment'
    },
    "/allocation/": {
        "POST": 'allocate_item'
    },
    "/withdrawns/": {
        "POST": 'create_withdrawn',
        "GET": 'list_withdrawn'
    },
    "/withdrawns/\d+/": {
        "GET": 'get_withdrawn'
    },
    "/deallocation/": {
        "POST": 'deallocate_item'
    },
    "/vehicles/": {
        "GET": 'list_vehicle',
        "POST": 'create_vehicle'
    },
    "/vehicles/\d+/": {
        "GET": 'get_vehicle',
        "PUT": 'update_vehicle',
        "DELETE": 'delete_vehicle'
    }
}

def get_number_from_mapping(url, method):
    """
    Retrieves a unique request identifier (request type) based on the provided URL and HTTP method.

    Args:
        url (str): The URL for which to retrieve the request type.
        method (str): The HTTP method associated with the request.

    Returns:
        int: The unique identifier (ID) of the request type.
    """
    for path in url_method_mapping.keys():
        path_re = re.compile(path)
        if path_re.fullmatch(url):
            request_name = url_method_mapping[path].get(method, None)
            if request_name == None:
                return None
            request = RequestType.objects.get_or_create(name=request_name)
            request_id = request[0].id
            return request_id
