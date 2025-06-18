from src.config.settings import config
import uvicorn

if __name__=="__main__":
    uvicorn.run(
        app="app:app",
        app_dir="src/main.py",
        host=config.server.host,
        port=config.server.port,
        reload=True
    )



