from fastapi import FastAPI
from src.api.routes import main_router
# from config.settings import config

app = FastAPI(
    
)
app.include_router(main_router)



# if __name__=="__main__":
#     uvicorn.run(
#         app="main:app",
#         host=config.server.host,
#         port=config.server.port,
#         reload=True
#     )

