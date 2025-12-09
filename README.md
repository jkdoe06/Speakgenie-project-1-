# Workflow Popularity Dashboard

Author: John de Vere

This project implements a data-collection and analytics system designed to evaluate the popularity of n8n workflows. The system collects engagement data from multiple online sources, stores the information in a SQLite database, and presents the latest and historical workflow popularity through a FastAPI web dashboard and JSON API.

Project Objectives

* Collect at least 50 unique n8n workflows
* Use multiple popularity indicators such as views, likes, comments, and engagement ratios
* Include data from at least two geographic regions (United States, India)
* Provide REST endpoints returning structured JSON
* Automate data refresh for ongoing measurement
* Deliver production-style code with documentation and UI

All objectives above are successfully completed.

System Architecture

Data Sources
• YouTube Data API v3
• n8n Community Forum API
• Google Trends via SerpAPI

Technology Stack
• FastAPI (web server + HTML rendering)
• SQLAlchemy (ORM + SQLite)
• Jinja2 templates (UI)
• Cron-ready refresh script

Directory Structure

Project_for_speakgenie/
│ workflows.db
│ README.md
│ src/
│  api/
│   main.py                  – Frontend routes and JSON endpoints
│   templates/               – HTML pages (dashboard)
│   static/styles.css        – Styling
│  core/
│   db.py                    – Database connection and session
│   models.py                – WorkflowMetric schema
│  collectors/
│   youtube.py               – YouTube collector
│   forum.py                 – Forum collector
│   trends.py                – Google Trends collector
│  jobs/
│   refresh_all.py           – Data refresh automation

Data Flow

1. Collect workflow metrics
2. Insert individual snapshots into database
3. Display most recent results on dashboard pages

Database Schema

Table: workflows
id – Primary key
workflow – Title of workflow or keyword
source – YouTube, Forum, or Trends
country – US or IN
snapshot_date – Timestamp of data collection
views – Engagement metric
likes – Engagement metric
comments – Engagement metric
like_to_view_ratio – Derived metric
comment_to_view_ratio – Derived metric

The system supports repeated snapshots over time. The dashboard displays the most recent snapshot per workflow.

Running the Project Locally

Install dependencies:

pip install fastapi uvicorn sqlalchemy requests python-dotenv

Start the application:

uvicorn src.api.main:app --reload

Access the dashboard in browser:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

Region Filtering

All dashboard pages and JSON endpoints accept a country query parameter:

?country=US
?country=IN

A region selector in the UI sidebar updates this parameter and navigation links preserve the selected region.

Example URLs:

/workflows?country=US
/workflows/leaderboard?country=IN
/workflows/history?country=US

Automated Data Refresh

The refresh script collects and inserts new workflow data for both regions:

python3 src/jobs/refresh_all.py

This script can be automated using a cron job (example: daily at 06:00):

0 6 * * * python3 /absolute/path/src/jobs/refresh_all.py >> refresh.log 2>&1

JSON API Endpoints

Latest snapshot of each workflow:

GET /api/workflows/latest?country=US

Historical snapshots grouped by workflow:

GET /api/workflows/history?country=IN

Example output (structure):

[
{
"workflow": "...",
"source": "YouTube",
"country": "US",
"views": ...,
"likes": ...,
"comments": ...,
"score": ...
}
]

Required Submission Screenshots

1. Home page: `/`
2. Latest Workflows (US): `/workflows?country=US`
3. Leaderboard (India): `/workflows/leaderboard?country=IN`
4. History page (either region): `/workflows/history?country=US`
5. Terminal output executing: `python3 src/jobs/refresh_all.py`

Ensure the browser URL is visible in each screenshot.

Key Features

* Real-time popularity scoring using weighted metrics
* Fully region-aware data pipeline and UI
* Latest-snapshot logic implemented using SQL subquery
* Aggregation and storage of more than 80 unique workflows
* Manual or automated refresh for continuous updates
* Clean, intuitive sidebar interface

Potential Future Enhancements

* Apply more advanced scoring models using engagement ratios
* Add search and pagination controls to the dashboard
* Incorporate timeline visualizations
* Package deployment using Docker

This project meets all functional and technical requirements defined for the assignment.