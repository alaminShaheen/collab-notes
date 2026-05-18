import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.mongo import close_mongo_connection, connect_to_mongo, get_database
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate


SEED_NOTES: list[NoteCreate] = [
    NoteCreate(
        title="Weekly planning checklist",
        content=(
            "Mondays are for triage. Walk through the inbox, archive anything older than two weeks, "
            "and convert anything actionable into a task with a clear next step. Block two focus hours "
            "for the most important deliverable before opening Slack."
        ),
    ),
    NoteCreate(
        title="Sourdough loaf — adjustments",
        content=(
            "Last bake was too dense. Next time: raise hydration from 70% to 75%, extend bulk ferment "
            "to 5 hours at 24°C, and do four sets of stretch-and-folds 30 minutes apart. Bake at 250°C "
            "with steam for the first 20 minutes, then drop to 220°C uncovered for another 25."
        ),
    ),
    NoteCreate(
        title="Books to read this quarter",
        content=(
            "1. Designing Data-Intensive Applications — Kleppmann\n"
            "2. The Pragmatic Programmer (20th anniversary edition)\n"
            "3. Thinking in Systems — Donella Meadows\n"
            "4. A Philosophy of Software Design — Ousterhout\n"
            "Aim for one per month, write a short reflection after each."
        ),
    ),
    NoteCreate(
        title="Apartment move — utilities checklist",
        content=(
            "Two weeks before move-out: schedule internet transfer, give written notice to landlord, "
            "book moving truck for Saturday morning. One week before: transfer hydro and gas accounts, "
            "redirect mail through Canada Post, return modem to provider. Day of: take meter readings, "
            "photograph empty unit, hand over keys."
        ),
    ),
    NoteCreate(
        title="Coffee brewing ratios",
        content=(
            "V60: 15g coffee to 250g water, 96°C, total brew time 2:45.\n"
            "Aeropress (inverted): 17g coffee to 220g water, 88°C, steep 1:30, press for 30s.\n"
            "French press: 30g coffee to 500g water, 94°C, steep 4:00, plunge slowly."
        ),
    ),
    NoteCreate(
        title="Interview prep — system design",
        content=(
            "Common patterns to rehearse: rate limiting (token bucket vs leaky bucket), caching layers "
            "(write-through, write-back, cache-aside), database sharding strategies, leader election, "
            "and consistent hashing. For each, be ready to discuss trade-offs and a real-world example. "
            "Practice drawing the diagrams on a whiteboard within 35 minutes."
        ),
    ),
    NoteCreate(
        title="Garden plans — spring",
        content=(
            "Raised bed A: tomatoes (San Marzano, Cherokee Purple), basil, marigolds along the border.\n"
            "Raised bed B: bush beans, carrots, radishes succession-planted every two weeks.\n"
            "Container row: jalapeños, shishito peppers, lemon thyme.\n"
            "Order seeds by mid-February, start tomatoes indoors under lights by March 10."
        ),
    ),
    NoteCreate(
        title="Side project ideas",
        content=(
            "- A CLI that summarises a git repository's activity over the past week.\n"
            "- A small web app that tracks weekly running mileage and computes a rolling 4-week average.\n"
            "- A browser extension that highlights cited sources on news articles.\n"
            "- A static site generator that builds a recipe book from markdown plus structured frontmatter."
        ),
    ),
    NoteCreate(
        title="1:1 talking points",
        content=(
            "Topics to bring up next 1:1: progress on the notes service migration, blockers around the "
            "Mongo connection pool sizing, feedback on the recent code review turnaround time, and the "
            "training budget for the distributed systems course next quarter."
        ),
    ),
    NoteCreate(
        title="Travel notes — Lisbon",
        content=(
            "Stay in Alfama or Príncipe Real for walkability. Must-do: tram 28 early morning before "
            "the crowds, pastéis de nata at Manteigaria, sunset at Miradouro da Senhora do Monte. "
            "Day trip to Sintra by train from Rossio — book Pena Palace tickets online to skip the "
            "queue. Skip taxis, the metro and walking cover most of what you need."
        ),
    ),
]


async def seed(user_id: int) -> None:
    await connect_to_mongo()
    try:
        db = get_database()
        repo = NoteRepository(db)
        for payload in SEED_NOTES:
            note = await repo.create(user_id, payload)
            print(f"created note {note['id']} — {note['title']}")
        print(f"\nseeded {len(SEED_NOTES)} notes for user {user_id}")
    finally:
        await close_mongo_connection()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Mongo with dummy notes for a user.")
    parser.add_argument("user_id", type=int, help="owner_id to attach the notes to")
    args = parser.parse_args()
    asyncio.run(seed(args.user_id))


if __name__ == "__main__":
    main()
