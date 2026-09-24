"""All SQL for the `players` table lives here.

Functions take an open connection and return plain dicts (RealDictCursor),
so the routers never have to know about SQL.
"""
from typing import Optional

from psycopg2.extensions import connection

# Constant, never built from user input -> safe to interpolate into the queries.
_COLUMNS = "id, name, number, position, citizenship, date_of_birth, height, weight"


def get_all(conn: connection, limit: int, offset: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT {_COLUMNS} FROM players ORDER BY id ASC LIMIT %s OFFSET %s;",
            (limit, offset),
        )
        return cur.fetchall()


def get_by_id(conn: connection, player_id: int) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute(f"SELECT {_COLUMNS} FROM players WHERE id = %s;", (player_id,))
        return cur.fetchone()


def get_by_number(conn: connection, number: int) -> Optional[dict]:
    with conn.cursor() as cur:
        cur.execute(f"SELECT {_COLUMNS} FROM players WHERE number = %s;", (number,))
        return cur.fetchone()


def search_by_position(conn: connection, position: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT {_COLUMNS} FROM players "
            "WHERE position ILIKE %s ORDER BY number ASC NULLS LAST;",
            (f"%{position}%",),
        )
        return cur.fetchall()


def search_by_name(conn: connection, name: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT {_COLUMNS} FROM players WHERE name ILIKE %s;",
            (f"%{name}%",),
        )
        return cur.fetchall()
