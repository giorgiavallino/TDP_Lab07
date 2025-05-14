from database.DB_connect import DBConnect
from model.situazione import Situazione

class MeteoDao:

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getMediaUmidita(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, AVG(s.Umidita) AS mediaUmidita
                    FROM situazione s 
                    WHERE MONTH(s.`Data`) = %s
                    GROUP BY s.Localita """
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append((row["Localita"], row["mediaUmidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getSituazioniMetaMese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Umidita, s.`Data`
                    FROM situazione s
                    WHERE MONTH(s.`Data`)=%s AND DAY(s.`Data`)<=15
                    ORDER BY s.`Data` ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result


if __name__=="__main__":
    print(MeteoDao.getSituazioniMetaMese(1))