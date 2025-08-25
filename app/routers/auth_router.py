from fastapi import Body
from fastapi.routing import APIRouter
from app.database import DB_DEPENDENCY
from app.models.app_user_model import AppUserModel
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/signup')
async def signup_user(db: DB_DEPENDENCY, user: AppUserModel = Body()):
    try:
        return await AuthService.signup_user(user=user, db=db)
    except ValueError as e:
          return {'error': str(e)}
    
@router.post('/login')
async def login(db: DB_DEPENDENCY, user: AppUserModel = Body()):
    try:
        return await AuthService.login(user=user, db=db)
    except ValueError as e:
          return {'error': str(e)}

from fastapi import Request

@router.post('/verify-token')
async def verify_token(token: str = Body()):
    return await AuthService.verify_token(token)
