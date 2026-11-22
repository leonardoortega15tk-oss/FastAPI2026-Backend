#Opereciones para trabajar entre los modelos y los datos en base de datos
def user_schema(user) -> dict:
      return {"id":str(user["_id"]),
              "username":user["username"],
              "email":user["email"]}   

def users_schema(users) -> list:
      return [user_schema(user) for user in users] #Aqui creo una lista de diccionariosw