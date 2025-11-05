from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_session
from models import Student, StudentProfile
from api.schemas.student import *
from ..autontification.haching import Hash
from datetime import datetime

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@router.get("/{student_id}", status_code=status.HTTP_200_OK, response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


@router.put("/{student_id}", status_code=status.HTTP_200_OK, response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    update_data = student_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_hash"] = Hash.hash_password(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(student, field, value)
    
    student.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(student)
    
    return student


@router.delete("/{student_id}", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()
    
    return DeleteResponse(
        success=True,
        message="Student deleted successfully",
        timestamp=datetime.utcnow()
    )


@router.post("/{student_id}/profile", status_code=status.HTTP_201_CREATED, response_model=ProfileResponse)
def create_profile(student_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    existing_profile = db.query(StudentProfile).filter(StudentProfile.student_id == student_id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists"
        )
    
    new_profile = StudentProfile(
        student_id=student_id,
        bio=profile.bio,
        goals=profile.goals,
        notification_preferences=profile.notification_preferences
    )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return new_profile


@router.get("/{student_id}/profile", status_code=status.HTTP_200_OK, response_model=ProfileResponse)
def get_profile(student_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.student_id == student_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile


@router.put("/{student_id}/profile", status_code=status.HTTP_200_OK, response_model=ProfileResponse)
def update_profile(student_id: int, profile_update: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.student_id == student_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    update_data = profile_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    profile.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    
    return profile


@router.delete("/{student_id}/profile", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
def delete_profile(student_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.student_id == student_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    db.delete(profile)
    db.commit()
    
    return DeleteResponse(
        success=True,
        message="Profile deleted successfully",
        timestamp=datetime.utcnow()
    )


