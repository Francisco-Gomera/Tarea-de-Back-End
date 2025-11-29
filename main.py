from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import mysql.connector
from configurations.conection import DatabaseConnection

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
async def get_users():
    mydb = DatabaseConnection(host="localhost", user="root", password="Fg20180418", database="class3")
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    mydb_conn.commit()
    return data

@app.post("/users/")
async def post_user(request: Request):
    mydb = DatabaseConnection(host="localhost", user="root", password="Fg20180418", database="class3")
    mydb_conn = await mydb.get_connection()
    request = await request.json()
    username = request['username']
    age = request['age']
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"INSERT INTO users (username, age) VALUES ('{username}', {age})")
    mydb_conn.commit()
    return JSONResponse(content={"message": "Usuario añadido correctamente"}, status_code=201)
   
