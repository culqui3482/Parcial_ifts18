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

def agregar_usuario(usuario,password):
    with open('csv/usuarios.csv','a') as archivo:
        archivo.write('{},{}\n'.format(usuario,password))
      #  linea= str(usuario)+','+str(password)+ '\n' 
      #  archivo.write(linea)




@app.route('/login',methods=['GET','POST'])
def login():
    miform=miformulario()
    if(miform.validate_on_submit()):
        if (validar(miform.usuario.data,miform.password.data)):
            modelo=leerArchivoFar()
            return (render_template('welcome_table.html',modelo=modelo,nombre=miform.usuario.data))
        else:
            return render_template('error_login.html')
            
    return (render_template('loginFar.html',form = miform))



@app.route('/ingreso',methods=['GET','POST'])
def Ingre_usuario():
    form = ingresoUsuario()
    if (form.validate_on_submit()):
        if(form.password.data != form.password1.data):
            return "Los passwords no coinciden!!!"
        else:
            agregar_usuario(form.usuario.data,form.password.data)
            return render_template('ingreso_usuario.html',form=form,mostrar_mje=True)
            
    return render_template('ingreso_usuario.html',form=form)






#Redireccion de  errores
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500  


