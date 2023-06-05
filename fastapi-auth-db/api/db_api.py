from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auth_api import get_current_active_user, get_current_user
from api.dps import get_db
from common import schemas, crud
from common.models import User

router = APIRouter()


@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)

@router.post("/users/me/items", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud.create_item(db=db, item=item, user_id=current_user.id)


@router.get("/users/me/items", response_model=list[schemas.Item])
async def read_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    items = crud.get_items(db, user_id=int(current_user.id))
    return items
