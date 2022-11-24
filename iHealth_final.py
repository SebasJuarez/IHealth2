#Proyecto 2 Base de Datos
#Sebastian Juarez 21471
#Creación de un porgrama que maneja a los usuarios de IHealth +
import sys
import psycopg2
from datetime import datetime
conn= psycopg2.connect(database="Proyecto2",
    user='postgres',
    password='Fac3viche',
    host='localhost')
conn.autocommit=True

cursor=conn.cursor()

#----------main-----------

def main():
    print("-----Bienvenido----------\nEste es IHealth+ su aplicacion de ejercicios!\n")
    print("Para iniciar, que desea hacer:")
    print("1. Inciciar sesion\n2. Crear una nueva cuenta\n3. Salir")
    opcion1 = input()
    if (opcion1=="1"):
        Inicio()
    if (opcion1 == "2"):
        Crearcuenta()
    if (opcion1 == "3"):
        print("Feliz día!")
        exit()
    else:
        print("numero equivocado")
        main()

#--------cuentas: inicio de sesion y creacion de las cuentas----

def Inicio():
    print("-----Inicio de sesión--------")
    print("Por favor ingrese sus datos: ")
    user=input("Ingrese su numero de usuario: ")
    password = input("Ingrese su contraseña: ")
    cursor.execute("select nombre from usuario where user_id = %s and contra = %s", (user,password))
    existe=cursor.rowcount
    if existe == 1:
        nombre=cursor.fetchone()[0]
        cursor.execute("select estado from suscripcion where user_id = %s ", (user,))
        mem=cursor.fetchone()[0]
        if mem == "activo":
            cursor.execute("select acc_type from usuario where user_id = %s and contra = %s", (user, password))
            acctype=cursor.fetchone()[0]
            print("Bienvenido usuario: "+nombre+" numero: "+user)
            print("Tipo de cuenta: "+acctype)
        
            if acctype != "Miembro":
                Admin()
            
            elif acctype == "Miembro":
                Miembro()
        if mem == "desactivado":
            print("necesita una membresia")
            suscripcion()    
    else:
        print("Este cliente no esta registrado!\nRegresando al inicio:")
        main()

def Crearcuenta():
    print("Gracias por preferirnos!")
    print("Registre algunos datos: ")
    contra1 = input("Escriba una contraseña: ")
    contra2 = input("verifique la contraseña: ")
    if contra1 == contra2:
        contra = contra1
    elif contra1 !=contra2:
        print("Contraseñas diferentes...")
        Crearcuenta()
    nombre=input("Ingrese su nombre: ")
    apellido = input("Ingrese apellido: ")
    edad = input("Ingrese edad (solo numero): ")
    altura = input("Ingrese altura (ej. 1.50): ")
    calorias = input("Cuantas calorias diarias desea quemar?: ")
    peso_act = input("Cual es su pero actual en lb? (ej. 159.2): ")
    admincontra = input("admin? (si no, de un enter): ")
    if admincontra == "admin1":
        acctype = "Admin_1"
    elif admincontra == "admin2":
        acctype = "Admin_2"
    elif admincontra == "admin3":
        acctype = "Admin_3"
    elif admincontra == "admin4":
        acctype = "Admin_4"
    else:
        acctype = "Miembro"
    cursor.execute("insert into usuario (nombre, apellido, edad, altura, calorias, peso_act, contra, acc_type) values (%s, %s, %s, %s, %s, %s, %s, %s)", (nombre, apellido, edad, altura, calorias, peso_act, contra, acctype))
    cursor.execute("select user_id from usuario where nombre=%s and apellido = %s",(nombre,apellido))
    user_id=cursor.fetchone()[0]
    print("cuenta creada exitosamente\nSu numero de usuario (que debe ingresar en el inicio de sesión) es: %s"%(user_id))
    if acctype=="Admin_1":
        print("Se le llevará al inicio de sesión")
        Inicio()
    elif acctype=="Admin_2":
        print("Se le llevará al inicio de sesión")
        Inicio()
    elif acctype=="Admin_3":
        print("Se le llevará al inicio de sesión")
        Inicio()
    elif acctype=="Admin_4":
        print("Se le llevará al inicio de sesión")
        Inicio()
    else:
        suscripcion()

def Admin():
    print("-----Permisos de administrador consedidos------")
    print("-----Menu de administrador------")
    print("Que desea hacer?: ")
    print("1. Modificar instructores\n2. Modificar sesiones\n3. Modificar usuarios\n4. Regresar al inicio")
    opcion1=input()
    if opcion1=="1":
        cont2=input("Escriba su contraseña de admin: ")
        if cont2 == "admin1" or "admin4":
            print("Elija entre las opciones:")
            print("1. Agregar un instructor\n2. Modificar un instructor\n3. Dar de baja a un instructor\n4. Regresar al inicio")
            opcion2=input()
            if opcion2=="1":
                print("Ingrese los datos del instructor a agregar:")
                inst_id = input("Numero de instructor: ")
                inst_nom= input("Nombre: ")
                inst_ape=input("Apellido del instructor: ")
                cursor.execute("insert into instructor (inst_id, inst_nombre, inst_apellido) values (%s, %s, %s)", (inst_id, inst_nom, inst_ape))
                print("Instructor agregado, regresando al menu")
                Admin()
            elif opcion2 =="2":
                instcod=input("Escriba el codigo del instructor que desa modificar: ")
                cursor.execute("select inst_id from instructor where inst_id = %s", (instcod))
                hay=cursor.rowcount
                if hay == 1:
                    inst_nom= input("Nombre: ")
                    nuenom=input("Nuevo nombre de instructor: ")
                    inst_ape=input("Apellido del instructor: ")
                    nueape=input("Nuevo apellido de instructor: ")
                    cursor.execute("update instructor set inst_nombre=%s where inst_nombre=%s", (nuenom,inst_nom))
                    cursor.execute("update instructor set inst_apellido=%s where inst_apellido=%s", (nueape,inst_ape))
                    print("Se ha cambiado exitosamente\nVolviendo al menu")
                    Admin()
                else:
                    print("No existe este instructor\nVolviendo al menu")
                    Admin()
            elif opcion2=="3":
                instcod=input("Escriba el codigo del instructor que desa dar de baja: ")
                cursor.execute("select inst_id from instructor where inst_id = %s", (instcod))
                hay=cursor.rowcount
                if hay == 1:
                    cursor.execute("delete from instructor where inst_id=%s", (instcod))
                    print("Se ha dado de baja exitosamente\nVolviendo al Menu")
                    Admin()
                else:
                    print("No existe este instructor\nVolviendo al menu")
                    Admin()

    if opcion1=="2":
        cont = input("Escriba su contraseña de admin: ")
        if cont == "admin2" or "admin4":
            print("Elija entre las opciones:")
            print("1. Agregar una sesión\n2. Modificar una sesión\n3. Eliminar una sesión\n4. Regresar al inicio")
            opcion2=input()
            if opcion2=="1":
                print("Ingrese los datos de la sesión a agregar:")
                ses_id = input("Numero de la sesión: ")
                ses_desc=input("Descripcion: ")
                ses_dura=input("Duracion de la sesión: ")
                ses_cate=input("Categoria de la sesión: ")
                ses_inst=input("Numero del instructor que la imparte: ")
                cursor.execute("insert into cursos (curso_id, descripcion, duracion, categoria, inst_id) values (%s, %s, %s, %s, %s)", (ses_id, ses_desc, ses_dura, ses_cate, ses_inst))
                print("Sesión agregada, regresando al menu")
                Admin()
            elif opcion2 =="2":
                sescod=input("Escriba el codigo de la sesión que desa modificar: ")
                cursor.execute("select curso_id from cursos where inst_id = %s", (sescod))
                hay=cursor.rowcount
                if hay == 1:
                    nue_dura=input("Duracion de la sesión: ")
                    nue_cate=input("Categoria de la sesión: ")
                    nue_inst=input("Nuevo instructor: ")
                    cursor.execute("update cursos set duracion=%s where curso_id=%s", (nue_dura,sescod))
                    cursor.execute("update cursos set categoria=%s where curso_id=%s", (nue_cate,sescod))
                    cursor.execute("update cursos set inst_id=%s where curso_id=%s", (nue_inst,sescod))
                    print("Se ha cambiado exitosamente\nVolviendo al menu")
                    Admin()
                else:
                    print("No existe esta sesión\nVolviendo al menu")
                    Admin()
            elif opcion2=="3":
                sescod=input("Escriba el codigo de la sesion que desa dar de baja: ")
                cursor.execute("select curso_id from cursos where curso_id = %s", (sescod))
                hay=cursor.rowcount
                if hay == 1:
                    cursor.execute("delete from cursos where curso_id=%s", (sescod))
                    print("Se ha dado de baja exitosamente\nVolviendo al Menu")
                    Admin()
                else:
                    print("No existe esta sesión\nVolviendo al menu")
                    Admin()
        else:
            print("Se necesitan permisos nivel 2 o 4 para este caso\nVolviendo al menu\n")
            Admin()
        
    if opcion1=="3":
        cont3=input("Escirba su contraseña de admin: ")
        if cont3 == "admin3" or "admin4":
            print("Elija entre las opciones:")
            print("1. Cambiar altura\n2. Cambiar peso\n3. Dar de baja\n4. Regresar al inicio")
            opcion2=input()
            if opcion2=="1":
                print("Ingrese algunos datos del usuario:")
                usu_id = input("Numero de usuario: ")
                usudesp=input("Nueva altura: ")
                cursor.execute("update usuario set altura = %s where user_id = %s", (usudesp, usu_id))
                print("Usuario modificado, regresando al menu")
                Admin()
            elif opcion2 =="2":
                usucod1=input("Escriba el codigo del miembro que desa modificar: ")
                cursor.execute("select user_id from usuario where user_id = %s", (usucod1))
                hay=cursor.rowcount
                if hay == 1:
                    print("Ingrese algunos datos del usuario:")
                    usupes=input("Nuevo peso: ")
                    cursor.execute("update usuario set peso_act = %s where user_id = %s", (usupes, usucod1))
                    print("Usuario modificado, regresando al menu")
                    Admin()
                else:
                    print("No existe este usuario\nVolviendo al menu")
                    Admin()
            elif opcion2=="3":
                usucod=input("Escriba el codigo del miembro que desa dar de baja: ")
                cursor.execute("select inst_id from usuario where inst_id = %s", (instcod))
                hay=cursor.rowcount
                if hay == 1:
                    cursor.execute("delete from usuario where inst_id=%s", (usucod))
                    print("Se ha dado de baja exitosamente\nVolviendo al Menu")
                    Admin()
                else:
                    print("No existe este usuario\nVolviendo al menu")
                    Admin()
        else:
            print("Se necesitan permisos nivel 3 o 4 para este caso\nVolviendo al menu\n")
            Admin()
    if opcion1=="4":
        main()

def Miembro():
    print("Este estas son las opciones que se le ofrecen:")
    print("1. Busqueda de sesiones\n2. Consultas de calendario o historial\n3. Estadisticas\n4. Configuracion\n5. volver al inicio")
    opcion=input()
    if opcion=="1":
        busqueda()
    if opcion=="2":
        consultas()
    if opcion=="3":
        estadisticas()
    if opcion=="4":
        configuracion()  
    if opcion=="5":
        main()

def suscripcion():
    print("Para usar estos servicios, debe utilizar seleccionar una suscripcion: ")
    print("1. Oro\n2. Diamante\n3. Realizar la compra\n4. soy cliente anterior")
    opcion3=input("Elija uno para ver una descripción mas detallada: ")
    if opcion3=="1":
        print("Con su suscripción oro, se le ofrecen las sesiones 24/7\ny el prestamo de un smartwatch para el registro del entrenamiento\n(este se debe retornar en caso de baja en el plan) con un contrato mínimo de 12 meses\nEl precio es de Q250.00 mensuales")
        suscripcion()
    if opcion3=="2":
        print("Con su suscripción diamante, se le ofrecen las sesiones 24/7\nUna sesión con nuestra nutricionista 1 vez al mes\ny el regalo de un smartwatch para el registro del entrenamiento\ncon un contrato mínimo de 12 meses\nEl precio es de Q500.00 mensuales")
        suscripcion()
    if opcion3=="3":
        print("-----Compra de suscripcion------")
        opcion4=input("Que tipo de suscripción elíge:\n1. Oro\n2. Diamante\n")
        if opcion4=="1":
            tipo="oro"
            costo="250"
        elif opcion4=="2":
            tipo="diamante"
            costo="500"
        else:
            print("no esta entre las opciones...")
            suscripcion()
        user=input("Numero de usuario (se le asigno al crear la cuenta): ")
        pago=input("Como desea pagar su suscripcion (debito o credito): ")
        estado="activo"
        fecha_init=datetime.today().strftime('%d-%m-%Y')
        fecha_fin=datetime.today().strftime('%d-%m-%Y')
        cursor.execute("insert into suscripcion (user_id, tipo, estado, costo, tipo_pago, fecha_init, fecha_fin) values (%s, %s, %s, %s, %s, %s, %s)", (user, tipo, estado, costo, pago, fecha_init, fecha_fin))
        print("transaccion realizada con exito!\nBienvenido!")
        Miembro()
    if opcion3 == "4":
        user=input("Numero de usuario: ")
        print("desea comprar una nueva membresia?\n1. Si\n2. No")
        opt5=input()
        if opt5 == "1":
            print("entendido, comprando!")
            print("listo, bienvenido/a")
            ac="activo"
            cursor.execute("update suscripcion set estado=%s where user_id=%s", (ac,user))
        if opt5=="2":
            print("Lo sentimos, necesita una suscripcion")
            Inicio()
def configuracion():
            print("-----Configuración de la cuenta-----")
            print("Que desea hacer:")
            print("1. Cambiar contraseña\n2. desactivar la suscripcion\n3. regresar")
            opcion5=input()
            if opcion5=="1":
                usu=input("Escriba el numero de usuario: ")
                antcontra=input("Escriba la anterior contraseña: ")
                cursor.execute("select contra from usuario where user_id = %s", (usu))
                contraant=cursor.fetchone()[0]
                if contraant == antcontra:
                    nuecontra=input("Cual es la nueva contraseña: ")
                    cursor.execute("update usuario set contra=%s where user_id=%s", (nuecontra,usu))
                    print("Contraseña actualizada exitosamente")
                else:
                    print("No coinciden las contraseñas\nVolviendo al menu")
                    configuracion()
                configuracion()
            if opcion5=="2":
                print("Desea desactivar su suscripcion?")
                print("1. si\n2. no")
                opcion51=input()
                if opcion51 =="1":
                    print("Se le extrañará, desactivando cuenta...")
                    usu=input("ingrese el numero de usuario: ")
                    des = "desactivado"
                    cursor.execute("update suscripcion set estado=%s where user_id=%s", (des,usu))
                    print("Cuenta desactivada exitosamente")
                    Inicio()
                if opcion51=="2":
                    configuracion()
            if opcion5=="3":
                Miembro()

def consultas():
    uscod = input("Escriba su numero de usuario: ")
    print("Consultas de:\n1. Calendario\n2. Historial\n3. Asignacion\n4. Regresar")
    opcion3=input()
    if opcion3=="1":
        print("Esto es lo que se tiene en su calendario:")
        cursor.execute("select * from sesiones where user_id = %s", (uscod,))
        lista=cursor.fetchall()
        print(lista)
        consultas()
    if opcion3=="2":
        print("Que desea consultar?\n1. Ultimos cursos tomados\n2. Ultimos instructores recibidos\n3. volver al menu")
        opt9=input()
        if opt9=="1":
            cursor.execute("select distinct s.curso_id, c.descripcion from sesiones s inner join cursos c on s.curso_id = c.curso_id where user_id=%s order by s.curso_id", (uscod))
            lista2=cursor.fetchall()
            print("Estos son los cursos: ")
            print(lista2)
            print("Volviendo al menu")
            consultas()
        if opt9 =="2":
            cursor.execute("select distinct s.inst_id, i.inst_nombre, i.inst apellido from sesiones s inner join intructor i on s.inst_id = i.inst_id where user_id=%s order by s.inst_id", (uscod))
            lista2=cursor.fetchall()
            print("Estos son los instructores: ")
            print(lista2)
            print("Volviendo al menu")
        if opt9=="3":
            print("Volviendo al menu")
            consultas()
    if opcion3=="3":
        asignacion()
    if opcion3=="4":
        Miembro()

def busqueda():
            print("que sesiones desea buscar:")
            print("1. Por categoria\n2. Por instructor\n3. por duracion\n4. Regresar")
            opcion2=input()
            if opcion2=="1":
                print("Estos son los cursos por categoria")
                cursor.execute("select * from cursos order by cursos asc")
                lista=cursor.fetchall()
                print(lista)
                busqueda()
            if opcion2=="2":
                print("Estos son los curos por instructor:")
                cursor.execute("select * from cursos order by inst_id asc")
                lista=cursor.fetchall()
                print(lista)
                busqueda()
            if opcion2=="3":
                print("Estos son los curos por duracion: ")
                cursor.execute("select * from cursos order by duracion asc")
                lista=cursor.fetchall()
                print(lista)
                busqueda()
            if opcion2=="4":
                Miembro()

def asignacion():
    print("Asignar un curso")
    user=input("Ingrese codigo de usuario:")
    curso=input("Ingrese el codigo del curso al cual se quiere asignar: ")
    fecha=datetime.today().strftime('%d-%m-%Y')
    cursor.execute("select inst_id from cursos where curso_id = %s", (curso,))
    ins=cursor.fetchone()
    inst=ins[0]
    cursor.execute("select categoria from cursos where curso_id = %s", (curso,))
    ca=cursor.fetchone()
    categoria=ca[0]
    cursor.execute("select duracion from cursos where curso_id = %s", (curso,))
    du=cursor.fetchone()
    duracion=du[0]
    cursor.execute("insert into sesiones (curso_id, fecha, duracion, inst_id, categoria, user_id) values (%s, %s, %s, %s, %s, %s)", (curso, fecha, duracion, inst, categoria, user))
    print("Se ha asignado correctamente!\nDesea asignar otro?")
    print("1. Si\n2. No")
    opcion31=input()
    if opcion31=="1":
        asignacion()
    if opcion31=="2":
        print("Regresando")
        consultas()

def estadisticas():
    user=input("ingrese el numero de usuario: ")
    print("Que desea ver:\n1. consultas\n2. historial\n3. regresar al menu")
    opt10=input()
    if opt10 == "1":
        consultas()
    if opt10 =="2":
        print("consultas de peso:")
        cursor.execute("select peso_act from usuario where user_id = %s", (user,))
        peso=cursor.fetchall()
        print(peso)
        Miembro()
    if opt10 == "3":
        print("Regresando!")
        Miembro()

main()



    
        