from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask import Flask

class miformulario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(message = "Tiene que ingresar un Ususario")])
    password = PasswordField('Password',[validators.data_required(message = "Tiene que ingresar una Password")])
    submit = SubmitField('Ingresar')



class ingresoUsuario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(message = "Tiene que ingresar un Ususario")])
    password = PasswordField('Password',[DataRequired(),EqualTo("password1",message = "Tiene que ingresar una Password")])
    password1= PasswordField('Repetir Password', [validators.data_required(message = "Ingresar la misma contrasenia")])
    submit = SubmitField("Enviar")

class cambioContrasenia(FlaskForm):
    password = PasswordField('Nuevo Password',[DataRequired(),EqualTo("password1",message = "Tiene que ingresar una Password")])
    password1= PasswordField('Repetir Password', [validators.data_required(message = "Ingresar la misma contrasenia")])
    submit = SubmitField("Enviar")
