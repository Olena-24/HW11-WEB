from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.todo import ContactSchema, ContactUpdateSchema


async def get_todos(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_todos function returns a list of todos for the user.
    
    :param limit: int: Limit the number of results returned
    :param offset: int: Specify the offset of the query
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Get the user from the database
    :return: All the todos in the database
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_all_todos(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_todos function returns a list of all todos in the database.
    
    :param limit: int: Limit the number of results returned by the function
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass the database connection to the function
    :return: A list of all todos in the database
    :doc-author: Trelent
    """
    stmt = select(Contact).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_todo(todo_id: int, db: AsyncSession, user: User):
    """
    The get_todo function returns a single todo item from the database.
    
    :param todo_id: int: Specify the type of the parameter
    :param db: AsyncSession: Pass in the database session
    :param user: User: Check if the user is allowed to access this resource
    :return: A todo object, which is a row in the database
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=todo_id, user=user)
    todo = await db.execute(stmt)
    return todo.scalar_one_or_none()


async def create_todo(body: ContactSchema, db: AsyncSession, user: User):
    todo = Contact(**body.model_dump(exclude_unset=True), user=user)  # (title=body.title, description=body.description)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(todo_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=todo_id, user=user)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()
    if todo:
        todo.title = body.title
        todo.description = body.description
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
    return todo


async def delete_todo(todo_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=todo_id, user=user)
    todo = await db.execute(stmt)
    todo = todo.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo