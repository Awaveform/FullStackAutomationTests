from typing import List

from pydantic import BaseModel, Field, RootModel


class Post(BaseModel):
    userId: int = Field(..., gt=0)
    id: int
    title: str
    body: str


class PostList(RootModel[List[Post]]):
    pass
