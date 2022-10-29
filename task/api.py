from fastapi import FastAPI, Request
from routes import router, CustomException
from fastapi.responses import JSONResponse




app = FastAPI()
app.include_router(router, prefix="/api")


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=422,
        content={"error": "string", "details": exc.details},
    )


