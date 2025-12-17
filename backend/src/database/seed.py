from src.database.core import SessionLocal
from src.entities import *
import bcrypt, uuid

import os

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
DEFAULT_QUIZROOM = 20

def seed_data():
    db = SessionLocal()
    try:
        default_level = db.query(LevelType).filter_by(level_name="Level 0").first()
        if not default_level:
            default_level = LevelType(
                level_name="Level 0",
                level_description="Default starting level for new users"
            )
            db.add(default_level)
            db.commit()
            db.refresh(default_level)
            print("Default LevelType 'Level 0' created")
            
        default_roomtype = db.query(RoomType).filter_by(room_type_name="Global Room").first()
        if not default_roomtype:
            default_roomtype = RoomType(
                room_type_name="Global Room",
                room_type_description="Default starting room for new users"
            )
            db.add(default_roomtype)
            db.commit()
            db.refresh(default_roomtype)
            print("Default RoomType 'Global Room' created")

        private_roomtype = db.query(RoomType).filter_by(room_type_name="Private Room").first()
        if not private_roomtype:
            private_roomtype = RoomType(
                room_type_name="Private Room",
                room_type_description="Room for new users"
            )
            db.add(private_roomtype)
            db.commit()
            db.refresh(private_roomtype)
            print("Default RoomType 'Private Room' created")

        quiz_roomtype = db.query(RoomType).filter_by(room_type_name="Quiz Room").first()
        if not quiz_roomtype:
            quiz_roomtype = RoomType(
                room_type_name="Quiz Room",
                room_type_description="Room for quiz solving"
            )
            db.add(quiz_roomtype)
            db.commit()
            db.refresh(quiz_roomtype)
            print("Default RoomType 'Quiz Room' created")
        
        admin_role = db.query(UserRole).filter_by(user_role_name="admin").first()
        if not admin_role:
            admin_role = UserRole(
                user_role_name="admin",
                user_role_description="Superuser with all permissions"
            )
            user_role = UserRole(
                user_role_name="user",
                user_role_description="User role"
            )
            db.add(admin_role)
            db.add(user_role)
            db.commit()
            db.refresh(admin_role)
            db.refresh(user_role)

        admin_user = db.query(User).filter_by(username=ADMIN_USERNAME).first()
        if not admin_user:
            hashed_pw = bcrypt.hashpw(ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            admin_user = User(
                username=ADMIN_USERNAME,
                password_hashed=hashed_pw,
                is_enabled=True,
                user_role_id=admin_role.user_role_id
            )
            db.add(admin_user)
            db.commit()
            print("Superuser 'admin' created with default password 'admin123'")
        else:
            print("Superuser already exists")
            
        default_user_room_role = db.query(UserRoomRole).filter_by(user_room_role_name="Host").first()
        if not default_user_room_role:
            default_user_room_role = UserRoomRole(
                user_room_role_name="Host",
                user_room_role_description="User created the room"
            )
            default_user_room_role_for_user = UserRoomRole(
                user_room_role_name="Member",
                user_room_role_description="User added in the room"
            )
            db.add(default_user_room_role)
            db.add(default_user_room_role_for_user)
            db.commit()
            db.refresh(default_user_room_role)
            db.refresh(default_user_room_role_for_user)
            
            print("Default UserRoomRole 'Host' created") 
            print("Default UserRoomRole 'Member' created") 
        
        global_room = db.query(RoomChat).filter_by(room_type_id=1).first()
        if not global_room:
            global_room = RoomChat(
                room_name="Global Room",
                room_type_id=default_roomtype.room_type_id
            )
            db.add(global_room)
            db.commit()
            db.refresh(global_room)
            print("Global room created")
            
            admin_user_room = UserRoom(
                room_chat_id=global_room.room_chat_id,
                user_id=admin_user.id,
                user_room_role_id=default_user_room_role.user_room_role_id
            )
            db.add(admin_user_room)
            db.commit()
            db.refresh(admin_user_room)
            print("Set Admin is the host of global room")
            
        existing = db.query(MessageType).filter_by(message_type_name="Normal").first()
        if not existing:
            new_type = MessageType(
                message_type_name="Normal",
                message_type_description="Default message type for standard messages",
            )
            db.add(new_type)
            db.commit()
            db.refresh(new_type)
        fill_blank_type = db.query(QuestionType).filter_by(name="Fill in the blank").first()
        if not fill_blank_type:
            fill_blank_type = QuestionType(
                name="Fill in the blank",
                description="Question where the user fills in missing words or numbers"
            )
            db.add(fill_blank_type)
            db.commit()
            db.refresh(fill_blank_type)
            print("Seeded QuestionType: 'Fill in the blank'")
        else:
            print("QuestionType 'Fill in the blank' already exists")

        # --- Seed Subject ---
        math_subject = db.query(Subject).filter_by(name="Math").first()
        if not math_subject:
            math_subject = Subject(
                name="Math",
                description="Mathematics subject including algebra, geometry, and arithmetic"
            )
            db.add(math_subject)
            db.commit()
            db.refresh(math_subject)
            print("Seeded Subject: 'Math'")
        else:
            print("Subject 'Math' already exists")
            
        quiz_room = db.query(RoomChat).filter_by(room_type_id=3).first()
        if not quiz_room:
            for i in range(1,DEFAULT_QUIZROOM + 1):
                quiz_room = RoomChat(
                    room_name=f"Quiz Room {i}",
                    room_type_id=quiz_roomtype.room_type_id,
                    room_capacity=4
                )
                db.add(quiz_room)
                db.commit()
                db.refresh(quiz_room)
                print(f"Quiz room {i} created")

    finally:
        db.close()
    