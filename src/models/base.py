from pydantic import BaseModel, ConfigDict


class BaseModelConfig(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True
    )
