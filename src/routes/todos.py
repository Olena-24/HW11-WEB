from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import todos as repositories_todos
from src.schemas.todo import ContactResponse, ContactUpdateSchema, ContactSchema

router = APIRouter()

# Todos Endpoints
@router.get("/todos", response_model=list[ContactResponse])
async def get_todos(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    todos = await repositories_todos.get_todos(limit, offset, db)
    return todos

@router.get("/todos/{todo_id}", response_model=ContactResponse)
async def get_todo(todo_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    todo = await repositories_todos.get_todo(todo_id, db)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return todo

@router.post("/todos", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    todo = await repositories_todos.create_todo(body, db)
    return todo

@router.put("/todos/{todo_id}")
async def update_todo(todo_id: int, body: ContactUpdateSchema, db: AsyncSession = Depends(get_db)):
    todo = await repositories_todos.update_todo(todo_id, body, db)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return todo

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await repositories_todos.delete_todo(todo_id, db)
    return todo