from fastapi import FastAPI 
from routers import products 
from routers import users
from routers import jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app=FastAPI() #contexto incial

#Routers 

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

#Recursos Estáticos

@app.get("/")
async def root():
     return "Hola FastAPI"

@app.get("/url")
async def url():
     return {"url_curso":"https//mouredev.com/python"}

#Swagger: http://127.0.0.1:8000/docs
#Redocly: http://127.0.0.1:8000/redoc 