from pydantic import BaseModel


class BaseModelConfig(BaseModel):
    class Config:
        use_enum_values = True
        validate_assignment = True
