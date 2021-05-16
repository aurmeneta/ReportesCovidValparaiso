from generar_csv import generar_csv
from juntar_csvs import juntar_csvs
from obtener_reportes_disponibles import obtener_reportes_disponibles
from os import path

def filtrar_reportes(reportes):
    reportes_nuevos = []

    for reporte in reportes:
        if path.exists(reporte.csv_path):
            print(reporte.date, "ya revisado!")
        else:
            print(reporte.date, "nuevo!")
            reportes_nuevos.append(reporte)

    return reportes_nuevos
        


if __name__ == "__main__":
    reportes_disponibles = obtener_reportes_disponibles()
    reportes_nuevos = filtrar_reportes(reportes_disponibles)
    print(len(reportes_nuevos), "reportes nuevos!")

    if len(reportes_nuevos) > 0:
        print("Revisando reportes nuevos...")
        # Revisar reportes nuevos
        for reporte in reportes_nuevos:
            generar_csv(reporte)

        juntar_csvs()

    else:
        print("Nada nuevo que revisar!")

