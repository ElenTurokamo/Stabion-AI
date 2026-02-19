from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import create_sql_agent
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Разрешаем React'у стучаться к нам
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Подключаем базу
db = SQLDatabase.from_uri("sqlite:///crm.db")

# 2. LLM через Ollama
llm = ChatOllama(
    model="deepseek-r1:8b", 
    streaming=True,
    temperature=0)

# 3. SQL agent БЕЗ tool-calling (текстовый ReAct)
agent_executor = create_sql_agent(
    llm,
    db=db,
    agent_type="zero-shot-react-description",
    verbose=True
)

class ChatRequest(BaseModel):
    text: str

def is_crm_question(text: str) -> bool:
    t = text.lower()
    # ключевые слова/паттерны под ваш домен
    keywords = [
        "заявк", "клиент", "договор", "счёт", "оплат", "контакт",
        "crm", "лид", "воронк", "заказ", "ремонт", "статус", "менеджер"
    ]
    if any(k in t for k in keywords):
        return True
    # простая эвристика: вопросы “покажи/сколько/список” часто про БД
    if re.search(r"\b(сколько|покажи|список|найди|выведи)\b", t):
        return True
    return False

@app.post("/chat")
async def chat(payload: ChatRequest):
    try:
        user_text = payload.text.strip()

        if is_crm_question(user_text):
            response = agent_executor.invoke({"input": user_text})
            reply = response.get("output", str(response))
            return {"reply": reply, "mode": "sql_agent"}
        else:
            # обычный чат-ответ (не про БД)
            resp = llm.invoke(user_text)
            return {"reply": resp.content, "mode": "general_llm"}

    except Exception as e:
        # лучше возвращать 500, но оставлю ваш формат
        return {"reply": f"Ошибка: {str(e)}", "mode": "error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)