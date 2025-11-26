from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(data=None, message="Operación exitosa"):
    content = jsonable_encoder(
        {
            "success": True,
            "message": message,
            "data": data,
        }
    )
    return JSONResponse(content=content, status_code=200)


def error_response(message="Error interno", status_code=500):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
        },
    )
