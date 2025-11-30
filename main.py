from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from configurations.conection import DatabaseConnection
import os
from services.openweathermapservice import get_meteorological_data


API_KEY = os.getenv("API_KEY_OpenWeatherMap")
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

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    mydb = DatabaseConnection(host="localhost", user="root", password="Fg20180418", database="class3")
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    data = mycursor.fetchone()
    mydb_conn.commit()
    if data is None:
        return JSONResponse(content={"message": "Usuario no encontrado"}, status_code=404)
    return data

@app.get("/weather/{city}")
async def get_weather(city: str):
    weather_data = get_meteorological_data(city, API_KEY)
    if "error" in weather_data:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return JSONResponse(content=weather_data, status_code=200)