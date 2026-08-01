from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr
from backend.operations.authentication.security import verify_password, create_access_token, create_refresh_token, get_password_hash
from backend.operations.authentication.session import session_manager
from backend.operations.audit.logger import audit_logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import get_db

router = APIRouter(prefix="/auth", tags=["Operations Auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

@router.post("/login")
async def login(request: Request, login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    if await session_manager.is_locked_out(login_data.email):
        raise HTTPException(status_code=429, detail="Account locked out due to too many failed attempts")
        
    query = text("SELECT id, password_hash, role FROM users WHERE email = :email")
    res = await db.execute(query, {"email": login_data.email})
    user = res.fetchone()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        locked = await session_manager.record_failed_login(login_data.email)
        await audit_logger.log_event("LOGIN_FAILED", "unknown", "login", ip_address=request.client.host)
        if locked:
            raise HTTPException(status_code=429, detail="Account locked out due to too many failed attempts")
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    await session_manager.clear_failed_logins(login_data.email)
    
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    session_id = await session_manager.create_session(
        user_id=str(user.id),
        user_agent=request.headers.get("user-agent", ""),
        ip_address=request.client.host
    )
    
    await audit_logger.log_event("LOGIN_SUCCESS", str(user.id), "login", ip_address=request.client.host)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session_id": session_id,
        "role": user.role
    }

@router.post("/logout")
async def logout(user_id: str, session_id: str):
    await session_manager.logout_session(user_id, session_id)
    await audit_logger.log_event("LOGOUT", user_id, "logout")
    return {"status": "Logged out"}
    
@router.post("/logout-all")
async def logout_all(user_id: str):
    await session_manager.logout_all(user_id)
    await audit_logger.log_event("LOGOUT_ALL", user_id, "logout_all_devices")
    return {"status": "Logged out of all devices"}
