import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Todo
from src.schemas import TodoSchema, TodoUpdateSchema
from src.repository.todos import get_todos, create_todo, update_todo


class TestAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, email="test@tes.com", password="qwerty", confirmed=True)

    async def test_get_todos(self):
        limit = 10
        offset = 0
        expected_todos = [Todo(), Todo(), Todo(), Todo()]
        mock_todos = MagicMock()
        mock_todos.scalars.return_value.all.return_value = expected_todos
        self.session.execute.return_value = mock_todos
        result = await get_todos(limit, offset, self.session, self.user)
        self.assertEqual(result, expected_todos)

    async def test_create_todo(self):
        body = TodoSchema(title="Test", description="QWERTY")
        result = await create_todo(body, self.session, self.user)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "completed"))

    async def test_update_todo(self):
        body = TodoUpdateSchema(title="Test", description="QWERTY", completed=True)
        todo = Todo(title="Test old", description="QWERTY old", completed=False, user_id=self.user.id)

        mock_todo = MagicMock()
        mock_todo.scalar_one_or_none.return_value = todo
        self.session.execute.return_value = mock_todo

        result = await update_todo(todo.id, body, self.session, self.user)

        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertTrue(result.completed, True)
