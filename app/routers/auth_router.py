from fastapi.routing import APIRouter

from app.database import DB_DEPENDENCY
from app.models.app_user_model import AppUserModel
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/signup')
async def signup_user(user: AppUserModel, db: DB_DEPENDENCY):
    try:
        await AuthService.signup_user(user=user, db=db)
    except ValueError as e:
          return {'error': str(e)}
    
@router.post('/login')
async def login(user: AppUserModel, db: DB_DEPENDENCY):
    try:
        await AuthService.login(user=user, db=db)
    except ValueError as e:
          return {'error': str(e)}
