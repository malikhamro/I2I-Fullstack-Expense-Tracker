from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for declarative base
Base = declarative_base()

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1024), nullable=True)

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}', description='{self.description}')>"

    @staticmethod
    def add_permission(session, name, description=None):
        """Add a new permission to the database."""
        try:
            permission = Permission(name=name, description=description)
            session.add(permission)
            session.commit()
            return permission
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_permission(session, permission_id):
        """Retrieve a permission by its ID."""
        return session.query(Permission).filter_by(id=permission_id).first()

    @staticmethod
    def list_permissions(session):
        """List all permissions in the database."""
        return session.query(Permission).all()

    @staticmethod
    def update_permission(session, permission_id, new_name=None, new_description=None):
        """Update the details of a specific permission."""
        try:
            permission = session.query(Permission).filter_by(id=permission_id).first()
            if not permission:
                return None
            if new_name:
                permission.name = new_name
            if new_description:
                permission.description = new_description
            session.commit()
            return permission
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def delete_permission(session, permission_id):
        """Delete a permission from the database."""
        try:
            permission = session.query(Permission).filter_by(id=permission_id).first()
            if permission:
                session.delete(permission)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e


# Example setup for a SQLite database
engine = create_engine('sqlite:///permissions.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
