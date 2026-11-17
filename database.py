from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Nombre del fichero de base de datos SQLite para producción
DB_NAME = "taxitech_prod.db"
DATABASE_URL = f"sqlite:///{DB_NAME}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CarreraModel(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    duracion_segundos = Column(Float, nullable=False)
    importe_eur = Column(Float, nullable=False)
    estado_final = Column(String, default="completada")

def init_db():
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Generador de sesiones para las consultas."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()