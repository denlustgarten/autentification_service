from fastapi import FastAPI, Form
from fastapi.responses import Response


app = FastAPI()

users = {
    "denis@user.com":{
        "name": "Denis",
        "password": "123456",
        "balans": 100_000
    },
    "mark@user.com":{
        "name": "Mark",
        "password": "87654321",
        "balans": 200_000
    }
}


@app.get("/")
def index_page():
    with open("templates/login.html", "r") as f:
        login_page = f.read()
    return Response(login_page, media_type="text/html")


@app.post("/login")
def process_login_page(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user["password"]!= password:
        return Response(f"{username}, я Вас не знаю!", media_type="text/html")

    return Response(f"Привет {user['name']}!<br />Твой баланс: {user['balans']}",
    media_type="text/html")