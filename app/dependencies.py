from fastapi import Header, HTTPException
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    )
from app.database import AsyncSessionLocal

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    return {"id": 1, "username": "demo_user"}

