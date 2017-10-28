from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
import csv


#login
class AdminBD():
    def __init__(self,ruta=''):
        self.rutaArchivo=ruta

    def leerArchivoFar(self):
        with open(self.rutaArchivo,'r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return lista
            
   
    def validar(self, user,passw):
        with open(self.rutaArchivo,'r') as archivo:
            encontrado = False
            for linea in archivo:
                lista= linea.split(",")
                usuario=lista[0].strip()
                password=lista[1].strip()
                if (usuario == user):
                    if (password== passw):
                        encontrado=True
        return encontrado
    '''def agregar(self,usuario,password):
        archivo = open(self.rutaArchivo,'a')
        try:
            linea= str(usuario)+','+str(password)+'\n'
            archivo.write(linea)
        finally:
            archivo.close()'''

app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)

class FormularioLogin(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/login',methods=['GET','POST'])
def login():
    miform= FormularioLogin()
    
    if(miform.validate_on_submit()):
        aut= AdminBD('usuarios.csv')
        if (aut.validar(miform.name.data,miform.password.data)):
            mostrar_tabla=AdminBD('archivoFar.csv')
            modelo=mostrar_tabla.leerArchivoFar()
            
            return (render_template('welcome_table.html',modelo=modelo,nombre=miform.name.data))
        else:
            return render_template('error_login.html')
            
    return (render_template('loginFar.html',form = miform))







if(__name__ == '__main__'):
    app.run(debug=True,host='0.0.0.0')

