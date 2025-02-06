from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def response(success: bool, message: str, data=None, status_code: int = 200):
    return JSONResponse(
        content={
            "success": success,
            "message": message,
            "data": jsonable_encoder(data) if data is not None else []
        },
        status_code=status_code
    )
