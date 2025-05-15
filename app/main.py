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

# Mount user management endpoints under /users
app.include_router(users_router, prefix="/users", tags=["users"])

# Mount authentication endpoints under /auth
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Mount service CRUD and invocation endpoints under /services
app.include_router(services_router, prefix="/services", tags=["services"])

# Mount access-control assignment/revocation endpoints under /access_controls
app.include_router(ac_router, prefix="/access_controls", tags=["access_controls"])

# Mount usage-history endpoints under /usage
app.include_router(usage_router, prefix="/usage", tags=["usage"])

# Mount permission creation and listing endpoints under /permissions
app.include_router(permissions_router, prefix="/permissions", tags=["permissions"])

# Mount plan creation, listing, updating, and deletion endpoints under /plans
app.include_router(plans_router, prefix="/plans", tags=["plans"])
