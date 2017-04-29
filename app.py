from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 
from Driver import Examinar, dbUsers
from flask import *
from functools import wraps
import random
import os

                                
iTestMe = Flask(__name__)
iTestMe.secret_key = os.urandom(12)
dbUsers.registrarUsuario("admin","admin")
datosGenerales = { 
		"titulo":"iTestMe",
}
def validarDatos_get(datos=None):
	for datoD in datosGenerales:
		if(datoD not in datos):
			datos[datoD] = datosGenerales[datoD]
	return datos
	
def verificar_login(route):
	@wraps(route)
	def verificarSesion(*args, **kwargs):
		if not session.get("en_sesion"):
			print("No estas logeado!")
			return redirect(url_for("logear"))
		else:
			return route()
	return verificarSesion


	
@iTestMe.route('/login', methods=["GET", "POST"])
def logear():
	if request.method == "POST":
		usuario = request.form["usuario"]
		password = request.form['password']
		print(usuario,password)
		if(dbUsers.verificarDatos(usuario,password)):
			session["en_sesion"] = True
			print("[+]Usuario %s logeado correctamente"%usuario)
			return redirect("/")
		else:
			redirect("/login")
	else:
		return render_template("login.html")

@iTestMe.route("/")
@verificar_login
def index():
	return render_template("home.html")
	


@iTestMe.route("/examen",methods=["GET", "POST"])
@verificar_login
def examen():
	if request.method == "GET":
		examenActual = Examinar("admin").Examen()
		#Si se va a enviar una consigna multiple choice
		if(examenActual["tipo"] == "choice"):				
			return render_template("multipleChoice.html", 
															**validarDatos_get(examenActual) )										
		#Si se va a enviar una consigna tipo Escrita
		if(examenActual["tipo"] == "consigna"):
			return render_template("escribirConsigna.html", 
															**validarDatos_get(examenActual) )
	if request.method == "POST":
		tipoPregunta = request.form.get("tipoPregunta")
		verificacionItem = request.form.get("respEnv")
		respuestaRecibida = request.form.get("respuestaEscrita")
		usuario = request.form.get("usuarioID")
		examinado = Examinar("admin")
		
		def validarDatos_post(datos_p,datos_html=None):
			for d in datos_p:
				if(d not in datos_html):
					datos_html[d] = datos_p[d]
			return datos_html
			
		#Si se recibio una respuesta tipo choice
		if(tipoPregunta == "choice"):
			if(verificacionItem == "valida"):
				examinado.respuestaAcertada()
			else:
				examinado.respuestaInvalida()
			return redirect("/examen")
		
		#Si recibio para validar una respuesta escrita
		if(tipoPregunta == "consignaVerificar"):
			verificacionConsigna = examinado.gConsigna(respuestaRecibida)
			if("valida" in verificacionConsigna):
				if(verificacionConsigna["valida"] == "respuestaValida"):
					examinado.respuestaAcertada()
				else:
					examinado.respuestaInvalida()
			return render_template("consignaVerificada.html", 
														**validarDatos_get(verificacionConsigna) )
		return render_template("error.html")


    

if __name__ == "__main__":
	print("[+]Iniciando iTestMe")
	
	print(os.urandom(12))
	iTestMe.run()
