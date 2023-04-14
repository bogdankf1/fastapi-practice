import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user,  get_user_exception, authenticate_user, get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserData(BaseModel):
    username: str
    old_password: str
    new_password: str



@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user_id)\
        .first()
    if user_model is not None:
        return user_model
    raise http_exception()


@router.get('/user/', status_code=status.HTTP_200_OK)
async def read_user_by_query(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user_id)\
        .first()
    if user_model is not None:
        return user_model
    raise http_exception()


@router.put('/change-password', status_code=status.HTTP_200_OK)
async def update_user_password(
        user_data: UserData,
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is None:
        raise get_user_exception()

    if user_data.username == user_model.username and verify_password(user_data.old_password, user_model.hashed_password):
        user_model.hashed_password = get_password_hash(user_data.new_password)

        db.add(user_model)
        db.commit()

        return successful_response(200)
    return http_exception()


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users)\
        .filter(models.Users.id == user_id) \
        .filter(models.Users.id == user.get("id")) \
        .first()

    if user_model is None:
        raise http_exception()

    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()

    return successful_response(200)


def http_exception():
    return HTTPException(status_code=404, detail='User not found')


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }

