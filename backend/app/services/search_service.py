from typing import Annotated

from fastapi import Depends

from app.repositories.search_repo import SearchRepository, get_search_repository
from app.schemas import SearchResult


class SearchService:
    def __init__(self, search_repo: SearchRepository):
        self.search_repo = search_repo

    async def index_note(self, note: dict) -> None:
        await self.search_repo.index_document(
            note["id"],
            {
                "title": note["title"],
                "content": note["content"],
                "tags": note["tags"],
                "created_at": note["created_at"].isoformat(),
            },
        )

    async def delete_note(self, note_id: str) -> None:
        await self.search_repo.delete(note_id)

    async def search_notes(
        self, query: str, limit: int = 20, skip: int = 0
    ) -> list[SearchResult]:
        hits = await self.search_repo.search(query, limit, skip)
        return [
            SearchResult(
                id=hit["_id"],
                title=hit["_source"]["title"],
                content=hit["_source"]["content"],
                tags=hit["_source"].get("tags", []),
                score=hit["_score"],
                highlight=hit.get("highlight"),
            )
            for hit in hits
        ]


SearchRepoDep = Annotated[SearchRepository, Depends(get_search_repository)]


def get_search_service(search_repo: SearchRepoDep) -> SearchService:
    return SearchService(search_repo)
