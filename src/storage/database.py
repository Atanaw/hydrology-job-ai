from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.config_loader import env

Base = declarative_base()

class JobRecord(Base):
    __tablename__ = "jobs"
    id = Column(String(64), primary_key=True)
    title = Column(Text)
    employer = Column(Text)
    location = Column(Text)
    salary = Column(Text)
    description = Column(Text)
    url = Column(Text)
    source = Column(Text)
    employer_type = Column(Text)
    score = Column(Integer)
    matched_keywords = Column(Text)
    priority = Column(Text)
    status = Column(Text, default="new")
    scraped_at = Column(Text)
    deadline = Column(Text)

class ApplicationRecord(Base):
    __tablename__ = "applications"
    id = Column(String(64), primary_key=True)
    job_id = Column(String(64))
    status = Column(Text, default="review")
    notes = Column(Text)
    applied_date = Column(Text)
    interview_date = Column(Text)
    outcome = Column(Text)

class Database:
    def __init__(self):
        db_url = env("DATABASE_URL", "sqlite:///data/jobs.db")
        self.engine = create_engine(db_url, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def upsert_jobs(self, jobs):
        new_jobs = []
        with self.Session() as session:
            for job in jobs:
                existing = session.get(JobRecord, job.id)
                if existing:
                    existing.score = job.score
                    existing.priority = job.priority
                    existing.matched_keywords = ", ".join(job.matched_keywords)
                    continue
                record = JobRecord(
                    id=job.id, title=job.title, employer=job.employer, location=job.location,
                    salary=job.salary, description=job.description, url=job.url, source=job.source,
                    employer_type=job.employer_type, score=job.score,
                    matched_keywords=", ".join(job.matched_keywords), priority=job.priority,
                    status=job.status, scraped_at=job.scraped_at, deadline=job.deadline
                )
                session.add(record)
                new_jobs.append(job)
            session.commit()
        return new_jobs

    def list_recent_alerts(self, min_score=70, limit=50):
        with self.Session() as session:
            rows = session.query(JobRecord).filter(JobRecord.score >= min_score).order_by(JobRecord.scraped_at.desc()).limit(limit).all()
            return rows

    def counts(self):
        with self.Session() as session:
            total = session.query(JobRecord).count()
            high = session.query(JobRecord).filter(JobRecord.priority == "high").count()
            alert = session.query(JobRecord).filter(JobRecord.priority == "alert").count()
            return {"total": total, "high": high, "alert": alert}
