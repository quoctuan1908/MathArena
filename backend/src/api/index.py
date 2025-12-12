from main import app
from vercel_fastapi import VercelASGI

handler = VercelASGI(app)