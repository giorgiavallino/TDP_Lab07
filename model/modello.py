import copy
from database.meteo_dao import MeteoDao

class Model:

    def __init__(self):
        self.nSoluzioni = 0
        self.costoOttimo = -1
        self.soluzioneOttima = []

    def getMediaUmidita(self, mese):
        return MeteoDao.getMediaUmidita(mese)

    def calcolaSequenza(self, mese):
        self.nSoluzioni = 0
        self.costoOttimo = -1
        self.soluzioneOttima = []
        situazioni = MeteoDao.getSituazioniMetaMese(mese)
        self._ricorsione([], situazioni)
        return self.costoOttimo, self.soluzioneOttima

    def trovaPossibiliStep(self, soluzione_parziale, lista_situazioni):
        giorno = len(soluzione_parziale) + 1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def isAdmissible(self, candidato, soluzione_parziale):
        # Vincolo sui 6 giorni
        counter = 0
        for situazione in soluzione_parziale:
            if situazione.localita == candidato.localita:
                counter = counter + 1
        if counter >= 6:
            return False
        # Vincolo sulla permanenza --> la condizione viene analizzata studiando i giorni precedenti (tranne quando si
        # analizza il primo giorno)
        if len(soluzione_parziale) == 0:
            return True
        # 1) se la lunghezza della soluzione parziale è minore di 3, nella prima città selezionata il tecnico dovrà
        # rimanerci tre giorni
        if len(soluzione_parziale) < 3:
            if candidato.localita != soluzione_parziale[0].localita:
                return False
        # 2) le tre situazioni precedenti non sono tutte uguali
        else:
            if (soluzione_parziale[-3].localita != soluzione_parziale[-2].localita
                or soluzione_parziale[-3].localita != soluzione_parziale[-1].localita
                or soluzione_parziale[-2].localita != soluzione_parziale[-1].localita):
                if soluzione_parziale[-1].localita != candidato.localita:
                    return False
        # Altrimenti va bene...
        return True

    def calcolaCosto(self, soluzione_parziale):
        costo = 0
        # Costo umidità
        for situazione in soluzione_parziale:
            costo = costo + situazione.umidita
        # Costo spostamenti
        for i in range(len(soluzione_parziale)):
            # Il controllo inizia dal terzo giorno: se i due giorni precedenti il tecnico non è stato nella stessa
            # città in cui si trova ora, il cliente deve pagare 100 euro aggiuntivi
            if  (i >= 2 and
                (soluzione_parziale[i-1].localita != soluzione_parziale[i].localita
                or soluzione_parziale[i-2].localita != soluzione_parziale[i].localita)):
                costo = costo + 100
        return costo

    def _ricorsione(self, soluzione_parziale, lista_situazioni):
        # Condizione terminale
        if len(soluzione_parziale) == 15:
            self.nSoluzioni = self.nSoluzioni + 1
            costo = self.calcolaCosto(soluzione_parziale)
            if self.costoOttimo == -1 or self.costoOttimo > costo:
                self.costoOttimo = costo
                self.soluzioneOttima = copy.deepcopy(soluzione_parziale)
        # Caso ricorsivo
        else:
            # Cercare le città per il giorno che serve
            candidati = self.trovaPossibiliStep(soluzione_parziale, lista_situazioni) # --> restituisce i candidati
            # che hanno il giorno richiesto
            # Provare ad aggiungere una di queste città e proseguire
            for candidato in candidati:
                # Bisogna verificare i vincoli prima di appendere il candidato alla soluzione parziale!
                if self.isAdmissible(candidato, soluzione_parziale):
                    soluzione_parziale.append(candidato)
                    self._ricorsione(soluzione_parziale, lista_situazioni)
                    soluzione_parziale.pop()


if __name__=="__main__":
    myModel = Model()
    print(myModel.calcolaSequenza(2))
    print(myModel.nSoluzioni)