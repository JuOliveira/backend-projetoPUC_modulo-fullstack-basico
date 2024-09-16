from pydantic import BaseModel
from typing import List, Optional

class GameSchema(BaseModel):
    """Representa o formato dos dados de um jogo quando é adicionado na coleção
    """
    title: str
    platform: str
    release_date: Optional[str]
    purchase_date: Optional[str]
    is_favorite: bool
    status: str
    cover_art: Optional[str]

class GameWithIDSchema(BaseModel):
    """Representa o formato dos dados de um jogo como é armazendo no banco de dados com ID
    """
    id: int
    title: str
    platform: str
    release_date: str
    purchase_date: str
    is_favorite: bool
    status: str
    cover_art: str

class GameCollectionSchema(BaseModel):
    """Representa o formato dos dados da coleção de jogos armazenada no banco de dados
    """
    game_collection: List[GameWithIDSchema]

class GameDeleteSchema(BaseModel):
    """Representa o formato dos dados usados para remover um jogo da coleção
    """
    id: int
class GameListSchema(BaseModel):
    """Representa o formato dos dados usados para realizar a busca de lista de jogos na biblioteca RAWG
    """
    query: str

class GameSearchPlatformSchema(BaseModel):
    """Representa o formato dos dados de uma plataforma retornada pela busca na biblioteca RAWG
    """
    id: int
    name: str
    slug: str

class GameSearchItemSchema(BaseModel):
    """Representa o formato dos dados da lista de plataformas retornada pela busca na biblioteca RAWG
    """
    cover_art: Optional[str]
    name: str
    release_date: str
    platforms: List[GameSearchPlatformSchema]

class GameSearchListSchema(BaseModel):
    """Representa o formato dos dados da lista de jogos retornada pela busca na biblioteca RAWG
    """
    result: List[GameSearchItemSchema]
