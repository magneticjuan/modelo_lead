import pandas as pd
import numpy as np
import funciones as fn  # Módulo personalizado 'funciones' que contiene funciones útiles
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from ydata_profiling import ProfileReport

# Cargar datos desde un archivo CSV
print("Cargando datos...")
df = pd.read_csv('Datos_Train_Calidad_Lead.csv')
print("Datos cargados exitosamente")

# Convertir la columna 'picklist_ciudad__c' en binaria (1 para 'Bogotá', 0 para otras ciudades)
print("Convirtiendo la columna 'picklist_ciudad__c' a binaria...")
df['picklist_ciudad__c'] = df['picklist_ciudad__c'].apply(lambda x: 1 if x == 'Bogotá' else 0)
print("Conversión completada")
print(df['picklist_ciudad__c'].value_counts())

# Mapeo de la columna 'Calidad_de_lead__c'
print("Mapeando la columna 'Calidad_de_lead__c'...")
mapping = {'Alta': 1, 'Media': 0, 'Descalificado': -1}
df['Calidad_de_lead__c'] = df['Calidad_de_lead__c'].map(mapping)
print("Mapeo completado")

# Identificar y mostrar los outliers en cada columna
print("Identificando outliers...")
for columna in df.columns:
    outliers = fn.identificar_outliers(df, columna)
    print(f'Columna {columna}: {len(outliers)} outliers encontrados')

# Inicializar el escalador robusto
scaler = RobustScaler()

# Escalar los valores outliers en cada columna
print("Escalando valores outliers...")
for columna in df.columns:
    outliers = fn.identificar_outliers(df, columna)
    if outliers:
        # Seleccionar los valores outliers y escalarlos
        outlier_values = df.loc[outliers, columna].values.reshape(-1, 1)
        scaled_values = scaler.fit_transform(outlier_values)
        df.loc[outliers, columna] = scaled_values.flatten()
print("Escalado de outliers completado")

# Mostrar el porcentaje de valores nulos en el DataFrame
print("Calculando porcentaje de valores nulos...")
fn.porcentaje_nulos(df)

# Imputar valores nulos con la media de la columna
print("Imputando valores nulos con la media de cada columna...")
imputer = SimpleImputer(strategy='mean')
df.loc[:, df.isnull().any()] = imputer.fit_transform(df.loc[:, df.isnull().any()])
print("Imputación completada")

# Mostrar nuevamente el porcentaje de valores nulos después de la imputación
print("Recalculando porcentaje de valores nulos después de la imputación...")
fn.porcentaje_nulos(df)

# Generar un informe de perfilado del DataFrame y guardarlo como archivo HTML
print("Generando informe de perfilado...")
profile = ProfileReport(df, title='EDA Data Salesforce', explorative=True)
profile.to_file('EDA Data Salesforce')
print("Informe de perfilado guardado como 'EDA Data Salesforce.html'")

# Guardar el DataFrame limpio en un nuevo archivo CSV
print("Guardando el DataFrame limpio en un nuevo archivo CSV...")
df.to_csv('Datos_Train_Calidad_Lead_Clean.csv', index=False)
print("Datos guardados en 'Datos_Train_Calidad_Lead_Clean.csv'")