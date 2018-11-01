from functools import reduce
from config import laps, via_arrivee, via_depart, via_ligne
import requests
import datetime

# 0 = éteinte
# 1 = allumée
# 2 = clignote
ledVianavigo = {
    "rouge": 0,
    "orange": 0,
    "vert": 0
}

messagesVianavigo = []

def estInTime(t):
    now = datetime.datetime.now()

    arrivée = (now.minute + int(t)) % 60
    if arrivée >= laps[0] and arrivée <= laps[1] and int(t) < 61:
        return True
    else:
        return False

def rechercheDansLaps(e):

    if e.get("time", False):
        decompte = e["time"]
    else:
        return 0

    if estInTime(decompte):
        return 1
    else:
        return 0

def rechercheRetards(e):

     return e["code"] == "message" and e["schedule"].lower() == "retardé"


def vianavigo():
    # Data
    rVIANAVIGO = requests.get("https://api.vianavigo.com/lines/{}/stops/{}/to/{}/realTime".format(via_ligne,
                                                                                                  via_depart,
                                                                                                  via_arrivee),
                              headers={'X-Host-Override':'vgo-api'})
    dataVIANAVIGO = rVIANAVIGO.json()

    # Somme de tous les trains dans le laps de temps donné
    nbTrains = reduce(lambda x, y: x+y, map(rechercheDansLaps, dataVIANAVIGO))
    if nbTrains <= 1:
        ledVianavigo["rouge"] = 1
        messagesVianavigo.append("Moins de 2 trains dans le laps de temps")
    else:
        messagesVianavigo.append("{} trains ont été trouvés dans le laps de temps".format(nbTrains))

    # Check les retards sur toute la période
    if True in list(map(rechercheRetards, dataVIANAVIGO)):
        ledVianavigo["rouge"] = 2
        messagesVianavigo.append("Au moins 1 train est marqué retardé")
    else:
        messagesVianavigo.append("{} trains sont ON_TIME".format(len(dataVIANAVIGO)))

if __name__ == "__main__":
    vianavigo()




