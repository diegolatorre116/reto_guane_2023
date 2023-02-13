import logging

from fastapi import Depends, HTTPException

from app.core.auth.auth import get_current_user

# This module defines the `RoleChecker` class that is used to validate
# the roles of the application's users

logger = logging.getLogger("role_checker")

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user=Depends(get_current_user)):
        if user["role"] not in self.allowed_roles:
            logger.debug(f"User with role {user['role']} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user


# Allow only to "C-LEVEL"
allow_clevel = RoleChecker(["C-LEVEL"])

# Allow "C-LEVEL" and "LEADER"
allow_clevel_leader = RoleChecker(["C-LEVEL", "LEADER"])
