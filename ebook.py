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

        testo_tema = "Passa a Modalità Chiara ☀️" if self.main_app.is_tema_scuro else "Passa a Modalità Scura 🌙"
        self.btn_tema = QPushButton(testo_tema)
        self.btn_tema.clicked.connect(self.cambia_tema)
        layout.addWidget(self.btn_tema)

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
            self.main_app.popola_libreria()

# --- BOTTONE DOPPIO CLIC ---
class BottoneStrumento(QPushButton):
    doppio_clic = pyqtSignal()
    def mouseDoubleClickEvent(self, evento):
        self.doppio_clic.emit()
        super().mouseDoubleClickEvent(evento)

# --- VISUALIZZATORE VETTORIALE (ORA UNIFICA DUE PAGINE IN UNA) ---
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
        self.item_sfondo = None
        self.modificata = False
        
        # Variabili per gestire sia la vista singola che doppia in un'unica tela
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
        
        self.adattato_in_larghezza = False
        self.pos_mouse_iniziale = None
        self.scroll_x_iniziale = 0

    def adatta_in_altezza(self):
        if self.immagine_corrente:
            self.fitInView(self.scena.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.adattato_in_larghezza = False

    # NUOVA LOGICA: Carica e fonde le due pagine in un'unica tela invisibile
    def carica_immagini(self, perc_sx, pix_sx, perc_dx, pix_dx):
        self.salva_modifiche()
        self.scena.clear()
        
        self.percorso_sx = perc_sx
        self.percorso_dx = perc_dx
        self.is_doppia = perc_dx is not None

        if not perc_sx and not perc_dx:
            self.immagine_corrente = None
            self.modificata = False
            return

        if self.is_doppia:
            # Calcola le dimensioni (se una pagina manca es. inizio libro dispari, lascia spazio bianco)
            w_sx = pix_sx.width() if pix_sx else (pix_dx.width() if pix_dx else 0)
            h_sx = pix_sx.height() if pix_sx else (pix_dx.height() if pix_dx else 0)
            w_dx = pix_dx.width() if pix_dx else w_sx
            h_dx = pix_dx.height() if pix_dx else h_sx

            self.size_sx = QSize(w_sx, h_sx)
            self.size_dx = QSize(w_dx, h_dx)

            # Crea una singola tela (canvas) larga quanto due pagine
            h_max = max(h_sx, h_dx)
            comp = QImage(w_sx + w_dx, h_max, QImage.Format.Format_RGB32)
            comp.fill(Qt.GlobalColor.white)
            
            painter = QPainter(comp)
            if pix_sx: painter.drawPixmap(0, 0, pix_sx)
            if pix_dx: painter.drawPixmap(w_sx, 0, pix_dx)
            painter.end()

            self.immagine_corrente = QPixmap.fromImage(comp)
        else:
            self.immagine_corrente = pix_sx
            self.size_sx = QSize(pix_sx.width(), pix_sx.height()) if pix_sx else QSize(0,0)

        self.item_sfondo = self.scena.addPixmap(self.immagine_corrente)
        self.item_sfondo.setZValue(-1) 
        self.setSceneRect(QRectF(self.immagine_corrente.rect()))
        self.modificata = False

    def salva_modifiche(self):
        if self.modificata and self.immagine_corrente:
            # Stampa tutto in un'unica super-immagine
            img = QImage(self.immagine_corrente.size(), QImage.Format.Format_RGB32)
            img.fill(Qt.GlobalColor.white) 
            pittore = QPainter(img)
            self.scena.render(pittore, target=QRectF(img.rect()), source=QRectF(self.immagine_corrente.rect()))
            pittore.end()
            
            # Se siamo in doppia, la taglia perfettamente a metà e salva i due file separati!
            if self.is_doppia:
                if self.percorso_sx:
                    img_sx = img.copy(0, 0, self.size_sx.width(), self.size_sx.height())
                    img_sx.save(self.percorso_sx, quality=95)
                if self.percorso_dx:
                    img_dx = img.copy(self.size_sx.width(), 0, self.size_dx.width(), self.size_dx.height())
                    img_dx.save(self.percorso_dx, quality=95)
            else:
                if self.percorso_sx:
                    img.copy(0, 0, self.size_sx.width(), self.size_sx.height()).save(self.percorso_sx, quality=95)
            
            self.modificata = False

    def crea_penna(self, strumento, spessore):
        penna = QPen()
        penna.setCapStyle(Qt.PenCapStyle.RoundCap)
        penna.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        if strumento == "penna": penna.setColor(self.colore_penna)
        elif strumento == "evidenziatore": penna.setColor(self.colore_evidenziatore)
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
        self.swipe_abilitato = True 
        
        self.cache_pagine = {}        
        self.coda_precaricamento = [] 

        self.crea_menu()
        self.crea_lettore()
        self.applica_tema()

    def carica_config(self):
        self.cartella_principale = ""
        self.is_tema_scuro = True
        try:
            with open(self.FILE_CONFIG, 'r') as f:
                dati = json.load(f)
                self.cartella_principale = dati.get("cartella", "")
                self.is_tema_scuro = dati.get("tema", True)
        except: pass

    def salva_config(self):
        try:
            dati = {"cartella": self.cartella_principale, "tema": self.is_tema_scuro}
            with open(self.FILE_CONFIG, 'w') as f:
                json.dump(dati, f)
        except: pass

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
        except: pass

    # Override della X della finestra
    def closeEvent(self, event):
        if self.schermate.currentIndex() == 1:
            # Se siamo dentro un libro, non chiudere il programma! Torna solo al menu.
            self.torna_al_menu()
            event.ignore() 
        else:
            # Se siamo già nel menu, salva la configurazione e chiudi l'app
            self.salva_config()
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
        for i in reversed(range(self.layout_griglia.count())): 
            widget = self.layout_griglia.itemAt(i).widget()
            if widget is not None: widget.setParent(None)

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
        
        # --- BARRA ALTA (Con il nuovo tasto Full Screen) ---
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

        self.btn_fullscreen_top = QPushButton("⛶ Schermo Intero")
        self.btn_fullscreen_top.setFixedSize(140, 40)
        self.btn_fullscreen_top.clicked.connect(self.toggle_fullscreen)

        self.barra_alta.addWidget(self.btn_penna)
        self.barra_alta.addWidget(self.btn_evid)
        self.barra_alta.addWidget(self.btn_gomma)
        self.barra_alta.addStretch()
        self.barra_alta.addWidget(self.btn_fullscreen_top)

        # --- CENTRO (Ora unificato con una sola vista) ---
        centro = QHBoxLayout()
        self.vista_libro = PaginaView()
        self.vista_libro.richiesta_cambio_pagina.connect(self.gestisci_swipe)
        self.vista_libro.richiesta_toggle_strumento.connect(self.toggle_penna_evid)
        centro.addWidget(self.vista_libro)

        # --- BARRA BASSA (Nascondibile) ---
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
        
        btn_toggle_vista = QPushButton("1/2 Pagine")
        btn_toggle_vista.clicked.connect(self.cambia_vista)
        
        self.barra_bassa.addStretch()
        self.barra_bassa.addWidget(btn_indietro)
        self.barra_bassa.addWidget(self.input_pag)
        self.barra_bassa.addWidget(btn_toggle_vista)
        self.barra_bassa.addWidget(btn_avanti)
        self.barra_bassa.addStretch()

        # --- ANGOLO BASSO DESTRA ---
        layout_nascondi = QHBoxLayout()
        layout_nascondi.addStretch()
        
        self.btn_nascondi = QPushButton("O")
        self.btn_nascondi.setFixedSize(40, 40)
        self.btn_nascondi.clicked.connect(self.toggle_interfaccia_bassa)
        
        self.btn_swipe = QPushButton("↔️ ON")
        self.btn_swipe.setFixedSize(65, 40)
        self.btn_swipe.setToolTip("Abilita/Disabilita lo Swipe per cambiare pagina")
        self.btn_swipe.clicked.connect(self.toggle_swipe)
        
        layout_nascondi.addWidget(self.btn_nascondi)
        layout_nascondi.addWidget(self.btn_swipe) 

        layout_principale.addLayout(self.barra_alta)
        layout_principale.addLayout(centro)
        layout_principale.addWidget(self.widget_basso)
        layout_principale.addLayout(layout_nascondi)

        self.schermate.addWidget(self.widget_lettore)

    def toggle_swipe(self):
        self.swipe_abilitato = not self.swipe_abilitato
        if self.swipe_abilitato:
            self.btn_swipe.setText("↔️ ON")
        else:
            self.btn_swipe.setText("🔒 OFF")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
            self.btn_fullscreen_top.setText("⛶ Schermo Intero")
            self.widget_basso.show()
            self.btn_nascondi.show()
            self.btn_swipe.show() 
        else:
            self.showFullScreen()
            self.btn_fullscreen_top.setText("✖ Riduci Schermo")
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
        
        indice_salvato = self.storico_pagine.get(percorso, 0)
        if indice_salvato >= len(self.pagine_libro): indice_salvato = 0
        self.indice_pagina_attuale = indice_salvato
        
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
        
        if strumento == "nessuno":
            self.vista_libro.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        else:
            self.vista_libro.setDragMode(QGraphicsView.DragMode.NoDrag)

    def toggle_penna_evid(self):
        if self.btn_penna.isChecked(): self.imposta_strumento("evidenziatore")
        else: self.imposta_strumento("penna")

    def imposta_penna(self):
        dialogo = DialogoImpostazioniStrumenti("Impostazioni Penna", self.vista_libro.spessore_penna, self.vista_libro.colore_penna, self.vista_libro.usa_pressione_penna, True, self)
        if dialogo.exec():
            self.vista_libro.spessore_penna = dialogo.spessore
            self.vista_libro.colore_penna = dialogo.colore
            self.vista_libro.usa_pressione_penna = dialogo.usa_pressione

    def imposta_evidenziatore(self):
        dialogo = DialogoImpostazioniStrumenti("Impostazioni Evidenziatore", self.vista_libro.spessore_evidenziatore, self.vista_libro.colore_evidenziatore, self.vista_libro.usa_pressione_evid, True, self)
        if dialogo.exec():
            self.vista_libro.spessore_evidenziatore = dialogo.spessore
            self.vista_libro.colore_evidenziatore = dialogo.colore
            self.vista_libro.usa_pressione_evid = dialogo.usa_pressione

    def imposta_gomma(self):
        dialogo = DialogoImpostazioniStrumenti("Spessore Gomma", self.vista_libro.spessore_gomma, None, False, False, self)
        if dialogo.exec():
            self.vista_libro.spessore_gomma = dialogo.spessore

    def torna_al_menu(self):
        self.aggiorna_ram_se_modificate()
        self.storico_pagine[self.cartella_corrente] = self.indice_pagina_attuale
        self.salva_storico()
        self.cache_pagine.clear()
        
        if self.isFullScreen():
            self.toggle_fullscreen()
            
        self.schermate.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = AppLibri()
    finestra.showMaximized()
    sys.exit(app.exec())