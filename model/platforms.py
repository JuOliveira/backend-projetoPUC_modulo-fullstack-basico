from sqlalchemy import Column, String, Integer

from  model import Base

class Platforms(Base):
  __tablename__ = 'platforms'

  id = Column(Integer, primary_key=True)
  platform = Column(String)

  def __init__(self, id:int, platform:str):
    self.id = id
    self.platform = platform