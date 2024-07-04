from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from fast.database import get_session
from fast.models import User
from fast.schemas import Message, UserPublic, UserSchema, userList

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'ola mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='nome já existe')
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='email já existe')
    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=userList)
def read_users(limit: int = 5, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPException.NOT_FOUND, detail='Usuario nao encontrado')

    db_user.password = user.password
    db_user.email = user.email
    db_user.username = user.username

    # session.add(db_user) NÃO PRECISA?!
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPException.NOT_FOUND, detail='Usuario nao encontrado')

    session.delete(db_user)
    session.commit()

    return {'message': 'usuario deletado'}


# @app.get('/users/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
# def retornar_user(id: int):
#    return database[id - 1]
# pragma: no cover  para não cobrir no teste