from src.config.settings import config
from src.main import app
import uvicorn



if __name__=="__main__":
    uvicorn.run(
        app=app,
        host=config.server.host,
        port=config.server.port,
        reload=True
    )



