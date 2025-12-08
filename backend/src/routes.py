from fastapi import APIRouter

# Import các controller
from src.modules.user.controller import user_controller
from src.modules.auth.controller import auth_controller
from src.modules.room.controller import room_controller
from src.modules.user_room.controller import user_room_controller
from src.modules.message.controller import message_controller
from src.modules.question.controller import question_controller

# Tạo APIRouter tổng
api_router = APIRouter()

# Include từng router
api_router.include_router(user_controller)
api_router.include_router(auth_controller)
api_router.include_router(room_controller)
api_router.include_router(user_room_controller)
api_router.include_router(message_controller)
api_router.include_router(question_controller)