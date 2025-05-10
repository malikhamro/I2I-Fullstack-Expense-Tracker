from sqlalchemy import Column, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class RolePermission(Base):
    __tablename__ = 'role_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)

    role = relationship('Role', back_populates='role_permissions')
    permission = relationship('Permission', back_populates='role_permissions')

    def __init__(self, role_id, permission_id):
        self.role_id = role_id
        self.permission_id = permission_id

    @staticmethod
    def add_role_permission(session, role_id, permission_id):
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        session.add(role_permission)
        try:
            session.commit()
            return role_permission
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def remove_role_permission(session, role_id, permission_id):
        role_permission = session.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first()
        if role_permission:
            session.delete(role_permission)
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                raise e
        raise ValueError("RolePermission not found")

    @staticmethod
    def get_role_permissions(session, role_id):
        return session.query(RolePermission).filter_by(role_id=role_id).all()

    @staticmethod
    def get_permission_roles(session, permission_id):
        return session.query(RolePermission).filter_by(permission_id=permission_id).all()

# Example Role and Permission dummy classes
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role_permissions = relationship('RolePermission', back_populates='role')

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    role_permissions = relationship('RolePermission', back_populates='permission')

# Database setup for testing
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a Role and Permission for testing
    new_role = Role(name="Admin")
    new_permission = Permission(name="Read", description="Read permission")
    session.add(new_role)
    session.add(new_permission)
    session.commit()

    # Add RolePermission
    role_permission = RolePermission.add_role_permission(session, new_role.id, new_permission.id)
    print(role_permission)

    # Get RolePermissions for a Role
    role_permissions = RolePermission.get_role_permissions(session, new_role.id)
    print(role_permissions)

    # Remove RolePermission
    RolePermission.remove_role_permission(session, new_role.id, new_permission.id)
    print(RolePermission.get_role_permissions(session, new_role.id))
