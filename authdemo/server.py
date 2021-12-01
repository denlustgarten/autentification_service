import base64
import hmac
import hashlib
from os import RTLD_NODELETE
from typing import Optional

from fastapi import FastAPI, Form, Cookie
from fastapi import responses
from fastapi.responses import Response


app = FastAPI()

SECRET_KEY = "553cc129ab9cf6247fab2db3550cb90d9822d8bae257b1f87fc401e521d561b5"
PASSWORD_SALT = "a67c233beafd397502a538f97c190a6cef74bdef41add1910d2457af1e792b62"

def sign_data(data: str) -> str:
    """Возвращает подписанные данные data"""
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_username_from_signed_string(user_name_signed: str) -> Optional[str]:
    user_name_base64, signed = user_name_signed.split(".")
    # .decode() - получение строки
    username = base64.b64decode(user_name_base64.encode()).decode()
    valid_signed = sign_data(username)
    if hmac.compare_digest(valid_signed, signed):
        return username


def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    password_hash_store = users[username]["password"].lower()
    return  password_hash == password_hash_store


users = {
    "denis@user.com":{
        "name": "Denis",
        "password": "553cc129ab9cf6247fab2db3550cb90d9822d8bae257b1f87fc401e521d561b5",#123456
        "balans": 100_000
    },
    "mark@user.com":{
        "name": "Mark",
        "password": "a67c233beafd397502a538f97c190a6cef74bdef41add1910d2457af1e792b62",#87654321
        "balans": 200_000
    }
}


@app.get("/")
def index_page(username: Optional[str] = Cookie(default=None)):
    with open("templates/login.html", "r") as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    try:
        return Response(f"Привет {users[valid_username]['name']}!", media_type="text/html")
    except KeyError:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response


@app.post("/login")
def process_login_page(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    print("user is ", user)
    print("password is ", password)
    
    if not user or not verify_password(user, password):
        return Response(f"{username}, я Вас не знаю!", media_type="text/html")

    response =  Response(
        f"Привет {user['name']}!<br />Твой баланс: {user['balans']}",
        media_type="text/html")

    username_signed = base64.b64encode(username.encode()).decode() + "." +  \
        sign_data(username)
    response.set_cookie(key="username", value=username_signed)
    return response












