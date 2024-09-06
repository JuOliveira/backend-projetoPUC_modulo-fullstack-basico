from sqlalchemy import Column, String, Integer, event

from  model import Base

class GameStatus(Base):
    __tablename__ = 'game_status'

    id = Column(Integer, primary_key=True)
    status = Column(String)

    def __init__(self, status:str):
      self.status = status

@event.listens_for(GameStatus.__table__, 'after_create')
def create_game_status(target, connection, **kw):
    connection.execute(
        target.insert().values([
            {'id': 0, 'status': 'Não Iniciado'},
            {'id': 1, 'status': 'Jogando'},
            {'id': 2, 'status': 'Concluído'},
        ])
    )