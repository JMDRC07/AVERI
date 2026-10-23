import speech_recognition as SR
from rapidfuzz import fuzz
import re, unicodedata
from ia_detect import  *

# FORZAR UTF-8 en la consola de Windows (importante)
"""if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')"""

r = SR.Recognizer()
mic = SR.Microphone()

#usa variaciones por si no detecta exactamente lo mismo
VARIANTES = ["avery", "averi", "aberi", "averi", "haber i", "a veri", "abril", "aver"]

#VARIACIONES ORDEN PARA DETECTAR
VARIANTES2 = ["que vez", "que ves", "ves", "bes", "bez", "ves", "queves", "que observas", "observas", "wachas", "mirar", "miras", "percibes"]

#VARIACIONES PARA CERRAR LA CAMARA
VARIANTES3 = ["cerrar", "cierra", "cierre", "cerra", "cerrado"]

#APAGAR EN SAFE
VARIANTES4 = ["adios", "nos vemos", "chao", "apagar", "bye"]

#NORMALIZA EL TEXTO QUITANDO CARACTERES RAROS Y CONVIRITIENDO A MINUSCULAS
def normalizar(t):
    t = t.lower()
    t = ''.join(c for c in unicodedata.normalize('NFD', t)
                if unicodedata.category(c) != 'Mn')
    t = re.sub(r'[^a-z0-9 ]', '', t)
    return t

#HACE LA COINCIDENCIA ENTRE EL TEXTO NORMALIZADO Y ALGUNA DE LAS DE VARIABLES PARA ALGUNA ORDEN ESPECIFICA
def coincide(texto, variantes, umbral=80):
    texto = normalizar(texto)
    for palabra in texto.split():
        for v in variantes:
            if fuzz.ratio(palabra, normalizar(v)) >= umbral:
                return True
    return False

#CODIGO DE PRUEBA #MICROFONO
with mic as source:
    r.adjust_for_ambient_noise(source, duration=1.5)
    print("Escuchando... di 'avery' para abrir la cámara, 'cerrar' para cerrarla.")
    while True:
        try: 
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            texto = r.recognize_google(audio, language="es-ES")
            print("Dijiste:", texto)
            if coincide(texto,VARIANTES):
                print(">>> BIENVENIDO <<<")
                detectar()
            elif coincide(texto,VARIANTES2):
                print(">>> REPORTE DE LA CÁMARA <<<")
                reporte = describe()
                print(reporte)
                hablar(reporte)
            elif coincide(texto,VARIANTES3):
                print("CERRANDO CAMARA")
                cerrar_camara()
            elif coincide(texto,VARIANTES4):
                hablar("Cerrado programa buen dia")
                print("BUEN DIA :D")
                cerrar_camara()
                break


        except SR.WaitTimeoutError:
            pass   # nadie hablo, sigo escuchando papi
        except SR.UnknownValueError:
            pass   # ignora erroreres inesperados
        except SR.RequestError as e:
            print("Error:", e)
            #usamos la api de google... a considerar para cambiar por una mejor

"""
#AUDIO PREGRABADO



with SR.AudioFile('C:\\Users\\jdelr\\OneDrive\\Escritorio\\SCRIPT\\audios\\avery_test.wav') as source:
    audio = r.listen(source)

    try:
        print('espere un momento, el audio se esta leyendo...')
        text = r.recognize_google(audio, language='es-ES')
        time.sleep(1.5)
        if "avery" in text:
            print("Redirigiendo, espere un minuto")
        print(text)
    except:
        print('No se logro reconocer el audio')"""
