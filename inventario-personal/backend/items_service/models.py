from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    quantity = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))