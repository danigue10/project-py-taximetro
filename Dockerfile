# Usamos una imagen oficial y ligera de Python
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos e instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente al contenedor
COPY . .

# Exponemos los puertos de FastAPI (8000) y Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Comando por defecto para arrancar la API (o podemos usar docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]