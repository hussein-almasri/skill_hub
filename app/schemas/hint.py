from pydantic import BaseModel


class HintCreate(BaseModel):
    hint_text: str
    cost: int


class HintResponse(BaseModel):
    id: int
    hint_text: str
    cost: int

    class Config:
        from_attributes = True