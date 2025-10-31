from app.celery_app import celery_app

@celery_app.task
def finalizar_sesion(sesion_id):
    print(f"La sesión {sesion_id} ha finalizado")
