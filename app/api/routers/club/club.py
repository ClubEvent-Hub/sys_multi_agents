from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_session
from models import Club
from api.schemas.club import *
from ..autontification.haching import Hash
from datetime import datetime

router = APIRouter(
    prefix="/clubs",
    tags=["Clubs"]
)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@router.get("/{club_id}", status_code=status.HTTP_200_OK, response_model=ClubResponse)
def get_club(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    return club


@router.put("/{club_id}", status_code=status.HTTP_200_OK, response_model=ClubResponse)
def update_club(club_id: int, club_update: ClubUpdate, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    
    update_data = club_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_hash"] = Hash.hash_password(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(club, field, value)
    
    club.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(club)
    
    return club


@router.delete("/{club_id}", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
def delete_club(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    
    db.delete(club)
    db.commit()
    
    return DeleteResponse(
        success=True,
        message="Club deleted successfully",
        timestamp=datetime.utcnow()
    )


