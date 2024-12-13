from sqlmodel import Field, SQLModel, Column, String
from sqlalchemy.dialects import postgresql
from typing import Optional, List
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: Optional[int] = Field(nullable=False, primary_key=True)
    user_id: str = Field(nullable=False)
    name: str = Field(nullable=False)
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(postgresql.ARRAY(String())))
    comments: Optional[str] = Field(nullable=True)
    created_at: datetime = Field(default=datetime.now())
    state: str = Field(nullable=False)
    deadline: Optional[datetime] = Field(nullable=True)
    
