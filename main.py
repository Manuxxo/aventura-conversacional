import mysql.connector
import os
import time

id_sala = 1
puntuacion = 0
monedas = 0
id_personaje_sala = 0
inventario = []
objetos_en_sala = []
salas_visitadas = [True, False, False, False, False]  # booleano para comprobar si ya entré en la sala
nombre = ""


# Pongo todas las variables a su valor inicial
def reiniciar():
    global id_sala
    global puntuacion
    global monedas
    global inventario
    global salas_visitadas
    id_sala = 1
    puntuacion = 0
    monedas = 0
    inventario = []
    salas_visitadas = [True, False, False, False, False]


# guardo los datos en la base de datos
def guardar():
    global id_sala
    global puntuacion
    global monedas
    global inventario
    global salas_visitadas
    global nombre
    objetos_guardar = ""
    sala_guardar = ""
    for x in inventario:
        objetos_guardar = objetos_guardar + x + " "  # guardo todos los objetos como varchar separados por espacio
    for x in salas_visitadas:  #
        if not x:
            sala_guardar = sala_guardar + '0 '  # si la sala no fue visitada, es un 0, en caso contrario 1
        else:
            sala_guardar = sala_guardar + '1 '
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    exe = "INSERT INTO partida (puntuacion, idsala, objetos, salavisitada, monedas, nombre) VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (puntuacion, id_sala, objetos_guardar, sala_guardar, monedas, nombre)
    cur.execute(exe, datos)
    mi_conexion.commit()
    cur.close()
    mi_conexion.close()


# pongo las variables globales con los datos guardados
def cargar():
    global id_sala
    global puntuacion
    global monedas
    global inventario
    global salas_visitadas
    global nombre
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT id FROM partida")
    partidas = cur.fetchall()
    cargar_partida = []
    objetos = []
    if partidas is None:
        print("No hay partidas guardadas")
        print(partidas)
        time.sleep(5)
    else:
        print("Dime el id de la partida")
        for x in partidas:
            print(x[0])
        id_cargar = input()
        cur.execute("SELECT objetos,puntuacion,idsala,salavisitada,monedas,nombre FROM partida WHERE id=%s",
                    (id_cargar,))
        records = cur.fetchall()
        for x in records:
            cargar_partida.append(x)
        salas_visitadas = []
        objetos = list(cargar_partida[0][0].split(" "))
        salas = list(cargar_partida[0][3].split(" "))
        for i in salas:
            if i == '0':
                salas_visitadas.append(False)
            elif i == '1':
                salas_visitadas.append(True)
        inventario = objetos
        id_sala = int(cargar_partida[0][2])
        puntuacion = cargar_partida[0][1]
        monedas = cargar_partida[0][4]
        nombre = cargar_partida[0][5]
    cur.close()


# donde defino lo que ve el usuario
def vista_usuario(id_sala_actual):
    limpiar_pantalla()  # limpio pantalla (solo para la consola)
    leer_descripcion_sala(id_sala_actual)
    personajes = personajes_sala(id_sala_actual)
    salidas_posibles = leer_salidas_en_sala(id_sala_actual)
    if personajes is None:
        print("Sala: ", id_sala_actual, " Puntuacion: ", puntuacion, " Monedas: ", monedas)
    elif personajes[0] == 2:
        print("Sala: ", id_sala_actual, " Puntuacion: ", puntuacion, " Personaje en la sala: Tendero   Monedas: ",
              monedas)
    elif personajes[0] == 1:
        print("Sala: ", id_sala_actual, " Puntuacion: ", puntuacion, " Personaje en la sala: Guerrero   Monedas: ",
              monedas)

    print("Salidas: ", *salidas_posibles, sep=" ")


# leo las salidas de cada sala
def leer_salidas_en_sala(id_sala_actual):
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT idsalida from salida WHERE idsala=%s", (id_sala_actual,))
    salidas_posibles = list()
    for salida in cur.fetchall():
        if salida == (1,):  # cada salida tiene un ID, que est asignado a una sala, veo cuál es
            salidas_posibles.append('este')
        elif salida == (2,):
            salidas_posibles.append('sur')
        elif salida == (3,):
            salidas_posibles.append('oeste')
        elif salida == (4,):
            salidas_posibles.append('sur')
        elif salida == (5,):
            salidas_posibles.append('este')
        elif salida == (6,):
            salidas_posibles.append('norte')
        elif salida == (7,):
            salidas_posibles.append('norte')
        elif salida == (8,):
            salidas_posibles.append('oeste')
        elif salida == (9,):
            salidas_posibles.append('este')
    cur.close()
    return salidas_posibles


# leo la descripcion
def leer_descripcion_sala(id_sala):
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT descripcion FROM sala WHERE idsala=%s", (id_sala,))
    for descripcion in cur.fetchall():
        print(descripcion[0])
    mi_conexion.close()


# leo los personajes en la sala
def personajes_sala(id_sala):
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT idpersonaje FROM personaje WHERE idsala=%s", (id_sala,))
    id_personaje_sala = cur.fetchone()
    mi_conexion.close()
    if cur.rowcount > 0:
        return id_personaje_sala
    else:
        return None


# limpio la pantalla
def limpiar_pantalla():
    # Limpia la pantalla de la consola
    time.sleep(5)
    if os.name == 'nt':  # Si es Windows
        _ = os.system('cls')
    else:  # Para los demás (Mac y Linux)
        _ = os.system('clear')


# donde leo las acciones del usuario
def leer_entrada():
    print("\n¿Qué quieres hacer ahora?\n")
    entrada = input()
    entrada_valida = validar_entrada(entrada)
    if not entrada_valida:
        leer_entrada()  # INFORMAR DEL ERROR Y CAMBIAR TODO
    else:
        return entrada


# proceso los verbos de comercio
def procesar_verbos_mercado(entrada, id_sala_actual):
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT idobjeto from objeto WHERE idsala=%s", (id_sala_actual,))
    palanca_no_comprada = False
    objeto_no_comerciable = False
    global monedas
    global inventario
    global puntuacion
    if not id_sala_actual == 4:  # si no es la sala 4 no puede comerciar
        print("No hay nadie con quien comerciar en esta sala")
        return
    else:
        for objeto in cur.fetchall():
            if entrada[0] == 'vender' and entrada[1] == 'candelabro' and 'candelabro' in inventario:
                print("Has vendido el candelabro por 50 monedas de oro")
                monedas += 50
                inventario.remove('candelabro')
                print("Ahora tienes ", monedas, " monedas de oro")
                cur.close()
                return
            elif entrada[0] == 'comprar' and objeto == (8,) and monedas >= 90:
                print("Has comprado una palanca")
                inventario.append('palanca')
                monedas -= 90
                puntuacion += 75
                print("Ahora tienes ", monedas, " monedas de oro")
                print("Has ganador 75 puntos!")
                cur.close()
                return
            elif monedas < 90 and entrada[1] == 'palanca':
                palanca_no_comprada = True
            else:
                objeto_no_comerciable = True

        if palanca_no_comprada:
            print("No tienes dinero para comprar la palanca")
            cur.close()
            return
        elif objeto_no_comerciable:
            print("No puedes comerciar con", entrada[1])
            cur.close()
            return


# proceso los comandos usados
def procesar_comando(entrada):
    global inventario
    if entrada[0] == 'inventario':
        print("En tu inventario tienes: ", *inventario, sep=" ")
        return
    elif entrada[0] == 'nuevo':
        reiniciar()
        main()
    elif entrada[0] == 'guardar':
        guardar()
    elif entrada[0] == 'cargar':
        cargar()


def procesar_ordenes(entrada):
    pass

# dependiendo de que sea la primera palabra, lo mando a hacer una acción u otra
def procesar_entrada(entrada, id_sala_actual):
    if entrada[0] in verbo:
        procesar_verbo(entrada, id_sala_actual)
    elif entrada[0] in ordenes:
        procesar_ordenes(entrada)
    elif entrada[0] in comando:
        procesar_comando(entrada)
    elif entrada[0] in verbosdireccion:
        return procesar_direccion(entrada, id_sala_actual)
    elif entrada[0] in verbosmercado:
        procesar_verbos_mercado(entrada, id_sala_actual)


# los verbos se procesan por separado, checkeando cuál objeto hay en cada sala
def procesar_verbo(entrada, id_sala_actual):
    global inventario
    global objetos_en_sala
    global monedas
    global puntuacion
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT idobjeto from objeto WHERE idsala=%s", (id_sala_actual,))
    if entrada[0] == 'mirar':
        if len(cur.fetchall()) > 0:
            if entrada[1] == 'cuadro':
                print("Puedes ver una llave antigua detrás del cuadro")
                objetos_en_sala.append('llave')
            elif entrada[1] == 'mesa':
                print("Puedes ver un candelabro encima de la mesa")
                objetos_en_sala.append('candelabro')
            else:
                print("No puedes mirar eso acá...")
                return
    elif entrada[0] == 'coger':
        if len(objetos_en_sala) > 0:
            if entrada[1] == 'llave' and 'llave' in objetos_en_sala:
                inventario.append('llave')
                print("Ahora la llave te pertenece...")
            elif entrada[1] == 'candelabro' and 'candelabro' in objetos_en_sala:
                inventario.append('llave')
                print("Tienes un candelabro bonito nuevo")
        elif id_sala_actual == 3:
            if entrada[1] == 'cuchillo' and 'cuchillo' not in inventario:
                print("Buena vista... Ahora tienes un cuchillo afilado")
                inventario.append('cuchillo')
                print("Has ganado 50 puntos!")
                puntuacion += 50

        else:
            print("No hay ningún objeto que puedas coger...")
            return
    elif entrada[0] == 'abrir':
        if 'llave' in inventario and entrada[1] == 'cofre':
            print("Has abierto un cofre antiguo, dentro habían 100 monedas de oro")
            monedas += 100
            print("Ahora tienes ", monedas, " de oro")
        else:
            print("No puedes abrir", entrada[1])
            return
    elif entrada[0] == 'empujar':
        if entrada[1] == 'guerrero' and 'cuchillo' in inventario and id_sala_actual == 3:
            print("Parecía fuerte, pero de un solo empujón se ha caido... Ahora te das cuenta que es de plástico")
            print("Tiene un escudo muy grande, te lo quedas")
            inventario.append("escudo")
            print("Has ganado 50 puntos!")
            puntuacion += 50
        elif entrada[1] == 'guerrero' and 'cuchillo' not in inventario and id_sala_actual == 3:
            print("No deberías hacer eso sin un arma...")
        else:
            print("No puedes empujar ", entrada[1])
    elif entrada[0] == 'usar':
        if entrada[1] == 'cuchillo' and 'cuchillo' in inventario and id_sala_actual == 3:
            print("Parece fuerte, pero el cuchillo rebota en él... Ahora te das cuenta que es de plástico")
            print("Tiene un escudo muy grande, te lo quedas")
            inventario.append("escudo")
            print("Has ganado 50 puntos!")
            puntuacion += 50
        elif entrada[1] == 'cuchillo' and 'cuchillo' not in inventario and id_sala_actual == 3:
            print("No deberías hacer eso sin un arma...")
        else:
            print("No puedes usar ", entrada[1])
    else:
        print("No puedes ", entrada[0], " aquí")
        return
    # cur.close()


# compruebo si la sala fue visitada
def sala_visitada(idsalida):
    global salas_visitadas
    global puntuacion
    if not salas_visitadas[idsalida]:
        print("Has entrado en una habitación nueva! Ganas 100 puntos")
        puntuacion += 100
        salas_visitadas[idsalida] = True


# para cambiar de sala, recibe la dirección y devuelve la sala que es, comprobando si la sala tiene ese ID
def procesar_direccion(entrada, id_sala_actual):
    global puntuacion
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT idsalida from salida WHERE idsala=%s", (id_sala_actual,))  # TODO CAMBIAR Y USAR CON LA FUNCIÓN
    for salida in cur.fetchall():
        if salida == (1,) and entrada[1] == 'este':
            cur.close()
            sala_visitada(2)
            return 2
        elif salida == (2,) and entrada[1] == 'sur':
            cur.close()
            sala_visitada(3)
            return 3
        elif salida == (3,) and entrada[1] == 'oeste':
            cur.close()
            return 1
        elif salida == (4,) and entrada[1] == 'sur':
            cur.close()
            sala_visitada(4)
            return 4
        elif salida == (5,) and entrada[1] == 'este':
            cur.close()
            sala_visitada(5)
            return 5
        elif salida == (6,) and entrada[1] == 'norte':
            cur.close()
            return 1
        elif salida == (7,) and entrada[1] == 'norte':
            cur.close()
            sala_visitada(2)
            return 2
        elif salida == (8,) and entrada[1] == 'oeste':
            cur.close()
            sala_visitada(2)
            return 2
        elif salida == (9,) and entrada[1] == 'este':
            if not 'palanca' in inventario:
                print("No puedes abrir esta puerta... Parece que se necesita una palanca...")
            elif not 'escudo' in inventario and 'palanca' in inventario:
                print("Notas mucha radiación fuera... Pero ya es tarde")
                print("Quizás un  escudo te hubiese servido...")
                return 10
            elif 'escudo' in inventario and 'palanca' in inventario:
                print("Consigues abrir la puerta y protegerte de la radiación")
                puntuacion += 1000
                cur.close()
                return 9
    cur.close()
    return 0


# compruebo si tiene un record mayor
def comprobar_record(puntuacion, nombre):
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("SELECT puntuacion from record")
    puntos = cur.fetchone()
    print(puntos)
    if not puntos:
        cur.execute("INSERT INTO record (idjugador, puntuacion, nombrejugador) VALUES (1, %s, %s)",
                    (puntuacion, nombre))
        mi_conexion.commit()
    else:
        if puntuacion > puntos[0]:
            insertar = (nombre, puntuacion)
            exe = "UPDATE record SET nombrejugador=%s, puntuacion=%s WHERE idjugador=1"
            cur.execute(exe, insertar)
            mi_conexion.commit()
            print("ENHORABUENA, HAS HECHO EL NUEVO RECORD CON LA PUNTUACIÓN ",puntuacion)
    cur.close()
    mi_conexion.close()


# conexión a la base de datos
def conexion_bd():
    return mysql.connector.connect(host='localhost', user='root', passwd='admin', db='juego')


# guardo cada partida cuando se gana
def guardar_jugador(puntuacion, nombre):
    mi_conexion = conexion_bd()
    cur = mi_conexion.cursor()
    cur.execute("INSERT INTO jugador(nombre, puntuacion) VALUES (%s, %s)", (nombre, puntuacion))
    mi_conexion.commit()
    mi_conexion.close()


def main():
    global puntuacion
    global id_sala
    global nombre
    nombre = input("Dime tu nombre: ")
    while id_sala < 9:  # 9 para ganar, 10 para morir
        vista_usuario(id_sala)
        entrada = leer_entrada()
        lista = list(entrada.split(" "))
        id_sala_nueva = procesar_entrada(lista, id_sala)
        if id_sala_nueva == 0:
            print("No hay ninguna puerta en el", lista[1])  # compruebo si la sala devuelta existe, sino vuelve
        else:
            if id_sala_nueva is not None:
                id_sala = id_sala_nueva
                id_sala_nueva = None
    if id_sala == 9:
        print("VICTORIA")
        print("Puntuación total: ", puntuacion)
        comprobar_record(puntuacion, nombre)
        guardar_jugador(puntuacion, nombre)
    elif id_sala <= 10:
        print("Has muerto")
        print("DERROTA")


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------

# PROCESADO Y VALIDACION DE LA ENTRADA

# futuros tókens
verbo = ['dar', 'abrir', 'cerrar', 'coger', 'hablar', 'mirar', 'usar', 'empujar', 'tirar']
verbosdireccion = ['ir']
comando = ['inventario', 'nuevo', 'guardar', 'cargar', 'mapa', 'ayuda']
objeto = ['llave', 'cofre', 'candelabro', 'pistola', 'cuchillo', 'pan', 'agua', 'palanca', 'mesa', 'cuadro']
personajes = ['mago', 'guerrero', 'doncella', 'tendero']
conjunciones = ['a', 'con']
verbosmercado = ['comprar', 'vender']
ordenes = ['si', 'no']
direccion = ['norte', 'sur', 'este', 'oeste']

# reglas grámaticales

procesoverbos = ['objeto', 'personaje', 'conjuncion', 'comando']
procesodireccion = ['norte', 'sur', 'este', 'oeste']
procesoconjuncion = ['personaje', 'objeto']
procesospersonaje = ['conjuncion', '']
procesosverbosmercado = ['objeto']
procesoobjeto = ['conjuncion']
procesopalabrafinal = ['personaje', 'objeto', 'direccion', 'ordenes', 'comando']


# compruebo que todas las palabras esten dentro de los tokens

def validacionsintaxis(lista):
    for i in lista:
        if i in verbo or i in personajes or i in comando or i in verbosdireccion or i in objeto or i in conjunciones or i in verbosmercado or i in ordenes or i in direccion:
            return True
        else:
            return False


# compruebo que la frase tenga sentido semanticamente

def validadcionsemantica(lista):
    token = []
    # creo la lista de token

    for i in lista:
        if i in verbo:
            token.append('verbo')
        elif i in comando:
            token.append('comando')
        elif i in verbosdireccion:
            token.append('verbosdireccion')
        elif i in objeto:
            token.append('objeto')
        elif i in conjunciones:
            token.append('conjuncion')
        elif i in verbosmercado:
            token.append('verbosmercado')
        elif i in ordenes:
            token.append('ordenes')
        elif i in direccion:
            token.append('direccion')
        elif i in personajes:
            token.append('personaje')
    longitud = len(token)
    contador = 1

    # primer token
    # no puede ser un objeto, direccion, personaje o conjuncion

    if token[contador - 1] == 'objeto':
        correcto = False
        return correcto
    if token[contador - 1] == 'direccion':
        correcto = False
        return correcto
    if token[contador - 1] == 'personaje':
        correcto = False
        return correcto
    if token[contador - 1] == 'conjuncion':
        correcto = False
        return correcto

    # del segundo token al final
    #

    while contador < longitud - 1:
        if token[contador] == 'verbo':
            if not token[contador + 1] in procesoverbos:
                correcto = False
                return correcto
        elif token[contador] == 'ordenes':
            if longitud > 1:
                correcto = False
                return correcto
            else:
                correcto = False
                return correcto
        elif token[contador] == 'verbosmercado':
            if token[contador + 1] in procesosverbosmercado:
                correcto = True
                return correcto
            else:
                correcto = False
                return correcto
        elif token[contador] == 'personaje':
            if not token[contador + 1] in procesospersonaje:
                correcto = False
                return correcto
        elif token[contador] == 'verbosdireccion':
            if not token[contador + 1] in direccion:
                correcto = False
                return correcto
        elif token[contador] == 'objeto':
            if not token[contador + 1] in procesoobjeto:
                correcto = False
                return correcto
        elif token[contador] == 'conjuncion':
            if not token[contador + 1] in procesoconjuncion:
                correcto = False
                return correcto
        elif token[contador] == 'direccion':
            if longitud > 2:
                correcto = False
                return correcto
            else:
                correcto = True

        contador = contador + 1

    if len(token) == 1:
        if token[contador - 1] in procesopalabrafinal:
            return True
        else:
            return False
    else:
        if token[contador] in procesopalabrafinal:
            return True
        else:
            return False


def validar_entrada(entrada):
    lista = list(entrada.split(" "))
    correcto_sintaxis = validacionsintaxis(lista)
    if correcto_sintaxis:
        correcto_semantica = validadcionsemantica(lista)
        if correcto_semantica:
            return True
        else:
            return False
    else:
        return False


main()
