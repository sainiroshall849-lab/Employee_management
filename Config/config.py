import os

# SQLite for development (no setup required)
DATABASE_URL = "sqlite:///./employee.db"

# Uncomment below to use MySQL instead
# DB_USER = "root"
# DB_PASSWORD = "password"
# DB_HOST = "localhost"
# DB_NAME = "employee_db"
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"