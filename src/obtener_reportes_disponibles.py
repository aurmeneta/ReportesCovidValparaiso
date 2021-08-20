from bs4 import BeautifulSoup
import requests
import datetime

from util import string_to_datetime, Reporte

START_DATE = datetime.date(2021, 2, 1)
URL_BASE = "https://seremi5.redsalud.gob.cl"
URL_REPORTES = "https://seremi5.redsalud.gob.cl/reporte-regional/"


def obtener_reportes_disponibles():
    # Descargar página del SEREMI.
    html = requests.get(URL_REPORTES)
    # Cargar página a bs.
    soup = BeautifulSoup(html.content, "html.parser")
    # Buscar tag section que es parent de los links a los reportes.
    section = soup.find("section", class_="body")
    # Buscar todos los tags a
    links = section.find_all("a")

    # Iniciar lista para guardar los reportes disponibles.
    reportes = []

    for a in links:
        # Obtener fecha del reporte
        date = string_to_datetime(a.contents[0])
        if date >= START_DATE:
            link = URL_BASE + a["href"]
            reportes.append(Reporte(date, link))
            print(Reporte(date, link))

    return reportes


if __name__ == "__main__":
    obtener_reportes_disponibles()
