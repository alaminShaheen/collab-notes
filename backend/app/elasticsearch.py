from elasticsearch import AsyncElasticsearch

from app.config import get_settings


class _ElasticsearchState:
    client: AsyncElasticsearch | None = None


_state = _ElasticsearchState()


async def connect_to_elasticsearch() -> None:
    settings = get_settings()
    _state.client = AsyncElasticsearch(settings.elasticsearch_url)

    info = await _state.client.info()
    print(f"Connected to Elasticsearch: {info['version']['number']}")

    index = settings.elasticsearch_index
    if not await _state.client.indices.exists(index=index):
        await _state.client.indices.create(
            index=index,
            mappings={
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "created_at": {"type": "date"},
                }
            },
        )
        print(f"Created Elasticsearch index: {index}")


async def close_elasticsearch_connection() -> None:
    if _state.client is not None:
        await _state.client.close()
        _state.client = None


def get_elasticsearch() -> AsyncElasticsearch:
    if _state.client is None:
        raise RuntimeError(
            "Elasticsearch is not connected — did the lifespan handler run?"
        )
    return _state.client
