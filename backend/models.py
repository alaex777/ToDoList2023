from enum import Enum
from pydantic import BaseModel


class Type(str, Enum):
    work = 'work'
    education = 'education'
    sport = 'sport'
    entertainment = 'entertainment'
    home = 'home'
    myself = 'myself'
    shopping = 'shopping'

class Record(BaseModel):
    content: str
    due_date: str
    type: Type
