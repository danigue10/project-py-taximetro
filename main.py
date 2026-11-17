from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Importamos nuestro motor de base de datos y modelos del Paso 1
from database import init_db, get_db, CarreraModel

app = FastAPI(title="TaxiTech API", version="1.0.0")

# Inicializamos la base de datos al arrancar la API
@app.on_event("startup")
def startup_event():
    init_db()

# Esquema de datos para validar lo que nos envían (Pydantic)
class CarreraCreate(BaseModel):
    duracion_segundos: float
    importe_eur: float

class CarreraResponse(CarreraCreate):
    id: int
    fecha: str
    estado_final: str

    class Config:
        from_attributes = True

# 1. Endpoint para guardar una nueva carrera (Método POST)
@app.post("/carreras", response_model=CarreraResponse)
def crear_carrera(carrera: CarreraCreate, db: Session = Depends(get_db)):
    nueva_carrera = CarreraModel(
        duracion_segundos=carrera.duracion_segundos,
        importe_eur=carrera.importe_eur
    )
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)
    return nueva_carrera

# 2. Endpoint para consultar todo el historial (Método GET)
@app.get("/carreras", response_model=List[CarreraResponse])
def obtener_carreras(db: Session = Depends(get_db)):
    carreras = db.query(CarreraModel).all()
    return carreras