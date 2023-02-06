from pydantic import BaseModel


class Record(BaseModel):
    content: str
