import fastapi
from api.api_v1.endpoinst import user
from api.api_v1.endpoinst import login
from api.api_v1.endpoinst import avatar
from api.api_v1.endpoinst import post
from api.api_v1.endpoinst import comment
from api.api_v1.endpoinst import follow


api_router = fastapi.APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(avatar.router, prefix="/avatar", tags=["avatar"])
api_router.include_router(post.router, prefix="/post", tags=["post"])
api_router.include_router(comment.router, prefix="/comment", tags=["comment"])
api_router.include_router(follow.router, prefix="/follow", tags=["follow"])
