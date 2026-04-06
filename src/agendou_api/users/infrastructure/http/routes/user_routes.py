from fastapi import APIRouter
from ..controllers.user_controller import UserController

router = APIRouter(
    prefix="/users"
)

controller = UserController()

@router.post("")
def create_user():
    return controller.create_user()