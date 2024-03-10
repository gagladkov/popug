from pydantic import BaseModel


class TaskCreatedSchema(BaseModel):
    uuid: str
    title: str
    description: str
    is_open: bool
