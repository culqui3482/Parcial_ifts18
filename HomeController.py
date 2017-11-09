from flask import Flask
from flask import render_template, session,flash,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
import csv
import pandas as pd



app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)


#objeto session para verificar que el usuario siga logueado o no.
session={}




#------------- clases generadas---------------------------------


class miformulario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(message = "Tiene que ingresar un Ususario")])
    password = PasswordField('Password',[validators.data_required(message = "Tiene que ingresar una Password")])
    submit = SubmitField('Ingresar')



class ingresoUsuario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(message = "Tiene que ingresar un Ususario")])
    password = PasswordField('Password',[DataRequired(),EqualTo("password1",message = "Tiene que ingresar una Password")])
    password1= PasswordField('Repetir Password', [validators.data_required(message = "Ingresar la misma contrasenia")])
    submit = SubmitField("Enviar")




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




def leerArchivoFar():
        with open('csv/archivoFar.csv','r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return lista




def agregar_usuario(usuario,password):
    with open('csv/usuarios.csv','a') as archivo:
        archivo.write('{},{}\n'.format(usuario,password))
      
#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------



# ...... Muesta la pagina de inicio del programa index......................................

@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')




# ...... Manda a la pagina de logeo donde permite en ingreso al usuario ..............

@app.route('/login',methods=['GET','POST'])
def login():
    miform=miformulario()
    if(miform.validate_on_submit()):
        if (validar(miform.usuario.data,miform.password.data)):
            modelo=leerArchivoFar()
            session['username']= miform.usuario.data
            return (render_template('welcome_table.html',modelo=modelo,nombre=miform.usuario.data))
        else:
            flash("contrasenia incorrecta")
            return redirect(url_for('login'))        
    return (render_template('loginFar.html',form = miform))





# ..... Manda a la pagina lista usuario donde se visualizara todos los usuarios ........

@app.route('/lista',methods=['GET'])
def listaUsuario():
    
    if 'username' in session:
        with open('csv/usuarios.csv','r') as archivo:
            reader= csv.reader(archivo)
            lista= list(reader)
        return render_template('lista_usuarios.html',model=lista)
    else:
        return render_template('error_login.html')




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
    if 'username' in session:
        return render_template('consulta.html')
    else: 
        return render_template('error_login.html') 

@app.route('/nologin',methods=['GET'])
def Nologeado():
    if 'username' not in session:
        return render_template('error_login.html')
    

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('username')
    return render_template('logout.html')
   


#Redireccion de  errores
@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500  

#------------------------------CONSULTAS---------------------------

ARCHIVO_FAR = 'csv/archivoFar.csv'

# class farmaConsulta():
#     def __init__(self,codigo='',nombre='',filtro=''):
#         self.codigo = codigo           
#         self.nombre = nombre
#         self.filtro = filtro


#sort de registros utilizando pandas
def productos_mas_vendidos():
    df = pd.read_csv(ARCHIVO_FAR)
    respuesta = df.groupby(by=['PRODUCTO'], as_index=False).sum()
    respuesta = respuesta.sort_values(by=['CANTIDAD'])
    respuesta = respuesta.tail(5).iloc[::-1]
    return respuesta

def clientes_que_mas_gastaron():
    df = pd.read_csv(ARCHIVO_FAR)
    df['TOTAL'] = df['CANTIDAD']*df['PRECIO']
    respuesta = df.groupby(by=['CLIENTE'], as_index=False).sum()
    respuesta = respuesta.sort_values(by=['TOTAL'])
    respuesta = respuesta.tail(5).iloc[::-1]
    return respuesta

def productos_por_cliente(filtroBusqueda):   
    df = pd.read_csv(ARCHIVO_FAR)
    respuesta = df[df.CLIENTE == filtroBusqueda]
    respuesta = df(['CLIENTE']).str.contains(filtroBusqueda)
    respuesta = respuesta.groupby(by=['CODIGO','PRODUCTO','CANTIDAD','CLIENTE'], as_index=False).sum().iloc[::-1]
    return respuesta

def clientes_por_producto(filtroBusqueda):  
    df = pd.read_csv(ARCHIVO_FAR)
    respuesta = df[df.PRODUCTO == filtroBusqueda]
    #respuesta = df(['PRODUCTO']).str.contains(filtroBusqueda)
    respuesta = respuesta.groupby(by=['CLIENTE','PRODUCTO','CODIGO','CANTIDAD','' ], as_index=False).sum().iloc[::-1]
    return respuesta

#(2)segun la opcion del select guardada en en tipoConsulta se deriva a la funcion correspondiente
def seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda):
    if tipoConsulta == 'pmv':
        respuesta = productos_mas_vendidos()
    elif tipoConsulta == 'cmg':
        respuesta = clientes_que_mas_gastaron()
    elif tipoConsulta == 'ppc':
        respuesta = productos_por_cliente(filtroBusqueda)
    elif tipoConsulta == 'cpp':
        respuesta = clientes_por_producto(filtroBusqueda)   
    else:
         '<div style="text-align: center;"> <p>no hay items para mostrar haga una nueva consulta verificando los datos</p><a href="/consulta" class="btn btn-default">Hacer una nueva consulta</a> </div>'   
    return respuesta

#(1) primero redirecciono a buscar y obtengo los datos del formulario ,
# llamando a seleccionar_tipo_consulta , llamo a la funcion que corresponda segun los datos
# (3)devuelvo el dataFrame a la vista
@app.route('/buscar',methods=['GET','POST'])
def buscar():
    if 'username' in session:
        tipoConsulta = request.form.get('consulta_seleccionada')
        if tipoConsulta == 'pmv'or 'cmg':
            filtroBusqueda = 0
        else:
            filtroBusqueda = str(request.form.get('fitroBusqueda'))
        respuesta = seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda)
    else: 
        return render_template('error_login.html') 
    return respuesta.to_html()
    #return render_template('consulta_respuesta.html',respuesta.to_html())
