from pydantic import BaseModel


class QueryResponseDTO(BaseModel):
    response: str
