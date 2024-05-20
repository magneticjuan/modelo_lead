import numpy as np
import pandas as pd

def identificar_outliers(df, columna):
    """
    Identifica los outliers en una columna de un DataFrame.

    Un outlier se define como un valor que se desvía más de tres desviaciones estándar de la media.

    Args:
    df (pd.DataFrame): El DataFrame que contiene los datos.
    columna (str): El nombre de la columna en la que se deben identificar los outliers.

    Returns:
    list: Una lista de índices de las filas que contienen outliers.
    """
    media = df[columna].mean()
    desv_std = df[columna].std()
    umbral = 3

    outliers = np.abs(df[columna] - media) > (umbral * desv_std)

    return df[outliers].index.tolist()

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