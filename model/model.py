from database.meteo_dao import MeteoDao

class Model:

    def __init__(self):
        pass

    def getMediaUmidita(self, mese):
        return MeteoDao.getMediaUmidita(mese)