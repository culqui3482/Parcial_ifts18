import csv
import pandas as pd

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
    respuesta = respuesta.groupby(by=['CODIGO','PRODUCTO','CANTIDAD','CLIENTE'], as_index=False).sum().iloc[::-1]
    return respuesta

def clientes_por_producto(filtroBusqueda):  
    df = pd.read_csv(ARCHIVO_FAR)
    respuesta = df[df.PRODUCTO == filtroBusqueda]
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

