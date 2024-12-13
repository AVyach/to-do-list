from dependency_injector import containers, providers
from sqlalchemy import Engine
from sqlmodel import create_engine
from applicaiton.services.task_service import TaskService
from infrastructure.repositories.task_repository import TaskRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    sql_engine: Engine = providers.Singleton(
        create_engine,
        url=providers.Callable(
                       lambda user, password, host, port, dbname: f"postgresql://{user}:{password}@{host}:{port}/{dbname}",
            config.postgres_user,
            config.postgres_password,
            config.postgres_host,
            config.postgres_port,
            config.postgres_dbname,
        )
    )

    task_repository: TaskRepository = providers.Singleton(
        TaskRepository, engine=sql_engine
    )
    task_service: TaskService = providers.Singleton(
        TaskService, task_repository=task_repository
    )