CATEGORIES=["água","energia","resíduos","mobilidade","consumo"]
def recommend(score:int,streak:int,last_result:bool|None,category:str|None)->dict:
    if score<40: level="iniciante"; message="Vamos por partes: procure a alternativa que reduz desperdício sem complicar a rotina."
    elif score<100: level="intermediário"; message="Bom progresso! Compare impacto imediato e hábito de longo prazo antes de escolher."
    else: level="avançado"; message="Excelente desempenho. Tente justificar mentalmente por que sua escolha é sustentável."
    if last_result is False: message="Errar também ensina. Leia o feedback e tente identificar qual recurso poderia ser poupado."
    elif streak>=3: message="Sequência ótima! Mantenha a atenção e experimente uma categoria diferente."
    suggested=CATEGORIES[(CATEGORIES.index(category)+1)%len(CATEGORIES)] if category in CATEGORIES else CATEGORIES[score%len(CATEGORIES)]
    confidence=0.70 if score<40 else 0.82 if score<100 else 0.90
    return {"agent":"EcoGuia","level":level,"message":message,"suggested_category":suggested,"confidence":confidence,"explanation":f"Regra baseada em score={score}, streak={streak} e último resultado={last_result}."}
