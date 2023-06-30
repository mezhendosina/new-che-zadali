from dataclasses import dataclass


@dataclass
class StudentEntity:
    snils: int
    sum_ege: int
    enemy: bool = False
