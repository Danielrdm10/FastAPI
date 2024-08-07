from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import Select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast.database import get_session
from fast.models import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'senha'
ALGORITHM = 'HS256'
ACCESS_TIME = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TIME)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        if not username:
            raise HTTPException(status_code=400)

    except PyJWTError:
        raise HTTPException(status_code=400)

    user = session.scalar(Select(User).where(User.email == username))

    if not user:
        raise HTTPException(status_code=400)

    return user
