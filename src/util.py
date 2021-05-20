import datetime

MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"]

COMUNAS = sorted([
    "Valparaíso",
    "Viña del Mar",
    "Puchuncaví",
    "Casablanca",
    "Quintero",
    "Concón",
    "Juan Fernández",
    "Villa Alemana",
    "Quilpué",
    "Limache",
    "Olmué",
    "Cartagena",
    "El Tabo",
    "El Quisco",
    "San Antonio",
    "Algarrobo",
    "Santo Domingo",
    "Los Andes",
    "Calle Larga",
    "San Esteban",
    "Rinconada",
    "Quillota",
    "La Calera",
    "Hijuelas",
    "Nogales",
    "La Cruz",
    "San Felipe",
    "Catemu",
    "Santa Maria",
    "Panquehue",
    "Putaendo",
    "Llay-Llay",
    "La Ligua",
    "Zapallar",
    "Petorca",
    "Papudo",
    "Cabildo",
    "Isla de Pascua"
])


def string_to_month(string):
    return MONTHS.index(string.lower()) + 1

def string_to_datetime(string):
    parts = string.split(" ")

    try:
        if len(parts) != 4:
          return datetime.date(2020, 1, 1)  
        else:
            day = int(parts[0])
            month = string_to_month(parts[2])
            year = int(parts[3])
            return datetime.date(year, month, day)
    except:
        return datetime.date(2020, 1, 1)


class Reporte:
    def __init__ (self, date, link):
        self.date = date
        self.link = link
        self.csv_path = f"./casos-nuevos/{date}.csv"
        self.pdf_path = f"./{date}.pdf"

    def __str__ (self):
        return "Informe " + str(self.date) + ", Link: " + self.link