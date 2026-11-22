from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)


class Task(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None

    @field_validator("title", "description", "completed", mode="before")
    @classmethod
    def prevent_none(cls, value):
        if value is None:
            raise ValueError("Este campo no puede ser nulo (null).")
        return value