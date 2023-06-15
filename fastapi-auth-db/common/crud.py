from sqlalchemy.orm import Session

from common import models, schemas
from common.security import get_password_hash


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: get_user = 0, limit: get_user = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_notes(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()


def get_note(db: Session, user_id: int, id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).filter(models.Note.id == id).first()


def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, original: models.Note) -> None:
    db.delete(original)
    db.commit()


def update_note(db: Session, new: schemas.NoteCreate, original: models.Note):
    original.title = new.title
    original.description = new.description
    db.add(original)
    db.commit()
    db.refresh(original)
    return original
