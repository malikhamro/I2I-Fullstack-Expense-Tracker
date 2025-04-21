from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MigrationProgress(db.Model):
    __tablename__ = 'migration_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    progress_percent = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, task_name, progress_percent):
        self.task_name = task_name
        self.progress_percent = progress_percent

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'progress_percent': self.progress_percent,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class MigrationStatus(db.Model):
    __tablename__ = 'migration_status'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, status, details=None):
        self.status = status
        self.details = details

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'details': self.details,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
