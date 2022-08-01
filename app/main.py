from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api.api_v1.api import api_router
from core.settings import settings
from db.session import global_init

api = fastapi.FastAPI(title=settings.PROJECT_NAME,
                      openapi_url=f"{settings.API_V1_STR}/openapi.json")


def main():
    configure()
    uvicorn.run(api, host="127.0.0.1", port=8000)


def configure():
    configure_db()
    configure_routes()


def configure_db():
    file = (Path(__file__).parent / 'db_file' / 'instedu.sqlite').absolute()
    global_init(file.as_posix())


def configure_routes():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.mount(f'/{settings.AVATARS_FOLDER}',
              StaticFiles(directory=settings.AVATARS_FOLDER), name='avatars')
    api.mount(f'/{settings.POST_IMAGES_FOLDER}',
              StaticFiles(directory=settings.POST_IMAGES_FOLDER), name='post images')
    api.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    main()
else:
    configure()
