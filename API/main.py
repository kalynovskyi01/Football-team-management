import os
from typing import List, Optional
from dotenv import load_dotenv
from datetime import date
from fastapi import FastAPI, HTTPException, Query
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, field_serializer


# DB connections
DATABASE_URL = os.getenv("DBURL")

## If API is in production the documentation will not be public
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "Production"

app = FastAPI(
    title="Football team API",
    description="API for fetching football team players",
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json"
)


def get_db_connection():
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500, 
            detail="Database connection error: DBURL environment variable is not set."
        )
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")



# --- PYDANTIC SCHEMAS ---

class PlayerSchema(BaseModel):
    id: int
    name: str
    number: Optional[int] = None
    position: Optional[str] = None
    #image_url: Optional[str] = None
    citizenship: Optional[List[str]] = None
    #citizenship_flag_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[int] = None

    @field_serializer("citizenship")
    def serialize_citizenship(self, value: Optional[List[str]]) -> Optional[str]:
        if value is None:
            return None
        return ", ".join(value)


# --- PLAYERS ENDPOINTS ---

@app.get("/players", response_model=List[PlayerSchema], tags=["Players"])
def get_all_players(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    """Get all players with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT id, name, number, position, citizenship, 
                date_of_birth, height, weight
        FROM players
        ORDER BY id ASC
        LIMIT %s OFFSET %s;
    """
    cur.execute(query, (limit, offset))
    players = cur.fetchall()

    cur.close()
    conn.close()
    return players


@app.get("/player/id/{player_id}", response_model=PlayerSchema, tags=["Players"])
def get_player_by_id(player_id: int):
    """Get a single player by ID."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT id, name, number, position, citizenship, 
                date_of_birth, height, weight
        FROM players
        WHERE id = %s;
    """
    cur.execute(query, (player_id,))
    player = cur.fetchone()

    cur.close()
    conn.close()

    if not player:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found.")

    return player


@app.get("/players/position/{position_name}", response_model=List[PlayerSchema], tags=["Players"])
def get_players_by_position(position_name: str):
    """Get all players filtered by position (e.g., Forward, Midfielder, Defender, Goalkeeper)."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT id, name, number, position, citizenship, 
                date_of_birth, height, weight
        FROM players
        WHERE position ILIKE %s
        ORDER BY number ASC NULLS LAST;
    """
    search_term = f"%{position_name}%"
    cur.execute(query, (search_term,))
    players = cur.fetchall()

    cur.close()
    conn.close()
    return players

@app.get("/player/number/{number}", response_model=PlayerSchema, tags=["Players"])
def get_players_by_number(number: int):
    """Get a signal player filtered by squad number."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT id, name, number, position, citizenship, 
                date_of_birth, height, weight
        FROM players
        WHERE number = %s
    """
    cur.execute(query, (number,))
    player = cur.fetchone()

    cur.close()
    conn.close()

    if not player:
        raise HTTPException(status_code=404, detail=f"Player with squad number {number} not found.")

    return player

@app.get("/players/name/{player_name}", response_model=List[PlayerSchema], tags=["Players"])
def get_players_by_name(player_name: str):
    """Get players whose name matches (partial, case-insensitive)."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT id, name, number, position, citizenship,
               date_of_birth, height, weight
        FROM players
        WHERE name ILIKE %s
    """
    cur.execute(query, (f"%{player_name}%",))
    players = cur.fetchall()

    cur.close()
    conn.close()

    return players