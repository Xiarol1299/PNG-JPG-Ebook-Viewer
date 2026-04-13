import sys
import os
import re
import shutil
import json
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

def ordina_naturale(testo):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', testo)]

def numero_da_nome(nome_file):
    numeri = re.findall(r'\d+', nome_file)
    if numeri: return str(int(numeri[-1]))
    return "?"

# --- CARTA DEL LIBRO (CON COPERTINA) ---
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
        file_path, _ = QFileDialog.getOpenFileName(self, "Scegli Copertina", "", "Immagini (*.png *.jpg *.jpeg)")
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

        self.lbl_spessore = QLabel(f"Spessore: {self.spessore}")
        layout.addWidget(self.lbl_spessore)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(self.spessore)
        self.slider.valueChanged.connect(self.aggiorna_spessore)
        layout.addWidget(self.slider)

        if mostra_pressione:
            self.chk_pressione = QCheckBox("Abilita sensibilità alla pressione")
            self.chk_pressione.setChecked(self.usa_pressione)
            self.chk_pressione.stateChanged.connect(self.aggiorna_pressione)
            layout.addWidget(self.chk_pressione)

        self.btn_colore = None
        if self.colore is not None:
            self.btn_colore = QPushButton("Scegli Colore")
            self.btn_colore.setStyleSheet(f"background-color: {self.colore.name()}; border-radius: 8px; padding: 10px; color: black;")
            self.btn_colore.clicked.connect(self.scegli_colore)
            layout.addWidget(self.btn_colore)

        btn_ok = QPushButton("Conferma")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def aggiorna_spessore(self, val):
        self.spessore = val
        self.lbl_spessore.setText(f"Spessore: {val}")

    def aggiorna_pressione(self, stato):
        self.usa_pressione = bool(stato)

    def scegli_colore(self):
        nuovo_colore = QColorDialog.getColor(self.colore, self, "Scegli Colore")
        if nuovo_colore.isValid():
            self.colore = nuovo_colore
            if "Evidenziatore" in self.windowTitle():
                self.colore.setAlpha(100)
            self.btn_colore.setStyleSheet(f"background-color: {self.colore.name()}; border-radius: 8px; padding: 10px; color: black;")

# --- FINESTRA DI DIALOGO IMPOSTAZIONI APP ---
class DialogoImpostazioniApp(QDialog):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.setWindowTitle("Impostazioni Programma")
        self.main_app = main_app
        self.resize(500, 200)

        layout = QVBoxLayout(self)

        # Bottone Tema
        testo_tema = "Passa a Modalità Chiara ☀️" if self.main_app.is_tema_scuro else "Passa a Modalità Scura 🌙"
        self.btn_tema = QPushButton(testo_tema)
        self.btn_tema.clicked.connect(self.cambia_tema)
        layout.addWidget(self.btn_tema)

        # Selezione Cartella
        layout.addWidget(QLabel("Cartella della tua Libreria:"))
        
        layout_cartella = QHBoxLayout()
        testo_cartella = self.main_app.cartella_principale if self.main_app.cartella_principale else "Nessuna cartella selezionata!"
        self.lbl_cartella = QLineEdit(testo_cartella)
        self.lbl_cartella.setReadOnly(True)
        
        btn_sfoglia = QPushButton("Sfoglia...")
        btn_sfoglia.clicked.connect(self.scegli_cartella)
        
        layout_cartella.addWidget(self.lbl_cartella)
        layout_cartella.addWidget(btn_sfoglia)
        layout.addLayout(layout_cartella)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(self.accept)
        layout.addWidget(btn_chiudi)

    def cambia_tema(self):
        self.main_app.cambia_tema()
        testo_tema = "Passa a Modalità Chiara ☀️" if self.main_app.is_tema_scuro else "Passa a Modalità Scura 🌙"
        self.btn_tema.setText(testo_tema)

    def scegli_cartella(self):
        cartella_iniziale = self.main_app.cartella_principale if self.main_app.cartella_principale else ""
        nuova_cartella = QFileDialog.getExistingDirectory(self, "Seleziona la cartella dei libri", cartella_iniziale)
        
        if nuova_cartella:
            self.lbl_cartella.setText(nuova_cartella)
            self.main_app.cartella_principale = nuova_cartella
            self.main_app.salva_config()
            self.main_app.popola_libreria() # Aggiorna istantaneamente la griglia home

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
        self.immagine_corrente = None
        self.item_sfondo = None
        self.percorso_corrente = ""
        self.modificata = False
        
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

        self.adattato_in_larghezza = False
        self.pos_mouse_iniziale = None
        self.scroll_x_iniziale = 0

    def carica_immagine(self, percorso, pixmap):
        self.salva_modifiche()
        self.percorso_corrente = percorso
        self.scena.clear()
        
        if pixmap:
            self.immagine_corrente = pixmap
            self.item_sfondo = self.scena.addPixmap(self.immagine_corrente)
            self.item_sfondo.setZValue(-1) 
            self.setSceneRect(QRectF(self.immagine_corrente.rect()))
            self.modificata = False
        else:
            self.immagine_corrente = None
            self.item_sfondo = None
            self.percorso_corrente = ""
            self.modificata = False

    def salva_modifiche(self):
        if self.modificata and self.immagine_corrente and self.percorso_corrente:
            img = QImage(self.immagine_corrente.size(), QImage.Format.Format_RGB32)
            img.fill(Qt.GlobalColor.white) 
            pittore = QPainter(img)
            self.scena.render(pittore, target=QRectF(img.rect()), source=QRectF(self.immagine_corrente.rect()))
            pittore.end()
            img.save(self.percorso_corrente, quality=95)
            self.modificata = False

    def crea_penna(self, strumento, spessore):
        penna = QPen()
        penna.setCapStyle(Qt.PenCapStyle.RoundCap)
        penna.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        if strumento == "penna":
            penna.setColor(self.colore_penna)
        elif strumento == "evidenziatore":
            penna.setColor(self.colore_evidenziatore)
        penna.setWidthF(spessore)
        return penna

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
            if self.adattato_in_larghezza:
                self.fitInView(self.scena.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
                self.adattato_in_larghezza = False
            else:
                scala = self.viewport().width() / self.immagine_corrente.width()
                self.resetTransform()
                self.scale(scala, scala)
                self.verticalScrollBar().setValue(0)
                self.adattato_in_larghezza = True
        super().mouseDoubleClickEvent(evento)

    def mousePressEvent(self, evento):
        self.pos_mouse_iniziale = evento.pos()
        self.scroll_x_iniziale = self.horizontalScrollBar().value()
        super().mousePressEvent(evento)

    def mouseReleaseEvent(self, evento):
        if self.pos_mouse_iniziale is not None:
            delta_x = evento.pos().x() - self.pos_mouse_iniziale.x()
            scroll_attuale = self.horizontalScrollBar().value()
            min_scroll = self.horizontalScrollBar().minimum()
            max_scroll = self.horizontalScrollBar().maximum()

            if delta_x < -60 and self.scroll_x_iniziale == max_scroll and scroll_attuale == max_scroll:
                self.richiesta_cambio_pagina.emit(1)
            elif delta_x > 60 and self.scroll_x_iniziale == min_scroll and scroll_attuale == min_scroll:
                self.richiesta_cambio_pagina.emit(-1)

        self.pos_mouse_iniziale = None
        super().mouseReleaseEvent(evento)

    def tabletEvent(self, evento):
        if self.strumento == "nessuno":
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
                usa_press = self.usa_pressione_penna if strumento_attivo == "penna" else self.usa_pressione_evid
                if not usa_press:
                    self.path_corrente = QPainterPath(self.ultimo_punto)
                    spessore = self.spessore_penna if strumento_attivo == "penna" else self.spessore_evidenziatore
                    self.item_tratto_corrente = self.scena.addPath(self.path_corrente, self.crea_penna(strumento_attivo, spessore))
                    self.item_tratto_corrente.setData(0, "disegno")
            evento.accept()
            
        elif evento.type() == QEvent.Type.TabletMove and self.disegnando:
            punto_smussato = QPointF(
                self.ultimo_punto.x() * 0.3 + punto_reale.x() * 0.7,
                self.ultimo_punto.y() * 0.3 + punto_reale.y() * 0.7
            )

            if strumento_attivo == "gomma":
                r = self.spessore_gomma / 2
                rect = QRectF(punto_reale.x() - r, punto_reale.y() - r, r*2, r*2)
                for item in self.scena.items(rect):
                    if item.data(0) == "disegno":
                        self.scena.removeItem(item)
                        self.modificata = True
            else:
                usa_press = self.usa_pressione_penna if strumento_attivo == "penna" else self.usa_pressione_evid
                if usa_press:
                    spessore_base = self.spessore_penna if strumento_attivo == "penna" else self.spessore_evidenziatore
                    moltiplicatore = 0.3 + (1.2 * ((pressione + self.ultima_pressione) / 2))
                    spessore = spessore_base * moltiplicatore
                    linea = self.scena.addLine(self.ultimo_punto.x(), self.ultimo_punto.y(), punto_smussato.x(), punto_smussato.y(), self.crea_penna(strumento_attivo, spessore))
                    linea.setData(0, "disegno") 
                else:
                    self.path_corrente.lineTo(punto_smussato)
                    self.item_tratto_corrente.setPath(self.path_corrente)

                self.modificata = True

            self.ultimo_punto = punto_smussato
            self.ultima_pressione = pressione
            evento.accept()
            
        elif evento.type() == QEvent.Type.TabletRelease and self.disegnando:
            self.disegnando = False
            evento.accept()

    def wheelEvent(self, evento):
        zoom = 1.15 if evento.angleDelta().y() > 0 else 1 / 1.15
        self.scale(zoom, zoom)
        self.adattato_in_larghezza = False


# --- FINESTRA PRINCIPALE ---
class AppLibri(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Il Mio Lettore Digitale")
        self.resize(1200, 800)
        
        # Capisce se stai usando il .py normale o l' .exe compilato
        if getattr(sys, 'frozen', False):
            cartella_programma = os.path.dirname(sys.executable)
        else:
            cartella_programma = os.path.dirname(os.path.abspath(__file__))
            
        self.FILE_STORICO = os.path.join(cartella_programma, "storico_lettura.json")
        self.FILE_CONFIG = os.path.join(cartella_programma, "config.json")
        
        self.carica_config()
        
        self.storico_pagine = {}
        self.carica_storico()
        
        self.schermate = QStackedWidget()
        self.setCentralWidget(self.schermate)
        
        self.pagine_libro = []
        self.indice_pagina_attuale = 0
        self.vista_doppia = False
        self.cache_pagine = {}

        self.crea_menu()
        self.crea_lettore()
        self.applica_tema()

    # --- LOGICA SALVATAGGIO STORICO E CONFIGURAZIONI ---
    def carica_config(self):
        self.cartella_principale = ""
        self.is_tema_scuro = True # Default
        try:
            with open(self.FILE_CONFIG, 'r') as f:
                dati = json.load(f)
                self.cartella_principale = dati.get("cartella", "")
                self.is_tema_scuro = dati.get("tema", True)
        except:
            pass

    def salva_config(self):
        try:
            dati = {
                "cartella": self.cartella_principale,
                "tema": self.is_tema_scuro
            }
            with open(self.FILE_CONFIG, 'w') as f:
                json.dump(dati, f)
        except Exception as e:
            print(f"Errore salvataggio config: {e}")

    def carica_storico(self):
        try:
            with open(self.FILE_STORICO, 'r') as f:
                self.storico_pagine = json.load(f)
        except:
            self.storico_pagine = {}

    def salva_storico(self):
        try:
            with open(self.FILE_STORICO, 'w') as f:
                json.dump(self.storico_pagine, f)
        except:
            pass

    def closeEvent(self, event):
        if hasattr(self, 'cartella_corrente') and self.cartella_corrente:
            self.storico_pagine[self.cartella_corrente] = self.indice_pagina_attuale
        self.salva_storico()
        self.vista_sx.salva_modifiche()
        self.vista_dx.salva_modifiche()
        super().closeEvent(event)

    def keyPressEvent(self, evento):
        if self.schermate.currentIndex() == 1 and not self.input_pag.hasFocus():
            if evento.key() == Qt.Key.Key_Right:
                self.pagina_avanti()
            elif evento.key() == Qt.Key.Key_Left:
                self.pagina_indietro()
        super().keyPressEvent(evento)

    def cambia_tema(self):
        self.is_tema_scuro = not self.is_tema_scuro
        self.salva_config() # Salva subito la preferenza nel file json!
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
        # SOSTITUITO IL BOTTONE TEMA CON QUELLO IMPOSTAZIONI
        self.btn_impostazioni = QPushButton("⚙️ Impostazioni")
        self.btn_impostazioni.setFixedSize(140, 40)
        self.btn_impostazioni.clicked.connect(self.apri_impostazioni)
        
        barra_superiore.addStretch()
        barra_superiore.addWidget(self.btn_impostazioni)
        layout_principale.addLayout(barra_superiore)

        self.layout_griglia = QGridLayout()
        self.layout_griglia.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.lbl_caricamento = QLabel("Caricamento libreria in corso...")
        self.lbl_caricamento.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(self.lbl_caricamento)
        
        layout_principale.addLayout(self.layout_griglia)
        layout_principale.addStretch()
        self.schermate.addWidget(self.widget_menu)

        QTimer.singleShot(100, self.popola_libreria)

    def apri_impostazioni(self):
        dialogo = DialogoImpostazioniApp(self)
        dialogo.exec()

    def popola_libreria(self):
        # Prima puliamo la griglia in caso stiamo ricaricando dopo aver cambiato cartella
        for i in reversed(range(self.layout_griglia.count())): 
            widget = self.layout_griglia.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)

        if not self.cartella_principale or not os.path.exists(self.cartella_principale):
            self.lbl_caricamento.setText("Benvenuto! Vai in ⚙️ Impostazioni per selezionare la cartella dei tuoi libri.")
            self.lbl_caricamento.show()
            return

        self.lbl_caricamento.hide() 

        riga, colonna = 0, 0
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
        cartelle_interne = [e for e in elementi if os.path.isdir(os.path.join(percorso, e))]
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
        self.btn_penna = BottoneStrumento("Penna")
        self.btn_penna.setCheckable(True)
        self.btn_penna.setChecked(True)
        self.btn_penna.clicked.connect(lambda: self.imposta_strumento("penna"))
        self.btn_penna.doppio_clic.connect(self.imposta_penna)
        
        self.btn_evid = BottoneStrumento("Evidenziatore")
        self.btn_evid.setCheckable(True)
        self.btn_evid.clicked.connect(lambda: self.imposta_strumento("evidenziatore"))
        self.btn_evid.doppio_clic.connect(self.imposta_evidenziatore)

        self.btn_gomma = BottoneStrumento("Gomma")
        self.btn_gomma.setCheckable(True)
        self.btn_gomma.clicked.connect(lambda: self.imposta_strumento("gomma"))
        self.btn_gomma.doppio_clic.connect(self.imposta_gomma)

        btn_menu = QPushButton("Torna al Menu")
        btn_menu.setFixedSize(120, 40)
        btn_menu.clicked.connect(self.torna_al_menu)

        self.barra_alta.addWidget(self.btn_penna)
        self.barra_alta.addWidget(self.btn_evid)
        self.barra_alta.addWidget(self.btn_gomma)
        self.barra_alta.addStretch()
        self.barra_alta.addWidget(btn_menu)

        centro = QHBoxLayout()
        btn_indietro = QPushButton("<")
        btn_indietro.setFixedSize(40, 100)
        btn_indietro.clicked.connect(self.pagina_indietro)
        
        btn_avanti = QPushButton(">")
        btn_avanti.setFixedSize(40, 100)
        btn_avanti.clicked.connect(self.pagina_avanti)

        self.vista_sx = PaginaView()
        self.vista_dx = PaginaView()
        self.vista_dx.hide()
        
        self.vista_sx.richiesta_cambio_pagina.connect(self.gestisci_swipe)
        self.vista_dx.richiesta_cambio_pagina.connect(self.gestisci_swipe)
        self.vista_sx.richiesta_toggle_strumento.connect(self.toggle_penna_evid)
        self.vista_dx.richiesta_toggle_strumento.connect(self.toggle_penna_evid)
        
        centro.addWidget(btn_indietro)
        centro.addWidget(self.vista_sx)
        centro.addWidget(self.vista_dx)
        centro.addWidget(btn_avanti)

        self.widget_basso = QWidget()
        self.barra_bassa = QHBoxLayout(self.widget_basso)
        
        self.input_pag = QLineEdit()
        self.input_pag.setFixedWidth(80)
        self.input_pag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_pag.returnPressed.connect(self.vai_a_pagina)
        
        btn_toggle_vista = QPushButton("1/2 Pagine")
        btn_toggle_vista.clicked.connect(self.cambia_vista)
        
        self.barra_bassa.addStretch()
        self.barra_bassa.addWidget(self.input_pag)
        self.barra_bassa.addWidget(btn_toggle_vista)
        self.barra_bassa.addStretch()

        layout_nascondi = QHBoxLayout()
        layout_nascondi.addStretch()
        btn_nascondi = QPushButton("O")
        btn_nascondi.setFixedSize(40, 40)
        btn_nascondi.clicked.connect(self.toggle_interfaccia_bassa)
        layout_nascondi.addWidget(btn_nascondi)

        layout_principale.addLayout(self.barra_alta)
        layout_principale.addLayout(centro)
        layout_principale.addWidget(self.widget_basso)
        layout_principale.addLayout(layout_nascondi)

        self.schermate.addWidget(self.widget_lettore)

    def gestisci_swipe(self, direzione):
        if direzione == 1: self.pagina_avanti()
        elif direzione == -1: self.pagina_indietro()

    def ottieni_da_cache(self, percorso):
        if percorso not in self.cache_pagine:
            self.cache_pagine[percorso] = QPixmap(percorso)
            if len(self.cache_pagine) > 40: del self.cache_pagine[next(iter(self.cache_pagine))]
        return self.cache_pagine[percorso]

    def aggiorna_cache_forzato(self, percorso):
        self.cache_pagine[percorso] = QPixmap(percorso)

    def apri_libro(self, percorso):
        immagini = [f for f in os.listdir(percorso) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.lower().startswith('copertina')]
        self.pagine_libro = sorted(immagini, key=ordina_naturale)
        self.cartella_corrente = percorso
        if not self.pagine_libro: return
        self.cache_pagine.clear()
        
        indice_salvato = self.storico_pagine.get(percorso, 0)
        if indice_salvato >= len(self.pagine_libro): indice_salvato = 0
        self.indice_pagina_attuale = indice_salvato
        
        self.schermate.setCurrentIndex(1)
        self.aggiorna_pagine()

    def aggiorna_pagine(self):
        if not self.pagine_libro: return
        QTimer.singleShot(10, self.precarica_pagine_vicine)
        
        if not self.vista_doppia:
            nome_file = self.pagine_libro[self.indice_pagina_attuale]
            self.input_pag.setText(numero_da_nome(nome_file))
            percorso = os.path.join(self.cartella_corrente, nome_file)
            self.vista_sx.carica_immagine(percorso, self.ottieni_da_cache(percorso))
        else:
            inizia_pari = False
            if int(numero_da_nome(self.pagine_libro[0])) % 2 == 0: inizia_pari = True
            indice_sx = self.indice_pagina_attuale
            
            if inizia_pari and indice_sx == 0:
                self.vista_sx.carica_immagine(None, None)
                percorso_dx = os.path.join(self.cartella_corrente, self.pagine_libro[0])
                self.vista_dx.carica_immagine(percorso_dx, self.ottieni_da_cache(percorso_dx))
                self.input_pag.setText(f"- / {numero_da_nome(self.pagine_libro[0])}")
            else:
                percorso_sx = os.path.join(self.cartella_corrente, self.pagine_libro[indice_sx])
                self.vista_sx.carica_immagine(percorso_sx, self.ottieni_da_cache(percorso_sx))
                if indice_sx + 1 < len(self.pagine_libro):
                    percorso_dx = os.path.join(self.cartella_corrente, self.pagine_libro[indice_sx + 1])
                    self.vista_dx.carica_immagine(percorso_dx, self.ottieni_da_cache(percorso_dx))
                    self.input_pag.setText(f"{numero_da_nome(self.pagine_libro[indice_sx])} - {numero_da_nome(self.pagine_libro[indice_sx + 1])}")
                else:
                    self.vista_dx.carica_immagine(None, None)
                    self.input_pag.setText(numero_da_nome(self.pagine_libro[indice_sx]))

    def precarica_pagine_vicine(self):
        inizio = max(0, self.indice_pagina_attuale - 2)
        fine = min(len(self.pagine_libro), self.indice_pagina_attuale + 4)
        for i in range(inizio, fine): self.ottieni_da_cache(os.path.join(self.cartella_corrente, self.pagine_libro[i]))

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
        if self.vista_doppia: self.vista_dx.show()
        else: self.vista_dx.hide()
        self.aggiorna_pagine()

    def aggiorna_ram_se_modificate(self):
        if self.vista_sx.modificata: self.aggiorna_cache_forzato(self.vista_sx.percorso_corrente)
        if self.vista_dx.modificata: self.aggiorna_cache_forzato(self.vista_dx.percorso_corrente)

    def toggle_interfaccia_bassa(self):
        self.widget_basso.setVisible(not self.widget_basso.isVisible())

    def imposta_strumento(self, strumento):
        self.vista_sx.strumento = self.vista_dx.strumento = strumento
        self.btn_penna.setChecked(strumento == "penna")
        self.btn_evid.setChecked(strumento == "evidenziatore")
        self.btn_gomma.setChecked(strumento == "gomma")
        
        self.vista_sx.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.vista_dx.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def toggle_penna_evid(self):
        if self.btn_penna.isChecked(): self.imposta_strumento("evidenziatore")
        else: self.imposta_strumento("penna")

    def imposta_penna(self):
        dialogo = DialogoImpostazioniStrumenti("Impostazioni Penna", self.vista_sx.spessore_penna, self.vista_sx.colore_penna, self.vista_sx.usa_pressione_penna, True, self)
        if dialogo.exec():
            self.vista_sx.spessore_penna = self.vista_dx.spessore_penna = dialogo.spessore
            self.vista_sx.colore_penna = self.vista_dx.colore_penna = dialogo.colore
            self.vista_sx.usa_pressione_penna = self.vista_dx.usa_pressione_penna = dialogo.usa_pressione

    def imposta_evidenziatore(self):
        dialogo = DialogoImpostazioniStrumenti("Impostazioni Evidenziatore", self.vista_sx.spessore_evidenziatore, self.vista_sx.colore_evidenziatore, self.vista_sx.usa_pressione_evid, True, self)
        if dialogo.exec():
            self.vista_sx.spessore_evidenziatore = self.vista_dx.spessore_evidenziatore = dialogo.spessore
            self.vista_sx.colore_evidenziatore = self.vista_dx.colore_evidenziatore = dialogo.colore
            self.vista_sx.usa_pressione_evid = self.vista_dx.usa_pressione_evid = dialogo.usa_pressione

    def imposta_gomma(self):
        dialogo = DialogoImpostazioniStrumenti("Spessore Gomma", self.vista_sx.spessore_gomma, None, False, False, self)
        if dialogo.exec():
            self.vista_sx.spessore_gomma = self.vista_dx.spessore_gomma = dialogo.spessore

    def torna_al_menu(self):
        self.storico_pagine[self.cartella_corrente] = self.indice_pagina_attuale
        self.salva_storico()
        
        self.vista_sx.salva_modifiche()
        self.vista_dx.salva_modifiche()
        self.schermate.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = AppLibri()
    finestra.showMaximized()
    sys.exit(app.exec())