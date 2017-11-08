from flask import Flask
from flask import render_template, session, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
import csv
import pandas as pandas

app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL']=True
boot=Bootstrap(app)

# class miformulario(FlaskForm):
#     tipoConsulta = StringField('Consulta seleccionada', [validators.data_required(message = "Seleccione un tipo de consulta")])
#     filtroBusqueda = StringField('Filtrar',[validators.data_required(message = "Tiene que ingresar un dato para filtrar la busqueda")])
#     submit = SubmitField('Buscar')

<<<<<<< HEAD
ARCHIVO_FAR = 'csv/archivoFar.csv'
=======
ARCHIVO_FAR = 'csv/ArchivoFar.csv'
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
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
<<<<<<< HEAD
    respuesta = TABLA1.groupby(colProducto,as_index=False)['CANTIDAD'].nlargest(7)
    respuesta = respuesta.as_matrix([colCodigo, colProducto, colCantidad])
    respuesta.to_html()
=======
     respuesta = TABLA1.groupby(colProducto,as_index=False)['CANTIDAD'].nlargest(7)
     respuesta = respuesta.as_matrix([colCodigo, colProducto, colCantidad])
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def clientes_que_mas_gastaron():
    col_gasto_total = TABLA1['GASTO_TOTAL']
    col_gasto_total = (colCantidad * colPrecio)
<<<<<<< HEAD
    respuesta = TABLA1[['GASTO_TOTAL'].nlargest(7).as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])]
    #respuesta = respuesta.as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])
    respuesta.to_html()
=======
    respuesta = TABLA1[['GASTO_TOTAL'].nlargest(7).as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])
    #respuesta = respuesta.as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def productos_por_cliente(filtroBusqueda):
    #respuesta = TABLA1,filter(like = filtroBusqueda)
    respuesta = colCliente == filtroBusqueda
<<<<<<< HEAD
    respuesta = respuesta.as_matrix([colCliente, colProducto, colCodigo, colPrecio, colCantidad].head(20))
    respuesta.to_html()
=======
    respuesta = respuesta.as_matrix([colCliente, colProducto, colCodigo, colPrecio, colCantidad].head(20)
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def clientes_por_producto(filtroBusqueda):
    respuesta = colProducto == filtroBusqueda
<<<<<<< HEAD
    respuesta = respuesta.as_matrix([colCodigo,colProducto,colPrecio, colCantidad, colCliente].head(20))
    respuesta.to_html()
    return render_template('consulta_respuesta.html',respuesta = respuesta)

=======
    respuesta = respuesta.as_matrix([colCodigo,colProducto,colPrecio, colCantidad, colCliente].head(20)
    return render_template('consulta_respuesta.html',respuesta = respuesta)


>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
def seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda):
    if tipoConsulta == 'pmv':
        productos_mas_vendidos()
    elif tipoConsulta == 'cmg':
        clientes_que_mas_gastaron()
    elif tipoConsulta == 'ppc':
        productos_por_cliente(filtroBusqueda)
    elif tipoConsulta == 'cpp':
        clientes_por_producto(filtroBusqueda)   

<<<<<<< HEAD

@app.route('/buscar',methods=['GET','POST'])
def buscar():
    if 'username' in session:
        tipoConsulta = request.form.get('consulta_seleccionada')
        filtroBusqueda = request.form.get('fitroBusqueda')
        seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda)
    else: 
        return render_template('error_login.html') 

=======
@app.route('/consulta',methods=['GET','POST'])
def consultar():
    miform= formularioConsulta()   
    if miform.validate_on_submit():
        tipoConsulta = request.form.get('consulta_seleccionada')
        filtroBusqueda = request.form.get('fitroBusqueda')
        seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda) 
    else:
        return "debe ingresar Filtros validos para buscar" 
    return render_template('consulta.html',form = miform)
>>>>>>> f33a877b420e3389939c0f8ab7894dee948a5b95
