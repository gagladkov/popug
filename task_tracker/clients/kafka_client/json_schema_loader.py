import json

from task_tracker import settings

SCHEMA_PATH = '{path_to_lib}{schema_name}/{version}.json'

TASK_ASSIGNED_SCHEMA_PATH = SCHEMA_PATH.format(path_to_lib=settings.POPUG_JSON_SCHEMA_LIB,
                                               schema_name=settings.TASK_ASSIGNED_SCHEMA,
                                               version=settings.TASK_ASSIGNED_SCHEMA_VERSION)

TASK_CREATED_SCHEMA_PATH = SCHEMA_PATH.format(path_to_lib=settings.POPUG_JSON_SCHEMA_LIB,
                                              schema_name=settings.TASK_CREATED_SCHEMA,
                                              version=settings.TASK_CREATED_SCHEMA_VERSION)

TASK_CLOSED_SCHEMA_PATH = SCHEMA_PATH.format(path_to_lib=settings.POPUG_JSON_SCHEMA_LIB,
                                             schema_name=settings.TASK_CLOSED_SCHEMA,
                                             version=settings.TASK_CLOSED_SCHEMA_VERSION)

USER_ROLE_CHANGED_SCHEMA_PATH = SCHEMA_PATH.format(path_to_lib=settings.POPUG_JSON_SCHEMA_LIB,
                                                   schema_name=settings.USER_ROLE_CHANGED_SCHEMA,
                                                   version=settings.USER_ROLE_CHANGED_SCHEMA_VERSION)

MAP_TOPIC_NAME_TO_JSON_SCHEMA_PATH = {
    settings.KAFKA_TOPIC_TASK_TRACKER_CREATED: TASK_CREATED_SCHEMA_PATH,
    settings.KAFKA_TOPIC_TASK_TRACKER_ASSIGNED: TASK_ASSIGNED_SCHEMA_PATH,
    settings.KAFKA_TOPIC_TASK_TRACKER_CLOSED: TASK_CLOSED_SCHEMA_PATH,
    settings.KAFKA_TOPIC_PROFILES_ROLE_CHANGED: USER_ROLE_CHANGED_SCHEMA_PATH,
}


def get_json_schema(topic_name: str):
    json_schema_path = MAP_TOPIC_NAME_TO_JSON_SCHEMA_PATH[topic_name]
    with open(json_schema_path) as file:
        return json.load(file)

