from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str


app = FastAPI()


users = {
    1: {
        "name": "Esther",
        "email": "esther@example.com"
    },
    2: {
        "name": "Bob",
        "email": "bob@example.com"
    },
    3: {
        "name": "John",
        "email": "john@example.com"
    }
}


tokens = {}


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/login")
def login(data: LoginRequest):

    for user_id, user in users.items():

        if user["name"] == data.username:
            token = f"token-{user_id}"
            tokens[token] = user_id

            return {
                "message": "Login successful",
                "user_id": user_id,
                "token": token
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid username"
    )


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    authorization: str = Header(None)
):
    token = authorization.replace("Bearer ", "")
    logged_in_user = tokens.get(token)

    if logged_in_user != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return users[user_id]