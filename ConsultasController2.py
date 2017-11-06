from flask import Flask
from flask import render_template
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

class miformulario(FlaskForm):
    tipoConsulta = StringField('tipoConsulta', [validators.data_required(message = "Selecciones un tipo de consulta")])
    filtroBusqueda = StringField('filtroBusqueda',[validators.data_required(message = "Tiene que ingresar un dato para filtrar la busqueda")])
    submit = SubmitField('Buscar')

ARCHIVO_FAR = 'csv/ArchivoFar.csv'
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
    respuesta = TABLA1.groupby(colProducto,as_index=False)['CANTIDAD'].nlargest(7).as_matrix([colCodigo, colProducto, colCantidad])
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def clientes_que_mas_gastaron():
    col_gasto_total = TABLA1['GASTO_TOTAL']
    col_gasto_total = (colCantidad * colPrecio)
    respuesta = TABLA1.groupby(colCliente, as_index=False)['GASTO_TOTAL'].nlargest(7).as_matrix([colCliente, colProducto, colCantidad, col_gasto_total])
    return render_template('consulta_respuesta.html',respuesta = respuesta)

def productos_por_cliente(filtroBusqueda):

    return render_template('consulta_respuesta.html',respuesta = respuesta)

def clientes_por_producto(filtroBusqueda):

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

@app.route('/consulta',methods=['GET','POST'])
def consultar():
    miform= formularioConsulta()   
    if miform.validate_on_submit():
        seleccionar_tipo_consulta(tipoConsulta, filtroBusqueda) 
    else:
        return "debe ingresar Filtros validos para buscar" 
    return render_template('consulta.html',form = miform)