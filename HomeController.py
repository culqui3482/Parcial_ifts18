from flask import Flask
from flask import render_template,session,flash,redirect,url_for,request,send_file,redirect
from flask_bootstrap import Bootstrap
import csv
from formularios import miformulario,ingresoUsuario,cambioContrasenia #importas del formularios.py
from consultas import productos_mas_vendidos,clientes_que_mas_gastaron,productos_por_cliente,clientes_por_producto,seleccionar_tipo_consulta #importas de consultas.py
from datetime import datetime, date, time, timedelta # importamos las fechas y calendario...
import calendar


app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)
       

#--------validacion de usuario------------
def validar(user,passw):
        with open("csv/usuarios.csv",'r') as archivo:
            encontrado = False
            for linea in archivo:
                lista= linea.split(",")
                usuario=lista[0].strip()
                password=lista[1].strip()
                if (usuario == user):
                    if (password== passw):
                        encontrado=True
        return encontrado

#--------- Lectura de archivoFarma ---------        
def leerArchivoFar():
        with open('csv/archivoFar.csv','r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return lista

#-------Aca se agrega un nuevo usuario-----------
def agregar_usuario(usuario,password):
    with open('csv/usuarios.csv','a') as archivo:
        archivo.write('{},{}\n'.format(usuario,password))

#-------Aca se cambia la contraseña--------------
def cambiar_contrasenia(usuario,nuevopassword):
    datos=[usuario,nuevopassword]
    with open('csv/usuarios.csv',newline='') as archivo:
        filereader=csv.reader(archivo.readlines())
    with open('csv/usuarios.csv','r+', newline='') as archivo:
        filewriter=csv.writer(archivo)
        for row in filereader:
            #print(row[0],datos[0])
            if row[0]==datos[0]:
                filewriter.writerow(datos)
            else:
                filewriter.writerow(row)
                



# ...... .................................................................................................
# ...... .................................................................................................
# ...... .................................................................................................
# ...... .................................................................................................

#----------- Lleva a la pagina de inicio ------------------------------------
@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    usuario_autenticado=('username' in session)
    return render_template('index.html',usuario_autenticado=usuario_autenticado)

# ....................................................................................................
#---------- Manda a la pagina de login donde permite en ingreso al usuario -----------
# Donde el usuario se tiene que ingresar con su usuario y contraseña, si la contraseña es 
# incorrecta se vizualizara un mensaje de contraseña incorrecta y se tendra ingresar nuevamente....
@app.route('/login',methods=['GET','POST'])#obtener y enviar datos....
def login():
    miform=miformulario()
    usuario_autenticado=('username' in session)

    if(miform.validate_on_submit()):
        if (validar(miform.usuario.data,miform.password.data)):
            session['username']= miform.usuario.data
            return redirect(url_for('lista'))
        else:
            flash("contrasenia incorrecta")
            return redirect(url_for('login'))
    if usuario_autenticado:
        return render_template('yaLogueado.html')
    else:   
        return (render_template('loginFar.html',form = miform))

# .....................................................................................................
#--------- Manda al usuario a la pagina de bienvenida-------------------------------------------------
# Si el usuario a ingresado al sistema .. estara como usuario autenticado... en el cual se le enviara al
# html de welcome_table donde se vizualizara el nombre del usuario y la lista archivoFar
@app.route('/lista',methods=['GET'])#Enviar datos
def lista():
    usuario_autenticado=('username' in session)
    if usuario_autenticado:
        modelo=leerArchivoFar()# lee el csv archivoFar
        nombre_usuario=session['username']
        return render_template('welcome_table.html',modelo=modelo,nombre=nombre_usuario,usuario_autenticado=usuario_autenticado)
    else:
        return redirect(url_for('login'))


# .....................................................................................................
# ------- Manda a la pagina lista usuario donde se visualizara todos los usuarios ---------------------
# si el usuario quiere ver a los usuarios y pass del sistema, tendra en el nav 'usuarios.'
@app.route('/listaUsuarios',methods=['GET'])#Enviar datos
def listaUsuario():#autenticacion del usuario
    usuario_autenticado=('username' in session)
    if usuario_autenticado:
        with open('csv/usuarios.csv','r') as archivo:#apertura del csv lista de usuario
            reader= csv.reader(archivo)
            lista= list(reader)
        return render_template('lista_usuarios.html',model=lista,usuario_autenticado=usuario_autenticado)
    else:
        return redirect(url_for('login'))# si no esta autenticado se ele envia al login..


# .....................................................................................................
# -------Manda a la pagina de registro de usuario donde se podra agregar nuevos usuarios ---------------
# se va ingresar un nombre de usuario nuevo y se tendra que repetir los pass dos veces si el ingreso 
# de usuario es exito se visualizara un html de registro exitoso. si no es asi se visualizara de nuevo 
# el registro.

@app.route('/registro',methods=['GET','POST'])#obtener y enviar datos....
def Ingre_usuario():
    form = ingresoUsuario()# llama a la clase ingresoUsuario de formulario.py
    if (form.validate_on_submit()):
        if(form.password.data != form.password1.data):# verifica el pass ingresado se identico ..
            flash("contrasenia incorrecta")
            return render_template('ingreso_usuario.html',form=form,mostrar_mje=True)
        else:
            agregar_usuario(form.usuario.data,form.password.data)
            return render_template('registroexitoso.html',form=form,mostrar_mje=True)
            
    return render_template('ingreso_usuario.html',form=form)

# .....................................................................................................
# --------Cambio de Contraseña ----------
# al ingresar del sistema el usuario ya validado puede modificar su contraseña.En la parte superior del nav
# estara ubicado una pestaña que indica cambio contraseña, que tan solo pordra colocar la nueva contraseña y 
# repetirla asi se podra cambiar ...

@app.route('/cambiopass',methods=['GET','POST'])#obtener y enviar datos....
def Cambio_pass():
    usuario_autenticado=('username' in session)#autenticacion del usuario
    if usuario_autenticado:
        nombre_usuario=session['username']
        form = cambioContrasenia()
        if (form.validate_on_submit()):
            if(form.password.data != form.password1.data):#compara la contraseña
                flash("contrasenia incorrecta")
                return render_template('nuevopass.html',form=form,mostrar_mje=True)
            else:
                cambiar_contrasenia(nombre_usuario,form.password.data)
                return render_template('registroexitoso.html',form=form,mostrar_mje=True)
                #registro exitoso se creo la nueva contraseña
        return render_template('nuevopass.html',form=form)
    else: 
        return redirect(url_for('login'))



# .....................................................................................................
# -----------------Consultas------------------------
# Aca el usuario podra realizar las consultas solicitas....

@app.route('/consulta',methods=['GET','POST'])#obtener y enviar datos....
def consultar():
    usuario_autenticado=('username' in session)#autenticacion del usuario
    if usuario_autenticado: #direcciona a html consulta..
        return render_template('consulta.html',usuario_autenticado=usuario_autenticado)
    else: 
        return redirect(url_for('login'))


# ..................................................................................................... 
# -------------- buscar consultas--------------------------------      
#(1) primero redirecciono a buscar y obtengo los datos del formulario ,
# llamando a seleccionar_tipo_consulta , llamo a la funcion que corresponda segun los datos
# (3)devuelvo el dataFrame a la vista
@app.route('/buscar',methods=['GET','POST'])#obtener y enviar datos....
def buscar():
    usuario_autenticado=('username' in session)#autenticacion del usuario
    if usuario_autenticado:
        tipoConsulta = request.form.get('consulta_seleccionada')# si la consulta seleccionada es pmv o cmg el filtro de busqueda sera 0
        if tipoConsulta == 'pmv' or tipoConsulta == 'cmg':
            filtroBusqueda = 0
        else:
            filtroBusqueda =str(request.form.get('filtroBusqueda')) # si la consulta es distinta el filtroBusqueda debera recibir un dato para comparar si esta en 
        respuesta = seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda)# el csv asi se podra realizar la vista de la consulta.
    else: 
        return redirect(url_for('login')) 
    return render_template('consulta_respuesta.html',tabla=respuesta.to_html(classes="table table-bordered table-condensed"),usuario_autenticado=usuario_autenticado)


# .....................................................................................................
# ----------Usuario no logeado-----------------------
# envia al error de logeo......
@app.route('/nologin',methods=['GET'])
def Nologueado():
    if 'username' not in session:
        return render_template('error_login.html')
    
# ..................................................................................................... 
# envia al login
@app.route('/logout',methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logout.html')
    else:
        return redirect(url_for('login'))

# .....................................................................................................
#--------- Descarga del csv--------------
# Aca permite descargar las consultas que se realizen como archivos csv, indicando la dia hora y segundos
# 
@app.route('/descargar')
def exportar():
    if 'username' in session: # si esta autenticada
        ahora = datetime.now() #en ahora colocamos el datatime.now el cual nos da la fecha y hora del momento...
        nombrearch = "Resultados_"+str(ahora.year)+str(ahora.month)+str(ahora.day)+"_"+str(ahora.hour)+str(ahora.minute)+str(ahora.second)+".csv" 
        return send_file('descarga.csv', as_attachment=True,attachment_filename=nombrearch)# renombramos al archivo ..
    return render_template('consulta.html')

# .....................................................................................................
# .....................................................................................................        
#----------------Redireccion de  errores -----------------------------
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500  
############################
        
if __name__=='__main__':
    app.run(debug=True)
