import requests
import json
from datetime import datetime

# Coordenades de Girona 
lat = 41.9794 
lon = 2.8214

# Data d'avui
avui = datetime.now().date()

# Crida a l'API Open‑Meteo per obtenir totes les temperatures horàries
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lat}&longitude={lon}"
    f"&hourly=temperature_2m&timezone=auto"
    f"&start_date={avui}&end_date={avui}"
)
resposta = requests.get(url)

if resposta.status_code == 200:
    dades = resposta.json()
    temps = dades["hourly"]["temperature_2m"]

    # Calculem màxima, mínima i mitjana sense usar max()/min()
    temp_max = temps[0]
    temp_min = temps[0]
    suma = 0

    for t in temps:
        if t > temp_max:
            temp_max = t
        if t < temp_min:
            temp_min = t
        suma += t

    temp_mitjana = round(suma / len(temps), 2)

    resultat = {
        "data": str(avui),
        "poblacio": "Girona",
        "temperatura_maxima": temp_max,
        "temperatura_minima": temp_min,
        "temperatura_mitjana": temp_mitjana
    }

    # Nom del fitxer amb la data actual
    nom_fitxer = f"temp_{avui.strftime('%Y%m%d')}.json"

    # Guardem el fitxer JSON
    with open(nom_fitxer, "w", encoding="utf-8") as f:
        json.dump(resultat, f, indent=4, ensure_ascii=False)

    print(f"Dades guardades a {nom_fitxer}")
else:
    print(f"Error en la petició: {resposta.status_code}")
