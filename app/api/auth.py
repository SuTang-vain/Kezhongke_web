from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import EmailStr, BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import auth_service
from app.services.email import email_service
from app.services.user import user_service
from app.services.jwt import jwt_service
from app.db.session import get_session
from app.models.user import UserRead, UserUpdate

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

async def get_current_user_obj(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = jwt_service.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="登录状态已过期")
    
    from uuid import UUID
    user_id = payload.get("sub")
    user = await user_service.get_user_by_id(UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.post("/request-otp")
async def request_otp(payload: EmailRequest):
    existing_user = await user_service.get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="该邮箱已注册，请直接登录")
    
    otp = await auth_service.generate_otp(payload.email)
    
    try:
        await email_service.send_otp(payload.email, otp)
    except Exception as e:
        print(f"Email Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "验证码已发送至您的邮箱"}

@router.post("/verify-otp")
async def verify_otp(payload: OTPVerifyRequest, session: AsyncSession = Depends(get_session)):
    is_valid = await auth_service.verify_otp(payload.email, payload.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="验证码错误或已过期")
    
    existing_user = await user_service.get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户已存在")
    
    from app.models.user import UserCreate
    user_create = UserCreate(
        email=payload.email,
        password=payload.password,
        is_active=True,
        is_verified=True,
        role="member"
    )
    user = await user_service.create_user(user_create)
    token = jwt_service.create_token_for_user(str(user.id), user.email, user.role)
    
    return TokenResponse(
        access_token=token,
        user=user_service.user_to_read(user)
    )

@router.post("/login")
async def login(payload: LoginRequest):
    user = await user_service.get_user_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    if not user_service.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    
    token = jwt_service.create_token_for_user(str(user.id), user.email, user.role)
    
    return TokenResponse(
        access_token=token,
        user=user_service.user_to_read(user)
    )

@router.get("/me", response_model=UserRead)
async def get_current_user(user=Depends(get_current_user_obj)):
    return user_service.user_to_read(user)

@router.patch("/me", response_model=UserRead)
async def update_current_user(user_update: UserUpdate, user=Depends(get_current_user_obj)):
    updated_user = await user_service.update_user(user.id, user_update)
    return user_service.user_to_read(updated_user)

@router.post("/logout")
async def logout():
    return {"message": "登出成功"}
