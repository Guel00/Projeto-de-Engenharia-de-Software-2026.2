from fastapi import FastAPI
from pydantic import BaseModel,Field
from .agent import recommend
app=FastAPI(title="EcoMissão EcoGuia Agent",version="1.0.0")
class RecommendRequest(BaseModel):
    score:int=Field(ge=0); streak:int=Field(default=0,ge=0); last_result:bool|None=None; category:str|None=None
@app.get("/health")
def health(): return {"service":"agent-service","status":"ok"}
@app.post("/recommend")
def recommendation(payload:RecommendRequest): return recommend(payload.score,payload.streak,payload.last_result,payload.category)
