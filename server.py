from socket import *
from threading import *
import pickle
import DB
# import mysql.connector

clientes = {}
direcciones = {}
DB.CREATE_DB()
DB.CREATE_TABLES()


def configuracion():
    global servidor
    servidor = socket()
    servidor.bind(("", 9999))
    servidor.listen(10)
    print("Esperando conexiones...")
    aceptar_hilo = Thread(target=aceptar_conexiones)
    aceptar_hilo.start()
    aceptar_hilo.join()

def aceptar_conexiones():
    while True:
        cliente_local, direccion_cliente = servidor.accept()
        print("%s:%s conectado. "% direccion_cliente)
        # cliente_local.send(bytes("Bienvenido, ingresa tu nombre y presiona Enter", "utf-8"))
        direcciones[cliente_local] = direccion_cliente
        Thread(target=encargarse_cliente,args=(cliente_local,)).start()

def encargarse_cliente(cliente):
    while True:
        opcion = cliente.recv(1024).decode("utf-8")

        if opcion == 'login':
            print("login")
            user_info =  cliente.recv(1024)
            user_info = pickle.loads(user_info)
            result = DB.SEARCH_USER(user_info[0], user_info[1])

            if result is None:
                cliente.send(bytes("error", "utf-8"))
            else:
                cliente.send(bytes("exito", "utf-8"))
                #envia el nombre de usuario y level
                result = [result[1], result[3]]
                data_string = pickle.dumps(result)
                cliente.send(data_string)

        if opcion == 'registrar':
            print("registrar cliente")
            client_info =  cliente.recv(1024)
            client_info = pickle.loads(client_info)
            DB.CREATE_CLIENT(client_info[0], client_info[1])

        if opcion == 'editar':
            print("editar")
            user_edit =  cliente.recv(1024)
            user_edit = pickle.loads(user_edit)
            if user_edit[1] == '':
                DB.UPDATE_USER(user_edit[0], user_info[1])
            else:
                DB.UPDATE_USER(user_edit[0], user_edit[1])

        if opcion == "listar_usuarios":
            print("listar usuarioss")
            result = DB.SELECT_USERS()
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        # nombre = cliente.recv(1024).decode("utf-8")
        # bienvenido = "Bienvenido %s! si quieres salir, escribe {salir}." %nombre
        # cliente.send(bytes(bienvenido, "utf-8"))
        # mensaje = "%s se ha unido al chat." % nombre
        # broadcast(bytes(mensaje, "utf-8"))
        # clientes[cliente] = nombre
        # while True:
        #     mensaje = cliente.recv(1024)
        #     if mensaje != bytes("{salir}", "utf-8"):
        #         # guardar_mensaje(nombre, mensaje)
        #         broadcast(mensaje, nombre+": ")
        #     else:
        #         del clientes[cliente]
        #         broadcast(bytes("%s ha salido del chat." % nombre, "utf-8"))
        #         break

def broadcast(mensaje, prefix=""):
    for sock in clientes:
        sock.send(bytes(prefix, "utf-8")+mensaje)

def guardar_mensaje(nombre,mensaje):
    conexion = mysql.connector.connect(user="root", password="", host="localhost", database="chat")
    cursor = conexion.cursor()
    sql = "INSERT INTO comunicaciones(usuario, mensaje)VALUES(%s,%s)"
    parametros = (str(nombre), str(mensaje))
    cursor.execute(sql,parametros)
    conexion.commit()
    conexion.close

if __name__ == "__main__":
    configuracion()
