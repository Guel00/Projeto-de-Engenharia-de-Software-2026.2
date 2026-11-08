"""API Gateway do EcoMissão.

Centraliza o acesso do frontend aos microserviços e implementa o fluxo de jogo.
"""
from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

PLAYER_URL = os.getenv("PLAYER_SERVICE_URL", "http://127.0.0.1:8001")
GAME_URL = os.getenv("GAME_SERVICE_URL", "http://127.0.0.1:8002")
AGENT_URL = os.getenv("AGENT_SERVICE_URL", "http://127.0.0.1:8003")
TIMEOUT = 4.0

app = FastAPI(title="EcoMissão API Gateway", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

class StartRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40)

class AnswerRequest(BaseModel):
    player_id: int
    challenge_id: str
    option_id: str
    streak: int = Field(default=0, ge=0)

async def request_json(method: str, url: str, **kwargs: Any) -> dict[str, Any] | list[Any]:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise HTTPException(status_code=503, detail=f"Serviço indisponível: {url}") from exc

@app.get("/health")
async def health() -> dict[str, str]:
    return {"service": "gateway", "status": "ok"}

@app.get("/api/services")
async def services_status() -> dict[str, list[dict[str, str]]]:
    services = [("API Gateway", "gateway", None),("Player Service", "player-service", f"{PLAYER_URL}/health"),("Game Service", "game-service", f"{GAME_URL}/health"),("EcoGuia Agent", "agent-service", f"{AGENT_URL}/health")]
    result=[]
    for display_name,key,url in services:
        if url is None: status="online"
        else:
            try:
                data=await request_json("GET",url)
                status="online" if isinstance(data,dict) and data.get("status")=="ok" else "degradado"
            except HTTPException: status="offline"
        result.append({"name":display_name,"id":key,"status":status})
    return {"services":result}

@app.post("/api/start")
async def start_game(payload: StartRequest) -> dict[str, Any]:
    player=await request_json("POST",f"{PLAYER_URL}/players",json=payload.model_dump())
    return {"player":player,"message":"Missão iniciada!"}

@app.get("/api/challenge")
async def get_challenge(player_id: int = Query(..., ge=1), exclude: str | None = None) -> dict[str, Any]:
    await request_json("GET",f"{PLAYER_URL}/players/{player_id}")
    params={"exclude":exclude} if exclude else None
    challenge=await request_json("GET",f"{GAME_URL}/challenge",params=params)
    return {"challenge":challenge}

@app.post("/api/answer")
async def answer(payload: AnswerRequest) -> dict[str, Any]:
    evaluation=await request_json("POST",f"{GAME_URL}/evaluate",json={"challenge_id":payload.challenge_id,"option_id":payload.option_id})
    if not isinstance(evaluation,dict): raise HTTPException(status_code=502,detail="Resposta inválida do Game Service")
    player=await request_json("POST",f"{PLAYER_URL}/players/{payload.player_id}/score",json={"delta":int(evaluation.get("points",0)),"reason":"desafio sustentável"})
    if not isinstance(player,dict): raise HTTPException(status_code=502,detail="Resposta inválida do Player Service")
    recommendation=await request_json("POST",f"{AGENT_URL}/recommend",json={"score":int(player.get("score",0)),"streak":payload.streak,"last_result":bool(evaluation.get("correct")),"category":evaluation.get("category")})
    return {"evaluation":evaluation,"player":player,"agent":recommendation}

@app.get("/api/player/{player_id}")
async def get_player(player_id: int) -> dict[str, Any] | list[Any]:
    return await request_json("GET",f"{PLAYER_URL}/players/{player_id}")
