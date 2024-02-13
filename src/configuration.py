from dataclasses import dataclass

@dataclass
class Configuration:
    url: str
    username: str
    password: str
    chainnumber: int
    storenumber: int
    posnumbers: list