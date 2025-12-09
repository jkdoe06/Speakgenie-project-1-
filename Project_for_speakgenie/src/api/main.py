from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.core.db import get_db
from src.core.models import WorkflowMetric

#Setup of the paths so from the base of the UI to the static implicaters 
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


#Helper function to compute a score based on what the metric is 
def compute_score(r: WorkflowMetric):
    return (
        (r.views or 0) * 0.001 +
        (r.likes or 0) * 0.1 +
        (r.comments or 0) * 0.5
    )


#a helper that filters by country the last workflow snapshot and puts it into history
#The main fuction is to make sure the newest workflow is on the main page
def latest_snapshot_subquery(db: Session, country: str):
    return (
        db.query(
            WorkflowMetric.workflow,
            func.max(WorkflowMetric.snapshot_date).label("max_date")
        )
        .filter(WorkflowMetric.country == country)
        .group_by(WorkflowMetric.workflow)
        .subquery()
    )


#Routing to differnt parts of the UI
@app.get("/", response_class=HTMLResponse)
def home(request: Request, country: str = "US"):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "country": country}
    )


@app.get("/workflows", response_class=HTMLResponse)
def list_workflows(request: Request, country: str = "US", db: Session = Depends(get_db)):
    sub = latest_snapshot_subquery(db, country)
    rows = (
        db.query(WorkflowMetric)
        .filter(WorkflowMetric.country == country)
        .join(
            sub,
            (WorkflowMetric.workflow == sub.c.workflow) &
            (WorkflowMetric.snapshot_date == sub.c.max_date)
        )
        .order_by(WorkflowMetric.views.desc())
        .all()
    )

    return templates.TemplateResponse(
        "workflows.html",
        {"request": request, "rows": rows, "compute_score": compute_score, "country": country}
    )


@app.get("/workflows/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request, country: str = "US", db: Session = Depends(get_db)):
    sub = latest_snapshot_subquery(db, country)
    rows = (
        db.query(WorkflowMetric)
        .filter(WorkflowMetric.country == country)
        .join(
            sub,
            (WorkflowMetric.workflow == sub.c.workflow) &
            (WorkflowMetric.snapshot_date == sub.c.max_date)
        )
        .all()
    )
    ranked = sorted(rows, key=lambda r: compute_score(r), reverse=True)

    return templates.TemplateResponse(
        "leaderboard.html",
        {"request": request, "rows": ranked, "compute_score": compute_score, "country": country}
    )


@app.get("/workflows/history", response_class=HTMLResponse)
def workflows_history(request: Request, country: str = "US", db: Session = Depends(get_db)):
    rows = (
        db.query(WorkflowMetric)
        .filter(WorkflowMetric.country == country)
        .order_by(WorkflowMetric.workflow, WorkflowMetric.snapshot_date.desc())
        .all()
    )

    history = {}
    for r in rows:
        history.setdefault(r.workflow, []).append(r)

    items = [{"workflow": w, "history": h} for w, h in history.items()]

    return templates.TemplateResponse(
        "history.html",
        {"request": request, "history": items, "country": country}
    )


#these get the json that are created and filter them to your liking and then include them into the API
#Returns a Json that is structured and not just the html pages

@app.get("/api/workflows/latest")
def api_latest_workflows(country: str = "US", db: Session = Depends(get_db)):
    sub = latest_snapshot_subquery(db, country)
    rows = (
        db.query(WorkflowMetric)
        .filter(WorkflowMetric.country == country)
        .join(
            sub,
            (WorkflowMetric.workflow == sub.c.workflow) &
            (WorkflowMetric.snapshot_date == sub.c.max_date)
        )
        .all()
    )
    return [
        {
            "workflow": r.workflow,
            "source": r.source,
            "country": r.country,
            "views": r.views,
            "likes": r.likes,
            "comments": r.comments,
            "score": compute_score(r),
        }
        for r in rows
    ]


@app.get("/api/workflows/history")
def api_history(country: str = "US", db: Session = Depends(get_db)):
    rows = (
        db.query(WorkflowMetric)
        .filter(WorkflowMetric.country == country)
        .order_by(WorkflowMetric.workflow, WorkflowMetric.snapshot_date.desc())
        .all()
    )
    history = {}
    for r in rows:
        history.setdefault(r.workflow, []).append({
            "source": r.source,
            "views": r.views,
            "likes": r.likes,
            "comments": r.comments,
            "snapshot_date": r.snapshot_date.isoformat(),
        })
    return history
