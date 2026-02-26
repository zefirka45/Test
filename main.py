from fastapi import FastAPI, HTTPException
from models import UserRequest, APIResponse
from graph import app_graph

app = FastAPI(title="Synonyms & Antonyms API")

@app.post("/get-words", response_model=APIResponse)
async def get_words(request: UserRequest):
    # Подготовка начального состояния для графа
    initial_state = {
        "word": request.word,
        "kind": request.type.value,
        "result": []
    }
    
    try:
        # Запуск графа
        # invoke возвращает финальное состояние
        final_state = app_graph.invoke(initial_state)
        
        if not final_state.get("result"):
            raise HTTPException(status_code=500, detail="LLM не вернул результат")
            
        return APIResponse(data=final_state["result"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)