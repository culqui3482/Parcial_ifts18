<h1> Final --- Farma@<h1>
<hr>
<h5>Esta es una aplicación Web creada  para consultar la base de datos  de  la empresa Farma@  en donde están almacenadas todas las ventas que se realizaron.<h5>
<br>
<h3 >Flujo del programa<h3>
<hr>

<h5>En el programa lo que primero se visualiza es el home, para seguir navegando pide al usuario que ingrese o se registre en el sistema. Una vez ingresado, podrá visualizar al usuario logueado, la consulta de las últimas ventas, un nuevo nav con otras opciones, otro tipo de consultas sobre los clientes y los productos .<h5>
<br>
<h3>Estructura de los archivos<h3>
<hr>

<h5>Desarrollada integramente en el lenguaje de programación PYTHON, en su versión 3.6<h5>
<h5>Se utilizaron módulos y repositorios:
Base de datos : archivos csv.
<h5>Repositorio: 
*CSV 
*Flask 
*Bootstrap 
*Flash message<h5>

<br>
<h3>Uso del programa<h3>
<hr>

<h5>El usuario de este sistema deberá ingresar a su cuenta,con el boton 'ingresar' o registrarse mediante el boton 'registrar' los cuales se encuentra en la parte superior de la pantalla.

Cuando el usuario este ingresado se llevara a una nueva ventana donde esta dandole la bienvenida, mostrando las ventas que se realizaron y se habilitaran varias funciones en la barra superior de la pantalla ( consultas, usuarios).<h5>

<h4>Template:<h4>
<hr>

 * <h5>Home: Muestra el home de la pagina y las opciones que puedes realizar.
 * Ingresar: Te deriva a una ventana donde el usuario podra abrir su session.
 * Registra: Donde el usuario para poder registarse.
 * Usuarios: En esta ventana se podra ver una lista de usuarios registrados.
 * Consultas: Donde podra realizar consulta realizando una busqueda por producto por cliente, productos mas vendidos.
 * Salir: cierra la session del usuario.
 * Vistas de errores: 500,404, logeo.<h5>
 
<hr>
<h4>Final <h4>
<hr>

 * Registro Usuario: Se mejoro el registro de usuario con mensaje de validacion ante contraseñas distintas.
 * Consultas: En la seleccion de datos para la consulta se valida que el filtro sea solo para los valores Productos por cliente  y  Clientes por producto. 
 *  Descarga de consultas en csv: Se agrego el punto solicitado de fecha y nombre en el archivo de consulta



