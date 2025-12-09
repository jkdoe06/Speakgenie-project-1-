from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

#Declare the base model 
#A snapshot of the data for the current workflow 
Base = declarative_base()

#This class is used to manage workflow db and what are included in them 
#Extracts from the API
class WorkflowMetric(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)

    # Core identifiers
    workflow = Column(String, index=True)   # e.g. "WhatsApp reminders"
    source = Column(String, index=True)     # youtube / forum / trends
    country = Column(String, index=True)    # US / IN

    # Snapshot metadata
    snapshot_date = Column(DateTime, default=datetime.utcnow, index=True)

    # Popularity metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)

    # Ratios
    like_to_view_ratio = Column(Float, default=0.0)
    comment_to_view_ratio = Column(Float, default=0.0)

#This inserts what is found in the the workflow class into a db
#Make sure only valid columns are inserted 
def insert_workflow_record(db, **kwargs):
    allowed = {
        "workflow", "source", "country", "snapshot_date",
        "views", "likes", "comments",
        "like_to_view_ratio", "comment_to_view_ratio"
    }
    clean = {k: v for k, v in kwargs.items() if k in allowed}
    wf = WorkflowMetric(**clean)
    db.add(wf)
