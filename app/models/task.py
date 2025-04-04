from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="backlog")
    card_title = Column(String, index=True)
    tag_title = Column(String)
    tag_color = Column(String)
    start_date_time = Column(DateTime)
    end_date_time = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
