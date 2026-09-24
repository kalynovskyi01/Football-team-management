"""Player endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from psycopg2.extensions import connection

from app.dbconfig.config import get_db_connection
from app.repository import repository_player as repo
from app.models.model import PlayerSchema

router = APIRouter(tags=["Players"])


@router.get("/players", response_model=List[PlayerSchema])
def get_all_players(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    conn: connection = Depends(get_db_connection),
):
    """Get all players with pagination."""
    return repo.get_all(conn, limit, offset)


@router.get("/player/id/{player_id}", response_model=PlayerSchema)
def get_player_by_id(player_id: int, conn: connection = Depends(get_db_connection)):
    """Get a single player by ID."""
    player = repo.get_by_id(conn, player_id)
    if not player:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found.")
    return player


@router.get("/players/position/{position_name}", response_model=List[PlayerSchema])
def get_players_by_position(position_name: str, conn: connection = Depends(get_db_connection)):
    """Get all players filtered by position (e.g., Forward, Midfielder, Defender, Goalkeeper)."""
    return repo.search_by_position(conn, position_name)


@router.get("/player/number/{number}", response_model=PlayerSchema)
def get_player_by_number(number: int, conn: connection = Depends(get_db_connection)):
    """Get a single player filtered by squad number."""
    player = repo.get_by_number(conn, number)
    if not player:
        raise HTTPException(status_code=404, detail=f"Player with squad number {number} not found.")
    return player


@router.get("/players/name/{player_name}", response_model=List[PlayerSchema])
def get_players_by_name(player_name: str, conn: connection = Depends(get_db_connection)):
    """Get players whose name matches (partial, case-insensitive)."""
    return repo.search_by_name(conn, player_name)
