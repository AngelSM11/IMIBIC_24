import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QSizePolicy
from PyQt6.uic import loadUi
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class Backend(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("IMIBIC-frontend.ui", self)
        
        self.action_Add_Patient.triggered.connect(self.patients_Conf)
        self.read_DB()
        self.setFixedSize(self.size())
        
        self.graphicsView = QWebEngineView()
        self.gridLayout_6.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.comboBox.currentIndexChanged.connect(self.update_graph)

        self.plotly_figure = make_subplots(rows=1, cols=1)
        self.update_graph()

        self.apply_Palette()

    def apply_Palette(self):
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

    def read_DB(self):
        try:
            with open("db.txt", 'r') as file:
                self.patients = [line.strip().split(', ') for line in file.readlines()]
                self.comboBox.clear()
                for patient in self.patients:
                    self.comboBox.addItem(patient[0])
        except FileNotFoundError:
            print("There are no patients in the database. Please add some with the 'Add Patient' option.")
    
    def update_graph(self):
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

    def patients_Conf(self):
        options = ["Añadir", "Eliminar", "Modificar"]
        option, ok = QInputDialog.getItem(self, "Gestionar Paciente", "Seleccione una opción:", options, 0, False)
        if ok:
            if option == "Añadir":
                self.add_Patient()
            elif option == "Eliminar":
                self.clean_Patient()
            elif option == "Modificar":
                self.modify_Patient()
    
    def add_Patient(self):
        dni, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce el DNI del nuevo paciente:")
        if ok:
            name, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce el nombre del nuevo paciente:")
            if ok:
                surname, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce los apellidos del nuevo paciente:")
                if ok:
                    age, ok = QInputDialog.getInt(self, "Añadir Paciente", "Introduce la edad del nuevo paciente:")
                    if ok:
                        danger, ok = QInputDialog.getText(self, "Añadir Paciente", "Introduce el nivel de peligro del nuevo paciente:")
                        if ok:
                            patient = f"\n{dni}, {name}, {surname}, {age}, {danger}"
                            with open("db.txt", 'a') as file:
                                file.write(patient)
                            self.comboBox.addItem(dni)
                            QMessageBox.information(self, "Éxito", "Paciente añadido correctamente.")

    def clean_Patient(self):
        dni, ok = QInputDialog.getText(self, "Eliminar Paciente", "Introduce el DNI del paciente a eliminar:")
        if ok:
            with open("db.txt", 'r') as file:
                patients = file.readlines()
            with open("db.txt", 'w') as file:
                for patient in patients:
                    if not patient.startswith(dni):
                        file.write(patient)
            self.read_DB()
            QMessageBox.information(self, "Éxito", "Paciente eliminado correctamente.")

    def modify_Patient(self):
        dni, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce el DNI del paciente a modificar:")
        if ok:
            with open("db.txt", 'r') as file:
                patients = file.readlines()
            with open("db.txt", 'w') as file:
                for patient in patients:
                    if patient.startswith(dni):
                        name, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce el nuevo nombre del paciente:")
                        if ok:
                            surname, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce los nuevos apellidos del paciente:")
                            if ok:
                                age, ok = QInputDialog.getInt(self, "Modificar Paciente", "Introduce la nueva edad del paciente:")
                                if ok:
                                    danger, ok = QInputDialog.getText(self, "Modificar Paciente", "Introduce el nuevo nivel de peligro del paciente:")
                                    if ok:
                                        nuevo_paciente = f"{dni}, {name}, {surname}, {age}, {danger}\n"
                                        file.write(nuevo_paciente)
                    else:
                        file.write(patient)
            self.cargar_patients()
            QMessageBox.information(self, "Éxito", "Paciente modificado correctamente.")

    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ventana_principal = Backend()
    
    ventana_principal.show()
    
    sys.exit(app.exec())