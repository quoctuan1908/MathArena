from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
import bcrypt
from uuid import UUID
from src.entities import *
from . import model
from sqlalchemy import func

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_user(db: Session, user_data: model.UserCreate) -> User:
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_pw = get_password_hash(user_data.password_hashed)

    user_role = db.query(UserRole).filter(UserRole.user_role_name == "user").first()

    db_user = User(
        username=user_data.username,
        password_hashed=hashed_pw,
        user_role_id=user_role.user_role_id
    )

    if user_data.user_info:
        db_user.user_info = UserInfo(
            user_id=db_user.id,
            name=user_data.user_info.name,
            birthday=user_data.user_info.birthday,
            address=user_data.user_info.address,
            phone=user_data.user_info.phone,
            email=user_data.user_info.email
        )
    
    default_level = db.query(LevelType).first()
    
    db_user.user_statistic = UserStatistic(
        user_id=db_user.id,
        level_id=default_level.level_id,
        problem_solved=0,
        score=0
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(user_data)
    global_room = db.query(RoomChat).filter(RoomChat.room_name=="Global Room").first() 
    if global_room:
        user_room_role = db.query(UserRoomRole).filter(UserRoomRole.user_room_role_name=="Member").first()
        if user_room_role:
            new_user_room = UserRoom(
                room_chat_id=global_room.room_chat_id,
                user_id=db_user.id,
                user_room_role_id=user_room_role.user_room_role_id
            )
            db.add(new_user_room)
            db.commit()
            db.refresh(new_user_room)
            
    return db_user


def get_all_users(db: Session):
    return (
        db.query(User)
        .options(joinedload(User.user_role), joinedload(User.user_info))
        .all()
    )
    

def get_all_user_roles(db: Session):
    return (
        db.query(UserRole)
        .options(joinedload(UserRole.users))
        .all()
    )

def create_user_role(db: Session, role_data: model.UserRoleCreate) -> UserRole:
    
    existed_user_role =  db.query(UserRole).filter(UserRole.user_role_name == role_data.user_role_name).first()
    if existed_user_role:
        return None
    new_user_role = UserRole(
        user_role_name=role_data.user_role_name,
        user_role_description=role_data.user_role_description
    )
    db.add(new_user_role)
    db.commit()
    db.refresh(new_user_role)
    return new_user_role

    
def update_user_role(db: Session, role_id: int, role_data: model.UserRoleUpdate):
    db_role = db.query(UserRole).filter(UserRole.user_role_id == role_id).first()
    if not db_role:
        return None
    for key, value in role_data.model_dump(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_user_role(db: Session, role_id: int):
    db_role = db.query(UserRole).filter(UserRole.user_role_id == role_id).first()
    if not db_role:
        return False
    try:
        db.delete(db_role)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False


def get_user_by_id(db: Session, user_id: UUID):
    return (
        db.query(User)
        .options(joinedload(User.user_role), joinedload(User.user_info), joinedload(User.user_statistic))
        .filter(User.id == user_id)
        .first()
    )
    
def get_user_by_username(db: Session, username: str):
    return (
        db.query(User)
        .options(joinedload(User.user_role), joinedload(User.user_info), joinedload(User.user_statistic))
        .filter(User.username == username)
        .first()
    )


def update_user_password(db: Session, user_id: UUID, password_data: model.UserPasswordUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    if not verify_password(password_data.current_password_hashed, db_user.password_hashed):
        return None 
    
    db_user.password_hashed = get_password_hash(password_data.password_hashed)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, user_data: model.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    # --- Cập nhật các field cơ bản ---
    if user_data.username is not None:
        db_user.username = user_data.username
    if user_data.is_enabled is not None:
        db_user.is_enabled = user_data.is_enabled

    # --- Cập nhật user_role_id và liên kết với bảng UserRole ---
    if user_data.user_role_id is not None:
        new_role = db.query(UserRole).filter(UserRole.user_role_id == user_data.user_role_id).first()
        if not new_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User role ID {user_data.user_role_id} not found"
            )
        db_user.user_role_id = new_role.user_role_id

        db_user.user_role = new_role

    # --- Cập nhật user_info ---
    if user_data.user_info is not None:
        info_data = user_data.user_info.model_dump(exclude_unset=True)
        if db_user.user_info:
            for field, value in info_data.items():
                setattr(db_user.user_info, field, value)
        else:
            db_user.user_info = UserInfo(**info_data)

    # --- Cập nhật user_statistic ---
    if user_data.user_statistic is not None:
        stat_data = user_data.user_statistic.model_dump(exclude_unset=True)
        if db_user.user_statistic:
            for field, value in stat_data.items():
                setattr(db_user.user_statistic, field, value)
        else:
            db_user.user_statistic = UserStatistic(
                user_id=user_id,
                **stat_data
            )

    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_stat(db: Session, user_id: UUID, stat_data: model.StatUpdate):
    """
    Cập nhật thống kê người dùng:
    - Cộng thêm điểm và số bài toán đã giải.
    - Kiểm tra, nâng cấp level nếu đạt đủ điểm.
    Mỗi 200 điểm = 1 cấp độ. Nếu level chưa tồn tại thì tự tạo.
    """
    user_stat = db.query(UserStatistic).filter(UserStatistic.user_id == user_id).first()
    if not user_stat:
        raise ValueError("Không tìm thấy thống kê người dùng")

    # ✅ Cộng thêm điểm và bài toán đã giải
    user_stat.score += stat_data.added_score
    user_stat.problem_solved += stat_data.added_solved

    # ✅ Tính lại cấp độ
    new_level_id = (user_stat.score // 200) + 1  # chia nguyên mỗi 200 điểm lên 1 level

    if user_stat.level_id != new_level_id:
        level = db.query(LevelType).filter(LevelType.level_id == new_level_id).first()
        if not level:
            level = LevelType(
                level_id=new_level_id,
                level_name=f"Level {new_level_id}",
                level_description=f"Đạt {new_level_id * 200} điểm trở lên"
            )
            db.add(level)
            db.flush()  # lấy id ngay sau khi insert

        user_stat.level_id = level.level_id

    db.commit()
    db.refresh(user_stat)
    return user_stat



def delete_user(db: Session, user_id: UUID) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

# ========================= SYSTEM STATISTICS =========================
def get_system_statistics(db: Session):
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_rooms = db.query(func.count(RoomChat.room_chat_id)).scalar() or 0
    total_messages = db.query(func.count(Message.message_id)).scalar() or 0
    total_questions = db.query(func.count(Question.id)).scalar() or 0

    # --- avg users per room ---
    subquery = (
        db.query(
            UserRoom.room_chat_id,
            func.count(UserRoom.user_id).label("user_count")
        )
        .group_by(UserRoom.room_chat_id)
        .subquery()
    )
    avg_users_per_room = db.query(func.avg(subquery.c.user_count)).scalar() or 0

    total_score = db.query(func.sum(UserStatistic.score)).scalar() or 0
    avg_score = db.query(func.avg(UserStatistic.score)).scalar() or 0

    return {
        "total_users": total_users,
        "total_rooms": total_rooms,
        "total_messages": total_messages,
        "total_questions": total_questions,
        "average_users_per_room": round(float(avg_users_per_room), 2),
        "total_score": total_score,
        "average_user_score": round(float(avg_score), 2),
    }

# ========================= USER STATISTICS =========================
def get_user_statistics(db: Session, user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    stat = user.user_statistic
    score = stat.score if stat else 0
    problem_solved = stat.problem_solved if stat else 0
    
    print(stat)
    print(stat.level_type.level_name)

    return {
        "user_id": str(user.id),
        "username": user.username,
        "role": user.user_role.user_role_name if user.user_role else None,
        "total_score": score,
        "problem_solved": problem_solved,
        "level": stat.level_type.level_name if stat and stat.level_type else None,
    }

# ========================= ROOM STATISTICS =========================
def get_room_statistics(db: Session, room_chat_id: UUID):
    room = db.query(RoomChat).filter(RoomChat.room_chat_id == room_chat_id).first()
    if not room:
        return None

    total_users = (
        db.query(func.count(UserRoom.user_id))
        .filter(UserRoom.room_chat_id == room_chat_id)
        .scalar()
        or 0
    )

    total_messages = (
        db.query(func.count(Message.message_id))
        .filter(Message.room_chat_id == room_chat_id)
        .scalar()
        or 0
    )

    return {
        "room_chat_id": str(room_chat_id),
        "room_name": room.room_name,
        "room_type": room.room_type.room_type_name if room.room_type else None,
        "total_users": total_users,
        "total_messages": total_messages,
        "created_at": str(room.created_at),
        "updated_at": str(room.updated_at),
    }