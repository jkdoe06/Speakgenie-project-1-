

import random
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.db import SessionLocal
from src.core.models import WorkflowMetric

WORKFLOWS = [
    ("Gmail → Slack Alerts", "YouTube"),
    ("WhatsApp Birthday Reminders", "Forum"),
    ("Google Sheets → CRM Sync", "YouTube"),
    ("Slack Channel Cleanup", "Google"),
    ("Airtable → Discord Notifications", "Forum"),
    ("Daily Reporting Dashboard", "YouTube"),
    ("Stripe Failed Payments Alerts", "Google"),
    ("RSS → Telegram Broadcaster", "Forum"),
    ("Asana Auto Task Generator", "YouTube"),
    ("LinkedIn Lead Capture", "Google"),
    ("Salesforce → Slack Handoff", "Forum"),
    ("Twitter Mentions Export", "YouTube"),
    ("HubSpot → Email Drip Trigger", "Google"),
    ("Time Tracking Auto Export", "Forum"),
    ("Jira → Weekly Digest Email", "YouTube"),
    ("YouTube Comment Scraper", "Google"),
    ("Reddit Topic Monitor", "YouTube"),
    ("Notion Task Sync", "Forum"),
    ("Zoom Webinar Attendees Export", "YouTube"),
    ("Zendesk Ticket Summaries", "Google"),
    ("Shopify Order Parsing", "YouTube"),
    ("Freshdesk → Slack Alerts", "Forum"),
    ("Outlook → To-Do Sync", "Google"),
    ("TikTok Content Scheduler", "YouTube"),
    ("GitHub Issue → Jira Ticket", "Forum"),
    ("Keyword Volume Tracker", "Google"),
    ("Slack Standup Bot", "YouTube"),
    ("Abandoned Cart Notifications", "Forum"),
    ("Weather Alerts by City", "Google"),
    ("PDF → Text Analyzer", "YouTube"),
    ("Crypto Price Drop Alerts", "Forum"),
    ("SLA Breach Monitor", "Google"),
    ("Spotify Playlist Generator", "YouTube"),
    ("Customer NPS Rollup", "Forum"),
    ("GST Invoice Automation", "Google"),
    ("Trello → Calendar Sync", "YouTube"),
    ("Call Logs → CRM Attach", "Forum"),
    ("File Virus Scan Trigger", "Google"),
    ("WhatsApp Status Auto-Poster", "YouTube"),
    ("DNS Uptime Monitor", "Forum"),
    ("Tracking Number Scraper", "Google"),
    ("Event Registration Sync", "YouTube"),
    ("Yelp Reviews Monitor", "Forum"),
    ("EOD Profit Email", "Google"),
    ("Slack Auto-Translate", "YouTube"),
    ("Inventory Restock Alerts", "Forum"),
    ("Task → Google Sheet Sync", "Google"),
    ("LinkedIn Profile Scanner", "YouTube"),
    ("Email Parsing Rules", "Forum"),
    ("Store Locator Builder", "Google"),
    ]

COUNTRIES = ["US", "IN"]


def create_record(name, source, country):
    views = random.randint(1000, 200000)
    likes = random.randint(10, 8000)
    comments = random.randint(0, 2000)

    return WorkflowMetric(
        workflow=name,
        source=source,
        country=country,
        snapshot_date=datetime.utcnow(),
        views=views,
        likes=likes,
        comments=comments,
        like_to_view_ratio=likes / views if views > 0 else 0,
        comment_to_view_ratio=comments / views if views > 0 else 0,
        )


def seed():
    db: Session = SessionLocal()
    db.query(WorkflowMetric).delete()
    db.commit()

    for name, source in WORKFLOWS:
        for c in COUNTRIES:
            rec = create_record(name, source, c)
            db.add(rec)

    db.commit()
    db.close()
    print("🔥 Seed complete — inserted", len(WORKFLOWS) * 2, "records")


if __name__ == "__main__":
    seed()
