from dataclasses import dataclass

@dataclass
class Item():
    id: str
    title: str
    content: str
    views: int
    timestamp: int


