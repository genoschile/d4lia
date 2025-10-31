import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://d4lia_redis:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://d4lia_redis:6379/1")

celery_app = Celery("app", broker=BROKER_URL, backend=BACKEND_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Santiago",
    enable_utc=True,

    # Concurrency
    worker_concurrency=4,   # número de procesos/threads del worker
    worker_prefetch_multiplier=1,  # cuántas tareas prefetch por worker
    worker_max_tasks_per_child=100, # reinicia procesos después de N tareas

    # Limites de memoria y CPU
    worker_max_memory_per_child=200000, # KB, reinicia proceso si supera 200 MB

    # Time limits
    task_soft_time_limit=300,  # segundos antes de lanzar excepción SoftTimeLimitExceeded
    task_time_limit=600,       # segundos antes de matar la tarea

    # Result expiration
    result_expires=3600,  # segundos para que Redis elimine resultados
)
