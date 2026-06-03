from fastapi import FastAPI, Request
from fastapi.responses import Response

from dashboard.api.routers.opportunities import router as opp_router
from dashboard.api.routers.snapshots import router as snap_router
from dashboard.api.routers.runs import router as run_router
from dashboard.api.routers.pipeline import router as pipeline_router


app = FastAPI(title="LEGO Arbitrage API")

@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    response: Response = await call_next(request)

    origin = request.headers.get("origin")
    allowed = {"http://localhost:5173", "http://localhost:5174"}

    if origin in allowed:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response


app.include_router(opp_router)
app.include_router(snap_router)
app.include_router(run_router)
app.include_router(pipeline_router)
