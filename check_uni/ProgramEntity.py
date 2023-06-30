from dataclasses import dataclass

from StudentEntity import StudentEntity


@dataclass
class ProgramEntity:
    name: str
    count: int
    date: str
    peoples: list
