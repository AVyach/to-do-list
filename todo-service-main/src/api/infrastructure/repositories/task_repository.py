from dataclasses import dataclass
from infrastructure.providers.postgres_provider import PostgresContextProvider
from sqlalchemy import Engine
from sqlmodel import select,delete, update
from domain.task import Task
import logging

module_logger = logging.getLogger()

@dataclass
class TaskRepository:
    engine: Engine

    def add(self, task: Task):
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                raise Exception("Could not connect to a database")
            else:

                session.add(task)

    def get_by_user_id(self, id: str):
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                raise Exception("Could not connect to a db")
            else:
                statement = select(Task).where(Task.user_id == id)
                result = [Task.model_validate(task) for task in session.exec(statement).all()]
                module_logger.info(result)
                return result

    def delete_by_id(self, id: str):
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                raise Exception("Could not connect to a db")
            else:
                statement = delete(Task).where(Task.id == id)
                session.exec(statement)
                
    def update_by_id(self, task: Task, id):
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                raise Exception("Could not connect to a db")
            else:
                module_logger.info(task)
                statement = update(Task).where(Task.id == id).values(**task.model_dump())
                session.exec(statement)
                module_logger.info("Task updated")
