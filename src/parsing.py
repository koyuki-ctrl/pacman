from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from sys import argv
import json5
import os

CONFIGS = [
    'lives',
    'pacgum',
    'level_max_time',
    'points_per_pacgum',
    'points_per_super_pacgum',
    'points_per_ghost'
]


def strip_hash_comments(text: str) -> str:
    """Remove # line(s) before reading json file"""
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def _get_argument() -> str:
    if len(argv) != 2:
        raise ValueError("[ERROR] Only one argument is valid")
    else:
        argument = argv[1]
        return argument


class GameConfigFile(BaseModel):
    lives: int = Field(..., ge=1, strict=True)
    pacgum: int = Field(..., ge=1, strict=True)
    level_max_time: int = Field(..., ge=60, strict=True)
    points_per_pacgum: int = Field(..., ge=1, strict=True)
    points_per_super_pacgum: int = Field(..., ge=1, strict=True)
    points_per_ghost: int = Field(..., ge=1, strict=True)

    @field_validator(*CONFIGS, mode='before')
    @classmethod
    def parse_value(cls, value):
        if isinstance(value, str):
            return int(value.strip())
        return value

    @classmethod
    def from_json(cls) -> "GameConfigFile":
        path = Path(_get_argument())
        if not os.path.exists(path):
            raise ValueError(f"[ERROR] {path} does not exist")
        if path.suffix != ".json":
            raise ValueError("[Error] Only .json files are accepted")
        raw = path.read_text(encoding="utf-8")
        raw = strip_hash_comments(raw)
        data = json5.loads(raw)

        if not isinstance(data, dict):
            raise ValueError(
                "[Error] JSON root must be an object, got "
                + f"{type(data).__name__}"
            )
        return cls.model_validate(data)
