from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITMO="HS256" #nosotros somos de encriptar y hacer el match, tendremos la contraseña encriptada en la base de datos
ACCESS_TOKEN_DURATION= 1
SECRET="SÑGFJSLDFKJGÑLSDJFGÑLSDKJFGÑSLDKFJGLSDÑK"

router=APIRouter(prefix="/jwtlogin", 
                 tags=["jwtlogin"],
                 responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

oauth2=OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"]) #algoritmo de encriptación

#hashed_password = crypt.hash("12345") --> si quisieramos encriptar la contraseña para que se suba así en la database al momento de registrar a un usuario

class User(BaseModel): 
    username: str 
    full_name:str
    email:str
    disabled: bool 


class UserDB(User): 
    password: str 

users_db = {
    "leonardo08": {
        "username": "leonardo08",
        "full_name": "Leonardo Ortega",
        "email": "ortega@mail.com",
        "disabled": False,
        "password":"$2a$12$7ePAMnO7NhTaHaiN0eXae.wFOjX7wktNICv4UEyaikD0xj8Ld53C6"
    },
    "figueroa08": {
            "username": "figueroa08",
            "full_name": "Alejandro Figueroa",
            "email": "alejandro_figueroa@mail.com",
            "disabled": True,
            "password":"$2a$12$ODQzhEOKd95YgB11n039q.vs8DgTCvYcniqfL5nhl5FSuw4n5NpmG"
        } 
}

def search_user_db(username:str): 
    if username in users_db: 
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    

async def auth_user(token:str= Depends(oauth2)): 
        exception= HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Credenciales de autenticación inválidas",
                                headers= {"WWW-Authenticate":"Bearer"})
        
        try:
            username=jwt.decode(token, SECRET, algorithms=ALGORITMO).get("sub") #Una vez obtenido en token de los headers tenemos que desencriptarlo para buscar el usuario y demás datos
            if username is None:
                raise exception
            
        except JWTError:
            raise exception
        return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled: 
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario Inactivo",)
    return user 

#-----------------------------------------------ENDPOINTS-----------------------------------------------------------------------------------

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token={"sub":user.username,
                  "exp": expire,
                  }

    return {"access_token":jwt.encode(access_token, SECRET, algorithm=ALGORITMO), "token_type":"bearer"}

#una operacion para obtener mis datos

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user 
