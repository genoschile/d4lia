from fastapi import APIRouter
from app.celery.task.task import finalizar_sesion
from app.celery.celery_app import celery_app


router = APIRouter(prefix="/test_celery", tags=["Test Celery"])


@router.get("/")
def init_task():
    id_sesion_creada = 12345
    task = finalizar_sesion.apply_async(args=[id_sesion_creada], countdown=10)
    return {"message": "Tarea enviada a Celery", "task_id": task.id}


@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": result.status,  # PENDING, STARTED, SUCCESS, FAILURE, etc.
        "result": result.result,  # El valor devuelto por la tarea (si terminó)
    }
