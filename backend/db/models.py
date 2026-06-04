from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

# 1. Project-Specific Database Configuration
# This ensures it creates 'nb_media_content.db' right inside the db/ folder
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nb_media_content.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Project-Specific Table Schema
class NBGeneratedPost(Base):
    __tablename__ = "nb_linkedin_posts"

    id = Column(Integer, primary_key=True, index=True)
    topic_title = Column(String, index=True)
    source_url = Column(String)
    hook = Column(Text)
    full_post_body = Column(Text)
    image_concept = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 3. Auto-Create the database file and tables when imported
Base.metadata.create_all(bind=engine)