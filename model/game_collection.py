from sqlalchemy import Column, String, Integer, Boolean

from  model import Base

class GameCollection(Base):
    __tablename__ = 'game_collection'

    id = Column('pk_game', Integer, primary_key=True)
    title = Column(String(140), unique=True)
    release_date = Column(String)
    purchase_date = Column(String)
    is_favorite = Column(Boolean)
    status = Column(String)
    cover_art = Column(String)

    def __init__(self, title:str, release_date:str, purchase_date:str,
                is_favorite:bool, status:str, cover_art:str):
        self.title = title
        self.release_date = release_date
        self.purchase_date = purchase_date
        self.is_favorite = is_favorite
        self.status = status
        self.cover_art = cover_art
