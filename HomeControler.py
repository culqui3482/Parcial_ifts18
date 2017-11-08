from flask import Flask
from flask import render_template, session,flash,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
#import pandas as pandas
import ConsultasController2
import csv
import pandas as pandas



app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)



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

<<<<<<< HEAD

=======
def leerArchiUsu():
        with open('csv/usuarios.csv','r') as archivo:
            reader= csv.reader(archivo)
            leer= list(reader)
        return leer
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95


def agregar_usuario(usuario,password):
    with open('csv/usuarios.csv','a') as archivo:
        archivo.write('{},{}\n'.format(usuario,password))
<<<<<<< HEAD
      
#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------
=======
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95

@app.route('/index',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


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
<<<<<<< HEAD
            session['username']= miform.usuario.data
=======
            #session["UserKey"] = miform.usuario.data
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
            return (render_template('welcome_table.html',modelo=modelo,nombre=miform.usuario.data))
        else:
            flash("contrasenia incorrecta")
            return redirect(url_for('login'))        
    return (render_template('loginFar.html',form = miform))

@app.route('/listausuario',methods=['GET','POST'])
def listaUsuario():
    listUsu=leerArchiUsu()
    if(miform.validate_on_submit()):
        if (validar(listUsu.usuario.data,listUsu.password.data)):
            modelo1=leerArchivoFar()
            #session["UserKey"] = miform.usuario.data
            return (render_template('lista_usuarios.html',modelo1=modelo1,nombre=listUsu.usuario.data,password=listUsu.password.data))





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
<<<<<<< HEAD
            flash("contrasenia incorrecta")
            return render_template('ingreso_usuario.html',form=form,mostrar_mje=True)

            #return redirect(url_for('login')) 

            #return "Los passwords no coinciden!!!"
=======

            return "Los passwords no coinciden!!!"
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
        else:
            agregar_usuario(form.usuario.data,form.password.data)
            return render_template('registroexitoso.html',form=form,mostrar_mje=True)
            
    return render_template('ingreso_usuario.html',form=form)

<<<<<<< HEAD
@app.route('/consulta',methods=['GET','POST'])
def consultar():
    if 'username' in session:
    #miform= formularioConsulta()   
    #if miform.validate_on_submit():
        return render_template('consulta.html')
    else: 
        return render_template('error_login.html') 
=======
'''@app.route('/logout')
def logout():
    session.pop('UserKey', None)
    return render_template('index.html')'''


>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95

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



<<<<<<< HEAD



































    

#------------------------------CONSULTAS
'''
ARCHIVO_FAR = 'csv/archivoFar.csv'
TABLA1 = pandas.read_csv(ARCHIVO_FAR)

colCodigo = TABLA1['CODIGO']
colProducto = TABLA1['PRODUCTO']
colCliente = TABLA1['CLIENTE']
colCantidad = TABLA1['CANTIDAD']
colPrecio = TABLA1['PRECIO']

# class farmaConsulta():
#     def __init__(self,codigo='',nombre='',filtro=''):
#         self.codigo = codigo           
#         self.nombre = nombre
#         self.filtro = filtro

def productos_mas_vendidos():
    #respuesta = TABLA1.groupby(colProducto,as_index=False)['CANTIDAD'].nlargest(7).as_matrix([colCodigo, colProducto, colCantidad])
    ##variante por si no anda
    df = pandas.read_csv(ARCHIVO_FAR)
    #df = df[df['CANTIDAD']]
    #respuesta = respuesta.groupby(colProducto)
    #respuesta = respuesta.as_matrix([colCodigo, colProducto, colCantidad])
    return render_template('consulta_respuesta.html',show = df.to_html())
    

def clientes_que_mas_gastaron():
    col_gasto_total = TABLA1['GASTO_TOTAL']
    col_gasto_total = (colCantidad * colPrecio)
    respuesta = TABLA1[['GASTO_TOTAL'].nlargest(7).as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])]
    #respuesta = respuesta.as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])
    respuesta.to_html()
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def productos_por_cliente(filtroBusqueda):
    #respuesta = TABLA1,filter(like = filtroBusqueda)
    respuesta = colCliente == filtroBusqueda
    respuesta = respuesta.as_matrix([colCliente, colProducto, colCodigo, colPrecio, colCantidad].head(20))
    respuesta.to_html()
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def clientes_por_producto(filtroBusqueda):
    respuesta = colProducto == filtroBusqueda
    respuesta = respuesta.as_matrix([colCodigo,colProducto,colPrecio, colCantidad, colCliente].head(20))
    respuesta.to_html()
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda):
    if tipoConsulta == 'pmv':
        productos_mas_vendidos()
    elif tipoConsulta == 'cmg':
        clientes_que_mas_gastaron()
    elif tipoConsulta == 'ppc':
        productos_por_cliente(filtroBusqueda)
    elif tipoConsulta == 'cpp':
        clientes_por_producto(filtroBusqueda)   


@app.route('/buscar',methods=['GET','POST'])
def buscar():
    if 'username' in session:
        tipoConsulta = request.form.get('consulta_seleccionada')
        filtroBusqueda = request.form.get('fitroBusqueda')
        seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda)
    else: 
        return render_template('error_login.html') '''
 

=======
if(__name__ == '__main__'):
    app.run(debug=True,host='0.0.0.0')
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
