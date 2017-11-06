from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap

import ConsultasController 
import csv

app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)

class miformulario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(message = "Tiene que ingresar un Ususario")])
    password = PasswordField('Password',[validators.data_required(message = "Tiene que ingresar una Password")])
    submit = SubmitField('Ingresar')

class ingresoUsuario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(message = "Tiene que ingresar un Ususario")])
    password = PasswordField('Password',[DataRequired(),EqualTo("password1",message = "Tiene que ingresar una Password")])
    password1= PasswordField('Repetir Password', [validators.data_required(message = "Ingresar la misma contraseña")])
    submit = SubmitField("Enviar")

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

def leerArchivoFar():
        with open('csv/archivoFar.csv','r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return lista

def leerArchiUsu():
        with open('csv/usuarios.csv','r') as archivo:
            reader= csv.reader(archivo)
            leer= list(reader)
        return leer


def agregar_usuario(usuario,password):
    with open('csv/usuarios.csv','a') as archivo:
        archivo.write('{},{}\n'.format(usuario,password))
      #  linea= str(usuario)+','+str(password)+ '\n' 
      #  archivo.write(linea)

@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    miform=miformulario()
    if(miform.validate_on_submit()):
        if (validar(miform.usuario.data,miform.password.data)):
            modelo=leerArchivoFar()
            #session["UserKey"] = miform.usuario.data
            return (render_template('welcome_table.html',modelo=modelo,nombre=miform.usuario.data))
        else:
            return render_template('error_login.html')
            
    return (render_template('loginFar.html',form = miform))

@app.route('/listausuario',methods=['GET','POST'])
def listaUsuario():
    listUsu=leerArchiUsu()
    if(miform.validate_on_submit()):
        if (validar(listUsu.usuario.data,listUsu.password.data)):
            modelo1=leerArchivoFar()
            #session["UserKey"] = miform.usuario.data
            return (render_template('lista_usuarios.html',modelo1=modelo1,nombre=listUsu.usuario.data,password=listUsu.password.data))



@app.route('/registro',methods=['GET','POST'])
def Ingre_usuario():
    form = ingresoUsuario()
    if (form.validate_on_submit()):
        if(form.password.data != form.password1.data):

            return "Los passwords no coinciden!!!"
        else:
            agregar_usuario(form.usuario.data,form.password.data)
            return render_template('ingreso_usuario.html',form=form,mostrar_mje=True)
            
    return render_template('ingreso_usuario.html',form=form)

'''@app.route('/logout')
def logout():
    session.pop('UserKey', None)
    return render_template('index.html')'''







#Redireccion de  errores
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500  



if(__name__ == '__main__'):
    app.run(debug=True,host='0.0.0.0')
