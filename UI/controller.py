import flet as ft

from UI.view import View
from model.modello import Model

class Controller:
    def __init__(self, view: View, model: Model):
        # The view, with the graphical elements of the UI
        self._view = view
        # The model, which implements the logic of the program and holds the data
        self._model = model
        # Other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value
        if mese == None:
            self._view.create_alert("Selezionare un mese dell'anno per proseguire nell'operazione")
            self._view.update_page()
            return
        result = self._model.getMediaUmidita(mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))
        for element in result:
            self._view.lst_result.controls.append(ft.Text(f"{element[0]} - {element[1]}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value
        if mese == None:
            self._view.create_alert("Selezionare un mese dell'anno per proseguire nell'operazione")
            self._view.update_page()
            return
        result = self._model.calcolaSequenza(mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {result[0]}"))
        for element in result[1]:
            self._view.lst_result.controls.append(ft.Text(f"{element}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

