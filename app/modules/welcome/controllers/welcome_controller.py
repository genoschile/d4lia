from fastapi import APIRouter
from app.modules.welcome.services.welcome_service import WelcomeService

router = APIRouter(tags=["Encuesta"])


@router.get("/")
async def read_root():
    try:
        use_case_welcome = WelcomeService()
        if not use_case_welcome:
            return {
                "success": False,
                "message": "No se pudo generar el mensaje de bienvenida",
                "status": "error",
            }, 500

        response = await use_case_welcome.execute()
        return response

    except Exception as e:
        return {
            "message": "Error interno del servidor",
            "success": False,
            "error": str(e),
        }, 500
