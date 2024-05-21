import numpy as np
import pandas as pd

def identificar_outliers(df, columna):
    media = df[columna].mean()
    desv_std = df[columna].std()
    umbral = 3
    outliers_std = np.abs(df[columna] - media) > (umbral * desv_std)
    return {
        'outliers_std': df[outliers_std].index.tolist()
    }

def porcentaje_nulos(df):
    """
    Calcula y muestra el porcentaje de valores nulos en cada columna de un DataFrame.

    Args:
    df (pd.DataFrame): El DataFrame que contiene los datos.

    Returns:
    None
    """
    total_filas = len(df)
    for columna in df.columns:
        nulos = df[columna].isnull().sum()
        porcentaje = (nulos / total_filas) * 100
        print(f"Porcentaje de valores nulos en '{columna}': {porcentaje:.2f}%")

def ajustar_valores(valor):
    """
    Ajusta el valor de entrada según las reglas especificadas.

    Esta función toma un valor entero como entrada y ajusta su valor según las siguientes reglas:
    1. Si el valor no es cero y es menor que 1,000,000, se redondea al múltiplo de 1,000,000 más cercano.
    2. Si el valor es cero o es 1,000,000 o mayor, permanece sin cambios.

    Parámetros:
    valor (int): El valor entero de entrada que se debe ajustar.

    Devuelve:
    int: El valor ajustado según las reglas especificadas.
    """
    if valor != 0 and valor < 1000000:
        return 1000000 * (valor // 1000000 + 1)
    return valor