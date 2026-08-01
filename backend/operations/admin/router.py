from fastapi import APIRouter, HTTPException, Depends
from backend.operations.monitoring.health import system_monitor
from backend.operations.workers.manager import worker_manager
from backend.operations.audit.logger import audit_logger
from backend.operations.reports.generator import report_generator
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/admin", tags=["Operations Admin Dashboard"])

@router.get("/health")
async def get_health():
    try:
        return await system_monitor.get_system_health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workers")
async def get_workers():
    return worker_manager.get_active_workers()

@router.get("/audit-logs")
async def get_audit_logs(count: int = 100):
    return await audit_logger.get_recent_events(count)

@router.get("/reports/user-growth", response_class=PlainTextResponse)
async def user_growth_report():
    csv_data = report_generator.generate_user_growth_report()
    return csv_data
    
@router.get("/reports/marketplace", response_class=PlainTextResponse)
async def marketplace_report():
    csv_data = report_generator.generate_marketplace_report()
    return csv_data
