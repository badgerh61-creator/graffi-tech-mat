from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.db.base import Base

class StudioSession(Base):
    __tablename__ = "studio_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    @property
    def is_active(self):
        from datetime import datetime
        return datetime.utcnow() < self.expires_at

