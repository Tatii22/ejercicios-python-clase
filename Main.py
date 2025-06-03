#Biblio campus
    #gestion libros 
        #agregar
        #actualizar 
        #eliminar 
    #prestamo de libros 
        #crear 
    #devolucion de libros 
        #crear 
    #listar libros
    #listar libros prestados 
        #lista solo los libros que no han sido devueltos
    # historial de prestamos 
        #listado 
    #salir 
#realizar en modulos (pendiente)

#libro -> codigo,nombre,autor,editorial.
#prestamo -> fecha.devolucion,nombre,documento 
#historial->[prestamo]

import os
from datetime import datetime, timedelta

def limpiarConsola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    input("Presione enter para continuar")

def enterParaContinuar(mensaje : str = "Enter para continuar..."):
    input(mensaje)

def validarInput(titulo : str, valMin: int = 0, valMax: int = 5):
    while True:
        try:
            rta = int(input(titulo))
            if rta >= valMin and rta <= valMax:
                return rta
            else:
                print(f"Por favor ingrese solo valores permitidos... \nRango de {valMin} a {valMax}")
                enterParaContinuar()
                limpiarConsola()
        except:
            enterParaContinuar("OIGA ESTA MAL, INTENTALO DE NUEVO")

def gestionarLibros(titulo :str):
    limpiarConsola()
    while True:
        encontrado = False
        print(titulo)
        opc = validarInput("Seleccione una opcion: ",valMin=1, valMax=4)
        if opc == 1:
            fields = [
                    {"titulo":"🆔 Ingrese el Codigo del Libro\n", "type": "entero"}, # 0
                    {"titulo":"📖 Ingrese el Nombre del Libro\n", "type": "texto"}, # 1
                    {"titulo":"✍️ Ingrese el Nombre del Autor\n", "type": "texto"}, # 2 
                    {"titulo":"🏢 Ingrese el Nombre del Editorial\n", "type": "texto"}, # 3
                ]
            datos = solicitarDatos(fields)
            nuevoLibro = libro(f'{datos[0]}', datos[1], datos[2], datos[3])
            #Guardamos en bibilioteca
            biblioteca["libros"].append(nuevoLibro)
            print("✅ ¡Libro agregado exitosamente!")
            print(biblioteca["libros"])
            enterParaContinuar()
        elif opc == 2:
            listarLibros()
            codLib = input("🔍 Indica el código del libro que deseas actualizar: ")
            for l in biblioteca["libros"]:
                if l["codigo"] == codLib:
                    print(f"📖 Libro actual: {l}")
                    campos = [
                        {"titulo":"📝 Nuevo nombre del libro: ", "type":"texto"},
                        {"titulo":"✍️ Nuevo autor del libro: ", "type":"texto"},
                        {"titulo":"🏢 Nueva editorial del libro: ", "type":"texto"},
                    ]
                    datos = solicitarDatos(campos)

                    l["nombre"] = datos[0]
                    l["autor"] = datos[1]
                    l["editorial"] = datos[2]
                    print("✅ ¡Libro actualizado exitosamente!")
                    encontrado = True
                    break

            if not encontrado:
                print("❌ Libro no encontrado.")
            enterParaContinuar()
        elif opc == 3:
            listarLibros()
            codElim = input("🗑️  Indica el código del libro que deseas eliminar: ")
            encontrado = False
            cancelado = False
            for l in biblioteca["libros"]:
                if l["codigo"] == codElim:
                    print(f"📖 Libro actual: {l}")
                    confirma = input("⚠️ ¿Estas seguro de eliminarlo? S o N\n")
                    if confirma.upper() == "N":
                        print("❎ Se cancela eliminación")
                        cancelado = True
                        break
                    biblioteca["libros"].remove(l)
                    print("✅ Libro eliminado.")
                    encontrado = True
                    break
            if not encontrado and not cancelado:
                print("❌ Libro no encontrado.")
            enterParaContinuar()  
        elif opc == 4:
            enterParaContinuar("🔙 Vuelve al menu principal")
            break
        else:
            enterParaContinuar("❗ Opción inválida. Intenta de nuevo.")
        limpiarConsola()

def solicitarDatos(campos:list):
    respuesta = []
    for c in campos:
        if c["type"] == "entero":
            respuesta.append(validarInput(c["titulo"], 1 , 100))
        elif c["type"] == "texto":
            respuesta.append(input(c["titulo"]))
    return respuesta

def libro(codigo: str, nombre: str, autor: str, editorial: str):
    return {"codigo": codigo, "nombre": nombre, "autor": autor, "editorial": editorial}

def listarLibros():
    print("\n📚 LISTADO DE LIBROS\n")
    for libro in biblioteca["libros"]:
        print(f"📖 {libro['codigo']} {libro['nombre']} {libro['autor']} {libro['editorial']}")
    enterParaContinuar()

def prestamo(codigo: str, nombre: str, documento: str, fechaDevolucion: datetime):
    return {"codigo": codigo, "nombre": nombre, "documento": documento, "fechaDevolucion": fechaDevolucion}

def verificacionPrestamo(codigo):
    for prestamo in biblioteca["prestamos"]:
        if prestamo["codigo"] == codigo:
            return True  
    return False  

def verificacionExistencia(codigo):
    for l in biblioteca["libros"]:
        if l["codigo"] == codigo:
            return True
    return False

def registrarPrestamo():
    listarLibros()
    codPrestamo = input("🔍 Indica el código del libro que deseas solicitar prestamo: ")
    if not verificacionExistencia(codPrestamo):
        print("❗ El código ingresado no corresponde a ningún libro registrado.")
        enterParaContinuar()
        return
    if verificacionPrestamo(codPrestamo):
        print("📕 El libro ya fue prestado.")
        enterParaContinuar()
    else:
        print(f"📗 El libro está disponible para préstamo.")
        datosPrestamo = [
                    {"titulo":"Ingresa tu nombre\n", "type": "texto"}, # 0
                    {"titulo":"Ingresa tu numero de documentos\n", "type": "texto"}, # 2 
                ]
        info = solicitarDatos(datosPrestamo)
        fecha_devolucion = datetime.now() + timedelta(days=15)
        registroPrest = prestamo(codPrestamo, info[0], info[1], fecha_devolucion)
        biblioteca["prestamos"].append(registroPrest)
        print("✅ Préstamo registrado con fecha de devolución:", fecha_devolucion.strftime("%d/%m/%Y"))
        enterParaContinuar()
        
def devolverLibro():
    codLibro = input("📦 Codigo del libro a devolver: ")
    encontrado = False

    for i in biblioteca["prestamos"]:
        if i["codigo"] == codLibro:
            biblioteca["prestamos"].remove(i)
            i["fechaDevolucion"] = datetime.now() 
            biblioteca["historial"].append(i)
            input(f"✅ El libro ha sido devuelto por {i['nombre']} el {i['fechaDevolucion'].strftime('%d/%m/%Y')}")
            encontrado = True
            break

    if not encontrado:
        print("❌ El libro no estaba registrado como prestado.")

def listarPrestamo():
    if not biblioteca["prestamos"]:
        print("❎ No hay libros prestados.")
    else:
        print("\n📚 LIBROS PRESTADOS ACTUALMENTE\n")
        for h in biblioteca["prestamos"]:
            print(f"Código: {h['codigo']} | Usuario: {h['nombre']} | Documento: {h['documento']} | Fecha devolución: {h['fechaDevolucion'].strftime('%d/%m/%Y')}")
    enterParaContinuar()

def listarHistorial():
    if not biblioteca["historial"]:
        print("❌ No hay libros en el historial.")
    else:
        print("\n📚 HISTORIAL PRESTAMOS\n")
        for h in biblioteca["historial"]:
            print(f"Código: {h['codigo']} | Usuario: {h['nombre']} | Documento: {h['documento']} | Fecha devolución: {h['fechaDevolucion'].strftime('%d/%m/%Y')}")
    enterParaContinuar()


menu = """
,---.    ,---.    .-''-.  ,---.   .--.  ___    _ 
|    \  /    |  .'_ _   \ |    \  |  |.'   |  | |
|  ,  \/  ,  | / ( ` )   '|  ,  \ |  ||   .'  | |
|  |\_   /|  |. (_ o _)  ||  |\_ \|  |.'  '_  | |
|  _( )_/ |  ||  (_,_)___||  _( )_\  |'   ( \.-.|
| (_ o _) |  |'  \   .---.| (_ o _)  |' (`. _` /|
|  (_,_)  |  | \  `-'    /|  (_,_)\  || (_ (_) _)
|  |      |  |  \       / |  |    |  | \ /  . \ /
'--'      '--'   `'-..-'  '--'    '--'  ``-'`-'' 

1. 📘 Gestión Libros  
2. 🤝 Préstamo De Libros  
3. 🔄 Devolución De Libros  
4. 📗 Listar Libros  
5. 📕 Listar Libros Prestados  
6. 📓 Historial De Préstamos  
7. ❌ Salir  


"""
subMenu = """
    📚 MENU - Gestión De Libros  
    1. ➕ Agregar  
    2. 📝 Actualizar  
    3. 🗑️  Eliminar  
    4. 🔙 Salir  
"""
biblioteca = {
    "libros":[],
    "prestamos":[],
    "historial":[]
}


while True:
    print(menu)
    opc = validarInput("Seleccione una opcion: \n", valMin=1, valMax=7)
    if opc == 1:
        gestionarLibros(titulo=subMenu)
    elif opc == 2:
        registrarPrestamo()
    elif opc == 3:
        devolverLibro()
    elif opc == 4:
        listarLibros()
    elif opc == 5:
        listarPrestamo()
    elif opc == 6:
        listarHistorial()
    elif opc == 7:
        enterParaContinuar("¡Chaooo!")
        break
    else:
        enterParaContinuar("OIGA ESTA MAL, INTENTALO DE NUEVO")
    limpiarConsola()