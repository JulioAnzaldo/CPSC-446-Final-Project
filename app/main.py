from fastapi import FastAPI

from . import models
from .db import engine
from .routers.access_controls import router as ac_router
from .routers.auth import router as auth_router
from .routers.permissions import router as permissions_router
from .routers.plans import router as plans_router
from .routers.services import router as services_router
from .routers.usage import router as usage_router

# Routers for each resource
from .routers.users import router as users_router

# Create all database tables based on models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount user management endpoints
app.include_router(users_router)

# Mount authentication endpoints
app.include_router(auth_router)

# Mount service CRUD and invocation endpoints
app.include_router(services_router)

# Mount access-control assignment/revocation endpoints
app.include_router(ac_router)

# Mount usage-history endpoints
app.include_router(usage_router)

# Mount permission creation and listing endpoints
app.include_router(permissions_router)

# Mount plan creation, listing, updating, and deletion endpoints
app.include_router(plans_router)
