from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
import csv
import pandas as pandas

archivoFar = 'csv/ArchivoFar.csv'
tabla1 = pandas.read_csv(archivoFar)

colCodigo = tabla1['CODIGO']
colProducto = tabla1['PRODUCTO']
colCliente = tabla1['CLIENTE']
colCantidad = tabla1['CANTIDAD']
colPrecio = tabla1['PRECIO']

#CONSULTA
class farmaConsulta():
    def __init__(self,nombre='',filtro=''):
        self.nombre=nombre
        self.filtro=filtro


def masVendidos():
        respuesta = tabla1.groupby(colProducto,as_index=False)['CANTIDAD'].nlargest(5).as_matrix([colCodigo,colProducto,colCantidad])
        return render_template('consulta_respuesta.html',respuesta = respuesta)

def masVendidos():
        respuesta = tabla1.groupby(colProducto,as_index=False)['CANTIDAD'].nlargest(5).as_matrix([colCodigo,colProducto,colCantidad])
        return render_template('consulta_respuesta.html',respuesta = respuesta)
# def Consutar():
#     form = formularioConsulta()
#     if(form.validate_on_submit()):
#         aut= AdminBD('usuarios.csv')
#         if (validar(form.name.data,form.password.data)):
#             mostrar_tabla=AdminBD('archivoFar.csv')
#             modelo=leerArchivoFar()
            
#     return render_template('consulta_respuesta.html',respuesta = respuesta)

      
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


@app.route('/consulta',methods=['GET','POST'])
def login():
    miform= formularioConsulta()
    
    if(miform.validate_on_submit()):
        #aut= AdminBD('usuarios.csv')
        #if (aut.validar(miform.name.data,miform.password.data)):
            mostrar_tabla=AdminBD('archivoFar.csv')
            modelo=mostrar_tabla.leerArchivoFar()
            
            return (render_template('welcome_table.html',modelo=modelo,nombre=miform.name.data))
        else:
            return render_template('error_login.html')
            
    return (render_template('loginFar.html',form = miform))





