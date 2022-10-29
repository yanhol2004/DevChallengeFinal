from pydantic import BaseModel


class ImageInput(BaseModel):
    min_level: int
    image: str

