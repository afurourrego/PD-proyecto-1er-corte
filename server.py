from socket import *
from threading import *
import pickle
import DB

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
            result = DB.SEARCH_USER_LOGIN(user_info[0], user_info[1])

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
            print("listar usuarios")
            result = DB.SELECT_USERS()
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        if opcion == "buscar_usuarios":
            print("buscar usuarios")
            filtro = cliente.recv(1024).decode("utf-8")
            result = DB.SELECT_USERS_FILTER(filtro)
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        if opcion == "eliminar_usuario":
            print("eliminar usuario")
            user_code = cliente.recv(1024).decode("utf-8")
            DB.DELETE_USER(user_code)

        if opcion == "crear_usuario":
            print("crear usuario")
            user_new =  cliente.recv(1024)
            user_new = pickle.loads(user_new)
            DB.CREATE_USER(user_new[0], user_new[1], user_new[2])

        if opcion == "listar_productos":
            print("listar productos")
            result = DB.SELECT_PRODUCTOS()
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        if opcion == "buscar_productos":
            print("buscar productos")
            filtro = cliente.recv(1024).decode("utf-8")
            result = DB.SELECT_PRODUCTOS_FILTER(filtro)
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        if opcion == "eliminar_producto":
            print("eliminar producto")
            producto_code = cliente.recv(1024).decode("utf-8")
            DB.DELETE_PRODUCTO(producto_code)

        if opcion == "crear_producto":
            print("crear producto")
            producto_new =  cliente.recv(1024)
            producto_new = pickle.loads(producto_new)
            DB.CREATE_PRODUCTO(producto_new[0], producto_new[1], producto_new[2])

        if opcion == 'editar_producto':
            print("editar producto")
            producto_edit =  cliente.recv(1024)
            producto_edit = pickle.loads(producto_edit)
            DB.UPDATE_PRODUCTO(producto_edit[0], producto_edit[1], producto_edit[2], producto_edit[3])

if __name__ == "__main__":
    configuracion()
