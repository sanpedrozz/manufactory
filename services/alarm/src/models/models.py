from typing import Optional

from pydantic import BaseModel


class Alarm(BaseModel):
    place_id: int
    alarm: int
    comment: Optional[str] = None
