from fastapi import FastAPI
from src.database.core import engine, Base, setup_database
from src.routes import api_router
from src.database.seed import seed_data
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from src.modules.message.socket_io import websocket_endpoint

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # hoặc đọc từ .env
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

async def lifespan(app: FastAPI):
    # Logic startup
    try:
        if not os.path.exists('.setup_complete'):
            setup_database()
            seed_data()
            with open('.setup_complete', 'w') as f:
                f.write('1')
    except Exception as e:
        print(f"Error during startup setup at {datetime.now().date()}: {e}")
    
    # Yield để chuyển sang giai đoạn running
    yield

app = FastAPI(lifespan=lifespan)

setup_cors(app)

app.add_api_websocket_route("/ws", websocket_endpoint)

app.include_router(api_router)
