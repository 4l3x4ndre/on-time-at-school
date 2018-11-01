from _functools import reduce
from config import laps, stifKey
import requests
import maya
import zulu

# 0 = éteinte
# 1 = allumée
# 2 = clignote
ledSTIF = {
    "rouge": 0,
    "orange": 0,
    "vert": 0
}

msgSTIF = []


def calculMinutesPourLasp(tAimed, tExpected):
    minutesExpected = maya.parse(tExpected).minute

    heureExpected = maya.parse(tExpected).hour
    heureActuelle = zulu.now().hour

    if minutesExpected >= laps[0] and minutesExpected <= laps[1] and heureExpected == heureActuelle:
        return True
    else:
        return False


def rechercheDansLaps(e):

    tAimed = e['MonitoredVehicleJourney']['MonitoredCall'].get('AimedArrivalTime',False)
    tExpected = e['MonitoredVehicleJourney']['MonitoredCall'].get('ExpectedArrivalTime', False)

    if tExpected != False and tAimed != False:

        if calculMinutesPourLasp(tAimed, tExpected):
            return 1
        else:
            return 0
    else:
        return 0


def rechercheOnTime(e):

    status = e['MonitoredVehicleJourney']['MonitoredCall']['ArrivalStatus']
    if status == "ON_TIME":
        return True
    else:
        return False

def stif() :
    #data STIF
    rSTIF = requests.get("https://api-lab-trone-stif.opendata.stif.info/service/tr-unitaire-stif/stop-monitoring",
                         params={'MonitoringRef': "STIF:StopPoint:Q:41177:",
                             'apikey': stifKey
                             },
                         headers={'Accept': 'application/json'})
    dataSTIF = rSTIF.json()
    extendDataSTIF = dataSTIF['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']

    # Somme de tous les trains dans le laps de temps donné
    nbTrains = reduce(lambda x, y: x+y, map(rechercheDansLaps, extendDataSTIF))
    if nbTrains <= 1:
        ledSTIF["rouge"] = 1
        msgSTIF.append("Moins de 2 trains dans le laps de temps")
    else:
        msgSTIF.append("{} trains ont été trouvés dans le laps de temps".format(nbTrains))

    # Cherche les train non On Time
    if False in list(map(rechercheOnTime, extendDataSTIF)):
        ledSTIF["rouge"] = 2
        msgSTIF.append("Au moins 1 train n'est pas ON_TIME")
    else:
        msgSTIF.append("{} trains sont ON_TIME".format(len(extendDataSTIF)))

if __name__ == "__main__":
    stif()