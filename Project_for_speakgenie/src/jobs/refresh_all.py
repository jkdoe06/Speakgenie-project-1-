from src.collectors.youtube import fetch_youtube_workflows
from src.collectors.forum import fetch_forum_workflows
from src.collectors.trends import fetch_trending_workflows

from src.core.db import get_db
from src.core.models import insert_workflow_record

# This script refreshes the database by collecting data from all three sources
# (YouTube, Forum, Google Trends) for both US and India. Designed to be run manually
# or as a scheduled cron job for continuous data updates.


#Runs a refresh of the db for each type of workflow to reset them
def run_refresh():
    db = next(get_db())

    sources = [
        ("YouTube", fetch_youtube_workflows),
        ("Forum", fetch_forum_workflows),
        ("Trends", fetch_trending_workflows),
    ]

    for country in ["US", "IN"]:
        print(f"\n=== Refreshing country: {country} ===")

        for name, fetcher in sources:
            print(f"> Fetching from: {name}")
            try:
                records = fetcher(country=country)
                for r in records:
                    insert_workflow_record(db, **r)
                print(f"  Inserted: {len(records)}")
            except Exception as e:
                print(f"  ERROR fetching {name}: {e}")

    db.commit()
    print("\n📌 Refresh complete. DB committed!")


if __name__ == "__main__":
    run_refresh()
