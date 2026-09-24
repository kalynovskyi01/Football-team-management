"""Application configuration, read once from environment variables / .env."""
import os
from dotenv import load_dotenv
import psycopg2
from fastapi import HTTPException
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from typing import Iterator
import logging

# DB connections
DATABASE_URL = os.getenv("DBURL")
# If API is in production the documentation will not be public
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "Production"

logger = logging.getLogger(__name__)

#Concection to the db with iterator
# yields a connection and always closes it afterwards
def get_db_connection() -> Iterator[connection]:
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500,
            detail="Database connection error: DBURL environment variable is not set.",
        )
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    except psycopg2.Error:
        logger.exception("Could not connect to the database")
        raise HTTPException(status_code=500, detail="Database connection error.")

    try:
        yield conn
    finally:
        conn.close()