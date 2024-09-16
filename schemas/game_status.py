from pydantic import BaseModel
from typing import List

class GameStatusSchema(BaseModel):
  """Representa o formato dos dados do status de um jogo
  """
  id: int
  status: str

class GameStatusListSchema(BaseModel):
  """Representa o formato da lista de status possíveis para um jogo
  """
  game_status_list: List[GameStatusSchema]