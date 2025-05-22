# bot/handlers/__init__.py
from .start import router as start_router
from .documents import router as documents_router
from .skills import router as skills_router
from .about import router as about_router
from .questions import router as question_router
from .pagination import router as pagination_router

routers = [
    start_router,
    documents_router,
    skills_router,
    about_router,
    question_router,
    pagination_router,
]

__all__ = ['routers']