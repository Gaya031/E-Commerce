import os


os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/rushcart_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("SECRET_KEY", "test-secret-key-with-at-least-32-bytes")
os.environ.setdefault("ADMIN_EMAIL", "admin@rushcart.local")
os.environ.setdefault("ADMIN_PASSWORD", "ChangeThisAdminPassword123!")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")
