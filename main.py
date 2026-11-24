from fastapi import FastAPI 
from routers import products 
from routers import users
from routers import jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app=FastAPI() #contexto incial

#Routers 

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

#Recursos Estáticos

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Para ti ❤️</title>

    <!-- Vista previa al compartir el link por WhatsApp -->
    <meta property="og:title" content="Para ti ❤️">
    <meta property="og:description" content="Ábrelo 😊">
    <meta property="og:image" content="https://fast-api-2026-backend-zdba.vercel.app/static/images/pompompurin.jpg">

    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #ffdde1, #ee9ca7);
            font-family: Georgia, serif;
            text-align: center;
            padding: 20px;
            box-sizing: border-box;
        }
        h1 {
            color: #fff;
            font-size: 2.2rem;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        }
        img {
            max-width: 90%;
            width: 400px;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        }
        p {
            color: #fff;
            font-size: 1.3rem;
            max-width: 500px;
        }
    </style>
</head>
<body>
    <h1>Hola FastAPI... y hola a ti ❤️</h1>
    <img src="/static/images/pompompurin.jpg" alt="Nosotros">
    <p>Mi primer deploy es un pompompurin para tu <3</p>
</body>
</html>
"""

@app.get("/url")
async def url():
     return {"url_curso":"https//mouredev.com/python"}

#Swagger: http://127.0.0.1:8000/docs
#Redocly: http://127.0.0.1:8000/redoc 