from pydantic import BaseModel
from typing import Optional, Any


class CommonResponse(BaseModel):
    message: str
    status_code: int
    data: Optional[Any] = None
    error: Optional[str] = None
