from pydantic import BaseModel
from typing import List

class PlatformSchema(BaseModel):
    """Representa o formato dos dados de uma plataforma de jogo
    """
    id: int
    name: str

class PlatformListSchema(BaseModel):
    """Representa o formato da lista de plataformas
    """
    platforms: List[PlatformSchema]