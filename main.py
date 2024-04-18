import re
from ipaddress import ip_address
from typing import Callable
from pathlib import Path
from contextlib import asynccontextmanager
import uvicorn

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.routes import todos, auth, users
from src.conf.config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
     """
     The lifespan function is a callback that will be executed when the application starts up and shuts down.
     It's useful for performing tasks that you only want to do once, like connecting to a database.
     
     :param app: FastAPI: Pass the fastapi object to the lifespan function
     :return: A context manager, which is used to
     :doc-author: Trelent
     """
     r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
     await FastAPILimiter.init(r)
     yield


app = FastAPI(lifespan=lifespan)

banned_ips = [
    ip_address("192.168.1.1"),
    ip_address("192.168.1.2"),
    ip_address("127.0.0.1"),
]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response

user_agent_ban_list = [r"Googlebot", r"Python-urllib"]


#@app.middleware("http")
#async def user_agent_ban_middleware(request: Request, call_next: Callable):
#    print(request.headers.get("Authorization"))
#    user_agent = request.headers.get("user-agent")
    # print(user_agent)
    # for ban_pattern in user_agent_ban_list:
    #     if re.search(ban_pattern, user_agent):
    #         return JSONResponse(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             content={"detail": "You are banned"},
    #         )
    # response = await call_next(request)
    # return response


BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("src").joinpath("static")
app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(todos.router, prefix="/api")




templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """
    The index function is the root of our application.
    It returns a Jinja2 template response, which means that it will render an HTML page using the Jinja2 templating engine.
    The templates folder contains all of our HTML files, and we are rendering index.html here.
    
    :param request: Request: Get the request object
    :return: A templateresponse object
    :doc-author: Trelent
    """
    return templates.TemplateResponse(
        "index.html", {"request": request, "our": "Build group WebPython #16"}
    )


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    The healthchecker function is a function that returns the message &quot;Welcome to FastAPI!&quot; if the database connection is successful.
    If there's an error connecting to the database, it will return a 500 status code with an error message.
    
    :param db: AsyncSession: Inject the database session into the function
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    """
    The healthchecker function is a function that returns the message &quot;Welcome to FastAPI!&quot; if the database connection is successful.
    If there's an error connecting to the database, it will return a 500 status code with an error message.
    
    :param db: AsyncSession: Pass the database session to the function
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    


if __name__=="__main__":
    uvicorn.run("main:app", reload=True)