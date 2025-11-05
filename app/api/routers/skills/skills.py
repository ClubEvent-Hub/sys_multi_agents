from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_session
from models import Skill
from api.schemas.skill import *
from datetime import datetime

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SkillResponse)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    existing_skill = db.query(Skill).filter(Skill.name == skill.name).first()
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already exists"
        )
    
    new_skill = Skill(
        name=skill.name,
        category=skill.category
    )
    
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    
    return new_skill


@router.get("/{skill_id}", status_code=status.HTTP_200_OK, response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    return skill


@router.put("/{skill_id}", status_code=status.HTTP_200_OK, response_model=SkillResponse)
def update_skill(skill_id: int, skill_update: SkillUpdate, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    update_data = skill_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(skill, field, value)
    
    db.commit()
    db.refresh(skill)
    
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    db.delete(skill)
    db.commit()
    
    return DeleteResponse(
        success=True,
        message="Skill deleted successfully",
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return [{
        "id": s.id,
        "name": s.name,
        "category": s.category
    } for s in skills]


@router.get("/category/{category}", status_code=status.HTTP_200_OK)
def get_skills_by_category(category: str, db: Session = Depends(get_db)):
    skills = db.query(Skill).filter(Skill.category == category).all()
    return [{
        "id": s.id,
        "name": s.name,
        "category": s.category
    } for s in skills]