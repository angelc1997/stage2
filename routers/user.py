from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from database import dbconfig
import mysql.connector
from mysql.connector import pooling
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from config import tokenconfig


SECRET_KEY = tokenconfig["SECRET_KEY"]
ALGORITHM = tokenconfig["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = tokenconfig["ACCESS_TOKEN_EXPIRE_DAYS"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth")
http_bearer = HTTPBearer()

user = APIRouter()
book = APIRouter()


class SuccessResponse(BaseModel):
    ok: bool = True

class ErrorResponse(BaseModel):
    error: bool = True
    message: str = "請按照情境提供對應的錯誤訊息"

class SignUpUser(BaseModel):
    name: str = "test"
    email: EmailStr = "test@gmail.com"
    password: str = "test"

class SignInUser(BaseModel):
    email: EmailStr = "test@gmail.com"
    password: str = "test"

class SignInResponse(BaseModel):
    token: str = "a21312xzDSA"

class UserAuthInfo(BaseModel):
    id: int = 1
    name: str = "test"
    email: EmailStr ="test@gmail.com"

class UserAuthInfoObject(BaseModel):
    data: UserAuthInfo

class BookingPost(BaseModel):
    attractionId: int = 10
    date: str = "2022/01/31"
    time: str  = "afternoon"
    price: int = 2500

class Attraction(BaseModel):
    id: int = 10
    name: str = "平安鐘"
    address: str = "臺北市大安區忠孝東路 4 段"
    image: str = "https://yourdomain.com/images/attraction/10.jpg"


class BookingInfo(BaseModel):
    attraction: Attraction
    date: str = "2022-01-31"
    time: str = "afternoon"
    price: int = 2000

class BookingInfoList(BaseModel):
    data: BookingInfo
    


# 驗證密碼
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 加密密碼
def get_password_hash(password):
    return pwd_context.hash(password)

# 取得使用者by email
def get_user(email: str):
    try:
        
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT * FROM member WHERE email = %s"
        cursor.execute(sql_string, (email,))
        data = cursor.fetchone()
        
        if not data:
            return None
        
        cursor.close()
        cnx.close()
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    
# 確認是否有使用者
def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user[3]):
        return False
    return user

# 產生TOKEN
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 使用TOKEN取得使用者
async def get_current_user(token: str):
    try:
        # 確認TOKEN
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT * FROM member WHERE token = %s"
        cursor.execute(sql_string, (token,))
        data = cursor.fetchone()
        
        # 確認是否有TOKEN
        if not data:
            return None
        
        cursor.close()
        cnx.close()
        
        # 解碼TOKEN
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="沒有授權")



@user.post("/user", summary="註冊一個新的會員", responses={
              200: {"model": SuccessResponse, "description": "註冊成功"},
              400: {"model": ErrorResponse,"description": "註冊失敗，重複的 Email 或其他原因"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}})

async def post_user(user: SignUpUser):
    try:
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT * FROM member WHERE email = %s"
        cursor.execute(sql_string, (user.email,))
        
        if cursor.fetchone():
            return ErrorResponse(message="此信箱已被註冊")

        # 存入加密的密碼
        hashed_password = pwd_context.hash(user.password)

        sql_string = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
        val = (user.name, user.email, hashed_password)
        cursor.execute(sql_string, val)
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"ok": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    
@user.get("/user/auth", summary="取得當前登入的會員資訊", responses={
    200: {"model": UserAuthInfoObject, "description": "已登入的會員資料，null 表示未登入"},
})
async def get_decode_token(credentials: HTTPBasicCredentials = Depends(http_bearer)):

    try:
        token = credentials.credentials
        email = await get_current_user(token)
        
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT id, name, email FROM member WHERE email = %s"
        cursor.execute(sql_string, (email,))
        data = cursor.fetchone()
        cursor.close()
        cnx.close()

        if data:
            user_info = UserAuthInfo(id=data[0], name=data[1], email=data[2])
            return {"data": user_info}
        else:
            return {"data": None}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    

@user.put("/user/auth", summary="登入會員帳戶", responses={
    200: {"model": SignInResponse, "description": "登入成功，得有效期為七天的 JWT 加密字串"},
    400: {"model": ErrorResponse, "description": "登入失敗，帳號或密碼錯誤或其他原因"},
    500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}
})
async def get_encode_token(user: SignInUser):
    try:
        user = authenticate_user(user.email, user.password)

        if not user:
            return ErrorResponse(message="帳號或密碼錯誤")
        
        access_token_expires = timedelta(days=7)
        access_token = create_access_token(
            data={"sub": user[2]},
            expires_delta=access_token_expires
        )

        # 紀錄使用者的TOKEN
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        sql_string = "UPDATE member SET token = %s WHERE email = %s"
        cursor.execute(sql_string, (access_token, user[2]))
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"token": access_token}

    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    

    

@book.get("/booking", summary= "取得尚未確認下單的預定行程", responses={
    200: {"model": BookingInfoList, "description": "尚未確認下單的預定行程資料，null 表示沒有資料"},
    403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"}
})
async def get_booking(credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        email = await get_current_user(token)
        
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT id FROM member WHERE email = %s"
        cursor.execute(sql_string, (email,))
        data = cursor.fetchone()        

        if not data:
            raise HTTPException(status_code=400, detail="未登入")
        
        # 獲取預定行程資訊
        sql_string = "SELECT booking.date, booking.time, booking.price, attractions.id AS AttractionID, attractions.name AS AttractionName, attractions.address, (SELECT CONCAT(GROUP_CONCAT(CONCAT(pictures.url))) FROM pictures WHERE pictures.attr_id = attractions.id) AS urls FROM booking INNER JOIN attractions ON booking.AttractionID = attractions.id WHERE booking.MemberID = %s;"

    
        cursor.execute(sql_string, (data[0],))
        booking = cursor.fetchone()

        if not booking:
            return {"data": None}

        booking = {
            "data": {
                "attraction" : {
                    "id": booking[3],
                    "name": booking[4],
                    "address": booking[5],
                    "image": booking[6].split(",")[0]
                },
                "date": booking[0],
                "time": booking[1],
                "price": booking[2]
                }
        }
            

        return booking

       

    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

@book.post("/booking", summary= "建立新的預定行程", responses={
    200: {"model": BookingPost, "description": "建立成功"},
    400: {"model": ErrorResponse, "description": "建立失敗，輸入不正確或其他原因"},
    403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"}
})
async def post_booking(form: BookingPost, credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        email = await get_current_user(token)
        
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT id FROM member WHERE email = %s"
        cursor.execute(sql_string, (email,))
        data = cursor.fetchone()
    
        if not data:
            raise HTTPException(status_code=403, detail="未登入")
        
        #  更新預定行程資訊
        if form.date is None:
            raise HTTPException(status_code=400, detail="請輸入日期")
        
        if form.time is None:
            raise HTTPException(status_code=400, detail="請輸入時間")
        
        if form.price is None:
            raise HTTPException(status_code=400, detail="請輸入價格")

        sql_string = """
        INSERT INTO booking (MemberID, AttractionID, Date, Time, Price) 
        VALUES (%s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
            AttractionID = VALUES(AttractionID), 
            Date = VALUES(Date), 
            Time = VALUES(Time), 
            Price = VALUES(Price);
        """
        val = (data[0], form.attractionId, form.date, form.time, form.price)        
        cursor.execute(sql_string, val)
        cnx.commit()
        cursor.close()
        cnx.close()


        return {"attractionId": form.attractionId, "date": form.date, "time": form.time, "price": form.price}
        
       
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

    

@book.delete("/booking", summary= "刪除目前的預定行程", responses={
    200: {"model": SuccessResponse, "description": "刪除成功"},
    403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"}
})
async def delete_booking(credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try: 
        token = credentials.credentials
        email = await get_current_user(token)
        
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT id FROM member WHERE email = %s"
        cursor.execute(sql_string, (email,))
        data = cursor.fetchone()

        if not data:
            raise ErrorResponse(message="未登入")
        
        #  刪除預定行程資訊
        sql_string = "DELETE FROM booking WHERE MemberID = %s"
        cursor.execute(sql_string, (data[0],))
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"ok": True}
    
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
