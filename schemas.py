from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    completed: bool = False

class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    completed: bool | None = None

class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str