import json

from oauth import settings

SCHEMA_PATH = '{path_to_lib}{schema_name}/{version}.json'

USER_ROLE_CHANGED_SCHEMA_PATH = SCHEMA_PATH.format(path_to_lib=settings.POPUG_JSON_SCHEMA_LIB,
                                                   schema_name=settings.USER_ROLE_CHANGED_SCHEMA,
                                                   version=settings.USER_ROLE_CHANGED_SCHEMA_VERSION)


def get_user_role_changed_json_schema():
    with open(USER_ROLE_CHANGED_SCHEMA_PATH) as file:
        return json.load(file)

