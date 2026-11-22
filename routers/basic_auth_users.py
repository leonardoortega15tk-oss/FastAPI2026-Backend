from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #la forma en que le vamos a enviar usuario y contra y la forma en que los va a capturar

router=APIRouter(prefix="/authlogin", 
                 tags=["authlogin"],
                 responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

oauth2=OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel): #esta entidad es la que irá a través de la red
    username: str 
    full_name:str
    email:str
    disabled: bool 


class UserDB(User): #hereda de usuario
    password: str 

users_db = {
    "leonardo08": {
        "username": "leonardo08",
        "full_name": "Leonardo Ortega",
        "email": "ortega@mail.com",
        "disabled": False,
        "password":"12345"
    },
    "figueroa08": {
            "username": "figueroa08",
            "full_name": "Alejandro Figueroa",
            "email": "alejandro_figueroa@mail.com",
            "disabled": True,
            "password":"54321"
        } 
}

def search_user_db(username:str): 
    if username in users_db: 
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers= {"WWW-Authenticate":"Bearer"})
    if user.disabled: 
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario Inactivo",)
    return user 


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password: 
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    return {"access_token":user.username , "token_type":"bearer"} #un token... ya que si no cada operación siempre pediría usuario y contraseña --> el token es lo que le mandamos a cada rato al backend

#Una vez autenticados:

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user 
