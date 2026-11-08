"""Componente de persistência do Player Service usando SQLite."""
from __future__ import annotations
import os, sqlite3
from pathlib import Path
from typing import Any
DB_PATH=os.getenv("PLAYER_DB",str(Path(__file__).resolve().parent/"players.db"))
def connect()->sqlite3.Connection:
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db()->None:
    with connect() as c: c.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,score INTEGER NOT NULL DEFAULT 0,rounds INTEGER NOT NULL DEFAULT 0)")
def create_player(name:str)->dict[str,Any]:
    with connect() as c: pid=int(c.execute("INSERT INTO players(name,score,rounds) VALUES (?,0,0)",(name.strip(),)).lastrowid)
    return get_player(pid)
def get_player(player_id:int)->dict[str,Any]:
    with connect() as c: row=c.execute("SELECT * FROM players WHERE id=?",(player_id,)).fetchone()
    if row is None: raise KeyError(player_id)
    return dict(row)
def update_score(player_id:int,delta:int)->dict[str,Any]:
    with connect() as c:
        cur=c.execute("UPDATE players SET score=MAX(0,score+?),rounds=rounds+1 WHERE id=?",(delta,player_id))
        if cur.rowcount==0: raise KeyError(player_id)
    return get_player(player_id)
def leaderboard(limit:int=10)->list[dict[str,Any]]:
    with connect() as c: rows=c.execute("SELECT * FROM players ORDER BY score DESC,rounds ASC,id ASC LIMIT ?",(limit,)).fetchall()
    return [dict(r) for r in rows]
