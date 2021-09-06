import requests
import tabula
import pandas as pd
from unidecode import unidecode
from util import COMUNAS


def search_table_1(tables):
    max_size = 0
    bigger_table = None

    for table in tables:
        size = table.size
        if size > max_size:
            max_size = size
            bigger_table = table

    return bigger_table


def clean_table_1(df):
    # Eliminar columnas sin datos
    df = df.dropna(axis=1, how="all")
    # Eliminar columnas no relevantes
    df = df.iloc[:, 0:2]
    # Renombrar columnas
    df = df.rename(columns={df.columns[0]: "Comuna", df.columns[1]: "Casos nuevos"})
    # Eliminar filas con datos faltantes
    df = df.dropna()
    # Eliminar columnas de provincias
    df = df.drop(df[df.Comuna.str.contains("rovincia")].index)
    return df


def clean_table_2(df):
    # Guardar info de primera fila, que está guardada cómo nombre de columna
    comuna = df.columns[0]
    casos_nuevos = df.columns[1]
    # Renombrar columnas
    df = df.rename(columns={df.columns[0]: "Comuna", df.columns[1]: "Casos nuevos"})
    # Eliminar columnas y filas no pertinentes
    df = df.iloc[:-3, 0:2]
    # Añadir comuna faltante
    df = df.append({"Comuna": comuna, "Casos nuevos": casos_nuevos}, ignore_index=True)
    # Eliminar filas sin datos.
    df = df.dropna()
    # Eliminar columnas de provincias
    df = df.drop(df[df.Comuna.str.contains("rovincia")].index)
    return df


def generar_csv(reporte):
    try:
        # Descargar reporte
        pdf = requests.get(reporte.link).content
        pdf_file = open(reporte.pdf_path, "wb")
        pdf_file.write(pdf)
        pdf_file.close()

        # Obtener tabla en primera página
        tables = tabula.read_pdf(reporte.pdf_path, pages=1, multiple_tables=True)
        tabla_casos_nuevos_1 = search_table_1(tables)
        tabla_casos_nuevos_1 = clean_table_1(tabla_casos_nuevos_1)

        # Tabla en segunda página
        tables = tabula.read_pdf(reporte.pdf_path, pages=2, multiple_tables=True)
        tabla_casos_nuevos_2 = tables[0]
        tabla_casos_nuevos_2 = clean_table_2(tabla_casos_nuevos_2)

        tabla_casos_nuevos = tabla_casos_nuevos_1.append(tabla_casos_nuevos_2)
        tabla_casos_nuevos = tabla_casos_nuevos.reset_index(drop=True)
        rows = len(tabla_casos_nuevos.index)

        print(reporte.date, "analizado. Se encontraron", rows, "filas con datos.")

        # Eliminar duplicados
        casos_nuevos = []
        for comuna in COMUNAS:
            resultados = tabla_casos_nuevos[
                tabla_casos_nuevos.Comuna.apply(unidecode) == unidecode(comuna)
            ]
            casos_nuevos_comuna = 0

            for resultado in resultados["Casos nuevos"]:
                if casos_nuevos_comuna == 0:
                    casos_nuevos_comuna = int(resultado)
                elif int(resultado) < casos_nuevos_comuna:
                    casos_nuevos_comuna = int(resultado)

            casos_nuevos.append([comuna, casos_nuevos_comuna])

        casos_nuevos = pd.DataFrame(casos_nuevos, columns=["Comuna", "Casos nuevos"])

        # Guardar en csv
        casos_nuevos.to_csv(reporte.csv_path, index=False)
    except Exception as e:
        print("Error al obtener el reporte", reporte)
        print(e)
