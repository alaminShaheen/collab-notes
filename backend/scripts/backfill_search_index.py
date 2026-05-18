import argparse
import asyncio
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
os.chdir(BACKEND_DIR)

from app.config import get_settings
from app.elasticsearch import (
    close_elasticsearch_connection,
    connect_to_elasticsearch,
    get_elasticsearch,
)
from app.mongo import close_mongo_connection, connect_to_mongo, get_database
from app.repositories.search_repo import SearchRepository
from app.services.search_service import SearchService


async def backfill() -> None:
    await connect_to_mongo()
    await connect_to_elasticsearch()
    try:
        db = get_database()
        es = get_elasticsearch()
        index = get_settings().elasticsearch_index
        search_service = SearchService(SearchRepository(es, index))

        indexed = 0
        skipped = 0
        async for doc in db["notes"].find({}):
            note_id = str(doc.pop("_id"))
            doc["id"] = note_id
            doc.setdefault("tags", [])

            if await es.exists(index=index, id=note_id):
                skipped += 1
                continue

            await search_service.index_note(doc)
            indexed += 1
            print(f"indexed {note_id} — {doc['title']}")

        print(f"\nbackfill complete: indexed {indexed}, skipped {skipped}")
    finally:
        await close_elasticsearch_connection()
        await close_mongo_connection()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill Elasticsearch with notes from Mongo. Skips notes already indexed.",
    )
    parser.parse_args()
    asyncio.run(backfill())


if __name__ == "__main__":
    main()
