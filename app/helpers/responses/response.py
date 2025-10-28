from fastapi.responses import JSONResponse

def success_response(data=None, message="Operación exitosa", status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )

def error_response(message="Error interno", status_code=500):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
        },
    )
