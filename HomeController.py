from flask import Flask
from flask import render_template,session,flash,redirect,url_for,request
#from flask_wtf import FlaskForm
#from wtforms import *
#from wtforms.validators import *
from flask_bootstrap import Bootstrap
import csv
#import pandas as pd
from formularios import miformulario,ingresoUsuario
from consultas import productos_mas_vendidos,clientes_que_mas_gastaron,productos_por_cliente,clientes_por_producto,seleccionar_tipo_consulta

app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)
       

#verificar si el usuario esta registrado
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

archivoFar = 'csv/archivoFar.csv'  

def leerArchivoFar():
        with open(archivoFar,'r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return lista

def agregar_usuario(usuario,password):
    with open('csv/usuarios.csv','a') as archivo:
        encontrado = False
            for linea in archivo:
                lista= linea.split(",")
                usuario=lista[0].strip()
                password=lista[1].strip()
                if (usuario == usuario):
                    if (password== password):
                        encontrado=True
        if encontrado = False:
              archivo.write('{},{}\n'.format(usuario,password))
        elif encontrado = True:
              mensaje = 'El usuario ya se encuentra registrado'
              return render_template('ingreso_usuario.html', mensaje = mensaje)
              

# ...... Muesta la pagina de inicio del programa index......................................

@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    usuario_autenticado=('username' in session)
    return render_template('index.html',usuario_autenticado=usuario_autenticado)


# ...... Manda a la pagina de logeo donde permite en ingreso al usuario ..............

@app.route('/login',methods=['GET','POST'])
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

@app.route('/lista',methods=['GET'])
def lista():
    usuario_autenticado=('username' in session)
    if usuario_autenticado:
        modelo=leerArchivoFar()
        nombre_usuario=session['username']
        return render_template('welcome_table.html',modelo=modelo,nombre=nombre_usuario,usuario_autenticado=usuario_autenticado)
    else:
        return redirect(url_for('login'))



# ..... Manda a la pagina lista usuario donde se visualizara todos los usuarios ........

@app.route('/listaUsuarios',methods=['GET'])
def listaUsuario():
    usuario_autenticado=('username' in session)
    if usuario_autenticado:
        with open('csv/usuarios.csv','r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return render_template('lista_usuarios.html',model=lista,usuario_autenticado=usuario_autenticado)
    else:
        #return render_template('error_login.html')
        return redirect(url_for('login'))



# ..... Manda a la pagina de registro de usuario donde se puede agregar usuarios nuevos ........

@app.route('/registro',methods=['GET','POST'])
def Ingre_usuario():
    form = ingresoUsuario()
    if (form.validate_on_submit()):
        if(form.password.data != form.password1.data):
            flash("contrasenia incorrecta")
            return render_template('ingreso_usuario.html',form=form,mostrar_mje=True)
        else:
            agregar_usuario(form.usuario.data,form.password.data)
            return render_template('registroexitoso.html',form=form,mostrar_mje=True)
            
    return render_template('ingreso_usuario.html',form=form)

@app.route('/consulta',methods=['GET','POST'])
def consultar():
    usuario_autenticado=('username' in session)
    if usuario_autenticado:
        return render_template('consulta.html',usuario_autenticado=usuario_autenticado)
    else: 
        #return render_template('error_login.html')
        return redirect(url_for('login'))
        
#(1) primero redirecciono a buscar y obtengo los datos del formulario ,
# llamando a seleccionar_tipo_consulta , llamo a la funcion que corresponda segun los datos
# (3)devuelvo el dataFrame a la vista
@app.route('/buscar',methods=['GET','POST'])
def buscar():
    usuario_autenticado=('username' in session)
    if usuario_autenticado:
        tipoConsulta = request.form.get('consulta_seleccionada')
        if tipoConsulta == 'pmv'or 'cmg':
            filtroBusqueda = 0
        else:
            filtroBusqueda = str(request.form.get('fitroBusqueda'))
        respuesta = seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda)
    else: 
        return redirect(url_for('login')) 
    return render_template('consulta_respuesta.html',tabla=respuesta.to_html(classes="table table-bordered table-condensed"),usuario_autenticado=usuario_autenticado)

@app.route('/nologin',methods=['GET'])
def Nologueado():
    if 'username' not in session:
        return render_template('error_login.html')
    

@app.route('/logout',methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logout.html')
    else:
        return redirect(url_for('login'))
#----------------- Validacion de archivos ----------------------------
@app.route('/validararchivo',methods=['GET'])
def validacion_de_datos():
    try:
            with open('csv/archivoFar.csv','r') as archivo:
                reader= csv.reader(archivo)
                datos= list(reader)
                validacion = False

                for indice in datos :
                    if len(indice) != 5 :
                        validacion = True                        
                        raise SalidaError("La cantidad de campos en el archivo es incorecta")

                    
                    if indice['CODIGO'] is None :
                        validacion = True
                  
                    
                    if float(indice['CANTIDAD']) % 1 == 0 :
                        validacion = True
                    else :
                        raise SalidaError("ingrese solo enteros")

                    
                    if float(indice['PRECIO']) % 1 == 0 or float(indice['PRECIO']) % 1 != 0 :
                        validacion = True
                    else:
                        raise SalidaError("El precio debe ser un numero")
            if validacion:
                 return True

    except SalidaError as errores :
        print(errores)
        print("El Archivo contiene errores")
#----------------------------------------------------------------------------

#Redireccion de  errores####
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500  
############################
        
if __name__=='__main__':
    app.run(debug=True)
