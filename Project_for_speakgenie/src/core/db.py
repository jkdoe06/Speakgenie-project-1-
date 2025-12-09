import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configures the SQLite database connection for the project
# The engine, session factory, and helpers used by the rest of the app are developed and defined here 


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "workflows.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

#Extracts the database from the local session and safely closes it 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Help to break circular dependency

def init_db():
    from src.core.models import Base  
    Base.metadata.create_all(bind=engine)


init_db()


#debug noise 
print(f"🔗 Connected DB: {DB_PATH}")
