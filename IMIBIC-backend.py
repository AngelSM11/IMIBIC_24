import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QSizePolicy
from PyQt6.QtGui import QPixmap,  QIcon, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
from PyQt6.uic import loadUi
from PyQt6.QtGui import QColor, QPalette, QStandardItemModel, QStandardItem
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dbConnection import select_PacientByDId, new_Patient, get_PacientsDNI, get_Patients, modify_Patient, delete_Patient
#Import correo
import smtplib
from email.mime.text import MIMEText
from email.mime.text import MIMEText

class Backend(QMainWindow):
    def __init__(self):
        super().__init__()
        self.patients = get_Patients()

        loadUi("IMIBIC-frontend.ui", self)

        self.setFixedSize(self.size())

        self.apply_Palette_black()
        self.palette.setVisible(False)

        self.palette.clicked.connect(self.apply_Palette_black)
        self.palette2.clicked.connect(self.apply_Palette_white)
        
        self.action_PatientsConf.triggered.connect(self.patients_Conf)
        self.show_DNI_List()
        
        self.graphicsView = QWebEngineView()
        self.gridLayout_6.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.comboBox.currentIndexChanged.connect(self.show_Graph1)
        self.comboBox.currentIndexChanged.connect(self.show_User_Info)
        
        self.plotly_figure = make_subplots(rows=1, cols=1)
        self.show_Graph1()

        self.Button1.clicked.connect(self.show_Graph1)
        self.Button2.clicked.connect(self.show_Graph2)
        self.Button3.clicked.connect(self.show_Graph3)
        self.Button4.clicked.connect(self.show_Graph4)


        #Crear un icono con la imagen que desees
        pixmap =QPixmap("data/icon_email.png")
        pixmap2 =QPixmap("data/logo_nombre.png")
        # Escalar el pixmap al tamaño del botón
        pixmap = pixmap.scaled(330, 130)
        pixmap2 = pixmap2.scaled(330, 130)

        icon=QIcon(pixmap)
        icon2=QIcon(pixmap2)

        #Asignar el icono al botón
        self.correo.setIcon(icon)
        self.email.setIcon(icon2)

        self.correo.clicked.connect(self.send_email)
        self.email.clicked.connect(self.openWebsite)

    def apply_Palette_black(self):
        self.palette.setVisible(False)
        self.palette2.setVisible(True)
        palette = QPalette()
        # Colores para la ventana principal
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        # Colores para la barra de herramientas (toolbar)
        palette.setColor(QPalette.ColorRole.Light, QColor(255, 53, 53))  # Color de fondo de la toolbar
        palette.setColor(QPalette.ColorRole.Mid, QColor(53, 53, 53))    # Color de fondo de los botones de la toolbar
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))  # Color del texto de la toolbar
        # Colores para la barra de estado (status bar)
        palette.setColor(QPalette.ColorRole.Base, QColor(53, 53, 53))    # Color de fondo de la barra de estado
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))  # Color del texto de la barra de estado
        # Otros colores
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        # Establecer la palette de colores personalizada
        self.setPalette(palette)

    def apply_Palette_white(self):
        self.palette.setVisible(True)
        self.palette2.setVisible(False)  
        palette = QPalette()
        # Colores para la ventana principal
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        # Colores para la barra de herramientas (toolbar)
        palette.setColor(QPalette.ColorRole.Light, QColor(255, 200, 200))  # Color de fondo de la toolbar
        palette.setColor(QPalette.ColorRole.Mid, QColor(240, 240, 240))    # Color de fondo de los botones de la toolbar
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))  # Color del texto de la toolbar
        # Colores para la barra de estado (status bar)
        palette.setColor(QPalette.ColorRole.Base, QColor(240, 240, 240))    # Color de fondo de la barra de estado
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))  # Color del texto de la barra de estado
        # Otros colores
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        # Establecer la palette de colores personalizada
        self.setPalette(palette)

    def show_DNI_List(self):

        dniList = get_PacientsDNI()
        self.comboBox.clear()
        
        for dni in dniList:
            self.comboBox.addItem(dni)

    
    def show_User_Info(self):
        selected_patient_index = self.comboBox.currentIndex()
        if selected_patient_index != -1:
            patient_data = self.patients[selected_patient_index]
            self.textBrowser.clear()
            self.textBrowser.append(f"<b>Nombre:</b> {patient_data['nombre']}")
            self.textBrowser.append(f"<b>Apellidos:</b> {patient_data['apellidos']}")
            self.textBrowser.append(f"<b>Edad:</b> {patient_data['edad']}")
            self.textBrowser.append(f"<b>Nivel de peligro:</b> {patient_data['nivel_riesgo']}")

    def show_Graph1(self):
        selected_patient_index = self.comboBox.currentIndex()
        if selected_patient_index != -1:
            patient_data = self.patients[selected_patient_index][-8:]
            x_values = [i for i in range(1, 9)]
            self.plotly_figure = go.Figure()
            self.plotly_figure.add_trace(go.Scatter(x=x_values, y=patient_data, mode='lines+markers', name='Impedancy Graph'))
            html = self.plotly_figure.to_html(full_html=False, include_plotlyjs='cdn')
            self.graphicsView.setHtml(html)
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            self.graphicsView.setSizePolicy(size_policy)
            self.add_data_to_model()
            self.update_warning()

    def show_Graph2(self):
        selected_patient_index = self.comboBox.currentIndex()
        if selected_patient_index != -1:
            patient_data = self.patients[selected_patient_index][-8:]
            x_values = [i for i in range(1, 9)]
            self.plotly_figure = go.Figure()
            self.plotly_figure.add_trace(go.Scatter(x=x_values, y=patient_data, mode='markers', name='Scatter Plot'))
            html = self.plotly_figure.to_html(full_html=False, include_plotlyjs='cdn')
            self.graphicsView.setHtml(html)
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            self.graphicsView.setSizePolicy(size_policy)
            self.add_data_to_model()
            self.update_warning()

    def show_Graph3(self):
        selected_patient_index = self.comboBox.currentIndex()
        if selected_patient_index != -1:
            patient_data = self.patients[selected_patient_index][-8:]
            x_values = [i for i in range(1, 9)]
            self.plotly_figure = go.Figure()
            self.plotly_figure.add_trace(go.Box(y=patient_data, name='Box Plot'))
            html = self.plotly_figure.to_html(full_html=False, include_plotlyjs='cdn')
            self.graphicsView.setHtml(html)
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            self.graphicsView.setSizePolicy(size_policy)
            self.add_data_to_model()
            self.update_warning()

    def show_Graph4(self):
        selected_patient_index = self.comboBox.currentIndex()
        if selected_patient_index != -1:
            patient_data = self.patients[selected_patient_index][-8:]
            x_values = [i for i in range(1, 9)]
            self.plotly_figure = go.Figure()
            self.plotly_figure.add_trace(go.Bar(x=x_values, y=patient_data, name='Bar Graph'))
            html = self.plotly_figure.to_html(full_html=False, include_plotlyjs='cdn')
            self.graphicsView.setHtml(html)
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            self.graphicsView.setSizePolicy(size_policy)
            self.add_data_to_model()
            self.update_warning()

    def patients_Conf(self):
        options = ["Añadir", "Eliminar", "Modificar"]
        option, ok = QInputDialog.getItem(self, "Gestionar Paciente", "Seleccione una opción:", options, 0, False)
        if ok:
            if option == "Añadir":
                self.new_Patient_UI()
            elif option == "Eliminar":
                self.remove_Patient_UI()
            elif option == "Modificar":
                self.modify_Patient_UI()
    
    def new_Patient_UI(self):
        dni, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce el DNI del nuevo paciente:")
        if ok:
            if select_PacientByDId(dni):
                QMessageBox.warning(self, "Error", "Ya existe un paciente con el DNI proporcionado.")
                return

            name, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce el nombre del nuevo paciente:")
            if ok:
                surname, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce los apellidos del nuevo paciente:")
                if ok:
                    age, ok = QInputDialog.getInt(self, "Añadir Paciente", "Introduce la edad del nuevo paciente:")
                    if ok:
                        danger, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce el nivel de peligro del nuevo paciente:")
                        if ok:
                            new_Patient(dni, name, surname, age, danger)
                            self.comboBox.addItem(dni)
                            self.patients = get_Patients()
                            QMessageBox.information(self, "Éxito", "Paciente añadido correctamente.")

    def remove_Patient_UI(self):
        dni, ok = QInputDialog.getText(self, "Eliminar Paciente", "Introduce el DNI del paciente a eliminar:")
        if ok:
            if not select_PacientByDId(dni):
                QMessageBox.warning(self, "Error", "El paciente con el DNI proporcionado no existe.")
                return

            if delete_Patient(dni):
                QMessageBox.information(self, "Éxito", "Paciente eliminado correctamente.")
                self.comboBox.removeItem(self.comboBox.findText(dni))
                self.patients = get_Patients()
                self.show_User_Info()
            else:
                QMessageBox.warning(self, "Error", "Error al eliminar paciente.")

    def modify_Patient_UI(self):
        dni, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce el DNI del paciente a modificar:")
        if ok:
            if not select_PacientByDId(dni):
                QMessageBox.warning(self, "Error", "El paciente con el DNI proporcionado no existe.")
                return

            name, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce el nuevo nombre del paciente:")
            if ok:
                surname, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce los nuevos apellidos del paciente:")
                if ok:
                    age, ok = QInputDialog.getInt(self, "Modificar Paciente", "Introduce la nueva edad del paciente:")
                    if ok:
                        danger, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce el nuevo nivel de peligro del paciente:")
                        if ok:
                            if modify_Patient(dni, name, surname, age, danger):
                                self.patients = get_Patients()
                                self.comboBox.currentIndexChanged.disconnect()  
                                self.show_User_Info()
                                QMessageBox.information(self, "Éxito", "Paciente modificado correctamente.") 
                            else:
                                QMessageBox.warning(self, "Error", "Error al modificar paciente.")

    def update_warning(self):
        # Carga la imagen desde un archivo
        selected_patient_index = self.comboBox.currentIndex()
        if selected_patient_index != -1:
            patient_data = self.patients[selected_patient_index][-8:]

            for value in patient_data:
                if float(value) > 4:
                    # Carga la imagen desde un archivo
                    pixmap = QPixmap("data/aviso.png")
                    
                    # Ajusta la imagen al QLabel
                    scaled_pixmap = pixmap.scaled(self.estado.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
                    self.estado.setPixmap(scaled_pixmap)
                    self.estado.setScaledContents(True)
                    break
                else :
                    pixmap = QPixmap("data/estable.png")
                    
                    # Ajusta la imagen al QLabel
                    scaled_pixmap = pixmap.scaled(self.estado.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
                    self.estado.setPixmap(scaled_pixmap)
                    self.estado.setScaledContents(True)
        
    def add_data_to_model(self):
         # Crear el modelo de datos
        self.model = QStandardItemModel()

        # Obtener el índice del paciente seleccionado en el comboBox
        selected_patient_index = self.comboBox.currentIndex()

        # Obtener los datos del paciente seleccionado
        patient_data = self.patients[selected_patient_index]

        # Agregar los datos del paciente al modelo
        row_items = [QStandardItem(str(item)) for item in patient_data]
        self.model.appendRow(row_items)

        # Establecer el modelo en el QTableView
        self.tableView.setModel(self.model)
    

    def send_email(self):
        # Mostrar un cuadro de diálogo de advertencia
        reply = QMessageBox.question(None, 'Enviar correo', '¿Estás seguro de que quieres enviar el correo?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Si se hace clic en "Sí", abrir el sitio web
        if reply == QMessageBox.StandardButton.Yes:
        
            # Configurar los parámetros del servidor SMTP
            smtp_server = 'smtp.gmail.com'
            port = 587
            sender_email = 'heartkathon@gmail.com'
            password = 'ikgb jrvp nquf xlzm'

            # Configurar el mensaje
            receiver_email = 'heartkathon@gmail.com'
            subject = 'AVISO DEL MÉDICO'
            body = 'Aviso de de contacto de su medico'

            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = receiver_email

            # Establecer la conexión SMTP y enviar el correo electrónico
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                #print("Correo electrónico enviado exitosamente")

            QMessageBox.information(None, ' ', 'Correo enviado correctamente', QMessageBox.StandardButton.Ok)

    
    def openWebsite(self):
        # Mostrar un cuadro de diálogo de advertencia
        reply = QMessageBox.question(None, 'Abrir Sitio Web', '¿Estás seguro de que quieres abrir el sitio web?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Si se hace clic en "Sí", abrir el sitio web
        if reply == QMessageBox.StandardButton.Yes:
            # URL del sitio web al que quieres dirigir
            url = QUrl('https://heartkathon.sencia.es/')

            # Abrir la URL en un navegador web externo
            QDesktopServices.openUrl(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    inicio_sesion = Backend()
    inicio_sesion.show()
    
    sys.exit(app.exec())