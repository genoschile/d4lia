from app.celery.celery_app import celery_app

@celery_app.task(bind=True)
def finalizar_sesion(self, sesion_id):
    print(f"La sesión {sesion_id} ha finalizado ✅")
    return {"status": "finalizada", "sesion_id": sesion_id}
