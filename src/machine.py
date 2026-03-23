from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Machine(BaseModel):
    """
    Represents a single virtual machine configuration.
    Validation is handled by Pydantic.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    ALLOWED_OSES: ClassVar[dict[str, str]] = {
        "ubuntu": "Ubuntu",
        "centos": "CentOS",
    }

    name: str = Field(min_length=1)
    os: str
    cpu: int = Field(ge=1, le=64)
    ram_gb: int = Field(ge=1, le=512)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Machine name cannot be empty.")
        return value

    @field_validator("os", mode="before")
    @classmethod
    def validate_os(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("OS must be a string.")

        normalized = value.strip().lower()

        if normalized in cls.ALLOWED_OSES:
            return cls.ALLOWED_OSES[normalized]

        raise ValueError(
            f"OS must be one of: {', '.join(cls.ALLOWED_OSES.values())}"
        )

    def to_dict(self) -> dict:
        return self.model_dump()

    def log_creation_message(self) -> str:
        return (
            f"Machine created: {self.name} "
            f"({self.os}, {self.cpu} vCPU, {self.ram_gb} GB RAM)"
        )