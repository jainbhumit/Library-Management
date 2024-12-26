from fastapi import APIRouter, HTTPException, status, Request
from src.app.controller.user.handler import UserHandler
from src.app.services.user_service import UserService
from src.app.dto.user import SignupDTO, LoginDTO  # Assuming DTOs are in `src/app/dto/user.py`

def create_user_routes(user_service: UserService):
    router = APIRouter(prefix="/user", tags=["user"])
    user_handler = UserHandler.create(user_service)

    @router.post("/login", status_code=status.HTTP_200_OK)
    async def login(request:Request,request_body: LoginDTO):
        return await user_handler.login(request,request_body)

    @router.post("/signup", status_code=status.HTTP_201_CREATED)
    async def signup(request:Request,request_body: SignupDTO):
        return await user_handler.signup(request,request_body)

    return router
