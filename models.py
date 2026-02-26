from pydantic import BaseModel, Field
from typing import List, Literal
from enum import Enum

# Допустимые типы запроса
class WordType(str, Enum):
    SYNONYM = "synonym"
    ANTONYM = "antonym"

# Запрос от пользователя
class UserRequest(BaseModel):
    word: str = Field(..., description="Слово для поиска")
    type: WordType = Field(..., description="Тип: synonym или antonym")

# Ожидаемая структура ответа от LLM (для структурированного вывода)
class WordItem(BaseModel):
    word: str = Field(..., description="Найденное слово")
    type: str = Field(..., description="Тип слова (synonym или antonym)")

class LLMResponse(BaseModel):
    items: List[WordItem] = Field(..., description="Список из 10 слов")

# Ответ API пользователю
class APIResponse(BaseModel):
    status: str = "success"
    data: List[WordItem]