import math
import random
from sklearn.metrics import calinski_harabasz_score


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


def coreAleatorio(listaPuntos , cantidadK):
    cantidadIteraciones=0
    cantidadCalculosDistancia=0
    cantidad=len(listaPuntos)
    listaCentroides=[]
    numsAux=[]
    listaPuntosCopia=listaPuntos.copy()

    while len(listaCentroides)<cantidadK:       #Asignación de centroides
    
        numRandom=random.randint(1,cantidad)    #Número aleatorio entre 1 y la cantidad de puntos del dataset
        bandera=0
        for k in numsAux:                       #Control centroides repetidos
            if numRandom==k:
                bandera=1
        
        if bandera==0:                          
            for j in listaPuntos:
                if j.punto==numRandom:
                    centroideCreado=dataPoint(j.valorX,j.valorY,j.punto,0,0,0,0)
                    listaCentroides.append(centroideCreado)
                    listaPuntos.remove(j)
        
    listaPuntos.clear()
    listaPuntos=listaPuntosCopia.copy()
    result=[]
    result.extend(kmeans(listaPuntosCopia,listaCentroides,cantidadCalculosDistancia,cantidadIteraciones))
    return(result)   

def coreHeuristica(listaPuntos , cantidadK):
    listaCentroides=[]
    listaPuntosMedia=[]
    listaPuntosCopia=[]
    cantidadIteraciones=0
    cantidadCalculosDistancia=0
    listaPuntosCopia.extend(listaPuntos.copy())
    cantidad1=len(listaPuntos)
    numRandom=random.randint(1,cantidad1)       #Número aleatorio entre 1 y la cantidad de puntos del dataset    
        
    for j in listaPuntos:                       #Asignacion del primner centroide de manera aleatoria
        if j.punto==numRandom:
            centroideCreado=dataPoint(j.valorX,j.valorY,j.punto,0,0,0,0)
            listaCentroides.append(centroideCreado)
            listaPuntosMedia.clear()
            listaPuntosMedia.append(centroideCreado)
            listaPuntos.remove(j)
            cantidad1-=1
    
    bandera3=0
    contador=0
    listaPuntos.clear()
    listaPuntos=listaPuntosCopia.copy()
    
    while len(listaCentroides)<cantidadK:           #Asignación de los demas centroides con calculos de distancias en base a los anteriores centroides
        mayorDistancia=0
        posLista=-1
        for k in listaPuntos:
            posLista+=1
            contador+=1
            distanciaTotal=0
            for j in listaPuntosMedia:
                resta1=k.valorX-j.valorX
                resta2=k.valorY-j.valorY
                distanciaPunto=math.sqrt(math.pow(resta1,2)+math.pow(resta2,2))
                distanciaTotal+=distanciaPunto
                cantidadCalculosDistancia+=1
            if mayorDistancia<distanciaTotal:
                mayorDistancia=distanciaTotal
                puntoMayor=dataPoint(k.valorX,k.valorY,k.punto,0,0,0,0)
                puntoMayorSacar=posLista
        
        if bandera3==0 and contador==cantidad1:
            listaPuntosMedia.clear()
            bandera3=1

        listaPuntosMedia.append(puntoMayor)
        listaCentroides.append(puntoMayor)
        listaPuntos.pop(puntoMayorSacar)
        cantidad1-=1

    result=[]
    result.extend(kmeans(listaPuntosCopia,listaCentroides,cantidadCalculosDistancia,cantidadIteraciones))
    return(result)    
    
    
    
    


def kmeans(listaPuntos, listaCentroides,cantidadCalculosDistancia,cantidadIteraciones):
    bandera1=True
    bandera2=True
    listaCentroidesActu=[]
    listaCentroidesAux=[]
    listaDistancias=[]

    while bandera1==True and bandera2==True:                    #Condiciones de parada
        cantidadIteraciones+=1
        bandera1=False
        bandera2=False
        listaCentroidesAux.clear()
        listaCentroidesAux.extend(listaCentroides.copy())

        for j in listaPuntos:
            listaDistancias.clear()
            """ Asignacion de distancias a centroides """
            for k in listaCentroides:
                resta1=j.valorX-k.valorX
                resta2=j.valorY-k.valorY
                valor1= math.sqrt(math.pow(resta1,2)+math.pow(resta2,2))
                objeto=distCentroide(valor1,k.punto)
                listaDistancias.append(objeto)
                cantidadCalculosDistancia+=1
            
            """ Obtencion de la menor distancia """
            menorDistancia=listaDistancias.__getitem__(0)
            for k in listaDistancias:
                if menorDistancia.distancia>k.distancia:
                    menorDistancia=k
            
            if j.centroide!=menorDistancia.punto:                   #Verificación de cambio de un cluster a otro para un punto y asignación de un punto a un cluster
                bandera1=True
                j.centroide=menorDistancia.punto
            
            for k in listaCentroides:                               #Busqueda del centroide a actualizar 
                if k.punto == menorDistancia.punto:
                    centroideActu=k
            
            listaCentroides.remove(centroideActu)                   #Eliminamos el centroide de la listaCentroides para actualizar los valores de cantidadX, cantidadY y cantidadCentroide
            cantidadCentroide2=centroideActu.cantidadCentroide+1
            cantidadX2=centroideActu.cantidadX+j.valorX
            cantidadY2=centroideActu.cantidadY+j.valorY
            valorX2=centroideActu.valorX
            valorY2=centroideActu.valorY
            punto2=centroideActu.punto
            listaCentroides.append(dataPoint(valorX2,valorY2,punto2,cantidadCentroide2,cantidadX2,cantidadY2,0))    #Volvemos a agregar el centroide a la listaCentroides
        
        listaCentroidesActu.clear()

        for j in listaCentroides:                   #Actualizamos la posición de los centroides
            if(j.cantidadCentroide!=0):
                mediaX=j.cantidadX/j.cantidadCentroide
                mediaY=j.cantidadY/j.cantidadCentroide
                punto1=j.punto
                cantidadCentroide1=0
                cantidadX1=0
                cantidadY1=0
                centroide1=0
                listaCentroidesActu.append(dataPoint(mediaX,mediaY,punto1,cantidadCentroide1,cantidadX1,cantidadY1,centroide1))
            else:
                mediaX=j.valorX
                mediaY=j.valorY
                punto1=j.punto
                cantidadCentroide1=0
                cantidadX1=0
                cantidadY1=0
                centroide1=0
                listaCentroidesActu.append(dataPoint(mediaX,mediaY,punto1,cantidadCentroide1,cantidadX1,cantidadY1,centroide1))

        
        for j in listaCentroidesAux:            #Verificamos si hubo modificación en la posición de los centroides
            for k in listaCentroidesActu:
                if j.punto==k.punto:
                    if j.valorX!=k.valorX or j.valorY!=k.valorY:
                        bandera2=True

        listaCentroides.clear()
        listaCentroides.extend(listaCentroidesActu.copy())
        
    
    #Conversión del formato de los datos al formato que necesita la gráfica
    colores=["red","blue","#00FF40","#D7DF01","#FF8000","#00FFFF"]
    contador=0
    listaPuntosGraficaX=[]
    listaPuntosGraficaY=[]
    listaColores=[]
    listaCalinskiX=[]
    listaCalinskiLabel=[]
    listaTupla=[]
    
    for j in listaCentroides:
        for k in listaPuntos:
            if j.punto==k.centroide:
                listaPuntosGraficaX.append(k.valorX)
                listaPuntosGraficaY.append(k.valorY)
                listaTupla.clear()
                listaTupla.append(k.valorX)
                listaTupla.append(k.valorY)
                listaCalinskiX.append(listaTupla)
                listaCalinskiLabel.append(k.centroide)
                listaColores.append(colores[contador])
        listaPuntosGraficaX.append(j.valorX)
        listaPuntosGraficaY.append(j.valorY)
        listaColores.append("#FE2EF7")
        contador+=1
    
    ch_index = calinski_harabasz_score(listaCalinskiX, listaCalinskiLabel)      #Cálculo de calinski harabasz score
    listaResultados=[]
    listaResultados.clear()
    listaResultados.append("Calinski harabasz score:\t"+str(ch_index))
    listaResultados.append("Cantidad de iteraciones:\t"+str(cantidadIteraciones))
    listaResultados.append("Cantidad de cálculos de distancia:\t"+str(cantidadCalculosDistancia))
    resultados=[]
    resultados.append(listaPuntosGraficaX)
    resultados.append(listaPuntosGraficaY)
    resultados.append(listaColores)
    resultados.append(listaResultados)
    return(resultados)
    