from pydantic import BaseModel


class UserRoleChangedSchema(BaseModel):
    username: str
    profile_uuid: str
    profile_role: str
