from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from models import WordItem, LLMResponse, WordType
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Определение состояния графа
class GraphState(TypedDict):
    word: str
    kind: str  # synonym или antonym
    result: List[dict]

# 2. Инициализация модели
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 3. Функция узла (Node)
def generate_words_node(state: GraphState) -> GraphState:
    word = state["word"]
    kind = state["kind"]
    
    # Создаем промпт
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Ты лингвистический ассистент. Твоя задача - предоставить ровно 10 {kind} к слову."),
        ("user", "Слово: {word}. Верни ответ строго в формате JSON списка объектов с полями 'word' и 'type'.")
    ])
    
    # Используем with_structured_output для гарантии JSON формата
    structured_llm = llm.with_structured_output(LLMResponse)
    
    chain = prompt | structured_llm
    
    try:
        response = chain.invoke({"word": word, "kind": kind})
        # Преобразуем Pydantic модели в словари для состояния
        result_data = [item.model_dump() for item in response.items]
        return {"result": result_data}
    except Exception as e:
        # В случае ошибки возвращаем пустой список или обрабатываем ошибку
        print(f"LLM Error: {e}")
        return {"result": []}

# 4. Построение графа
def build_graph():
    workflow = StateGraph(GraphState)
    
    # Добавляем узел
    workflow.add_node("generator", generate_words_node)
    
    # Добавляем ребра: Start -> Generator -> End
    workflow.add_edge(START, "generator")
    workflow.add_edge("generator", END)
    
    return workflow.compile()

# Экспортируем готовый граф
app_graph = build_graph()