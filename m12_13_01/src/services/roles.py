from typing import List

from fastapi import Request, Depends, HTTPException, status

from src.database.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        print(user.role)
        print(self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")
