from fastapi import APIRouter
from backend.operations.authentication.router import router as auth_router
from backend.operations.admin.router import router as admin_router
from backend.operations.settings.router import router as settings_router
from backend.operations.notifications.router import router as notif_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(settings_router)
router.include_router(notif_router)
