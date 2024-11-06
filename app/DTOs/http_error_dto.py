from pydantic import BaseModel


class HTTPErrorDTO(BaseModel):
    detail: str
