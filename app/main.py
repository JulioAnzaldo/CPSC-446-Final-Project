from fastapi import FastAPI

from . import models
from .db import engine
from .routers.access_controls import router as ac_router
from .routers.auth import router as auth_router
from .routers.permissions import router as permissions_router
from .routers.plans import router as plans_router
from .routers.services import router as services_router
from .routers.usage import router as usage_router
from .routers.users import router as users_router

# Create all database tables based on models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount routers; each router defines its own prefix and tags
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(services_router)
app.include_router(ac_router)
app.include_router(usage_router)
app.include_router(permissions_router)
app.include_router(plans_router)
