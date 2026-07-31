from typing import Optional, List
from sqlalchemy.orm import Session
from models.user import User
from models.role import Role
from models.user_role import UserRole
from schemas.user import ExternalUserCreate, ExternalUserUpdate
from core.security import get_password_hash, SUPER_ADMIN_EMAIL
import uuid

class ExternalUserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_in: ExternalUserCreate) -> User:
        """Create a new user marked as external (internal_user=0)."""
        hashed_password = get_password_hash(user_in.password)
        
        user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=hashed_password,
            internal_user=0  # 0 indicates created by external system
        )
        self.db.add(user)
        self.db.flush()

        # Assign role: requested role or default to org_admin
        role = None
        if user_in.system_role_id:
            role = self.db.query(Role).filter(Role.id == user_in.system_role_id, Role.deleted_at.is_(None)).first()
        
        if not role:
            role = self.db.query(Role).filter(Role.slug == "org_admin", Role.deleted_at.is_(None)).first()

        if role:
            user.system_role_id = role.id
            assignment = UserRole(
                id=str(uuid.uuid4()),
                user_id=user.id,
                role_id=role.id,
                scope_type="global",
            )
            self.db.add(assignment)

        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()

    def list_users(self, skip: int = 0, limit: int = 100, internal_only: Optional[bool] = None, external_only: Optional[bool] = None) -> List[User]:
        query = self.db.query(User).filter(User.deleted_at.is_(None))
        
        if internal_only:
            query = query.filter(User.internal_user != 0)
        elif external_only:
            query = query.filter(User.internal_user == 0)
            
        return query.offset(skip).limit(limit).all()

    def update_user(self, user_id: str, data: ExternalUserUpdate) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None

        if user.email == SUPER_ADMIN_EMAIL:
            if data.email is not None and data.email != SUPER_ADMIN_EMAIL:
                raise ValueError("Cannot change the email of the super admin.")
            if data.system_role_id is not None and data.system_role_id != user.system_role_id:
                raise ValueError("Cannot change the role of the super admin.")

        if data.name is not None:
            user.name = data.name
        
        if data.email is not None and data.email != user.email:
            existing = self.get_user_by_email(data.email)
            if existing:
                raise ValueError("A user with this email already exists")
            user.email = data.email

        if data.system_role_id is not None:
            role = self.db.query(Role).filter(Role.id == data.system_role_id).first()
            if role and role.slug == "super_admin" and user.email != SUPER_ADMIN_EMAIL:
                raise ValueError("Cannot assign super admin role to this email.")
            user.system_role_id = data.system_role_id

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: str) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
            
        if user.email == SUPER_ADMIN_EMAIL:
            raise ValueError("The system super administrator cannot be deleted.")

        import datetime
        suffix = f"-del-{int(datetime.datetime.now().timestamp())}"
        user.email = f"{user.email}{suffix}"
        user.soft_delete()
        self.db.commit()
        return True
