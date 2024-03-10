from pydantic import BaseModel


class TaskClosedSchema(BaseModel):
    uuid: str
    title: str
    description: str
    is_open: bool
    assigned_user_uuid: str
