from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.database.config import get_db_session
from backend.dependencies.auth import get_current_admin_user
from backend.models.scraper import ScrapeJob, ScrapeLog
from backend.models.enums import ScrapeJobStatus
from pydantic import BaseModel

router = APIRouter()

class JobResponse(BaseModel):
    id: str
    status: str
    marketplace_id: str
    retry_count: int

@router.get("/jobs", dependencies=[Depends(get_current_admin_user)])
async def list_jobs(db: AsyncSession = Depends(get_db_session), limit: int = 50):
    result = await db.execute(select(ScrapeJob).order_by(ScrapeJob.created_at.desc()).limit(limit))
    return result.scalars().all()

@router.post("/jobs/{job_id}/restart", dependencies=[Depends(get_current_admin_user)])
async def restart_job(job_id: str, db: AsyncSession = Depends(get_db_session)):
    job = await db.get(ScrapeJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job.status = ScrapeJobStatus.PENDING
    job.error = None
    job.retry_count = 0
    await db.commit()
    return {"message": f"Job {job_id} queued for restart"}
