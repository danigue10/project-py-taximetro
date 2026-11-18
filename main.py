from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import init_db, get_db, CarreraModel

app = FastAPI(title="TaxiTech API Producción", version="2.0.0")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def leer_raiz():
    return {"mensaje": "API de TaxiTech en Producción operativa. Visita /docs"}

# --- Esquemas Pydantic para validar datos ---
class CarreraIniciar(BaseModel):
    estado_inicial: str = "parado"

class CarreraActualizarEstado(BaseModel):
    estado_actual: str

class CarreraFinalizar(BaseModel):
    duracion_segundos: float
    importe_eur: float

class CarreraResponse(BaseModel):
    id: int
    fecha: str
    duracion_segundos: float
    importe_eur: float
    estado_final: str

    class Config:
        from_attributes = True

# --- Endpoints del Ciclo de Vida de la Carrera ---

@app.post("/carreras/iniciar")
def iniciar_carrera(datos: CarreraIniciar, db: Session = Depends(get_db)):
    nueva_carrera = CarreraModel(
        duracion_segundos=0.0,
        importe_eur=0.0,
        estado_final=f"en_curso_{datos.estado_inicial}"
    )
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)
    return {"mensaje": "Carrera iniciada", "id_carrera": nueva_carrera.id}

@app.put("/carreras/{carrera_id}/estado")
def cambiar_estado(carrera_id: int, datos: CarreraActualizarEstado, db: Session = Depends(get_db)):
    carrera = db.query(CarreraModel).filter(CarreraModel.id == carrera_id).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    carrera.estado_final = f"en_curso_{datos.estado_actual}"
    db.commit()
    return {"mensaje": f"Estado actualizado a {datos.estado_actual}"}

@app.post("/carreras/{carrera_id}/finalizar", response_model=CarreraResponse)
def finalizar_carrera(carrera_id: int, datos: CarreraFinalizar, db: Session = Depends(get_db)):
    carrera = db.query(CarreraModel).filter(CarreraModel.id == carrera_id).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    carrera.duracion_segundos = datos.duracion_segundos
    carrera.importe_eur = datos.importe_eur
    carrera.estado_final = "completada"
    db.commit()
    db.refresh(carrera)
    return carrera

@app.get("/carreras", response_model=List[CarreraResponse])
def obtener_historial(db: Session = Depends(get_db)):
    carreras = db.query(CarreraModel).filter(CarreraModel.estado_final == "completada").all()
    return carreras