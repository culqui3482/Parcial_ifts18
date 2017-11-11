import csv
import pandas as pd

#------------------------------CONSULTAS---------------------------
# class farmaConsulta():
#     def __init__(self,codigo='',nombre='',filtro=''):
#         self.codigo = codigo           
#         self.nombre = nombre
#         self.filtro = filtro

tabla1 = pd.read_csv(archivoFar)
#sort de registros utilizando pandas todos devuelven una respuesta que se muestra en un solo template dinamico
def productos_mas_vendidos():
    respuesta = tabla1.groupby(by=['PRODUCTO'], as_index=False).sum().sort_values(by=['CANTIDAD'])
    respuesta = respuesta.head().iloc[::-1]
    return respuesta

def clientes_que_mas_gastaron():
    tabla1['TOTAL'] = tabla1['CANTIDAD']*tabla1['PRECIO']
    respuesta = tabla1.groupby(by=['CLIENTE'], as_index=False).sum().sort_values(by=['TOTAL'])
    respuesta = respuesta.head().iloc[::-1]
    return respuesta

def productos_por_cliente(filtroBusqueda):
    respuesta = tabla1[tabla1.CLIENTE == filtroBusqueda]
    respuesta = respuesta.groupby(by=['CODIGO','PRODUCTO','CANTIDAD','CLIENTE'], as_index=False).sum().iloc[::-1]
    return respuesta

def clientes_por_producto(filtroBusqueda):
    respuesta = tabla1[tabla1.PRODUCTO == filtroBusqueda]
    respuesta = respuesta.groupby(by=['CLIENTE','PRODUCTO','CODIGO','CANTIDAD'], as_index=False).sum().iloc[::-1]
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
         respuesta='<div style="text-align: center;"> <p>no hay items para mostrar haga una nueva consulta verificando los datos</p><a href="/consulta" class="btn btn-default">Hacer una nueva consulta</a> </div>'   
    return respuesta

