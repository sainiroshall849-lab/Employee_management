"""
Database configuration and session management for the Employee Management System.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from Config.config import DATABASE_URL

logger = logging.getLogger(__name__)

# Configure database engine with appropriate settings
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
pool_class = StaticPool if "sqlite" in DATABASE_URL else None

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        poolclass=pool_class,
        echo=False  # Set to True for SQL query logging
    )
    logger.info(f"Database engine created successfully: {DATABASE_URL}")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session.

    Yields:
        Database session

    Automatically closes session after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()