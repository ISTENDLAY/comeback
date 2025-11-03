from fastapi import FastAPI
import uvicorn

from app.endpoints import router 
from app.app_logging import logger


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def start():
    logger.info("Backend started app")


if __name__=="__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000
                )