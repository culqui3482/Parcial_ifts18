import csv
import pandas as pd 

#------------------------------CONSULTAS---------------------------
#--- importamos el archivo csv y lo colocamos en una variable para luego ser llamado.
ARCHIVO_FAR = 'csv/archivoFar.csv' 
# .....................................................................................................

# .....................................................................................................
# consulta PMV en cual nos va a mostrar los productos mas vendidos el archivoFar
#----sort de registros utilizando pandas
def productos_mas_vendidos():
    df = pd.read_csv(ARCHIVO_FAR)#llamamos al archivo csv
    respuesta = df.groupby(by=['PRODUCTO'], as_index=False).sum()# agrupamos por producto en el cual no se visualiza el index
    respuesta = respuesta.sort_values(by=['CANTIDAD']) #Ordena por los valores a cantidad.
    respuesta = respuesta.tail(4).iloc[:,0:3] # aca llamo a respuesta el cual se vera solo los 5 registros y modificamos el orden de las columnas a visualizar
    #Guarda los datos en un nuevo CSV,este se guarda codificado en UTF-8, separado con ",",en el cual hemos modicado en nombre de las columnas.
    respuesta.to_csv('descarga.csv',columns=['Prods. mas Vendidos: ','PRODUCTO','CODIGO','CANTIDAD'], index=False)
    return respuesta

def clientes_que_mas_gastaron():
    df = pd.read_csv(ARCHIVO_FAR)#llamamos al archivo csv
    df['TOTAL'] = df['CANTIDAD']*df['PRECIO']# creamos una columna total el cual va indicar el multiplo de cantidad y precio
    respuesta = df.groupby(by=['CLIENTE'], as_index=False).sum() # se va agrupar por cliente
    respuesta = respuesta.sort_values(by=['TOTAL'])
    respuesta = respuesta.tail(4).iloc[:,[0,1,2,4]]# aca llamo a respuesta el cual se vera solo los 5 registros y modificamos el orden de las columnas a visualizar
    #Guarda los datos en un nuevo CSV,este se guarda codificado en UTF-8, separado con ",",en el cual hemos modicado en nombre de las columnas
    respuesta.to_csv('descarga.csv',columns=['Clientes_mas_Gastaron: ','CLIENTE','CODIGO','CANTIDAD','TOTAL'], index=False)
    return respuesta

def productos_por_cliente(filtroBusqueda): #deacuerod al filtro de busqueda.. 
    df = pd.read_csv(ARCHIVO_FAR)#llamamos al archivo csv
    respuesta = df[df.CLIENTE.str.upper() == filtroBusqueda.upper()]#comparamos el ingreso del cliente(ya sea mayuscula o minuscula)comparamos q sea igual al filtro
    respuesta = respuesta.groupby(by=['CLIENTE','PRODUCTO','CANTIDAD'], as_index=False).sum().iloc[:,[0,1,2,4]]
    #Guarda los datos en un nuevo CSV,este se guarda codificado en UTF-8, separado con ",",en el cual hemos modicado en nombre de las columnas
    respuesta.to_csv('descarga.csv',columns=['Prods_por_cliente: ','CLIENTE','PRODUCTO','CANTIDAD','PRECIO'], index=False)
    return respuesta


def clientes_por_producto(filtroBusqueda):  
    df = pd.read_csv(ARCHIVO_FAR)
    df['TOTAL'] = df['CANTIDAD']*df['PRECIO']
    respuesta = df[df.PRODUCTO.str.upper() == filtroBusqueda.upper()]#comparamos el ingreso del product(ya sea mayuscula o minuscula)comparamos q sea igual al filtro
    respuesta = respuesta.sort_values(by=['TOTAL'])
    respuesta = respuesta.groupby(by=['PRODUCTO','CLIENTE','CANTIDAD','TOTAL'], as_index=False).sum().iloc[:,[0,1,2,3]]
    #Guarda los datos en un nuevo CSV,este se guarda codificado en UTF-8, separado con ",",en el cual hemos modicado en nombre de las columnas
    respuesta.to_csv('descarga.csv',columns=['Cliente_por_Prods: ','PRODUCTO','CLIENTE','CANTIDAD','TOTAL'], index=False)
    return respuesta



# ....................................................................................................
# ....................................................................................................
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

