from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Definir una clase para el cuerpo de la solicitud
class PredictionRequest(BaseModel):
    pctcuota_inicial__c: float
    Presupuesto_inmueble_a_comprar__c: float
    de_ingresos_sobre_el_inmueble__c: float
    picklist_ciudad__c: bool

    class Config:
        schema_extra = {
            "example": {
                "pctcuota_inicial__c": 0.2,
                "Presupuesto_inmueble_a_comprar__c": 300000.0,
                "de_ingresos_sobre_el_inmueble__c": 0.3,
                "picklist_ciudad__c": True
            }
        }

# Cargar el modelo al iniciar la aplicación
try:
    model = joblib.load("modelo.pkl")  # Ajusta el nombre del archivo si es necesario
except FileNotFoundError:
    raise RuntimeError("El archivo del modelo no se encontró. Asegúrate de que 'modelo.pkl' esté en el directorio correcto.")

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "API is working"}

# Ruta para hacer predicciones
@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Extraer los valores de las características en el orden esperado por el modelo
        input_data = request.dict()
        input_array = np.array([input_data[feature] for feature in input_data.keys()]).reshape(1, -1)
        
        # Realizar la predicción
        prediction = model.predict(input_array)

        return {"prediction": prediction.tolist()}  # Convertir la predicción a lista para JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Correr la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)