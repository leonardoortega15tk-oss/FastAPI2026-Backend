from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router=APIRouter(tags=["users"])

#Iniciar el server: uvicorn users:app --reload

#Debemos crear una entidad que sirva para definir a un usuario

#GET

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Leonardo", "surname":"Ortega", "url":"https://www.google.com", "age":23}, #Usuario 1
            {"name":"Diego", "surname":"Carton", "url":"https://www.google.com"}, #Usuario 2
            {"name":"Gera", "surname":"Anos", "url":"https://www.google.com"}] #Usuario 3

#Podemos trabajar con objetos --> usuario

class User(BaseModel):
    id: int #BaseModel nos da la capacidad de crear una entidad --> como crear una clase (que hereda un comportamiento de BaseModel), debemos mandarle los argumentos indicando a que pertenece
    name: str 
    surname: str
    url: str
    age: int 

users_fake_db = [User(id=1, name="Leonardo", surname="Ortega", url="https://www.google.com", age=23),
                 User(id=2, name="Diego", surname="Carton", url="https://www.google.com", age=24),
                 User(id=3, name="Gera", surname="Ano", url="https://www.google.com", age=24)]

@router.get("/users")
async def users():
    return users_fake_db

#Path
@router.get("/user/{id}")
async def user(id: int):
    return search_users(id)

#Query
@router.get("/userquery/")
async def userquery(id: int, name:str):
    return search_users(id)



#POST
@router.post("/user/")
async def user(user: User):
    if type(search_users(user.id)) == User: 
        return {"error": "El usuario ya existe"}
    else: 
        users_fake_db.append(user)
    return user 

#PUT
@router.put("/user/")
async def user(user: User): 
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index]= user
            found =True
    if not found:
        return {"error":"Usuario no actualizado (no se ha encontrado)"} 
    return user 

#DELETE
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found=True
            
    if not found:
            return {"error":"Usuario no actualizado (no se ha encontrado)"}  
            

#--------   Funciones auxiliares de búsqueda   --------

def search_users(id:int):
    users = filter (lambda user: user.id == id, users_fake_db)
    try:
        return list(users)[0]
    except:
        return {"error": f"No se ha encontrado un usuario con id: {id}"}


#------------------- STATUS CODES ------------------------
@router.post("/usernew/", response_model=User, status_code=201)
async def user(user:User):
    if type (search_users(user.id))==User:
        raise HTTPException(status_code=404, detail=f"El usuario {user.id} ya existe")
    else: users_fake_db.append(user)

    return user 