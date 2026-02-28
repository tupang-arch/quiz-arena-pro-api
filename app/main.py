from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .database import Base, engine
from .routers.auth import router as auth_router
from .routers.notes import router as notes_router
from .routers.health import router as health_router  # dacă ai health


app = FastAPI(title="Quiz Arena Pro API")

# creează tabele (ok pt sqlite / demo)
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(health_router)   # optional
app.include_router(auth_router)
app.include_router(notes_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="API with JWT Bearer auth",
        routes=app.routes,
    )

    # ✅ adaugă Bearer auth în Swagger (Authorize button)
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    # (opțional) pui security global, ca să se aplice peste tot
    # Dacă nu vrei global, poți comenta linia de mai jos.
    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Quiz Arena Pro API is running"}