import os

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")  # schimbă în prod
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Database (dacă îți trebuie și în database.py)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")