import sys
import csv
import matplotlib.pyplot as plt
from ventana6 import *
from coreAlgoritmo import *


from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget, QGridLayout,QLineEdit,QPushButton, QLabel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from pathlib import Path
from math import sqrt,pow

class dataPoint:
    def __init__(self,valorX, valorY, punto, cantidadCentroide,cantidadX,cantidadY,centroide):
        self.valorX = valorX
        self.valorY = valorY
        self.punto = punto
        self.cantidadCentroide = cantidadCentroide
        self.cantidadX = cantidadX
        self.cantidadY = cantidadY
        self.centroide = centroide

class distCentroide:
    def __init__(self,distancia, punto):
        self.distancia = distancia
        self.punto=punto

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt File Dialog')
        self.setGeometry(100, 100, 400, 100)

        layout = QGridLayout()
        self.setLayout(layout)

        # file selection
        file_browse = QPushButton('Browse')
        file_browse.clicked.connect(self.open_file_dialog)
        self.filename_edit = QLineEdit()

        layout.addWidget(QLabel('File:'), 0, 0)
        layout.addWidget(self.filename_edit, 0, 1)
        layout.addWidget(file_browse, 0 ,2)

      
        self.show()


class interfazGUIa(QtWidgets.QWidget):
    rutaArchivo=" "
    model2 = QStandardItemModel()
    def __init__(self, parent=None):    
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.botonBuscarArchivo.clicked.connect(self.open_file_dialog)
        self.ui.botonAleatorio.clicked.connect(self.aleatorio)
        self.ui.botonHeuristica.clicked.connect(self.heuristica)
        self.ui.kSlider.valueChanged.connect(self.update)
        self.ui.vistaResultados.setModel(self.model2)
    
    def update(self):
        self.ui.valoresK.setText(f'Cantidad de clusters: {self.ui.kSlider.value()}')
    
    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            "D:\\icons\\avatar\\", 
            "Files (*.csv)"
        )
        
        if filename:
            path = Path(filename)
            self.ui.archivoBuscado.setText(str(path))
            self.rutaArchivo = path
            

    def aleatorio(self):
        listaPuntos=[]
        
        if self.rutaArchivo!=" ":
            with open(self.rutaArchivo, "r") as archivo:
                lector = csv.reader(archivo, delimiter=";")
                cantidad=1
                # Omitir el encabezado
                next(lector, None)
                for fila in lector:
                    # Tenemos la lista. En la 0 tenemos el nombre, en la 1 la calificación y en la 2 el precio
                    datoX = float(fila[0].replace(",","."))
                    datoY = float(fila[1].replace(",","."))
                    punto=dataPoint(datoX,datoY,cantidad,0,0,0,0)
                    listaPuntos.append(punto)
                    cantidad+=1
                cantidad-=1

                cantidadK=self.ui.kSlider.value()
                resultados=[]
                listaResultados=[]
                resultados.extend(coreAleatorio(listaPuntos,cantidadK))
                listaResultados.extend(resultados[3])
                self.model2.clear()

                for i in listaResultados:
                    self.model2.appendRow(QStandardItem(i))
                    
                self.ui.vistaResultados.setModel(self.model2)
                plt.scatter(resultados[0],resultados[1],color=resultados[2])
                plt.xlabel("Eje X")
                plt.ylabel("Eje Y")
                plt.title("Kmeans Aleatorio")
                plt.show()
        else:
            QMessageBox.about(self, "Alerta", 'Debe selecionar un archivo dataset primero')


    def heuristica(self):
        listaPuntos=[]
        
        if self.rutaArchivo!=" ":
            with open(self.rutaArchivo, "r") as archivo:
                lector = csv.reader(archivo, delimiter=";")
                cantidad=1
                # Omitir el encabezado
                next(lector, None)

                for fila in lector:
                    # Tenemos la lista. En la 0 tenemos el nombre, en la 1 la calificación y en la 2 el precio
                    datoX = float(fila[0].replace(",","."))
                    datoY = float(fila[1].replace(",","."))
                    punto=dataPoint(datoX,datoY,cantidad,0,0,0,0)
                    listaPuntos.append(punto)
                    cantidad+=1

                cantidad-=1
                cantidadK=self.ui.kSlider.value()
                resultados2=[]
                listaResultados=[]
                resultados2.extend(coreHeuristica(listaPuntos,cantidadK))
                listaResultados.extend(resultados2[3])
                self.model2.clear()

                for i in listaResultados:
                    self.model2.appendRow(QStandardItem(i))

                plt.scatter(resultados2[0],resultados2[1],color=resultados2[2])
                plt.xlabel("Eje X")
                plt.ylabel("Eje Y")
                plt.title("Kmeans Heurística")
                plt.show()
        
        else:
            QMessageBox.about(self, "Alerta", 'Debe selecionar un archivo dataset primero')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mi_app = interfazGUIa()
    mi_app.show()
    sys.exit(app.exec())