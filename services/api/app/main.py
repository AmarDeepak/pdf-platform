from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from app.api.routes import router as api_router


app = FastAPI(title="PDF Platform API")
app.include_router(api_router, prefix="/v1")


@app.get("/healthz")
def healthz():
return {"status": "ok"}
