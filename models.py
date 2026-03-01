from pydantic import BaseModel, Field
from typing import List, Literal
from enum import Enum

# Допустимые типы запроса
class UserRequest(BaseModel):
    word: str = Field(..., description="Слово для поиска")

# Запрос от пользователя
class WordItem(BaseModel):
    word: str = Field(..., description="Найденное слово")
    type: str = Field(..., description="Тип слова: 'synonym' или 'antonym'")

# Ожидаемая структура ответа от LLM (для структурированного вывода)
class LLMResponse(BaseModel):
    items: List[WordItem] = Field(..., description="Список из 20 слов (10 синонимов и 10 антонимов)")


# Ответ API пользователю
class APIResponse(BaseModel):
    status: str = "success"
    data: List[WordItem]