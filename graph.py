from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from models import WordItem, LLMResponse
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Определение состояния графа
class GraphState(TypedDict):
    word: str
    kind: str
    result: List[dict]

# 2. Инициализация модели
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 3. Функция узла (Node)
def generate_words_node(state: GraphState) -> GraphState:
    word = state["word"]
    kind = state["kind"]
    
    # Создаем промпт (убраны пробелы в ключах ролей)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Ты лингвистический ассистент. Твоя задача - предоставить ровно 10 {kind} к слову."),
        ("user", "Слово: {word}. Верни ответ строго в формате JSON списка объектов с полями 'word' и 'type'.")
    ])

    # Используем with_structured_output для гарантии JSON формата
    structured_llm = llm.with_structured_output(LLMResponse)
    chain = prompt | structured_llm

    try:
        # Исправлено: ключи без пробелов соответствуют плейсхолдерам в промпте
        response = chain.invoke({"word": word, "kind": kind})
        
        # Преобразуем Pydantic модели в словари
        result_data = [item.model_dump() for item in response.items]
        
        # Исправлено: ключ 'result' без пробела
        return {"result": result_data}
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"result": []}

# 4. Построение графа
def build_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("generator", generate_words_node)
    workflow.add_edge(START, "generator")
    workflow.add_edge("generator", END)
    return workflow.compile()

app_graph = build_graph()