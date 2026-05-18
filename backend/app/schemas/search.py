from pydantic import BaseModel, ConfigDict


class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    tags: list[str]
    score: float
    highlight: dict | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "FastAPI Tutorial",
                "content": "FastAPI is a modern web framework...",
                "tags": ["fastapi", "python"],
                "score": 8.5,
                "highlight": {"title": ["<em>FastAPI</em> Tutorial"]},
            }
        }
    )
