from fastapi import APIRouter, HTTPException
from app.database import fetch_query, execute_query

router = APIRouter()

def load_sql(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    query = load_sql("app/queries/users/get_user.sql")
    rows = await fetch_query(query, user_id)
    if not rows:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(rows[0])

@router.post("/users")
async def create_user(name: str, email: str):
    query = load_sql("app/queries/users/create_user.sql")
    rows = await fetch_query(query, name, email)
    return dict(rows[0])
