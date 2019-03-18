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

if __name__ == "__main__":
    configuracion()
