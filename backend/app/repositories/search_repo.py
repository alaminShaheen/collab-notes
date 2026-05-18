from typing import Annotated, Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from app.config import get_settings
from app.elasticsearch import get_elasticsearch


class SearchRepository:
    def __init__(self, es: AsyncElasticsearch, index: str):
        self.es = es
        self.index = index

    async def index_document(self, doc_id: str, document: dict[str, Any]) -> None:
        await self.es.index(index=self.index, id=doc_id, document=document)

    async def delete(self, doc_id: str) -> None:
        try:
            await self.es.delete(index=self.index, id=doc_id)
        except NotFoundError:
            pass

    async def search(
        self, query: str, limit: int = 20, skip: int = 0
    ) -> list[dict[str, Any]]:
        response = await self.es.search(
            index=self.index,
            query={
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"],
                }
            },
            highlight={"fields": {"title": {}, "content": {}}},
            from_=skip,
            size=limit,
        )
        return response["hits"]["hits"]


EsClientDep = Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]


def get_search_repository(es: EsClientDep) -> SearchRepository:
    return SearchRepository(es, get_settings().elasticsearch_index)
