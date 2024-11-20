from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.test import validate_item_exists, generate_new_id
from typing import Union
from utils.test_chatbot import dummy_chatbot
# FastAPI 앱 생성
app = FastAPI(
    title="Vue.js Integration Backend",
    description="This FastAPI server acts as the backend for a Vue.js frontend.",
    version="1.0.0"
)

# 데이터 모델 정의 (Pydantic)
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    available: bool

# 임시 데이터 저장소
fake_db = {}

# ----------------- HTTP 메서드 예제 ------------------

#0. 기본

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ask")
def read_item(ask_query: str):
    chatbot = dummy_chatbot(ask_query)  # 클래스 인스턴스 생성
    answer = chatbot.reuturn_ANS()  # 인스턴스 메서드 호출
    return {"answer": answer}

# 1. GET - 데이터 조회
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return validate_item_exists(item_id, fake_db)

# 2. POST - 데이터 생성
@app.post("/items")
def create_item(item: Item):
    new_id = generate_new_id(fake_db)
    item.id = new_id
    fake_db[new_id] = item.dict()
    return {"message": "Item created successfully", "item": fake_db[new_id]}

# 3. PUT - 데이터 전체 업데이트
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    validate_item_exists(item_id, fake_db)
    item.id = item_id
    fake_db[item_id] = item.dict()
    return {"message": "Item updated successfully", "item": fake_db[item_id]}

# 4. PATCH - 데이터 부분 업데이트
@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, name: Optional[str] = None, price: Optional[float] = None):
    item = validate_item_exists(item_id, fake_db)
    if name:
        item["name"] = name
    if price:
        item["price"] = price
    fake_db[item_id] = item
    return {"message": "Item partially updated", "item": fake_db[item_id]}

# 5. DELETE - 데이터 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    validate_item_exists(item_id, fake_db)
    del fake_db[item_id]
    return {"message": "Item deleted successfully"}

# 6. Health Check (Vue.js와 연결 테스트)
@app.get("/health")
def health_check():
    return {"status": "Backend is up and running"}
