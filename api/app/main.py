from typing import Union

import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import pymysql
from dotenv import load_dotenv
import os

from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.environ.get("MYSQL_DB", "users")


def connect():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )


class User(BaseModel):
    __tablename__ = "users"

    name: str
    email: str
    password: str


@app.get("/")
def read_root():
    return {"message": "Hello"}


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print(f"Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "error": str(exc)}
    )


@app.post("/create_user")
async def create_user(user: User):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (user.name, user.email, user.password))
    conn.commit()
    conn.close()
    return {"message": "User created successfully"}


@app.put("/update_user/{user_name}")
async def update_user(user_name: str, user: User):
    conn = connect()
    cursor = conn.cursor()
    query = "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s"
    cursor.execute(query, (user.name, user.email, user.password, user_name))
    conn.commit()
    conn.close()
    return {"message": "User updated successfully"}


@app.delete("/delete_user/{user_name}")
async def delete_user(user_name: str):
    conn = connect()
    cursor = conn.cursor()
    query = "DELETE FROM users WHERE name=%s"
    cursor.execute(query, (user_name,))
    conn.commit()
    conn.close()
    return {"message": "User deleted successfully"}


@app.get("/get_users")
async def get_users():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT name, email FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return {"users": [{"name": row[0], "email": row[1]} for row in rows]}