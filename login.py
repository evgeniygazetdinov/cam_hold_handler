from fastapi import FastAPI,Depends,status, Request
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager #Loginmanager Class
from fastapi_login.exceptions import InvalidCredentialsException #Exception class
from fastapi.templating import Jinja2Templates
from os import path
import uvicorn

app= FastAPI()

SECRET = "secret-key"
# To obtain a suitable secret key you can run | import os; print(os.urandom(24).hex())
pth = path.dirname(__file__)
templates = Jinja2Templates(directory=path.join(pth, "templates"))

manager = LoginManager(SECRET, token_url="/auth/login",use_cookie=True)
manager.cookie_name = "some-name"

DB = {"username":{"password":"qwertyuiop"}} # unhashed

@manager.user_loader()
def load_user(username:str):
    user = DB.get(username)
    return user

@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={"sub":username}
    )
    resp = RedirectResponse(url="/private",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    return resp
    

@app.get("/private")
def getPrivateendpoint(_=Depends(manager)):
    return "You are an authentciated user"

@app.get("/",response_class=HTMLResponse)
def loginwithCreds(request:Request):
    with open(path.join(pth, "templates/login_form.html")) as f:
        return HTMLResponse(content=f.read())


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)