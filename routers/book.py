# from datetime import datetime, timedelta, timezone
# from typing import Annotated, List, Union
# from fastapi import APIRouter, Depends, HTTPException, Response, status
# from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials, HTTPBasicCredentials
# from pydantic import BaseModel, EmailStr
# from database import dbconfig
# import mysql.connector
# from mysql.connector import pooling
# import jwt
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
# from config import tokenconfig

# book = APIRouter()

# SECRET_KEY = tokenconfig["SECRET_KEY"]
# ALGORITHM = tokenconfig["ALGORITHM"]
# ACCESS_TOKEN_EXPIRE_DAYS = tokenconfig["ACCESS_TOKEN_EXPIRE_DAYS"]

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth")
# http_bearer = HTTPBearer()

# class SuccessResponse(BaseModel):
#     ok: bool = True

# class ErrorResponse(BaseModel):
#     error: bool = True
#     message: str = "請按照情境提供對應的錯誤訊息"

# class BookingPost(BaseModel):
#     attractionId: int = 10
#     date: str = "2022/01/31"
#     time: str  = "afternoon"
#     price: int = 2500

    

# @book.get("/booking", summary= "取得尚未確認下單的預定行程")
# async def get_booking():
#     pass

# @book.post("/booking", summary= "建立新的預定行程")
# async def post_booking(form: BookingPost, user: UserAuthInfo = Depends(get_user)):
#     pass

    


# @book.delete("/booking", summary= "刪除目前的預定行程")
# async def delete_booking():
#     return True