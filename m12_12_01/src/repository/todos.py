from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Todo, User
from src.schemas import TodoSchema, TodoUpdateSchema


async def get_todos(limit: int, offset: int, db: AsyncSession, user: User):
    sq = select(Todo).filter_by(user=user).offset(offset).limit(limit)
    todos = await db.execute(sq)
    return todos.scalars().all()


async def get_todo(todo_id: int, db: AsyncSession, user: User):
    sq = select(Todo).filter_by(id=todo_id, user=user)
    todo = await db.execute(sq)
    return todo.scalar_one_or_none()


async def create_todo(body: TodoSchema, db: AsyncSession, user: User):
    todo = Todo(title=body.title, description=body.description, user=user)
    if body.completed:
        todo.completed = body.completed
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(todo_id: int, body: TodoUpdateSchema, db: AsyncSession, user: User):
    sq = select(Todo).filter_by(id=todo_id, user=user)
    result = await db.execute(sq)
    todo = result.scalar_one_or_none()
    if todo:
        todo.title = body.title
        todo.description = body.description
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
        # await db.refresh(todo, attribute_names=["user"])
    return todo


async def remove_todo(todo_id: int, db: AsyncSession, user: User):
    sq = select(Todo).filter_by(id=todo_id, user=user)
    result = await db.execute(sq)
    todo = result.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo
