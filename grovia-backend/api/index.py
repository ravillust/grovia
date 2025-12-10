from fastapi import FastAPI
from app.main import app as fastapi_app

# Vercel expects an 'app' object at the root
app = fastapi_app
