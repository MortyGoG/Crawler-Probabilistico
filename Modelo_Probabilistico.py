import subprocess
import os
import re
from unidecode import unidecode
import numpy as np

import time

''' Stemming '''
import nltk  # Importamos la bilbioteca nltk
# Importamos la funcion word_tokenize desde el modulo tokenize
from nltk.tokenize import word_tokenize
# Se importa la funcion stopwords desde el modulo corpus
from nltk.corpus import stopwords
# Algoritmos de stemming
from nltk.stem import SnowballStemmer# Importamos la funcion word_tokenize desde el modulo tokenize
from nltk.tokenize import word_tokenize
# Se importa la funcion stopwords desde el modulo corpus
from nltk.corpus import stopwords
# Algoritmos de stemming
from nltk.stem import SnowballStemmer
import string  # Importar el módulo de caracteres de puntuación
import pandas as pd

''' Tkinter '''
import tkinter as tk # Importar libreria tk
from tkinter import * # libreria para hacer interfaces
import os #libreria para manipular directorios del S.O
from tkinter import font


# Carpeta de Dcoumentos txt
carpeta_txt = 'gatos\\gatos\\spiders\\'
# Nombre de archivos
archivos_txt = []
# Texto de los PDFs
texto_txt = ''
# Texto sin modificaciones
texto_original = ''
# Texto tokenizado
texto_tokenizado = []
# Diccionario de terminos tokenizados
diccionario_terminos = {}
# Diccionario sin tokenizacion
diccionario_terminos_originales = {}
# Matriz TD_IDF
matriz_booleana = []
# Documentos
documentos_en_cluster_consulta = []

# Vector qj
qj = []

# Matriz Similitud
matriz_similitud = []

#Vector consulta
vector_en_consulta = []

# Ventana ------------------------------------------------------------------------
''' Configuracion inicial de botones y ventana '''
raiz = Tk() #se crea el objeto de la ventana

# Funciones ----------------------------------------------------------------------
def on_cerrar_ventana():
    # Cerrar Tkinter
    raiz.destroy()    


def abrir_txt_con_aplicacion_predeterminada(nombre_txt):
    ''' Abrir txt con app predeterminada'''
    try:
        subprocess.Popen([nombre_txt], shell=True)
    except Exception as e:
        print(f"No se pudo abrir el archivo text: {e}")


def ejecutarScript():
    # Ruta del script a ejecutar
    ruta_script = 'gatos\\gatos\\spiders\\spider1.py'

    # Obtiene la ruta completa al directorio del script actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Obtén el directorio actual antes de cambiarlo
    directorio_actual = os.getcwd()

    # Concatena la ruta del script con la ruta completa
    ruta_completa = os.path.join(directorio_actual, ruta_script)

    # Cambia el directorio actual al directorio del script
    os.chdir(os.path.dirname(ruta_completa))

    # Ejecuta el comando "scrapy crawl ejemplo_spider"
    subprocess.run(["scrapy", "crawl", "spider1"])
    print("Comando ejecutado")

    # Regresa al directorio anterior
    os.chdir(directorio_actual)


def biblioteca_nltk():
    ''' Eliminacion de StopWords, Signos de puntuacion, Tokenizacion y Stemming '''
    # Descargar recursos de NLTK
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('snowball_data')
    print("Se descargaron los recursos de NLTK")


def quitar_acentos(palabra):
    # Utiliza unidecode para quitar acentos y caracteres diacríticos
    palabra_sin_acentos = unidecode(palabra)
    return palabra_sin_acentos


def quitar_acentos_de_texto(texto):
    palabras = texto.split()  # Divide el texto en palabras
    palabras_sin_acentos = [quitar_acentos(palabra) for palabra in palabras]
    texto_sin_acentos = ' '.join(palabras_sin_acentos)
    return texto_sin_acentos


def leer_txt(ruta_txt):
    """ Función para leer un archivo PDF y retornar su contenido de texto """
    print(ruta_txt)
    texto = ''
    with open(ruta_txt, 'r', encoding = 'utf-8', errors='ignore') as archivo:
        texto = archivo.read()
        texto = texto.lower()  # Convertir todo el texto a minúsculas
        texto = ''.join(c for c in texto if c not in string.punctuation or c in '()')
        texto = re.sub(r'[^\w\s]', '', texto)  # Eliminar símbolos de puntuación y otros caracteres no alfanuméricos
        texto = quitar_acentos_de_texto(texto)  # Eliminar acentos
        print(texto)     # Log en consola
        return texto


def tokenizar_stopwords(texto):
    """ Eliminar Signos de Puntuacion """
    texto = texto.translate(str.maketrans('', '', string.punctuation))  # Eliminar signos de puntuación
    
    ''' Texto Tokenizado y sin StopWords '''
    # Tokenización
    tokens = word_tokenize(texto)
    
    ''' Texto sin StopWords '''
    # Eliminación de stopwords en español
    sw = set(stopwords.words('spanish'))
    # Guardamos palabra por palabra de los tokens anteriores verifica la version en minusculas
    stop_words = [word for word in tokens if word.lower() not in sw]
    
    ''' Stemming '''
    # Stemming en español
    stemmer = SnowballStemmer('spanish')
    # Realiza stemming palabra por palabra de
    stemming_stopWords_tokens = [stemmer.stem(
        word) for word in stop_words]
    return stemming_stopWords_tokens


def tokenizado_sinsteamming(texto):
    """ Eliminar Signos de Puntuacion """
    texto = texto.translate(str.maketrans(
        '', '', string.punctuation))  # Eliminar signos de puntuación
    ''' Texto Tokenizado y sin StopWords '''
    # Tokenización
    tokens = word_tokenize(texto)
    # Eliminación de stopwords en español
    sw = set(stopwords.words('spanish'))
    # Guardamos palabra por palabra de los tokens anteriores verifica la version en minusculas
    tokenizado = [word for word in tokens if word.lower() not in sw]
    return tokenizado


def obtener_texto_tokenizado():
    # Ruta de pdf's
    global carpeta_txt
    # Texto de los PDFs
    global texto_txt
    # Recabar nombres de txt
    global archivos_txt
    # Texto sin modificaciones
    global texto_original
    # Texto tokenizado
    global texto_tokenizado
    # Diccionario de terminos tokenizados
    global diccionario_terminos
    # Diccionario sin tokenizacion
    global diccionario_terminos_originales
    # Contador de terminos
    contador = 0
    # 2do contador
    contador2 = 0
    # 3er contador
    contador3 = 0
    # 4to contador
    contador4 = 0

    # Ciclo de lectura por archivo
    for archivo in archivos_txt:
        ruta_txt = os.path.join(carpeta_txt, archivo)
        texto_txt = leer_txt(ruta_txt)  # Extraer el texto del txt actual
        # Texto con terminos tokenizados
        terminos = tokenizar_stopwords(texto_txt)
        # Guardar texto sin modificaciones
        texto_original += texto_txt + '\n'
        # Guardar texto tokenizado, stemming, etc.
        texto_tokenizado += terminos
    
        ''' Guardar en diccionario tokenizado '''
        # Iteramos en el tamaño de terminos totales que tenemos
        for i in range(len(terminos)):
            # Termino por termino si esta en el diccionario de terminos
            if terminos[i] in diccionario_terminos:
                # Si el "archivo" no esta en el diccionario del termino[i]
                if archivo not in diccionario_terminos[terminos[i]]:
                    # Si archivo no pertenece a la clave del termino, agrega el nombre del archivo
                    diccionario_terminos[terminos[i]].append(archivo)
            else:
                # Si el término no está en el diccionario, crea una nueva entrada con el archivo
                diccionario_terminos[terminos[i]] = [archivo]
                contador+=1
            print(contador)     # Log en consola

        terminos_sin_stem = tokenizado_sinsteamming(texto_txt)

        ''' Guardar en diccionario sin stem '''            
        # Iteramos en el tamaño de terminos totales que tenemos
        for j in range(len(terminos_sin_stem)):
             # Termino por termino si esta en el diccionario de terminos
            if terminos_sin_stem[j] in diccionario_terminos_originales:
                # Si el "archivo" no esta en el diccionario del termino[i]
                if archivo not in diccionario_terminos_originales[terminos_sin_stem[j]]:
                    # Si el término está en el diccionario, agrega el nombre del archivo
                    diccionario_terminos_originales[terminos_sin_stem[j]].append(archivo)
            else:
                diccionario_terminos_originales[terminos_sin_stem[j]] = [archivo]
                contador2+=1
            print(contador2)     # Log en consola
    print("Se guardo todo")     # Log en consola
    
    ''' Guardar texto tokenizado y sin StopWords '''
    texto_procesado = (f"'{word}'\n" if word ==
                        'endDoc$' else f"'{word}', " for word in texto_tokenizado)
    with open('swandSStep3-4.txt', 'w', encoding='utf-8') as archivo_tokenizado:
        archivo_tokenizado.writelines(texto_procesado)
    print("Se guardo swandSStep3-4.txt")


    ''' Diccionarios '''
    ''' txt de Diccionario(Con stem) '''
    diccionario1 = 'DiccionarioStep2.txt'   # Guardar texto extraido
    with open(diccionario1, 'w') as archivo:
        for palabra, documentos in diccionario_terminos.items():
            documentos_str = ', '.join(documentos)
            archivo.write(f'{palabra}: {documentos_str}\n')
            contador3+=1
            print(contador3)
    print("Se guardo DiccionarioStep2.txt")

    ''' txt de Diccionario (sin stem) '''
    diccionario2 = 'Diccionario_sinstem_Step2.txt'   # Guardar texto extraido
    with open(diccionario2, 'w') as archivo:
        for palabra, documentos in diccionario_terminos_originales.items():
            documentos_str = ', '.join(documentos)
            archivo.write(f'{palabra}: {documentos_str}\n')
            contador4+=1
            print(contador4)
    print("finalizo todo")     # Log en consola
    return texto_tokenizado


def generar_matriz_booleana():
    ''' Matriz Booleana '''
    global diccionario_terminos
    global matriz_booleana
    global archivos_txt

    matriz_booleana = np.zeros((len(archivos_txt), len(diccionario_terminos)))
    #matriz_booleana = np.zeros((len(archivos_txt), len(diccionario_terminos)))
    
    contador = 0

    # Llenado de la matriz booleana
    for i, archivo in enumerate(archivos_txt):
        for j, termino_n in enumerate(diccionario_terminos.keys()):  
            # Calcula tf              
            tf = diccionario_terminos[termino_n].count(archivo)
            # print(idf)
            matriz_booleana [i, j] = tf
            
            contador+=1
            print(contador)

                
    # Guardar matriz tf-idf en un archivo csv
    tf = pd.DataFrame(matriz_booleana)
    fila_nombre = archivos_txt.copy()
    tf.index = fila_nombre
    tf.to_csv('matriz_booleana.csv', sep='\t', header= list(diccionario_terminos.keys()))


def vector_consulta(terminos_consulta):
    global matriz_booleana
    global diccionario_terminos
    global archivos_txt
    global vector_en_consulta

    # Vecto de consulta
    vector_en_consulta = np.zeros((1,len(diccionario_terminos)))

    # Llenado del vector con tf
    for i, termino_diccionario in enumerate(diccionario_terminos.keys()): 
        tf = 0

        # Para cada termino de la consulta
        for termino_consulta in terminos_consulta:
            # Si el termino esta en el diccionario   
            if termino_consulta == termino_diccionario:
                # Colocar 1 o 0
                tf = 1
                break
        # Colocamos el valor en el vector de consulta
        vector_en_consulta[0, i] = tf
        # input("Press Enter to continue...")
    
    # Guardar matriz tf en un archivo csv
    idf = pd.DataFrame(vector_en_consulta)
    fila_nombre = ['Consulta']
    idf.index = fila_nombre
    idf.to_csv('vector_consulta.csv', sep='\t', header= list(diccionario_terminos.keys()))
    print("Vector_Consulta:")
    print(vector_en_consulta)


def calcular_qj():
    global qj
    global matriz_booleana
    global diccionario_terminos
    global archivos_txt
    
    suma = 0 
    
    # Vector qj
    qj = np.zeros((1,len(diccionario_terminos)))
     
    # En cada columna de la matriz booleana
    for j in range(len(diccionario_terminos)):
        # Suma de los valores de la columna
        for i in range(len(archivos_txt)):
            suma += matriz_booleana[i][j]
        # Colocar el valor en el vector qj
        qj[0, j] = suma / len(archivos_txt)
        # Reiniciar la suma
        suma = 0
    print("qj:")
    print(qj)
    
    
def sumar_filas():
    global matriz_similitud
    global archivos_txt
    global diccionario_terminos
    
    resultado = []
    
    # Suma de los valores de la fila
    for i in range(len(archivos_txt)):
        suma = 0
        for j in range(len(diccionario_terminos)):
            suma += matriz_similitud[i][j]
        # Colocar el valor en la fila
        resultado.append(suma)
    print("Resultado suma filas:")
    print(resultado)
    return resultado    
    
    
def calcular_similitud():
    global qj
    global matriz_similitud
    global matriz_booleana
    global diccionario_terminos
    global archivos_txt
    global vector_en_consulta
    
    calcular_qj()
    
    pj = 0.5
    
    # Matriz de similitud
    matriz_similitud = np.zeros((len(archivos_txt), len(diccionario_terminos)))
     
    # En cada columna de la matriz de similitud
    for j in range(len(diccionario_terminos)):
        # Operacion por documento
        for i in range(len(archivos_txt)):
            similitud = matriz_booleana[i][j] * vector_en_consulta[0][j] * np.log10((pj*(1-qj[0][j]))/(qj[0][j]*(1-pj)))
            # Colocar el valor en matriz de similitud
            matriz_similitud[i][j] = similitud
        
    # Guardar matriz tf en un archivo csv
    ms = pd.DataFrame(matriz_similitud)
    fila_nombre = []
    for i in range(len(archivos_txt)):
        fila_nombre.append(f'sem(q,d{i+1})')
    ms.index = fila_nombre
    ms.to_csv('matriz_similitud.csv', sep='\t', header= list(diccionario_terminos.keys()))
    print("Matriz de similitud creada con exito...")
    
    # Sumar filas
    resultado = sumar_filas()
    return resultado


# Boton 1
# Función para cambiar el color del botón al pasar el mouse sobre él
def cambiar_color1(event):
    boton_DicMos.configure(bg="#202123", fg="white")
# Función para restaurar el color original del botón al salir del mouse
def restaurar_color1(event):
    boton_DicMos.configure(bg="#444654", fg="white")


# Boton 2
# Función para cambiar el color del botón al pasar el mouse sobre él
def cambiar_color2(event):
    boton_StemStop.configure(bg="#202123", fg="white")
# Función para restaurar el color original del botón al salir del mouse
def restaurar_color2(event):
    boton_StemStop.configure(bg="#444654", fg="white")


# Boton 3
# Función para cambiar el color del botón al pasar el mouse sobre él
def cambiar_color3(event):
    boton_MatrizTxt.configure(bg="#202123", fg="white")
# Función para restaurar el color original del botón al salir del mouse
def restaurar_color3(event):
    boton_MatrizTxt.configure(bg="#444654", fg="white")

# Boton 4
# Función para cambiar el color del botón al pasar el mouse sobre él
def cambiar_color4(event):
    boton_guardar.configure(bg="#202123", fg="white")
# Función para restaurar el color original del botón al salir del mouse
def restaurar_color4(event):
    boton_guardar.configure(bg="#444654", fg="white")


# Crear una fuente personalizada con un tamaño grande
fuente_grande = ("Arial", 17)


# Botón 1 Mostar Diccionario -----------------------------------------------------------------------------
def mostar_diccionario():
    print("Mostró el diccionario")
    nombre_txt = "DiccionarioStep2.txt"
    # Abre txt
    abrir_txt_con_aplicacion_predeterminada(nombre_txt)

# Crear un botón y asociarle la función mostrar diccionario
boton_DicMos = Button(raiz, text="Mostrar Diccionario", command = mostar_diccionario, bg="#444654", fg="white", relief="flat", padx=10, pady=5)

# se enpaqueta el botón y se colóca en la ventana. 
boton_DicMos.pack()
# posiciona el bóton en los pixeles de la pantallas
boton_DicMos.place(x=100, y=60)


# Botón 2 Mostar Texto Stem y sin Stop -----------------------------------------------------------------------------
def mostar_Stem_Stop():
    print("Mostró el Texto steam y sin StopWords")
    nombre_txt = "swandSStep3-4.txt"
    # Abre txt
    abrir_txt_con_aplicacion_predeterminada(nombre_txt)


# Crear un botón y asociarle la función mostar_Stem_Stop)
boton_StemStop = Button(raiz, text="Mostrar Texto Procesado", command = mostar_Stem_Stop, bg="#444654", fg="white", relief="flat", padx=10, pady=5)
# se enpaqueta el botón y se colóca en la ventana. 
boton_StemStop.pack()
# posiciona el bóton en los pixeles de la pantallas
boton_StemStop.place(x=250, y=60) 


# Botón 3 Mostar Matriz -----------------------------------------------------------------------------
def btnMatrizTxt():
    print("Mostró el Texto steam y sin StopWords")
    nombre_txt = "matriz_booleana.csv"
    # Abre txt
    abrir_txt_con_aplicacion_predeterminada(nombre_txt)


# Crear un botón y asociarle la función btnMatrizTxt
boton_MatrizTxt = Button(raiz, text="Mostrar Matriz TF_IDF", command = btnMatrizTxt, bg="#444654", fg="white", relief="flat", padx=10, pady=5)
# se enpaqueta el botón y se colóca en la ventana. 
boton_MatrizTxt.pack()
# posiciona el bóton en los pixeles de la pantallas
boton_MatrizTxt.place(x=428, y=60)   


# Lienzo --------------------------------------------------------------------------------

# Crear un lienzo (Canvas) para contener el panel desplazable
lienzo = tk.Canvas(raiz)
lienzo.config(width=1378, height=650)
lienzo.pack(side="left", fill="both", expand=True)


# Crear un marco que actuará como el panel desplazable
panel = tk.Frame(lienzo)
lienzo.place(x=8, y=220)
panel.configure(bg="#343641")
lienzo.configure(bg="#343641")
lienzo.create_window((510, 0), window=panel, anchor="nw")


# Configurar el lienzo para el desplazamiento
def on_configure(event):
    lienzo.configure(scrollregion=lienzo.bbox("all"))

lienzo.bind("<Configure>", on_configure)

# Botón Consulta -----------------------------------------------------------------------------
# Función para obtener el texto del Entry al presionar el botón
def obtener_texto():
    global matriz_booleana
    
    # Abrir ventana de carga
    ventana_emergente = tk.Toplevel(raiz)
    ventana_emergente.title("Espera un momento")

    # Calcular el centro de la ventana principal
    ancho_ventana_principal = raiz.winfo_width()
    alto_ventana_principal = raiz.winfo_height()
    x_centro = (ancho_ventana_principal - 400) // 2  # Ajusta el ancho de la ventana emergente
    y_centro = (alto_ventana_principal - 200) // 2  # Ajusta el alto de la ventana emergente
    
    # Colocar la ventana emergente en el centro
    ventana_emergente.geometry(f"+{x_centro}+{y_centro}")
    ventana_emergente.configure(bg="lightblue")
    
    etiqueta = tk.Label(ventana_emergente, text="C A R G A N D O...", bg="lightblue", fg="black", font="Arial 20")
    etiqueta.pack(fill="both", expand=True)
    etiqueta.configure(bg="lightblue") 

    raiz.update()

    ''' Obtener consulta '''
    consulta = entry.get()

    print("Obtener consulta")
    print(consulta)

    ''' Aplicar Stopwods y stemming '''
    consulta = tokenizar_stopwords(consulta)
    print(consulta)
    print("Aplicar Stopwods y stemming con exito")
    
    ''' Agregar consulta en Matriz tf-idf '''
    vector_consulta(consulta)
    
    ''' Mostrar resultado '''
    # Procesar Matriz de similitud
    resultado_consulta = calcular_similitud()
    print("Resultado consulta:")
    print(resultado_consulta)

    # Mostramos los documentos en terminal y los guardamos en una lista
    print("sem(q,di):")
    with open('resultado.txt', 'w') as archivo:
        archivo.write(f"Consulta: {consulta}" + "\n")
        archivo.write(f"Resultados: " + "\n")
        i = 0
        for resultado in resultado_consulta:
            i += 1
            print(f"Doc{i}.txt : " + str(resultado))
            archivo.write(f"Doc{i}.txt : ")
            archivo.write(str(resultado))
            archivo.write("\n")
            
    # Guardar indice y ordenar resultados descendente
    diccionario_resultados = {indice+1: valor for indice, valor in enumerate(resultado_consulta)}
    
    # Ordenar resultados descendente
    diccionario_ordenado = dict(sorted(diccionario_resultados.items(), key=lambda item: item[1], reverse=True))
    
    # Asignar indice a resultados y mostrarlos
    for clave, valor in diccionario_ordenado.items():
        print(f"Clave: {clave}, Valor: {valor}")

    # Antes de agregar los nuevos hipervínculos, eliminar los antiguos
    for widget in panel.winfo_children():
        widget.destroy()

    # Agregar contenido al panel
    for documento in diccionario_ordenado.keys():
        documento = str(documento)
        documento_formato= documento.zfill(2)
        # Crea una fuente con subrayado
        fuente_subrayada = font.Font(underline=True)
        # Crear un label con apariencia de hipervínculo
        hipervinculo = tk.Label(panel, text=f"Click para acceder al Documento {documento_formato}", fg="blue", bg="#343641", cursor="hand2", font=fuente_subrayada)
        # Cambiar el color de la letra y el tamaño
        hipervinculo.configure(font=("Arial", 20))
        hipervinculo.pack()
        # Vincular el evento de clic a la función
        hipervinculo.bind("<Button-1>", lambda event, nombre_txt=f"gatos\\gatos\\spiders\\Doc{documento_formato}.txt": abrir_txt_con_aplicacion_predeterminada(nombre_txt))

    # Nombre del txt
    nombre_txt = "resultado.txt"
    # Abre txt
    abrir_txt_con_aplicacion_predeterminada(nombre_txt)

    # Cerrar ventana de carga
    ventana_emergente.destroy()  # Cierra la ventana de carga

# Botón Consulta -----------------------------------------------------------------------------

def borrar_texto_ejemplo(event):
    entry.delete(0, "end")

# Crear un Entry para Buscar
entry = Entry(raiz,  width=80, bg="#444654", fg="white", relief="flat", font=fuente_grande)
entry.insert(0, "       Buscar en el conjunto de Documentos")
entry.bind("<Button-1>", borrar_texto_ejemplo)
entry.pack(pady=30, ipady=30)
entry.place(x=100, y=150)

# Crear un botón para guardar el texto
boton_guardar = Button(raiz, text= " BUSCAR " , command=obtener_texto, bg="#444654", fg="white", relief="flat", padx=35, pady=20)
boton_guardar.pack(pady=50)
boton_guardar.place(x=1200, y=140)

# Info
fuente_pequeña = ("Arial", 8)
label_facts = tk.Label(raiz, text="Free Research. RI Sistem must produce accurate information, powered by team 9. RI Sistem October 20 Version", bg="#343641", fg="#C5C5D2", font=fuente_pequeña)
label_facts.pack()
label_facts.place(x=410, y=15) 

# Ventana principal ------------------------------------------------------------------

# Titulo de la ventana
raiz.title("RI Sistem") 
# Tamaño de la ventana
raiz.geometry("1400x900+200+50")
#raiz.geometry("1400x900")
# Desactivar el redimensionamiento de la ventana
raiz.resizable(False, False)
#Color de la ventana
raiz.config(bg="#343641")  # Establecer el color de fondo en el formato hexadecimal
# Configurar el manejador de eventos para el cierre de la ventana
raiz.protocol("WM_DELETE_WINDOW", on_cerrar_ventana)


# Eventos boton 1
boton_DicMos.bind("<Enter>", cambiar_color1)
boton_DicMos.bind("<Leave>", restaurar_color1)

# Eventos boton 2
boton_StemStop.bind("<Enter>", cambiar_color2)
boton_StemStop.bind("<Leave>", restaurar_color2)

# Eventos boton 3
boton_MatrizTxt.bind("<Enter>", cambiar_color3)
boton_MatrizTxt.bind("<Leave>", restaurar_color3)

# Evento Boton consulta
boton_guardar.bind("<Enter>", cambiar_color4)
boton_guardar.bind("<Leave>", restaurar_color4)

# Ejecucion de Script Web Crawling
# ejecutarScript()
# print("Se ejecuto el script")

# Recabar nombres de txt obtenidos
archivos_txt = [archivo for archivo in os.listdir(
    carpeta_txt) if archivo.endswith('.txt')]

# Cargar bibliotecas de NLTK
biblioteca_nltk()
print("Bibliotecas cargadas")

# Obtener texto tokenizado
texto_tokenizado = obtener_texto_tokenizado()
print("Texto Tokenizado con exito...")


# Crear matriz tf-idf
generar_matriz_booleana()
print("Puedes escribir tú consulta...")


''' Mostrar Ventana '''
#Se visualiza la ventena (Siempre debe de ir al final)
raiz.mainloop()