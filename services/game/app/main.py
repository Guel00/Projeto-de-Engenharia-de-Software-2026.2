from itertools import cycle
from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel
from .challenges import CHALLENGES
app=FastAPI(title="EcoMissão Game Service",version="1.0.0"); _challenge_cycle=cycle(CHALLENGES)
class EvaluationRequest(BaseModel): challenge_id:str; option_id:str
def public_challenge(c:dict)->dict: return {"id":c["id"],"category":c["category"],"title":c["title"],"question":c["question"],"options":[{"id":o["id"],"text":o["text"]} for o in c["options"]]}
@app.get("/health")
def health(): return {"service":"game-service","status":"ok"}
@app.get("/challenges")
def challenges(): return {"challenges":[public_challenge(i) for i in CHALLENGES]}
@app.get("/challenge")
def challenge(exclude:str|None=Query(default=None)):
    for _ in range(len(CHALLENGES)):
        c=next(_challenge_cycle)
        if c["id"]!=exclude:return public_challenge(c)
    return public_challenge(CHALLENGES[0])
@app.post("/evaluate")
def evaluate(payload:EvaluationRequest):
    c=next((i for i in CHALLENGES if i["id"]==payload.challenge_id),None)
    if c is None: raise HTTPException(status_code=404,detail="Desafio não encontrado")
    o=next((i for i in c["options"] if i["id"]==payload.option_id),None)
    if o is None: raise HTTPException(status_code=400,detail="Opção inválida")
    return {"challenge_id":c["id"],"category":c["category"],"correct":payload.option_id==c["best_option"],"points":o["points"],"feedback":c["feedback"],"best_option":c["best_option"]}
