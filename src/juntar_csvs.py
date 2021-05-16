import glob
import pandas as pd
from util import COMUNAS
from os import path

CSV_FILE_PATH = "./Casos Nuevos/*.csv"

def juntar_csvs():
    print("Juntanto archivos csv...")
    file_paths = glob.glob(CSV_FILE_PATH)
    print("Se encotraron", len(file_paths), "archivos csv")

    casos_nuevos_diarios = pd.DataFrame(columns=COMUNAS)

    for file_path in file_paths:
        file_base = path.basename(file_path)
        # Ignorar archivos "Casos Diarios.csv"
        if ((file_base == "Casos Diarios.csv")
                or (file_base == "Casos Diarios_T.csv")):
            continue
        
        file_name = path.splitext(file_base)[0]
        # Abrir archivo csv
        reporte_dia = pd.read_csv(file_path)
        reporte_dia = reporte_dia.rename(columns={"Casos nuevos": file_name})
        reporte_dia = reporte_dia.set_index("Comuna")
        reporte_dia = reporte_dia.T
        casos_nuevos_diarios = casos_nuevos_diarios.append(reporte_dia)

    casos_nuevos_diarios = casos_nuevos_diarios.sort_index()

    casos_nuevos_diarios.T.to_csv("./Casos Nuevos/casos-diarios.csv")
    casos_nuevos_diarios.to_csv("./Casos Nuevos/casos-diarios_T.csv")