from simple_salesforce import Salesforce
import pandas as pd
from dotenv import load_dotenv
from os import getenv

# Cargar variables de entorno desde el archivo .env
load_dotenv('.env', override=True)

# Obtener credenciales de Salesforce desde las variables de entorno
USERNAME = getenv('USERNAME')
PASSWORD = getenv('PASSWORD')
SECURITY_TOKEN = getenv('SECURITY_TOKEN')

try:
    # Autenticarse en Salesforce
    sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)
    print('Conectado a Salesforce exitosamente.')
    
    # Definir los parámetros de la consulta
    columna_fecha = 'CreatedDate'
    fecha_corte = '2024-01-01T00:00:00Z'
    objeto = 'Lead'
    campo_1 = 'Cuota_Inicial__C'
    campo_2 = 'Presupuesto_inmueble_a_comprar__c'
    campo_3 = 'ingresos_totales__c'
    campo_4 = 'Ingresos_familiares__c'
    campo_5 = 'Calidad_de_lead__c'
    campo_6 = 'picklist_ciudad__c'
    
    # Formar la consulta SOQL
    query = f"SELECT {campo_1}, {campo_2}, {campo_3}, {campo_4}, {campo_5}, {campo_6} FROM {objeto} WHERE {columna_fecha} > {fecha_corte}"
    result = sf.query(query)
    print('Consulta realizada correctamente.')
    
    # Convertir el resultado de la consulta en un DataFrame de pandas
    df = pd.DataFrame(result['records'])
    
    # Eliminar la columna 'attributes' si existe
    if 'attributes' in df.columns:
        df = df.drop(columns='attributes')
    
    # Guardar el DataFrame en un archivo CSV
    df.to_csv('Datos_Train_Calidad_Lead.csv', index=False)
    print('Datos guardados en "Datos_Train_Calidad_Lead.csv".')

except Exception as e:
    print("Error conectándose a Salesforce o en la consulta:")
    print(e)