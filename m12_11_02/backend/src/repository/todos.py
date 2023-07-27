from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Todo
from src.schemas import TodoSchema, TodoUpdateSchema


async def get_todos(limit: int, offset: int, db: AsyncSession):
    sq = select(Todo).offset(offset).limit(limit)
    todos = await db.execute(sq)
    return todos.scalars().all()


async def get_todo(todo_id: int, db: AsyncSession):
    sq = select(Todo).filter_by(id=todo_id)
    todo = await db.execute(sq)
    return todo.scalar_one_or_none()


async def create_todo(body: TodoSchema, db: AsyncSession):
    todo = Todo(title=body.title, description=body.description)
    if body.completed:
        todo.completed = body.completed
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(todo_id: int, body: TodoUpdateSchema, db: AsyncSession):
    sq = select(Todo).filter_by(id=todo_id)
    result = await db.execute(sq)
    todo = result.scalar_one_or_none()
    if todo:
        todo.title = body.title
        todo.description = body.description
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
    return todo


async def remove_todo(todo_id: int, db: AsyncSession):
    sq = select(Todo).filter_by(id=todo_id)
    result = await db.execute(sq)
    todo = result.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo
