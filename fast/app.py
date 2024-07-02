from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from fast.models import User
from fast.schemas import Message, UserPublic, UserSchema, userDB, userList
from fast.database import get_session

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'ola mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session = Depends(get_session)):
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
def read_users(limit: int = 5, session = Depends(get_session)):
    users = session.scalars(select(User).limit(limit))
    return {'users':users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    # validar se existe e retorna o raise
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado!')

    user_with_id = userDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    # validar se existe e retorna o raise
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado!')

    del database[user_id - 1]

    return {'message': 'deletado'}


@app.get('/users/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def retornar_user(id: int):
    return database[id - 1]
