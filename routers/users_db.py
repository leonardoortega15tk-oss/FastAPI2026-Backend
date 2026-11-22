#Users DB API

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client 
from bson import ObjectId

router=APIRouter(prefix="/userdb", 
                 tags=["userdb"],
                 responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

users_fake_db = []

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

#Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id",ObjectId(id))

#Query
@router.get("/")
async def userquery(id: str):
    return search_user("_id",ObjectId(id))



#POST
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  "El usuario ya existe")
    
    user_dict= dict(user)
    del user_dict["id"] #Aqui como lo estamos eliminando MongoDB automaticamente genera un id 

    id= db_client.users.insert_one(user_dict).inserted_id #Aqui ya hace por defecto la transformación del id con ObjectID

    new_user=user_schema(db_client.users.find_one({"_id":id})) #Especificar con un JSON
    
    return User(**new_user)

#PUT
@router.put("/", response_model=User)
async def user(user: User): 
    try:
        user_dict=dict(user)
        del user_dict["id"]
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error":"Usuario no actualizado (no se ha encontrado)"} 
   
    return search_user("_id", ObjectId(user.id)) 


#DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
            
    if not found:
            return {"error":"Usuario no actualizado (no se ha encontrado)"}  
            

#--------   Funciones auxiliares de búsqueda   --------

def search_user(field:str, key):
    try:
       user=user_schema(db_client.users.find_one({field:key}))
       return User(**user)
    except:
        return {"error": f"No se ha encontrado un usuario con id: {key}"}



#------------------- STATUS CODES ------------------------
#@router.post("/usernew/", response_model=User, status_code=status.HTTP_201_CREATED)
#async def user(user:User):
 #   if type (search_users(user.id))==User:
  #      raise HTTPException(status_code=404, detail=f"El usuario {user.id} ya existe")
   # else: users_fake_db.append(user)

    #return user 