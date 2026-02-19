from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import create_sql_agent
from fastapi.middleware.cors import CORSMiddleware

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

# 2. Подключаем DeepSeek (укажи модель: deepseek-r1 или deepseek-r1:1.5b)
llm = ChatOllama(model="deepseek-r1", temperature=0)

# 3. Создаем агента (он умнее, чем просто цепочка)
# Агент сам поймет: нужно ли лезть в базу или просто ответить "Привет"
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

class Query(BaseModel):
    text: str

@app.post("/chat")
async def chat(query: Query):
    # Передаем вопрос агенту
    # handle_parsing_errors=True помогает, если DeepSeek чуть ошибся в формате
    try:
        response = agent_executor.invoke(query.text)
        return {"reply": response["output"]}
    except Exception as e:
        return {"reply": f"Ошибка: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)