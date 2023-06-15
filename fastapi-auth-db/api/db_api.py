from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dps import get_db
from common.auth import get_current_active_user, get_current_user
from common import schemas, crud
from common.models import User

router = APIRouter()


@router.get("/user", response_model=schemas.User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)


@router.post("/user/note", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud.create_note(db=db, note=note, user_id=current_user.id)


@router.get("/user/notes", response_model=list[schemas.Note])
def read_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    notes = crud.get_notes(db, user_id=int(current_user.id))
    return notes


@router.delete("/user/notes/{note_id}", response_model=None)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    note = crud.get_note(db, user_id=int(current_user.id), id=note_id)
    if note is None:
        raise HTTPException(status_code=400, detail="Note is not found")
    return crud.delete_note(db, original=note)


@router.put("/user/notes/{note_id}", response_model=schemas.Note)
def update_note(new_note: schemas.NoteCreate, note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    original_note = crud.get_note(db, user_id=int(current_user.id), id=note_id)
    if original_note is None:
        raise HTTPException(status_code=400, detail="Note is not found")
    return crud.update_note(db, original=original_note, new=new_note)
