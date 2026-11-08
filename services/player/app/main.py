"""Microserviço responsável por jogadores e pontuação."""
from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel,Field
from . import db
app=FastAPI(title="EcoMissão Player Service",version="1.0.0")
class PlayerCreate(BaseModel): name:str=Field(min_length=2,max_length=40)
class ScoreUpdate(BaseModel):
    delta:int=Field(ge=0,le=100)
    reason:str=Field(default="rodada",max_length=80)
@app.on_event("startup")
def startup()->None: db.init_db()
@app.get("/health")
def health()->dict[str,str]: return {"service":"player-service","status":"ok"}
@app.post("/players")
def create_player(payload:PlayerCreate)->dict: return db.create_player(payload.name)
@app.get("/players/{player_id}")
def get_player(player_id:int)->dict:
    try:return db.get_player(player_id)
    except KeyError as exc: raise HTTPException(status_code=404,detail="Jogador não encontrado") from exc
@app.post("/players/{player_id}/score")
def score(player_id:int,payload:ScoreUpdate)->dict:
    try:return db.update_score(player_id,payload.delta)
    except KeyError as exc: raise HTTPException(status_code=404,detail="Jogador não encontrado") from exc
@app.get("/leaderboard")
def get_leaderboard(limit:int=Query(default=10,ge=1,le=50))->dict: return {"players":db.leaderboard(limit)}
