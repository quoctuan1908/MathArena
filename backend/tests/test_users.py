import os
import pytest
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from dotenv import load_dotenv
from uuid import uuid4, UUID
from datetime import date
import pytest_asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app
from src.database.core import Base, get_db
from src.entities import User, UserInfo, UserRole, UserStatistic, LevelType
from src.modules.user.service import get_password_hash

# Load .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL_TEST")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME_TEST")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD_TEST")

# Kết nối DB thật
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest_asyncio.fixture
async def setup_db():
    # Tạo các bảng trong cơ sở dữ liệu
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest_asyncio.fixture
async def sample_user(db: Session = next(override_get_db())):
    # Tạo dữ liệu mẫu
    level = LevelType(
        level_id=uuid4(),
        level_name="Beginner",
        level_description="Entry level"
    )
    role = UserRole(
        user_role_id=uuid4(),
        user_role_name="User",
        user_role_description="Regular user"
    )
    user = User(
        id=uuid4(),
        username="testuser",
        password_hashed="$2b$12$abcdefghijklmnopqrstuv",  # Mật khẩu giả
        is_enabled=True,
        role_id=role.user_role_id
    )
    user_info = UserInfo(
        user_id=user.id,
        name="Test User",
        birthday=date(1990, 1, 1),
        address="123 Test St",
        phone="1234567890",
        email="test@example.com"
    )
    user_statistic = UserStatistic(
        user_id=user.id,
        level_id=level.level_id,
        problem_solved=10,
        score=100
    )
    db.add_all([level, role, user, user_info, user_statistic])
    db.commit()
    return user

@pytest.mark.asyncio
async def test_create_user(setup_db):
    user_data = {
        "username": "newuser",
        "password_hashed": "password123",
        "is_enabled": True,
        "user_info": {
            "name": "New User",
            "birthday": "1995-05-05",
            "address": "456 New St",
            "phone": "0987654321",
            "email": "newuser@example.com"
        },
        "role_id": str(uuid4())
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["user_info"] is not None
    assert data["user_info"]["name"] == "New User"
    assert data["user_info"]["email"] == "newuser@example.com"
    assert data["user_statistic"] is not None
    assert data["user_statistic"]["problem_solved"] == 0
    assert data["user_statistic"]["score"] == 0
    assert UUID(data["id"])  # Kiểm tra id là UUID hợp lệ

@pytest.mark.asyncio
async def test_create_user_without_user_info(setup_db):
    user_data = {
        "username": "newuser2",
        "password_hashed": "password123",
        "is_enabled": True,
        "role_id": str(uuid4())
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser2"
    assert data["user_info"] is not None  # UserInfo luôn được tạo
    assert data["user_info"]["name"] is None
    assert data["user_statistic"] is not None  # UserStatistic luôn được tạo
    assert data["user_statistic"]["problem_solved"] == 0
    assert data["user_statistic"]["score"] == 0

@pytest.mark.asyncio
async def test_create_user_duplicate_username(setup_db, sample_user):
    user_data = {
        "username": "testuser",  # Trùng với sample_user
        "password_hashed": "password123",
        "is_enabled": True
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"

@pytest.mark.asyncio
async def test_list_users(setup_db, sample_user):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "testuser"
    assert data[0]["user_info"]["name"] == "Test User"
    assert data[0]["user_statistic"]["problem_solved"] == 10

@pytest.mark.asyncio
async def test_list_user_roles(setup_db, sample_user):
    response = client.get("/users/roles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_role_name"] == "User"
    assert UUID(data[0]["user_role_id"])  # Kiểm tra id là UUID hợp lệ

@pytest.mark.asyncio
async def test_update_user_role(setup_db, sample_user, db: Session = next(override_get_db())):
    role_id = sample_user.role_id
    role_data = {
        "user_role_name": "Updated User",
        "user_role_description": "Updated description"
    }
    response = client.put(f"/users/roles/{role_id}", json=role_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_role_name"] == "Updated User"
    assert data["user_role_description"] == "Updated description"

@pytest.mark.asyncio
async def test_update_user_role_not_found(setup_db):
    role_data = {
        "user_role_name": "Nonexistent Role"
    }
    response = client.put(f"/users/roles/{uuid4()}", json=role_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"

@pytest.mark.asyncio
async def test_delete_user_role(setup_db, sample_user):
    role_id = sample_user.role_id
    response = client.delete(f"/users/roles/{role_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"

@pytest.mark.asyncio
async def test_delete_user_role_not_found(setup_db):
    response = client.delete(f"/users/roles/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"

@pytest.mark.asyncio
async def test_get_user_statistic(setup_db, sample_user):
    user_id = sample_user.id
    response = client.get(f"/users/stat/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["problem_solved"] == 10
    assert data["score"] == 100

@pytest.mark.asyncio
async def test_get_user_statistic_not_found(setup_db):
    response = client.get(f"/users/stat/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_get_user_info(setup_db, sample_user):
    user_id = sample_user.id
    response = client.get(f"/users/info/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_info_not_found(setup_db):
    response = client.get(f"/users/info/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user_password(setup_db, sample_user):
    user_id = sample_user.id
    password_data = {
        "current_password_hashed": "password123",  # Giả sử mật khẩu đúng
        "password_hashed": "newpassword123"
    }
    response = client.put(f"/users/{user_id}/password", json=password_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user_id)

@pytest.mark.asyncio
async def test_update_user_password_invalid(setup_db, sample_user):
    user_id = sample_user.id
    password_data = {
        "current_password_hashed": "wrongpassword",
        "password_hashed": "newpassword123"
    }
    response = client.put(f"/users/{user_id}/password", json=password_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid current password or user not found"

@pytest.mark.asyncio
async def test_get_user(setup_db, sample_user):
    user_id = sample_user.id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["user_info"]["name"] == "Test User"
    assert data["user_statistic"]["problem_solved"] == 10

@pytest.mark.asyncio
async def test_get_user_not_found(setup_db):
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user(setup_db, sample_user):
    user_id = sample_user.id
    user_data = {
        "username": "updateduser",
        "is_enabled": False,
        "user_info": {
            "name": "Updated User",
            "email": "updated@example.com"
        }
    }
    response = client.put(f"/users/{user_id}", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
    assert data["is_enabled"] is False
    assert data["user_info"]["name"] == "Updated User"

@pytest.mark.asyncio
async def test_update_user_not_found(setup_db):
    user_data = {
        "username": "nonexistent"
    }
    response = client.put(f"/users/{uuid4()}", json=user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user(setup_db, sample_user):
    user_id = sample_user.id
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"

@pytest.mark.asyncio
async def test_delete_user_not_found(setup_db):
    response = client.delete(f"/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"