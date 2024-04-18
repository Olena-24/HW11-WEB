from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, Role
from src.repository import todos as repositories_todos
from src.schemas.todo import ContactSchema, ContactUpdateSchema, ContactResponse
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/todos', tags=['todos'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.get("/", response_model=list[ContactResponse])
async def get_todos(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    todos = await repositories_todos.get_todos(limit, offset, db, user)
    return todos


@router.get("/all", response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_todos(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                        db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    todos = await repositories_todos.get_all_todos(limit, offset, db)
    return todos


@router.get("/{todo_id}", response_model=ContactResponse)
async def get_todo(todo_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                   user: User = Depends(auth_service.get_current_user)):
    todo = await repositories_todos.get_todo(todo_id, db, user)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return todo


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(body: ContactSchema, db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    todo = await repositories_todos.create_todo(body, db, user)
    print(todo)
    return todo


@router.put("/{todo_id}")
async def update_todo(body: ContactUpdateSchema, todo_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    todo = await repositories_todos.update_todo(todo_id, body, db, user)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    todo = await repositories_todos.delete_todo(todo_id, db, user)
    return todo