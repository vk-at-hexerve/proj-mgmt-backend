from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from api.deps import get_db, verify_external_api_key
from schemas.user import UserResponse, ExternalUserCreate, ExternalUserUpdate
from services.external_user_service import ExternalUserService

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_external_user(
    user_in: ExternalUserCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_external_api_key),
):
    service = ExternalUserService(db)
    existing = service.get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    try:
        new_user = service.create_user(user_in)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[UserResponse])
def list_external_users(
    skip: int = 0, 
    limit: int = 100,
    internal_only: Optional[bool] = None,
    external_only: Optional[bool] = None,
    db: Session = Depends(get_db),
    _: str = Depends(verify_external_api_key),
):
    service = ExternalUserService(db)
    return service.list_users(skip=skip, limit=limit, internal_only=internal_only, external_only=external_only)

@router.get("/{user_id}", response_model=UserResponse)
def get_external_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_external_api_key),
):
    service = ExternalUserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/by-email/{email}", response_model=UserResponse)
def get_external_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_external_api_key),
):
    service = ExternalUserService(db)
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserResponse)
def update_external_user(
    user_id: str,
    user_in: ExternalUserUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_external_api_key),
):
    service = ExternalUserService(db)
    try:
        updated_user = service.update_user(user_id, user_in)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_external_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_external_api_key),
):
    service = ExternalUserService(db)
    try:
        success = service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
