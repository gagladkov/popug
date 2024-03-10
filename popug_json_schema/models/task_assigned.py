from pydantic import BaseModel


class TaskAssignedSchema(BaseModel):
    uuid: str
    title: str
    description: str
    is_open: bool
    assigned_user_uuid: str
