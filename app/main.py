import fastapi
import uvicorn

api = fastapi.FastAPI()


@api.get("/")
async def index():
    return fastapi.responses.HTMLResponse(
        """
        <h1> Hello FastAPI </h1>
        """
    )

if __name__ == "__main__":
    uvicorn.run(api)
