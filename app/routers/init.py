from .health import router as health_router
from .auth import router as auth_router
from .quizzes import router as quizzes_router

__all__ = ["health_router", "auth_router", "quizzes_router"]