from dataclasses import dataclass

@dataclass
class PosUser:
    posnumber: int
    cashiernumber: int
    cashierpassword: int

@dataclass
class Configuration:
    url: str
    username: str
    password: str
    chainnumber: int
    storenumber: int
    posusers: list[PosUser]