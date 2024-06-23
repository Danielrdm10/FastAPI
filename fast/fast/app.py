from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast.schemas import Message, UserPublic, UserSchema, userDB, userList

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'ola mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def creat_user(user: UserSchema):
    user_with_id = userDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=userList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):

    # validar se existe e retorna o raise
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado!'
        )

    user_with_id = userDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    # validar se existe e retorna o raise
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado!'
        )

    del database[user_id - 1]

    return {'message': 'deletado'}

@app.get('/users/{id}',status_code=HTTPStatus.OK, response_model=UserPublic)
def retornar_user(id: int):
    return database[id-1]
