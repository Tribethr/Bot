#Desarrolado por Tribeth Rivas
#Fecha de creación: 23/06/18
# -----------------------------------Imports--------------------------------------
import random
import pyttsx3
import easygui
import pickle
import os
import pyaudio
import wave
import win32api
import win32con
import winsound
import time
import speech_recognition as sr
from threading import Thread
# ---------------------------Variables de respuesta-------------------------------
baseDeDatos = [None]*28
respuesta = [None]
verificadorDeRuta = [None]
texto = [""]
# ----------------------------Variables de control--------------------------------
comando = True
depurar = False
probabilidades = "áéíóúý"
retornos = "aeiouy"
# -------------------------Variables de reconocimiento----------------------------
formatoGrabacion = pyaudio.paInt16
"EASYGUI!!!!!!!"
def registrarDatos(texto,dato):
    """
    Funcion: Toma un texto y lo convierte en la ruta de almacenamiento, en una lista crea sublistas basado en la posicion de los valores de cada letra del texto.
    Entradas: Texto(str) es el nombre con el cual se creará la ruta de guardado y dato(str) es lo que se ejecuta al buscarlo.
    Salidas: N/A Solo guarda el nuevo comando o respuesta.
    """
    if(dato == "cancelar"):
        return
    ruta = "baseDeDatos["
    for i in texto:
        ruta += str(ord(i)-97)+"]" if i != " " else "27]"
        exec("verificadorDeRuta[0] = "+ruta)
        if(verificadorDeRuta[0] == None):
            exec(ruta+"=["+"None,"*28+"[]]") 
        ruta+="["
    exec(ruta+"28].append(dato)")
    memorizar()

def buscarRespuesta(texto):
    """
    Funcion: Toma el texto y basado en los valores de sus letras genera un ruta de busqueda y su existe retorna lo que haya almacenado ahí, de lo contrario retorna False.
    Entradas: texto(str) El texto con el cual se verificará la ruta.
    Salidas: Respuesta(str) o False si no existe.
    """
    global depurar
    ruta = "baseDeDatos"
    for i in texto:
        ruta+="["+str(+ord(i)-97)+"]" if i != " " else "[27]"
    try:
        exec("respuesta[0] = "+ruta+"[28]")
        if(depurar):
            return (ruta+"[28]")
        return random.choice(respuesta[0])
    except:
        return False
    
def hablar(texto, imprimir = True):
    """
    Funcion: Se le ingresa un texto y lo convierte a audio, además de imprmirlo en pantalla.
    Entradas: texto(str) a decir y imprimir(bool)si se quiere su impresión en pantalla.
    Salidas: N/A
    """
    if(imprimir):
        print("\nBot: "+texto+"\n")
    voz.say(texto)
    voz.runAndWait()

def cambiarModo(imprimir = True):
    """
    Funcion: Cambia a modo ejecución o a modo charla.
    Entradas: imprimir(bool) si se quiere imprimir.
    Salidas: N/A
    """
    global comando
    if(comando):
        comando = False
        if(imprimir):
            hablar("Cambiando a modo charla")
        return
    comando = True
    if(imprimir):
        hablar("Cambiando a modo ejecución")

def modoDepuracion(imprimir = True):
    """
    Funcion: Cambia a modo depuración o sale de él.
    Entradas: imprimir(bool) si se quiere imprimir.
    Salidas: N/A
    """
    global depurar
    if(depurar):
        depurar = False
        hablar("Saliendo de modo depuracion")
    else:
        depurar = True
        hablar("Cambiando a modo depuracion")
    cambiarModo(imprimir)

def revisarComandos(lista = baseDeDatos,ruta = "baseDeDatos"):
    """
    Funcion: Recorre la base de datos del bot e imprime todos sus comandos.
    Entradas: La lista a recorrer(list) y la ruta a utilizar(str)
    Salidas: N/A
    """
    for i in range(len(lista)):
        indice = "["+str(i)+"]"
        ruta += indice
        if(type(lista[i]) == list):
            revisarComandos(lista[i],ruta)
        elif(lista[i] != None):
            print(traductorDeRutas(ruta[11:]))
        ruta = ruta[:-len(indice)]

def traductorDeRutas(ruta):
    """
    Funcion: Recibe un ruta y traduce sus posiciones como texto.
    Entradas: ruta(str).
    Salidas: El texto basado en la ruta(str).
    """
    ruta = ruta.replace("[","")
    if(len(ruta)<2):
        return ""
    letra = chr(int(ruta[:ruta.index("]")])+97)
    if(letra == '|' or letra == "}"):
        letra = " "
    return letra + traductorDeRutas(ruta[ruta.index("]")+1:])
        
def revisarRespuestas(lista):
    """
    Funcion: Recorre la base de datos e imprime todas las respuestas de todos los comandos.
    Entradas: Lista a recorrer(list)
    Salidas: N/A
    """
    for i in lista:
        if(type(i) == list):
            revisarRespuestas(i)
        elif(i != None):
            print(i)

def escuchar(tiempoGrabacion = 3,ruido = True):
    """
    Funcion: Escuha lo que el usuario diga durante el tiempo de grabación y luego lo convierte a texto y lo retorna.
    Entradas: ruido(bool) si quiere sonar el beep e imprimir.
    Salidas: Texto que escuchó(str) o False si no pudo escuchar bien(bool).
    """
    audio = grabarAudio(tiempoGrabacion,ruido)
    return traducirAudio(audio)
    
def esperar():
    """
    Funcion: Espera hasta que se le vuelva a decir 'bot', entonces ejecutará de nuevo los comandos.
    Entradas: N/A
    Salidas: N/A
    """
    hablar("Ok, esperaré")
    while(not "bod" in texto[0]):
        audio = grabarAudio(tiempoGrabacion = 3,ruido = False)
        t1 = Thread(target = traducirAudio, args = (audio,True) )
        t1.start()
    texto[0] = ""
    hablar("Dime")

def grabarAudio(tiempoGrabacion = 3,ruido = True):
    p = pyaudio.PyAudio()
    stream = p.open(format=formatoGrabacion,channels=2,rate=44100,input=True,frames_per_buffer=1024)
    if(ruido):
        winsound.Beep(3800,120)
        print("\nGrabando...\n")
    frames = []
    for i in range(0, int(44100 / 1024 * tiempoGrabacion)):
        data = stream.read(1024)
        frames.append(data)
    if(ruido):
        winsound.Beep(2500,120)
        print("\nTerminé de grabar\n")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("grabacion.wav", 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(formatoGrabacion))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    if(ruido):
        print("\nTraduciendo...\n")
    r = sr.Recognizer()
    grabacion = sr.AudioFile("grabacion.wav")
    with grabacion as fuente:
        audio = r.record(fuente)
    return audio

def traducirAudio(audio,esperar = False):
    try:
        r = sr.Recognizer()
        respuesta = r.recognize_google(audio,language = "es-CR")
        if(esperar):
            exec("texto[0] = respuesta")
        return respuesta
    except:
        return False

def despertar():   
    """
    Funcion: Lleva el control de todas las funciones del bot
    Entradas: N/A
    Salidas: N/A
    """
    recordar()
    hablar("¡Ya estoy lista!\n")
    while(True):
        busqueda = validarBusqueda(escuchar())
        if(not busqueda):
            hablar("Disculpa no te escuché")
            continue
        if(not busqueda.replace(" ","").isalpha()):
            hablar("Debe decir solo texto")
            continue
        print("Yo: "+busqueda)
        respuesta = buscarRespuesta(busqueda)
        if(respuesta == "modo"):
            cambiarModo()
            continue
        if(respuesta):
            if(comando):
                try:
                    exec(respuesta)
                    continue
                except Exception:
                    hablar("Lo siento, no has dicho un comando")
                    continue
            elif(depurar):
                print(respuesta)
                continue
            hablar(respuesta)
        else:
            revisarReconocimiento(busqueda)
            
def revisarReconocimiento(busqueda):
    """
    Funcion: Revisa si ocurrió un error al hacer la busqueda y pregunta si este ocurrió, si lo hubo no hace nada, de lo contrario regustra el nuevo comando.
    Entradas: La busqueda que se solicitó(str).
    Salidas: N/A
    """
    hablar("¿Quisiste decir "+busqueda+"?")
    resp = validarBusqueda(escuchar())
    if(not resp == "si"):
        hablar("Ok, escuchare de nuevo")
        return
    hablar("Lo siento todavía no sé que responder a eso")
    print("\n¿Qué puedo responder?\nSi deseas omitir la respuesta ingresa cancelar\n")
    registrarDatos(busqueda,input("Ingrese la respuesta: "))
    
def validarBusqueda(busqueda):
    """
    Funcion: Valida que no sea False, que no tenga tildes y que esté en minúscula.
    Entradas: El texto a buscar(str).
    Salidas: El texto con todo corregido(str)
    """
    if(not busqueda):
        return False
    for i in range(len(busqueda)):
        if(busqueda[i] in probabilidades):
            busqueda = busqueda[:i]+retornos[probabilidades.index(busqueda[i])]+busqueda[i+1:]
    return busqueda.lower()
        
def recordar():
    """
    Funcion: Carga todos los datos en memoria.
    Entradas: N/A
    Salidas: N/A
    """
    try:
        global baseDeDatos
        archivo = open(os.getcwd()+"\\Memoria","rb")
        baseDeDatos = pickle.load(archivo)
        archivo.close()
    except:
        hablar("No he encontrado ningun archivo de memoria")
        pass
    
def memorizar():
    """
    Funcion: Guarda todos los datos en memoria.
    Entradas: N/A
    Salidas: N/A
    """
    archivo = open("Memoria","wb")
    pickle.dump(baseDeDatos,archivo)
    archivo.close()
    print("¡Gracias, ahora sé qué responder!\n")

voz = pyttsx3.init()
voz.setProperty("rate",150)
despertar()
