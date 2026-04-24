import sys
import os
import re
import shutil
import json
import ctypes 
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# Prova a importare la libreria per convertire i PDF
try:
    from pdf2image import convert_from_path, pdfinfo_from_path
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False

# --- DIZIONARIO MULTILINGUA ---
CURRENT_LANG = "it"

STRINGS = {
    "it": {
        "titolo_app": "Il Mio Lettore Digitale",
        "impostazioni": "⚙️ Impostazioni",
        "caricamento": "Caricamento libreria in corso...",
        "benvenuto": "Benvenuto! Vai in ⚙️ Impostazioni per selezionare la cartella dei tuoi libri.",
        "penna": "Penna",
        "evidenziatore": "Evidenziatore",
        "gomma": "Gomma",
        "schermo_intero": "⛶ Schermo Intero",
        "riduci_schermo": "✖ Riduci Schermo",
        "mezze_pagine": "1/2 Pagine",
        "tooltip_swipe": "Abilita/Disabilita lo Swipe per cambiare pagina",
        "scegli_copertina": "Scegli Copertina",
        "impostazioni_prog": "Impostazioni Programma",
        "tema_chiaro": "Passa a Modalità Chiara ☀️",
        "tema_scuro": "Passa a Modalità Scura 🌙",
        "cartella_lib": "Cartella della tua Libreria:",
        "nessuna_cartella": "Nessuna cartella selezionata!",
        "sfoglia": "Sfoglia...",
        "strum_predefiniti": "Strumenti Predefiniti (applicati ai nuovi libri):",
        "esporta_pdf": "📄 Esporta Libri in PDF (Unito agli Appunti)",
        "chiudi": "Chiudi",
        "spessore": "Spessore",
        "opacita": "Trasparenza (Opacità)",
        "abilita_pressione": "Abilita sensibilità alla pressione",
        "scegli_colore": "Scegli Colore",
        "conferma": "Conferma",
        "attenzione": "Attenzione",
        "creazione_pdf": "Creazione PDF in corso...",
        "annulla": "Annulla",
        "esportazione_pdf": "Esportazione PDF",
        "esporta_pag": "Esportazione pagina",
        "di": "di",
        "annullato": "Annullato",
        "export_interrotta": "L'operazione è stata interrotta.",
        "fatto": "Fatto!",
        "export_successo": "I libri sono stati esportati in PDF con successo nella cartella della libreria!",
        "errore": "Errore",
        "export_errore": "C'è stato un problema:\n",
        "lingua": "Lingua / Language / Sprache:",
        "trasforma_pdf": "Trasforma PDF\nin un Libro",
        "nessun_pdf": "Nessun file PDF trovato nella cartella principale della libreria!",
        "scegli_pdf": "Scegli il PDF da convertire:",
        "nome_libro": "Come vuoi chiamare questo libro?",
        "scegli_dpi": "Scegliere la risoluzione (100 -> 1000 dpi, consigliato: 650):",
        "scegli_inizio_pagina": "Da quale pagina vuoi iniziare a contare? (Anche negativo):",
        "conv_in_corso": "Conversione PDF in corso...",
        "manca_libreria": "Libreria 'pdf2image' mancante!\nApri il terminale e scrivi: pip install pdf2image\n(Ricorda di installare anche Poppler su Windows!)",
        "seleziona_libri": "Seleziona i libri da esportare:"
    },
    "en": {
        "titolo_app": "My Digital Reader",
        "impostazioni": "⚙️ Settings",
        "caricamento": "Loading library...",
        "benvenuto": "Welcome! Go to ⚙️ Settings to select your books folder.",
        "penna": "Pen",
        "evidenziatore": "Highlighter",
        "gomma": "Eraser",
        "schermo_intero": "⛶ Full Screen",
        "riduci_schermo": "✖ Exit Full Screen",
        "mezze_pagine": "1/2 Pages",
        "tooltip_swipe": "Enable/Disable Swipe to turn pages",
        "scegli_copertina": "Choose Cover",
        "impostazioni_prog": "Program Settings",
        "tema_chiaro": "Switch to Light Mode ☀️",
        "tema_scuro": "Switch to Dark Mode 🌙",
        "cartella_lib": "Your Library Folder:",
        "nessuna_cartella": "No folder selected!",
        "sfoglia": "Browse...",
        "strum_predefiniti": "Default Tools (applied to new books):",
        "esporta_pdf": "📄 Export Books to PDF (Merged with Notes)",
        "chiudi": "Close",
        "spessore": "Thickness",
        "opacita": "Transparency (Opacity)",
        "abilita_pressione": "Enable pressure sensitivity",
        "scegli_colore": "Choose Color",
        "conferma": "Confirm",
        "attenzione": "Warning",
        "creazione_pdf": "Creating PDF...",
        "annulla": "Cancel",
        "esportazione_pdf": "PDF Export",
        "esporta_pag": "Exporting page",
        "di": "of",
        "annullato": "Canceled",
        "export_interrotta": "The operation was interrupted.",
        "fatto": "Done!",
        "export_successo": "Books successfully exported to PDF in the library folder!",
        "errore": "Error",
        "export_errore": "There was a problem:\n",
        "lingua": "Lingua / Language / Sprache:",
        "trasforma_pdf": "Convert PDF\ninto Book",
        "nessun_pdf": "No PDF files found in the main library folder!",
        "scegli_pdf": "Choose the PDF to convert:",
        "nome_libro": "What do you want to name this book?",
        "scegli_dpi": "Choose resolution (100 -> 1000 dpi, recommended: 650):",
        "scegli_inizio_pagina": "From which page do you want to start counting? (Even negative):",
        "conv_in_corso": "Converting PDF...",
        "manca_libreria": "'pdf2image' library missing!\nOpen terminal and type: pip install pdf2image\n(Remember to install Poppler on Windows too!)",
        "seleziona_libri": "Select the books to export:"
    },
    "de": {
        "titolo_app": "Mein Digitaler Leser",
        "impostazioni": "⚙️ Einstellungen",
        "caricamento": "Bibliothek wird geladen...",
        "benvenuto": "Willkommen! Gehe zu ⚙️ Einstellungen, um deinen Bücherordner auszuwählen.",
        "penna": "Stift",
        "evidenziatore": "Textmarker",
        "gomma": "Radiergummi",
        "schermo_intero": "⛶ Vollbild",
        "riduci_schermo": "✖ Vollbild beenden",
        "mezze_pagine": "1/2 Seiten",
        "tooltip_swipe": "Wischen zum Umblättern aktivieren/deaktivieren",
        "scegli_copertina": "Cover auswählen",
        "impostazioni_prog": "Programmeinstellungen",
        "tema_chiaro": "Zum Hellmodus wechseln ☀️",
        "tema_scuro": "Zum Dunkelmodus wechseln 🌙",
        "cartella_lib": "Dein Bibliotheksordner:",
        "nessuna_cartella": "Kein Ordner ausgewählt!",
        "sfoglia": "Durchsuchen...",
        "strum_predefiniti": "Standardwerkzeuge (für neue Bücher):",
        "esporta_pdf": "📄 Bücher als PDF exportieren (mit Notizen)",
        "chiudi": "Schließen",
        "spessore": "Dicke",
        "opacita": "Transparenz (Deckkraft)",
        "abilita_pressione": "Druckempfindlichkeit aktivieren",
        "scegli_colore": "Farbe wählen",
        "conferma": "Bestätigen",
        "attenzione": "Achtung",
        "creazione_pdf": "PDF wird erstellt...",
        "annulla": "Abbrechen",
        "esportazione_pdf": "PDF-Export",
        "esporta_pag": "Exportiere Seite",
        "di": "von",
        "annullato": "Abgebrochen",
        "export_interrotta": "Der Vorgang wurde abgebrochen.",
        "fatto": "Erledigt!",
        "export_successo": "Bücher erfolgreich als PDF in den Bibliotheksordner exportiert!",
        "errore": "Fehler",
        "export_errore": "Es gab ein Problem:\n",
        "lingua": "Lingua / Language / Sprache:",
        "trasforma_pdf": "PDF in Buch\numwandeln",
        "nessun_pdf": "Keine PDF-Dateien im Hauptordner gefunden!",
        "scegli_pdf": "Wähle die PDF zur Konvertierung:",
        "nome_libro": "Wie soll dieses Buch heißen?",
        "scegli_dpi": "Wähle die Auflösung (100 -> 1000 dpi, empfohlen: 650):",
        "scegli_inizio_pagina": "Ab welcher Seite möchtest du anfangen zu zählen? (auch negativ):",
        "conv_in_corso": "Konvertiere PDF...",
        "manca_libreria": "Die Bibliothek 'pdf2image' fehlt!\nÖffne das Terminal und gib ein: pip install pdf2image\n(Installiere auch Poppler unter Windows!)",
        "seleziona_libri": "Wähle die zu exportierenden Bücher:"
    }
}

def tr(chiave):
    return STRINGS.get(CURRENT_LANG, STRINGS["it"]).get(chiave, chiave)

def ordina_naturale(testo):
    # Riconosce il meno SOLO se è all'inizio della stringa per i file come "-3.png"
    return [int(c) if re.match(r'^-?\d+$', c) else c.lower() for c in re.split(r'(^-?\d+|\d+)', testo)]

def numero_da_nome(nome_file):
    # Se il file si chiama letteralmente "-3.png"
    if re.match(r'^-\d+\.', nome_file):
        match = re.search(r'^-\d+', nome_file)
        if match: return match.group(0)
    
    numeri = re.findall(r'\d+', nome_file)
    if numeri: return str(int(numeri[-1]))
    return "?"

# --- CARTA DEL LIBRO ---
class CartaLibro(QWidget):
    def __init__(self, nome, percorso, apri_callback):
        super().__init__()
        self.setFixedSize(160, 220)
        self.percorso = percorso
        self.apri_callback = apri_callback
        self.nome_libro = nome

        self.btn_copertina = QPushButton(self.nome_libro, self)
        self.btn_copertina.setGeometry(0, 0, 160, 220)
        self.btn_copertina.clicked.connect(lambda: self.apri_callback(self.percorso))

        self.btn_modifica = QPushButton("📷", self) 
        self.btn_modifica.setGeometry(130, 5, 25, 25)
        self.btn_modifica.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 100, 100, 150); 
                color: white;
                border-radius: 12px; 
                padding: 0px; 
                font-size: 12px;
                border: none;
            }
            QPushButton:hover { background-color: rgba(50, 50, 50, 200); }
        """)
        self.btn_modifica.clicked.connect(self.scegli_copertina)
        self.aggiorna_aspetto()

    def aggiorna_aspetto(self):
        copertina_path = None
        for estensione in ["jpg", "jpeg", "png"]:
            temp_path = os.path.join(self.percorso, f"copertina.{estensione}")
            if os.path.exists(temp_path):
                copertina_path = temp_path
                break

        if copertina_path:
            self.btn_copertina.setText("")
            percorso_css = copertina_path.replace("\\", "/") 
            self.btn_copertina.setStyleSheet(f"""
                QPushButton {{
                    background-image: url('{percorso_css}');
                    background-position: center;
                    background-repeat: no-repeat;
                    border-radius: 12px;
                }}
            """)
        else:
            self.btn_copertina.setStyleSheet("")
            self.btn_copertina.setText(self.nome_libro)

    def scegli_copertina(self):
        file_path, _ = QFileDialog.getOpenFileName(self, tr("scegli_copertina"), "", "Immagini (*.png *.jpg *.jpeg)")
        if file_path:
            estensione = file_path.split(".")[-1]
            nuovo_percorso = os.path.join(self.percorso, f"copertina.{estensione}")
            shutil.copy(file_path, nuovo_percorso)
            self.aggiorna_aspetto()

# --- FINESTRA DI DIALOGO PER STRUMENTI PENNA ---
class DialogoImpostazioniStrumenti(QDialog):
    def __init__(self, titolo, spessore, colore=None, usa_pressione=False, mostra_pressione=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.spessore = spessore
        self.colore = colore
        self.usa_pressione = usa_pressione

        layout = QVBoxLayout(self)

        self.lbl_spessore = QLabel(f"{tr('spessore')}: {self.spessore}")
        layout.addWidget(self.lbl_spessore)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(self.spessore)
        self.slider.valueChanged.connect(self.aggiorna_spessore)
        layout.addWidget(self.slider)

        if self.colore is not None and "Evidenziatore" in self.windowTitle() or "Highlighter" in self.windowTitle() or "Textmarker" in self.windowTitle():
            opacita_iniziale = int((self.colore.alpha() / 255) * 100)
            self.lbl_opacita = QLabel(f"{tr('opacita')}: {opacita_iniziale}%")
            layout.addWidget(self.lbl_opacita)
            
            self.slider_opacita = QSlider(Qt.Orientation.Horizontal)
            self.slider_opacita.setRange(10, 100)
            self.slider_opacita.setValue(opacita_iniziale)
            self.slider_opacita.valueChanged.connect(self.aggiorna_opacita)
            layout.addWidget(self.slider_opacita)

        if mostra_pressione:
            self.chk_pressione = QCheckBox(tr("abilita_pressione"))
            self.chk_pressione.setChecked(self.usa_pressione)
            self.chk_pressione.stateChanged.connect(self.aggiorna_pressione)
            layout.addWidget(self.chk_pressione)

        self.btn_colore = None
        if self.colore is not None:
            self.btn_colore = QPushButton(tr("scegli_colore"))
            self.aggiorna_bottone_colore()
            self.btn_colore.clicked.connect(self.scegli_colore)
            layout.addWidget(self.btn_colore)

        btn_ok = QPushButton(tr("conferma"))
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def aggiorna_spessore(self, val):
        self.spessore = val
        self.lbl_spessore.setText(f"{tr('spessore')}: {val}")

    def aggiorna_opacita(self, val):
        self.lbl_opacita.setText(f"{tr('opacita')}: {val}%")
        alpha = int((val / 100) * 255)
        self.colore.setAlpha(alpha)
        self.aggiorna_bottone_colore()

    def aggiorna_pressione(self, stato):
        self.usa_pressione = bool(stato)

    def aggiorna_bottone_colore(self):
        if self.btn_colore and self.colore:
            sfondo = f"rgba({self.colore.red()}, {self.colore.green()}, {self.colore.blue()}, {self.colore.alpha()})"
            self.btn_colore.setStyleSheet(f"background-color: {sfondo}; border-radius: 8px; padding: 10px; color: black;")

    def scegli_colore(self):
        nuovo_colore = QColorDialog.getColor(self.colore, self, tr("scegli_colore"), options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if nuovo_colore.isValid():
            self.colore = nuovo_colore
            if hasattr(self, 'slider_opacita'):
                if self.colore.alpha() == 255:
                    self.colore.setAlpha(128)
                nuova_opacita = int((self.colore.alpha() / 255) * 100)
                self.slider_opacita.setValue(nuova_opacita)
                self.lbl_opacita.setText(f"{tr('opacita')}: {nuova_opacita}%")
            
            self.aggiorna_bottone_colore()

# --- FINESTRA DI DIALOGO IMPOSTAZIONI APP ---
class DialogoImpostazioniApp(QDialog):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.main_app = main_app
        self.resize(550, 450)

        layout = QVBoxLayout(self)

        layout_lingua = QHBoxLayout()
        self.lbl_lingua = QLabel(tr("lingua"))
        layout_lingua.addWidget(self.lbl_lingua)
        self.combo_lingua = QComboBox()
        self.combo_lingua.addItems(["Italiano", "English", "Deutsch"])
        
        if CURRENT_LANG == "it": self.combo_lingua.setCurrentIndex(0)
        elif CURRENT_LANG == "en": self.combo_lingua.setCurrentIndex(1)
        elif CURRENT_LANG == "de": self.combo_lingua.setCurrentIndex(2)
        
        self.combo_lingua.currentIndexChanged.connect(self.cambia_lingua)
        layout_lingua.addWidget(self.combo_lingua)
        layout.addLayout(layout_lingua)

        self.btn_tema = QPushButton()
        self.btn_tema.clicked.connect(self.cambia_tema)
        layout.addWidget(self.btn_tema)

        self.lbl_cartella_titolo = QLabel()
        layout.addWidget(self.lbl_cartella_titolo)
        
        layout_cartella = QHBoxLayout()
        self.lbl_cartella = QLineEdit()
        self.lbl_cartella.setReadOnly(True)
        
        self.btn_sfoglia = QPushButton()
        self.btn_sfoglia.clicked.connect(self.scegli_cartella)
        
        layout_cartella.addWidget(self.lbl_cartella)
        layout_cartella.addWidget(self.btn_sfoglia)
        layout.addLayout(layout_cartella)

        riga = QFrame()
        riga.setFrameShape(QFrame.Shape.HLine)
        riga.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(riga)

        self.lbl_strum = QLabel()
        layout.addWidget(self.lbl_strum)
        layout_strumenti = QHBoxLayout()
        
        self.btn_def_penna = QPushButton()
        self.btn_def_penna.clicked.connect(self.modifica_def_penna)
        layout_strumenti.addWidget(self.btn_def_penna)
        
        self.btn_def_evid = QPushButton()
        self.btn_def_evid.clicked.connect(self.modifica_def_evid)
        layout_strumenti.addWidget(self.btn_def_evid)
        
        self.btn_def_gomma = QPushButton()
        self.btn_def_gomma.clicked.connect(self.modifica_def_gomma)
        layout_strumenti.addWidget(self.btn_def_gomma)
        
        layout.addLayout(layout_strumenti)

        riga2 = QFrame()
        riga2.setFrameShape(QFrame.Shape.HLine)
        riga2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(riga2)

        self.btn_esporta = QPushButton()
        self.btn_esporta.setStyleSheet("background-color: #d9534f; color: white;")
        self.btn_esporta.clicked.connect(self.esporta_pdf)
        layout.addWidget(self.btn_esporta)

        layout.addStretch()

        self.btn_chiudi = QPushButton()
        self.btn_chiudi.clicked.connect(self.accept)
        layout.addWidget(self.btn_chiudi)
        
        self.aggiorna_testi_ui()

    def aggiorna_testi_ui(self):
        self.setWindowTitle(tr("impostazioni_prog"))
        self.lbl_lingua.setText(tr("lingua"))
        self.btn_tema.setText(tr("tema_chiaro") if self.main_app.is_tema_scuro else tr("tema_scuro"))
        self.lbl_cartella_titolo.setText(tr("cartella_lib"))
        self.lbl_cartella.setText(self.main_app.cartella_principale if self.main_app.cartella_principale else tr("nessuna_cartella"))
        self.btn_sfoglia.setText(tr("sfoglia"))
        self.lbl_strum.setText(tr("strum_predefiniti"))
        self.btn_def_penna.setText("✒️ " + tr("penna"))
        self.btn_def_evid.setText("🖍️ " + tr("evidenziatore"))
        self.btn_def_gomma.setText("🧽 " + tr("gomma"))
        self.btn_esporta.setText(tr("esporta_pdf"))
        self.btn_chiudi.setText(tr("chiudi"))

    def cambia_lingua(self, indice):
        global CURRENT_LANG
        if indice == 0: CURRENT_LANG = "it"
        elif indice == 1: CURRENT_LANG = "en"
        elif indice == 2: CURRENT_LANG = "de"
        
        self.main_app.salva_config()
        self.aggiorna_testi_ui()
        self.main_app.aggiorna_testi_ui()

    def cambia_tema(self):
        self.main_app.cambia_tema()
        self.btn_tema.setText(tr("tema_chiaro") if self.main_app.is_tema_scuro else tr("tema_scuro"))

    def scegli_cartella(self):
        cartella_iniziale = self.main_app.cartella_principale if self.main_app.cartella_principale else ""
        nuova_cartella = QFileDialog.getExistingDirectory(self, tr("cartella_lib"), cartella_iniziale)
        if nuova_cartella:
            self.lbl_cartella.setText(nuova_cartella)
            self.main_app.cartella_principale = nuova_cartella
            self.main_app.salva_config()
            self.main_app.popola_libreria()

    def modifica_def_penna(self):
        d = self.main_app.default_tools["penna"]
        dialogo = DialogoImpostazioniStrumenti(tr("penna"), d["spessore"], QColor(d["colore"]), d["pressione"], True, self)
        if dialogo.exec():
            self.main_app.default_tools["penna"] = {
                "spessore": dialogo.spessore,
                "colore": dialogo.colore.name(QColor.NameFormat.HexArgb),
                "pressione": dialogo.usa_pressione
            }
            self.main_app.salva_config()
            
    def modifica_def_evid(self):
        d = self.main_app.default_tools["evidenziatore"]
        dialogo = DialogoImpostazioniStrumenti(tr("evidenziatore"), d["spessore"], QColor(d["colore"]), d["pressione"], True, self)
        if dialogo.exec():
            self.main_app.default_tools["evidenziatore"] = {
                "spessore": dialogo.spessore,
                "colore": dialogo.colore.name(QColor.NameFormat.HexArgb),
                "pressione": dialogo.usa_pressione
            }
            self.main_app.salva_config()

    def modifica_def_gomma(self):
        d = self.main_app.default_tools["gomma"]
        dialogo = DialogoImpostazioniStrumenti(tr("gomma"), d["spessore"], None, False, False, self)
        if dialogo.exec():
            self.main_app.default_tools["gomma"] = {"spessore": dialogo.spessore}
            self.main_app.salva_config()

    def esporta_pdf(self):
        if not self.main_app.cartella_principale: return
        
        cartelle_libri = [f for f in os.listdir(self.main_app.cartella_principale)
                          if os.path.isdir(os.path.join(self.main_app.cartella_principale, f)) and not f.startswith('.')]
        
        if not cartelle_libri:
            QMessageBox.warning(self, tr("attenzione"), tr("nessuna_pagina"))
            return

        dialogo = QDialog(self)
        dialogo.setWindowTitle(tr("esporta_pdf"))
        dialogo.resize(400, 300)
        layout = QVBoxLayout(dialogo)
        
        layout.addWidget(QLabel(tr("seleziona_libri")))
        
        lista = QListWidget()
        lista.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        lista.addItems(cartelle_libri)
        layout.addWidget(lista)

        btn_ok = QPushButton(tr("conferma"))
        btn_ok.clicked.connect(dialogo.accept)
        layout.addWidget(btn_ok)

        if dialogo.exec() == QDialog.DialogCode.Accepted:
            libri_scelti = [item.text() for item in lista.selectedItems()]
            if not libri_scelti: return
            
            annullato = False
            for libro in libri_scelti:
                if annullato: break
                
                cartella_libro = os.path.join(self.main_app.cartella_principale, libro)
                file_pdf = os.path.join(self.main_app.cartella_principale, f"{libro}.pdf")
                
                try:
                    immagini = [f for f in os.listdir(cartella_libro) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.lower().startswith('copertina')]
                    immagini = sorted(immagini, key=ordina_naturale)
                    totale_pagine = len(immagini)
                    
                    if totale_pagine == 0: continue

                    progress = QProgressDialog(f"{tr('creazione_pdf')} ({libro})", tr("annulla"), 0, totale_pagine, self)
                    progress.setWindowTitle(tr("esportazione_pdf"))
                    progress.setWindowModality(Qt.WindowModality.WindowModal)
                    progress.setMinimumDuration(0) 
                    progress.setValue(0)
                    
                    writer = QPdfWriter(file_pdf)
                    writer.setResolution(300)
                    painter = QPainter()
                    painter.begin(writer)
                    
                    cartella_edit = os.path.join(cartella_libro, ".edit")
                    
                    for i, nome in enumerate(immagini):
                        if progress.wasCanceled():
                            annullato = True
                            break
                        
                        progress.setValue(i)
                        progress.setLabelText(f"[{libro}] {tr('esporta_pag')} {i+1} {tr('di')} {totale_pagine}...")
                        QApplication.processEvents()
                        
                        if i > 0: writer.newPage()
                        
                        perc_base = os.path.join(cartella_libro, nome)
                        img_base = QImage(perc_base)
                        
                        perc_edit = os.path.join(cartella_edit, os.path.splitext(nome)[0] + ".png")
                        if os.path.exists(perc_edit):
                            img_layer = QImage(perc_edit)
                            p_comb = QPainter(img_base)
                            p_comb.drawImage(0, 0, img_layer)
                            p_comb.end()
                        
                        rect_pdf = writer.pageLayout().paintRectPixels(writer.resolution())
                        img_scalata = img_base.scaled(rect_pdf.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        
                        x = (rect_pdf.width() - img_scalata.width()) // 2
                        y = (rect_pdf.height() - img_scalata.height()) // 2
                        painter.drawImage(x, y, img_scalata)
                        
                    painter.end()
                    progress.setValue(totale_pagine)
                except Exception as e:
                    QMessageBox.critical(self, tr("errore"), f"{tr('export_errore')}{str(e)}")

            if annullato:
                QMessageBox.warning(self, tr("annullato"), tr("export_interrotta"))
            else:
                QMessageBox.information(self, tr("fatto"), tr("export_successo"))

# --- BOTTONE DOPPIO CLIC ---
class BottoneStrumento(QPushButton):
    doppio_clic = pyqtSignal()
    def mouseDoubleClickEvent(self, evento):
        self.doppio_clic.emit()
        super().mouseDoubleClickEvent(evento)

# --- VISUALIZZATORE VETTORIALE ---
class PaginaView(QGraphicsView):
    richiesta_toggle_strumento = pyqtSignal()
    richiesta_cambio_pagina = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.scena = QGraphicsScene()
        self.setScene(self.scena)
        
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)
        self.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontSavePainterState, True)
        
        self.immagine_corrente = None
        self.layer_disegno = None 
        self.item_sfondo = None
        self.item_layer = None
        self.modificata = False
        
        self.is_doppia = False
        self.percorso_sx = None
        self.percorso_dx = None
        self.size_sx = QSize(0,0)
        self.size_dx = QSize(0,0)
        
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        self.strumento = "penna"
        self.colore_penna = QColor(0, 0, 0)
        self.spessore_penna = 4
        self.usa_pressione_penna = True
        self.colore_evidenziatore = QColor(255, 255, 0, 100)
        self.spessore_evidenziatore = 20
        self.usa_pressione_evid = False
        self.spessore_gomma = 40
        self.disegnando = False
        
        self.path_corrente = None
        self.item_tratto_corrente = None
        self.usa_press_corrente = False
        
        self.tratti_temporanei_dati = []
        self.tratti_temporanei_items = []
        
        self.update_gomma_in_attesa = False
        
        self.adattato_in_larghezza = False
        self.pos_mouse_iniziale = None
        self.scroll_x_iniziale = 0

    def adatta_in_altezza(self):
        if self.immagine_corrente:
            self.fitInView(self.scena.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.adattato_in_larghezza = False

    def carica_immagini(self, perc_sx, pix_sx, perc_dx, pix_dx):
        self.salva_modifiche()
        self.scena.clear()
        
        self.percorso_sx = perc_sx
        self.percorso_dx = perc_dx
        self.is_doppia = perc_dx is not None

        if not perc_sx and not perc_dx:
            self.immagine_corrente = None
            self.layer_disegno = None
            self.modificata = False
            return

        w_sx = pix_sx.width() if pix_sx else (pix_dx.width() if pix_dx else 0)
        h_sx = pix_sx.height() if pix_sx else (pix_dx.height() if pix_dx else 0)
        w_dx = pix_dx.width() if pix_dx else w_sx
        h_dx = pix_dx.height() if pix_dx else h_sx

        self.size_sx = QSize(w_sx, h_sx)
        self.size_dx = QSize(w_dx, h_dx)

        h_max = max(h_sx, h_dx)
        w_tot = w_sx + w_dx if self.is_doppia else w_sx
        
        comp_base = QImage(w_tot, h_max, QImage.Format.Format_RGB888)
        comp_base.fill(Qt.GlobalColor.white)
        p_base = QPainter(comp_base)
        if pix_sx: p_base.drawPixmap(0, 0, pix_sx)
        if pix_dx: p_base.drawPixmap(w_sx, 0, pix_dx)
        p_base.end()
        
        self.immagine_corrente = QPixmap.fromImage(comp_base)
        self.item_sfondo = self.scena.addPixmap(self.immagine_corrente)
        self.item_sfondo.setZValue(-1) 

        self.layer_disegno = QPixmap(w_tot, h_max)
        self.layer_disegno.fill(Qt.GlobalColor.transparent)
        
        p_layer = QPainter(self.layer_disegno)
        
        def load_layer(perc, offset_x):
            if perc:
                cartella = os.path.dirname(perc)
                nome = os.path.basename(perc)
                perc_edit = os.path.join(cartella, ".edit", os.path.splitext(nome)[0] + ".png")
                if os.path.exists(perc_edit):
                    pix_edit = QPixmap(perc_edit)
                    p_layer.drawPixmap(offset_x, 0, pix_edit)
                    
        load_layer(perc_sx, 0)
        if self.is_doppia:
            load_layer(perc_dx, w_sx)
            
        p_layer.end()
        
        self.item_layer = self.scena.addPixmap(self.layer_disegno)
        self.item_layer.setZValue(1)

        self.setSceneRect(QRectF(comp_base.rect()))
        self.modificata = False

    def salva_modifiche(self):
        if self.modificata and self.layer_disegno:
            img_layer = self.layer_disegno.toImage()
            
            def salva_layer(img_taglio, perc_orig):
                if perc_orig:
                    cartella = os.path.dirname(perc_orig)
                    cartella_edit = os.path.join(cartella, ".edit")
                    
                    if not os.path.exists(cartella_edit):
                        os.makedirs(cartella_edit, exist_ok=True)
                        if os.name == 'nt':
                            FILE_ATTRIBUTE_HIDDEN = 0x02
                            ctypes.windll.kernel32.SetFileAttributesW(cartella_edit, FILE_ATTRIBUTE_HIDDEN)
                            
                    nome = os.path.basename(perc_orig)
                    perc_edit = os.path.join(cartella_edit, os.path.splitext(nome)[0] + ".png")
                    img_taglio.save(perc_edit, "PNG")

            if self.is_doppia:
                img_sx = img_layer.copy(0, 0, self.size_sx.width(), self.size_sx.height())
                salva_layer(img_sx, self.percorso_sx)
                img_dx = img_layer.copy(self.size_sx.width(), 0, self.size_dx.width(), self.size_dx.height())
                salva_layer(img_dx, self.percorso_dx)
            else:
                salva_layer(img_layer, self.percorso_sx)
            
            self.modificata = False

    def crea_penna(self, strumento, spessore):
        penna = QPen()
        penna.setCapStyle(Qt.PenCapStyle.RoundCap)
        penna.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        if strumento == "penna": penna.setColor(self.colore_penna)
        elif strumento == "evidenziatore": penna.setColor(self.colore_evidenziatore)
        penna.setWidthF(spessore)
        return penna

    def keyPressEvent(self, evento):
        if evento.key() in (Qt.Key.Key_Right, Qt.Key.Key_Left):
            evento.ignore() 
        else:
            super().keyPressEvent(evento)

    def event(self, evento):
        if evento.type() == QEvent.Type.Gesture:
            pinch = evento.gesture(Qt.GestureType.PinchGesture)
            if pinch:
                cambio_zoom = pinch.scaleFactor()
                self.scale(cambio_zoom, cambio_zoom)
                self.adattato_in_larghezza = False
            return True
        return super().event(evento)

    def mouseDoubleClickEvent(self, evento):
        if self.immagine_corrente:
            punto_scena = self.mapToScene(evento.pos())
            
            if self.adattato_in_larghezza:
                self.fitInView(self.scena.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
                self.adattato_in_larghezza = False
            else:
                scala = self.viewport().width() / self.immagine_corrente.width()
                self.resetTransform()
                self.scale(scala, scala)
                self.centerOn(punto_scena) 
                self.adattato_in_larghezza = True
        super().mouseDoubleClickEvent(evento)

    def mousePressEvent(self, evento):
        self.pos_mouse_iniziale = evento.pos()
        self.scroll_x_iniziale = self.horizontalScrollBar().value()
        super().mousePressEvent(evento)

    def mouseReleaseEvent(self, evento):
        if self.pos_mouse_iniziale is not None:
            delta_x = evento.pos().x() - self.pos_mouse_iniziale.x()
            delta_y = evento.pos().y() - self.pos_mouse_iniziale.y()
            scroll_attuale = self.horizontalScrollBar().value()
            min_scroll = self.horizontalScrollBar().minimum()
            max_scroll = self.horizontalScrollBar().maximum()

            if abs(delta_x) > 60 and abs(delta_x) > abs(delta_y) * 2:
                if delta_x < 0 and self.scroll_x_iniziale == max_scroll and scroll_attuale == max_scroll:
                    self.richiesta_cambio_pagina.emit(1)
                elif delta_x > 0 and self.scroll_x_iniziale == min_scroll and scroll_attuale == min_scroll:
                    self.richiesta_cambio_pagina.emit(-1)

        self.pos_mouse_iniziale = None
        super().mouseReleaseEvent(evento)

    def aggiorna_ui_gomma(self):
        if self.item_layer and self.layer_disegno:
            self.item_layer.setPixmap(self.layer_disegno)
        self.update_gomma_in_attesa = False

    def tabletEvent(self, evento):
        if self.strumento == "nessuno" or not self.layer_disegno:
            evento.ignore()
            return

        if evento.type() == QEvent.Type.TabletPress:
            if evento.button() in (Qt.MouseButton.MiddleButton, Qt.MouseButton.ExtraButton1, Qt.MouseButton.ExtraButton2, Qt.MouseButton.ForwardButton, Qt.MouseButton.BackButton):
                self.richiesta_toggle_strumento.emit()
                evento.accept()
                return

        punto_reale = self.mapToScene(evento.position().toPoint())
        pressione = evento.pressure() if evento.pressure() > 0 else 0.5
        is_gomma_temporanea = bool(evento.buttons() & Qt.MouseButton.RightButton)
        strumento_attivo = "gomma" if is_gomma_temporanea else self.strumento

        if evento.type() == QEvent.Type.TabletPress:
            self.disegnando = True
            self.ultimo_punto = punto_reale
            self.ultima_pressione = pressione
            
            if strumento_attivo != "gomma":
                self.usa_press_corrente = self.usa_pressione_penna if strumento_attivo == "penna" else self.usa_pressione_evid
                
                if not self.usa_press_corrente:
                    self.path_corrente = QPainterPath(self.ultimo_punto)
                    spessore = self.spessore_penna if strumento_attivo == "penna" else self.spessore_evidenziatore
                    penna = self.crea_penna(strumento_attivo, spessore)
                    self.item_tratto_corrente = self.scena.addPath(self.path_corrente, penna)
                    self.item_tratto_corrente.setZValue(2)
                else:
                    self.tratti_temporanei_dati.clear()
                    self.tratti_temporanei_items.clear()
            
            evento.accept()
            
        elif evento.type() == QEvent.Type.TabletMove and self.disegnando:
            punto_smussato = QPointF(
                self.ultimo_punto.x() * 0.3 + punto_reale.x() * 0.7,
                self.ultimo_punto.y() * 0.3 + punto_reale.y() * 0.7
            )

            if strumento_attivo == "gomma":
                pittore = QPainter(self.layer_disegno)
                pittore.setRenderHint(QPainter.RenderHint.Antialiasing)
                pittore.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
                penna = QPen(Qt.GlobalColor.transparent, self.spessore_gomma)
                penna.setCapStyle(Qt.PenCapStyle.RoundCap)
                penna.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                pittore.setPen(penna)
                pittore.drawLine(self.ultimo_punto, punto_smussato)
                pittore.end()
                
                if not self.update_gomma_in_attesa:
                    self.update_gomma_in_attesa = True
                    QTimer.singleShot(33, self.aggiorna_ui_gomma) 
            else:
                if not self.usa_press_corrente:
                    self.path_corrente.lineTo(punto_smussato)
                    self.item_tratto_corrente.setPath(self.path_corrente)
                else:
                    spessore_base = self.spessore_penna if strumento_attivo == "penna" else self.spessore_evidenziatore
                    moltiplicatore = 0.3 + (1.2 * ((pressione + self.ultima_pressione) / 2))
                    spessore = spessore_base * moltiplicatore
                    
                    penna = self.crea_penna(strumento_attivo, spessore)
                    linea = self.scena.addLine(self.ultimo_punto.x(), self.ultimo_punto.y(), punto_smussato.x(), punto_smussato.y(), penna)
                    linea.setZValue(2)
                    
                    self.tratti_temporanei_items.append(linea)
                    self.tratti_temporanei_dati.append((self.ultimo_punto, punto_smussato, penna))

            self.modificata = True
            self.ultimo_punto = punto_smussato
            self.ultima_pressione = pressione
            evento.accept()
            
        elif evento.type() == QEvent.Type.TabletRelease and self.disegnando:
            self.disegnando = False
            
            if strumento_attivo == "gomma":
                self.aggiorna_ui_gomma()
            else:
                pittore = QPainter(self.layer_disegno)
                pittore.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                if not self.usa_press_corrente:
                    if self.path_corrente is not None:
                        spessore = self.spessore_penna if strumento_attivo == "penna" else self.spessore_evidenziatore
                        pittore.setPen(self.crea_penna(strumento_attivo, spessore))
                        pittore.drawPath(self.path_corrente)
                        
                        self.scena.removeItem(self.item_tratto_corrente)
                        self.path_corrente = None
                        self.item_tratto_corrente = None
                else:
                    if self.tratti_temporanei_dati:
                        for (p1, p2, penna) in self.tratti_temporanei_dati:
                            pittore.setPen(penna)
                            pittore.drawLine(p1, p2)
                        
                        for item in self.tratti_temporanei_items:
                            self.scena.removeItem(item)
                            
                        self.tratti_temporanei_dati.clear()
                        self.tratti_temporanei_items.clear()
                        
                pittore.end()
                self.item_layer.setPixmap(self.layer_disegno)
                
            evento.accept()

# --- FINESTRA PRINCIPALE ---
class AppLibri(QMainWindow):
    def __init__(self):
        super().__init__()
        
        QApplication.instance().setDoubleClickInterval(350)
        
        if getattr(sys, 'frozen', False):
            cartella_programma = os.path.dirname(sys.executable)
        else:
            cartella_programma = os.path.dirname(os.path.abspath(__file__))
            
        self.FILE_STORICO = os.path.join(cartella_programma, "storico_lettura.json")
        self.FILE_CONFIG = os.path.join(cartella_programma, "config.json")
        
        self.carica_config()
        self.storico_pagine = {}
        self.carica_storico()
        
        self.setWindowTitle(tr("titolo_app"))
        self.resize(1200, 800)
        
        self.schermate = QStackedWidget()
        self.setCentralWidget(self.schermate)
        
        self.pagine_libro = []
        self.indice_pagina_attuale = 0
        self.vista_doppia = False
        self.swipe_abilitato = True 
        
        self.cache_pagine = {}        
        self.coda_precaricamento = [] 

        self.crea_menu()
        self.crea_lettore()
        self.applica_tema()

    def carica_config(self):
        global CURRENT_LANG
        self.cartella_principale = ""
        self.is_tema_scuro = True
        
        self.default_tools = {
            "penna": {"spessore": 4, "colore": "#ff000000", "pressione": True},
            "evidenziatore": {"spessore": 20, "colore": "#64ffff00", "pressione": False},
            "gomma": {"spessore": 40}
        }
        
        try:
            with open(self.FILE_CONFIG, 'r') as f:
                dati = json.load(f)
                CURRENT_LANG = dati.get("lingua", "it")
                self.cartella_principale = dati.get("cartella", "")
                self.is_tema_scuro = dati.get("tema", True)
                if "default_tools" in dati:
                    for k in ["penna", "evidenziatore", "gomma"]:
                        if k in dati["default_tools"]:
                            self.default_tools[k].update(dati["default_tools"][k])
        except: pass

    def salva_config(self):
        try:
            dati = {
                "lingua": CURRENT_LANG,
                "cartella": self.cartella_principale, 
                "tema": self.is_tema_scuro,
                "default_tools": self.default_tools
            }
            with open(self.FILE_CONFIG, 'w') as f:
                json.dump(dati, f)
        except: pass

    def carica_storico(self):
        try:
            with open(self.FILE_STORICO, 'r') as f:
                dati = json.load(f)
                self.storico_pagine = {}
                for k, v in dati.items():
                    if isinstance(v, int):
                        self.storico_pagine[k] = {"pagina": v}
                    else:
                        self.storico_pagine[k] = v
        except:
            self.storico_pagine = {}

    def salva_stato_libro_corrente(self):
        if hasattr(self, 'cartella_corrente') and self.cartella_corrente:
            strumenti_attuali = {
                "penna": {
                    "spessore": self.vista_libro.spessore_penna,
                    "colore": self.vista_libro.colore_penna.name(QColor.NameFormat.HexArgb),
                    "pressione": self.vista_libro.usa_pressione_penna
                },
                "evidenziatore": {
                    "spessore": self.vista_libro.spessore_evidenziatore,
                    "colore": self.vista_libro.colore_evidenziatore.name(QColor.NameFormat.HexArgb),
                    "pressione": self.vista_libro.usa_pressione_evid
                },
                "gomma": {
                    "spessore": self.vista_libro.spessore_gomma
                }
            }
            self.storico_pagine[self.cartella_corrente] = {
                "pagina": self.indice_pagina_attuale,
                "strumenti": strumenti_attuali
            }

    def salva_storico(self):
        try:
            with open(self.FILE_STORICO, 'w') as f:
                json.dump(self.storico_pagine, f)
        except: pass

    def closeEvent(self, event):
        if self.schermate.currentIndex() == 1:
            self.torna_al_menu()
            event.ignore() 
        else:
            self.salva_config()
            self.salva_stato_libro_corrente()
            self.salva_storico()
            super().closeEvent(event)

    def keyPressEvent(self, evento):
        if self.schermate.currentIndex() == 1 and not self.input_pag.hasFocus():
            if evento.key() == Qt.Key.Key_Right: self.pagina_avanti()
            elif evento.key() == Qt.Key.Key_Left: self.pagina_indietro()
        super().keyPressEvent(evento)

    def cambia_tema(self):
        self.is_tema_scuro = not self.is_tema_scuro
        self.salva_config()
        self.applica_tema()

    def applica_tema(self):
        if self.is_tema_scuro:
            bg_main = "#1e1e1e"
            bg_card = "#2d2d30"
            text_color = "#ffffff"
            border = "#3f3f46"
            hover = "#3e3e42"
        else:
            bg_main = "#f5f5f7"
            bg_card = "#ffffff"
            text_color = "#000000"
            border = "#d1d1d6"
            hover = "#e5e5ea"

        stile_globale = f"""
            QMainWindow, QDialog, QWidget#sfondo_menu, QWidget#sfondo_lettore {{
                background-color: {bg_main};
            }}
            QLabel, QCheckBox {{ color: {text_color}; }}
            QPushButton {{
                background-color: {bg_card}; color: {text_color}; border-radius: 12px; padding: 10px; border: 1px solid {border}; font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
            QPushButton:checked {{ background-color: #007aff; color: white; border: none; }}
            QLineEdit {{
                border-radius: 10px; padding: 5px; border: 1px solid {border}; color: {text_color}; background-color: {bg_card};
            }}
            QGraphicsView {{ background-color: transparent; border: none; }}
            QMenu {{ background-color: {bg_card}; color: {text_color}; border: 1px solid {border}; }}
            QMenu::item:selected {{ background-color: #007aff; color: white; }}
        """
        QApplication.instance().setStyleSheet(stile_globale)

    def crea_menu(self):
        self.widget_menu = QWidget()
        self.widget_menu.setObjectName("sfondo_menu")
        
        layout_principale = QVBoxLayout(self.widget_menu)

        barra_superiore = QHBoxLayout()
        self.btn_impostazioni = QPushButton()
        self.btn_impostazioni.setFixedSize(160, 40)
        self.btn_impostazioni.clicked.connect(self.apri_impostazioni)
        
        barra_superiore.addStretch()
        barra_superiore.addWidget(self.btn_impostazioni)
        layout_principale.addLayout(barra_superiore)

        self.layout_griglia = QGridLayout()
        self.layout_griglia.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.lbl_caricamento = QLabel()
        self.lbl_caricamento.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(self.lbl_caricamento)
        
        layout_principale.addLayout(self.layout_griglia)
        layout_principale.addStretch()
        self.schermate.addWidget(self.widget_menu)

        QTimer.singleShot(100, self.popola_libreria)

    def apri_impostazioni(self):
        dialogo = DialogoImpostazioniApp(self)
        dialogo.exec()

    def avvia_importazione_pdf(self):
        if not HAS_PDF2IMAGE:
            QMessageBox.critical(self, tr("errore"), tr("manca_libreria"))
            return

        pdfs = [f for f in os.listdir(self.cartella_principale) if f.lower().endswith(".pdf")]
        if not pdfs:
            QMessageBox.warning(self, tr("attenzione"), tr("nessun_pdf"))
            return

        pdf_scelto, ok = QInputDialog.getItem(self, "PDF", tr("scegli_pdf"), pdfs, 0, False)
        if not ok or not pdf_scelto: return

        nome_libro, ok = QInputDialog.getText(self, "Nome", tr("nome_libro"))
        if not ok or not nome_libro.strip(): return
        nome_libro = nome_libro.strip()

        dpi_scelto, ok = QInputDialog.getInt(self, "DPI", tr("scegli_dpi"), 650, 100, 1000, 50)
        if not ok: return

        # --- NUOVA OPZIONE: Scelta del numero di partenza ---
        inizio_pag, ok = QInputDialog.getInt(self, "Pagina Iniziale", tr("scegli_inizio_pagina"), 1, -10000, 10000, 1)
        if not ok: return

        cartella_destinazione = os.path.join(self.cartella_principale, nome_libro)
        if not os.path.exists(cartella_destinazione):
            os.makedirs(cartella_destinazione)

        percorso_completo = os.path.join(self.cartella_principale, pdf_scelto)

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            info = pdfinfo_from_path(percorso_completo)
            totale_pagine = info["Pages"]

            progress = QProgressDialog(tr("conv_in_corso"), tr("annulla"), 0, totale_pagine, self)
            progress.setWindowTitle("Conversione")
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)

            annullato = False
            for i in range(1, totale_pagine + 1):
                if progress.wasCanceled():
                    annullato = True
                    break

                progress.setValue(i - 1)
                progress.setLabelText(f"Pagina {i} {tr('di')} {totale_pagine}...")
                QApplication.processEvents()

                pagine = convert_from_path(percorso_completo, first_page=i, last_page=i, dpi=dpi_scelto)
                if pagine:
                    # Calcola il numero effettivo di salvataggio (anche negativo)
                    numero_pagina_corrente = inizio_pag + (i - 1)
                    nome_immagine = f"{numero_pagina_corrente}.png"
                    
                    percorso_immagine = os.path.join(cartella_destinazione, nome_immagine)
                    pagine[0].save(percorso_immagine, "PNG")

            progress.setValue(totale_pagine)
            QApplication.restoreOverrideCursor()
            self.popola_libreria()
            
            if annullato:
                QMessageBox.warning(self, tr("annullato"), tr("export_interrotta"))
            else:
                QMessageBox.information(self, tr("fatto"), "Conversione completata con successo!")

        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, tr("errore"), f"{tr('export_errore')}{str(e)}")

    def popola_libreria(self):
        for i in reversed(range(self.layout_griglia.count())): 
            widget = self.layout_griglia.itemAt(i).widget()
            if widget is not None: widget.setParent(None)

        if not self.cartella_principale or not os.path.exists(self.cartella_principale):
            self.lbl_caricamento.setText(tr("benvenuto"))
            self.lbl_caricamento.show()
        else:
            self.lbl_caricamento.hide() 

        self.btn_impostazioni.setText(tr("impostazioni"))
        self.setWindowTitle(tr("titolo_app"))

        if not self.cartella_principale or not os.path.exists(self.cartella_principale):
            return

        riga, colonna = 0, 0
        
        btn_importa = QPushButton(tr("trasforma_pdf"))
        btn_importa.setFixedSize(160, 220)
        btn_importa.setStyleSheet("background-color: #d9534f; color: white; border-radius: 12px; font-size: 16px; font-weight: bold;")
        btn_importa.clicked.connect(self.avvia_importazione_pdf)
        self.layout_griglia.addWidget(btn_importa, riga, colonna)
        colonna += 1

        for nome in os.listdir(self.cartella_principale):
            percorso = os.path.join(self.cartella_principale, nome)
            if os.path.isdir(percorso) and not nome.startswith("."):
                carta = CartaLibro(nome, percorso, self.gestisci_cartella)
                self.layout_griglia.addWidget(carta, riga, colonna)
                
                colonna += 1
                if colonna > 4:
                    colonna = 0
                    riga += 1

    def gestisci_cartella(self, percorso):
        elementi = os.listdir(percorso)
        cartelle_interne = [e for e in elementi if os.path.isdir(os.path.join(percorso, e)) and not e.startswith('.')]
        if len(cartelle_interne) > 0:
            menu_parti = QMenu(self)
            for cartella in cartelle_interne:
                azione = menu_parti.addAction(cartella)
                azione.triggered.connect(lambda checked, p=os.path.join(percorso, cartella): self.apri_libro(p))
            menu_parti.exec(QCursor.pos())
        else:
            self.apri_libro(percorso)

    def crea_lettore(self):
        self.widget_lettore = QWidget()
        self.widget_lettore.setObjectName("sfondo_lettore")
        layout_principale = QVBoxLayout(self.widget_lettore)
        
        self.barra_alta = QHBoxLayout()
        self.btn_penna = BottoneStrumento()
        self.btn_penna.setCheckable(True)
        self.btn_penna.setChecked(True)
        self.btn_penna.clicked.connect(lambda: self.imposta_strumento("penna"))
        self.btn_penna.doppio_clic.connect(self.imposta_penna)
        
        self.btn_evid = BottoneStrumento()
        self.btn_evid.setCheckable(True)
        self.btn_evid.clicked.connect(lambda: self.imposta_strumento("evidenziatore"))
        self.btn_evid.doppio_clic.connect(self.imposta_evidenziatore)

        self.btn_gomma = BottoneStrumento()
        self.btn_gomma.setCheckable(True)
        self.btn_gomma.clicked.connect(lambda: self.imposta_strumento("gomma"))
        self.btn_gomma.doppio_clic.connect(self.imposta_gomma)

        self.btn_fullscreen_top = QPushButton()
        self.btn_fullscreen_top.setFixedSize(160, 40)
        self.btn_fullscreen_top.clicked.connect(self.toggle_fullscreen)

        self.barra_alta.addWidget(self.btn_penna)
        self.barra_alta.addWidget(self.btn_evid)
        self.barra_alta.addWidget(self.btn_gomma)
        self.barra_alta.addStretch()
        self.barra_alta.addWidget(self.btn_fullscreen_top)

        centro = QHBoxLayout()
        self.vista_libro = PaginaView()
        self.vista_libro.richiesta_cambio_pagina.connect(self.gestisci_swipe)
        self.vista_libro.richiesta_toggle_strumento.connect(self.toggle_penna_evid)
        centro.addWidget(self.vista_libro)

        self.widget_basso = QWidget()
        self.barra_bassa = QHBoxLayout(self.widget_basso)
        
        btn_indietro = QPushButton("<")
        btn_indietro.setFixedSize(40, 40)
        btn_indietro.clicked.connect(self.pagina_indietro)
        
        btn_avanti = QPushButton(">")
        btn_avanti.setFixedSize(40, 40)
        btn_avanti.clicked.connect(self.pagina_avanti)

        self.input_pag = QLineEdit()
        self.input_pag.setFixedWidth(80)
        self.input_pag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_pag.returnPressed.connect(self.vai_a_pagina)
        
        self.btn_toggle_vista = QPushButton()
        self.btn_toggle_vista.clicked.connect(self.cambia_vista)
        
        self.barra_bassa.addStretch()
        self.barra_bassa.addWidget(btn_indietro)
        self.barra_bassa.addWidget(self.input_pag)
        self.barra_bassa.addWidget(self.btn_toggle_vista)
        self.barra_bassa.addWidget(btn_avanti)
        self.barra_bassa.addStretch()

        layout_nascondi = QHBoxLayout()
        layout_nascondi.addStretch()
        
        self.btn_nascondi = QPushButton("O")
        self.btn_nascondi.setFixedSize(40, 40)
        self.btn_nascondi.clicked.connect(self.toggle_interfaccia_bassa)
        
        self.btn_swipe = QPushButton("↔️ ON")
        self.btn_swipe.setFixedSize(65, 40)
        self.btn_swipe.clicked.connect(self.toggle_swipe)
        
        layout_nascondi.addWidget(self.btn_nascondi)
        layout_nascondi.addWidget(self.btn_swipe) 

        layout_principale.addLayout(self.barra_alta)
        layout_principale.addLayout(centro)
        layout_principale.addWidget(self.widget_basso)
        layout_principale.addLayout(layout_nascondi)

        self.schermate.addWidget(self.widget_lettore)
        self.aggiorna_testi_ui()

    def aggiorna_testi_ui(self):
        self.btn_penna.setText(tr("penna"))
        self.btn_evid.setText(tr("evidenziatore"))
        self.btn_gomma.setText(tr("gomma"))
        self.btn_toggle_vista.setText(tr("mezze_pagine"))
        self.btn_swipe.setToolTip(tr("tooltip_swipe"))
        if self.isFullScreen():
            self.btn_fullscreen_top.setText(tr("riduci_schermo"))
        else:
            self.btn_fullscreen_top.setText(tr("schermo_intero"))

    def toggle_swipe(self):
        self.swipe_abilitato = not self.swipe_abilitato
        if self.swipe_abilitato:
            self.btn_swipe.setText("↔️ ON")
        else:
            self.btn_swipe.setText("🔒 OFF")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
            self.btn_fullscreen_top.setText(tr("schermo_intero"))
            self.widget_basso.show()
            self.btn_nascondi.show()
            self.btn_swipe.show() 
        else:
            self.showFullScreen()
            self.btn_fullscreen_top.setText(tr("riduci_schermo"))
            self.widget_basso.hide()
            self.btn_nascondi.hide()
            self.btn_swipe.hide() 

    def gestisci_swipe(self, direzione):
        if not self.swipe_abilitato: return
        if direzione == 1: self.pagina_avanti()
        elif direzione == -1: self.pagina_indietro()

    def ottieni_da_cache(self, percorso):
        if percorso not in self.cache_pagine:
            self.cache_pagine[percorso] = QPixmap(percorso)
        return self.cache_pagine[percorso]

    def apri_libro(self, percorso):
        immagini = [f for f in os.listdir(percorso) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.lower().startswith('copertina')]
        self.pagine_libro = sorted(immagini, key=ordina_naturale)
        self.cartella_corrente = percorso
        if not self.pagine_libro: return
        self.cache_pagine.clear()
        
        book_data = self.storico_pagine.get(percorso, {})
        indice_salvato = book_data.get("pagina", 0) if isinstance(book_data, dict) else 0
        tools = book_data.get("strumenti", self.default_tools) if isinstance(book_data, dict) else self.default_tools

        if indice_salvato >= len(self.pagine_libro): indice_salvato = 0
        self.indice_pagina_attuale = indice_salvato
        
        p_data = tools.get("penna", self.default_tools["penna"])
        self.vista_libro.spessore_penna = p_data.get("spessore", 4)
        self.vista_libro.colore_penna = QColor(p_data.get("colore", "#ff000000"))
        self.vista_libro.usa_pressione_penna = p_data.get("pressione", True)

        e_data = tools.get("evidenziatore", self.default_tools["evidenziatore"])
        self.vista_libro.spessore_evidenziatore = e_data.get("spessore", 20)
        self.vista_libro.colore_evidenziatore = QColor(e_data.get("colore", "#64ffff00"))
        self.vista_libro.usa_pressione_evid = e_data.get("pressione", False)

        g_data = tools.get("gomma", self.default_tools["gomma"])
        self.vista_libro.spessore_gomma = g_data.get("spessore", 40)

        self.schermate.setCurrentIndex(1)
        self.aggiorna_pagine()
        QTimer.singleShot(100, self.adatta_pagine_iniziali)

    def adatta_pagine_iniziali(self):
        self.vista_libro.adatta_in_altezza()

    def aggiorna_ram_se_modificate(self):
        if self.vista_libro.modificata: 
            perc_sx = self.vista_libro.percorso_sx
            perc_dx = self.vista_libro.percorso_dx
            
            self.vista_libro.salva_modifiche()
            
            if perc_sx:
                if perc_sx in self.cache_pagine: del self.cache_pagine[perc_sx]
                QPixmapCache.clear() 
                self.cache_pagine[perc_sx] = QPixmap(perc_sx)
            if perc_dx:
                if perc_dx in self.cache_pagine: del self.cache_pagine[perc_dx]
                QPixmapCache.clear() 
                self.cache_pagine[perc_dx] = QPixmap(perc_dx)

    def aggiorna_pagine(self):
        if not self.pagine_libro: return
        
        if not self.vista_doppia:
            nome_file = self.pagine_libro[self.indice_pagina_attuale]
            self.input_pag.setText(numero_da_nome(nome_file))
            percorso = os.path.join(self.cartella_corrente, nome_file)
            self.vista_libro.carica_immagini(percorso, self.ottieni_da_cache(percorso), None, None)
        else:
            inizia_pari = False
            if int(numero_da_nome(self.pagine_libro[0])) % 2 == 0: inizia_pari = True
            indice_sx = self.indice_pagina_attuale
            
            if inizia_pari and indice_sx == 0:
                percorso_dx = os.path.join(self.cartella_corrente, self.pagine_libro[0])
                self.vista_libro.carica_immagini(None, None, percorso_dx, self.ottieni_da_cache(percorso_dx))
                self.input_pag.setText(f"- / {numero_da_nome(self.pagine_libro[0])}")
            else:
                percorso_sx = os.path.join(self.cartella_corrente, self.pagine_libro[indice_sx])
                
                if indice_sx + 1 < len(self.pagine_libro):
                    percorso_dx = os.path.join(self.cartella_corrente, self.pagine_libro[indice_sx + 1])
                    self.vista_libro.carica_immagini(percorso_sx, self.ottieni_da_cache(percorso_sx), percorso_dx, self.ottieni_da_cache(percorso_dx))
                    self.input_pag.setText(f"{numero_da_nome(self.pagine_libro[indice_sx])} - {numero_da_nome(self.pagine_libro[indice_sx + 1])}")
                else:
                    self.vista_libro.carica_immagini(percorso_sx, self.ottieni_da_cache(percorso_sx), None, None)
                    self.input_pag.setText(numero_da_nome(self.pagine_libro[indice_sx]))

        QTimer.singleShot(50, self.precarica_pagine_vicine)

    def precarica_pagine_vicine(self):
        inizio = max(0, self.indice_pagina_attuale - 3)
        fine = min(len(self.pagine_libro), self.indice_pagina_attuale + 4)
        
        percorsi_utili = []
        for i in range(inizio, fine):
            percorsi_utili.append(os.path.join(self.cartella_corrente, self.pagine_libro[i]))
            
        da_cancellare = [p for p in self.cache_pagine if p not in percorsi_utili]
        for p in da_cancellare:
            del self.cache_pagine[p]
            
        self.coda_precaricamento = [p for p in percorsi_utili if p not in self.cache_pagine]
        self.carica_prossima_in_coda()

    def carica_prossima_in_coda(self):
        if hasattr(self, 'coda_precaricamento') and self.coda_precaricamento:
            percorso = self.coda_precaricamento.pop(0)
            if percorso not in self.cache_pagine:
                self.cache_pagine[percorso] = QPixmap(percorso)
            QTimer.singleShot(50, self.carica_prossima_in_coda)

    def pagina_avanti(self):
        self.aggiorna_ram_se_modificate()
        salto = 2 if self.vista_doppia else 1
        if self.indice_pagina_attuale + salto < len(self.pagine_libro):
            self.indice_pagina_attuale += salto
            self.aggiorna_pagine()

    def pagina_indietro(self):
        self.aggiorna_ram_se_modificate()
        salto = 2 if self.vista_doppia else 1
        if self.indice_pagina_attuale - salto >= 0:
            self.indice_pagina_attuale -= salto
            self.aggiorna_pagine()
            
    def vai_a_pagina(self):
        self.aggiorna_ram_se_modificate()
        testo = self.input_pag.text().strip()
        for i, nome in enumerate(self.pagine_libro):
            if numero_da_nome(nome) == testo:
                self.indice_pagina_attuale = i
                if self.vista_doppia and self.indice_pagina_attuale % 2 != 0:
                    self.indice_pagina_attuale = max(0, self.indice_pagina_attuale - 1)
                self.aggiorna_pagine()
                break

    def cambia_vista(self):
        self.aggiorna_ram_se_modificate()
        self.vista_doppia = not self.vista_doppia
        self.aggiorna_pagine()

    def toggle_interfaccia_bassa(self):
        self.widget_basso.setVisible(not self.widget_basso.isVisible())

    def imposta_strumento(self, strumento):
        self.vista_libro.strumento = strumento
        self.btn_penna.setChecked(strumento == "penna")
        self.btn_evid.setChecked(strumento == "evidenziatore")
        self.btn_gomma.setChecked(strumento == "gomma")
        self.vista_libro.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def toggle_penna_evid(self):
        if self.btn_penna.isChecked(): self.imposta_strumento("evidenziatore")
        else: self.imposta_strumento("penna")

    def imposta_penna(self):
        dialogo = DialogoImpostazioniStrumenti(tr("penna"), self.vista_libro.spessore_penna, self.vista_libro.colore_penna, self.vista_libro.usa_pressione_penna, True, self)
        if dialogo.exec():
            self.vista_libro.spessore_penna = dialogo.spessore
            self.vista_libro.colore_penna = dialogo.colore
            self.vista_libro.usa_pressione_penna = dialogo.usa_pressione
        self.vista_libro.clearFocus()
        self.vista_libro.setFocus()

    def imposta_evidenziatore(self):
        dialogo = DialogoImpostazioniStrumenti(tr("evidenziatore"), self.vista_libro.spessore_evidenziatore, self.vista_libro.colore_evidenziatore, self.vista_libro.usa_pressione_evid, True, self)
        if dialogo.exec():
            self.vista_libro.spessore_evidenziatore = dialogo.spessore
            self.vista_libro.colore_evidenziatore = dialogo.colore
            self.vista_libro.usa_pressione_evid = dialogo.usa_pressione
        self.vista_libro.clearFocus()
        self.vista_libro.setFocus()

    def imposta_gomma(self):
        dialogo = DialogoImpostazioniStrumenti(tr("gomma"), self.vista_libro.spessore_gomma, None, False, False, self)
        if dialogo.exec():
            self.vista_libro.spessore_gomma = dialogo.spessore
        self.vista_libro.clearFocus()
        self.vista_libro.setFocus()

    def torna_al_menu(self):
        self.aggiorna_ram_se_modificate()
        self.salva_stato_libro_corrente()
        self.salva_storico()
        self.cache_pagine.clear()
        
        if self.isFullScreen():
            self.toggle_fullscreen()
            
        self.schermate.setCurrentIndex(0)
        self.popola_libreria() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = AppLibri()
    finestra.showMaximized()
    sys.exit(app.exec())