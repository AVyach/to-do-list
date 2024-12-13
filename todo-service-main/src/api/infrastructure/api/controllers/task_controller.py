from fastapi.routing import APIRouter
from infrastructure.container import Container
from domain.task import Task
from dependency_injector.wiring import inject, Provide
from applicaiton.services.task_service import TaskService
from fastapi import Depends
from infrastructure.api.auth.keycloak_auth import verify_token
import logging

module_logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/add")
@inject
def add_task(task: Task, task_service: TaskService = Depends(Provide[Container.task_service]), user_data: dict = Depends(verify_token)):
    task_service.process_task(task)
    return "Task recieved"


@router.get("/all")
@inject
def get_tasks(task_service: TaskService = Depends(Provide[Container.task_service]), user_data: dict = Depends(verify_token)):
    module_logger.info(user_data["sub"])
    result = task_service.get_tasks_by_user_id(user_data["sub"])
    module_logger.info(result)
    return result


@router.delete("/{task_id}")
@inject
def delete_task_by_id(task_id,task_service: TaskService = Depends(Provide[Container.task_service]), user_data: dict = Depends(verify_token)):
    module_logger.info(task_id)
    task_service.delete_task_by_id(task_id)
    return "Task deleted successfully"

@router.put("/{task_id}")
@inject
def update_task_by_id(task_id, task: Task, task_service: TaskService = Depends(Provide[Container.task_service]), user_data: dict = Depends(verify_token)):
    task_service.update_task_by_id(task, task_id)