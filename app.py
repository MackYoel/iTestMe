from flask import *
import random
import evaluacion

app = Flask(__name__)

examen_actual = evaluacion.Evaluacion()

datosGenerales = { 
		"titulo":"iTestMe",
}

def validarDatos_get(datos=None):
			for datoD in datosGenerales:
				if(datoD not in datos):
					datos[datoD] = datosGenerales[datoD]
			return datos
			
@app.route("/")
def index():
	return render_template("home.html")
	
@app.route("/examen",methods=["GET","POST"])
def examen():
	print("========================================================");
	if request.method == "GET":
		datos = examen_actual.lanzarPregunta()
		#Si se va a enviar una consigna multiple choice
		if(datos["tipo"] == "choice"):				
			return render_template("multipleChoice.html", 
															**validarDatos_get(datos) )										
		#Si se va a enviar una consigna tipo Escrita
		if(datos["tipo"] == "consigna"):
			return render_template("escribirConsigna.html", 
															**validarDatos_get(datos) )
			
	if request.method == "POST":
		tipoPregunta = request.form.get("tipoPregunta")
		verificacionItem = request.form.get("respEnv")
		respuestaRecibida = request.form.get("respuestaEscrita")
		def validarDatos_post(datos_p,datos_html=None):
			for d in datos_p:
				if(d not in datos_html):
					datos_html[d] = datos_p[d]
			return datos_html
			
		#Si no se recibio un tipo de respuesta valido
		if(tipoPregunta == None):
			examen_actual.resetearPregunta()
			return redirect("/examen")
		
		#Si se recibio una respuesta tipo choice
		if(tipoPregunta == "choice"):
			if(verificacionItem == "valida" and examen_actual != -1):
				examen_actual.respuestaAcertada()
			else:
				examen_actual.respuestaInvalida()
			return redirect("/examen")
		
		#Si recibio para validar una respuesta escrita
		if(tipoPregunta == "consignaVerificar"):
			verificacionConsigna = examen_actual.gConsigna(respuestaRecibida)
			if(verificacionConsigna["valida"] == "respuestaValida"):
				examen_actual.respuestaAcertada()
			else:
				examen_actual.respuestaInvalida()
			return render_template("consignaVerificada.html", 
														**validarDatos_get(verificacionConsigna) )

			
		
		
		return render_template("error.html")

if __name__ == "__main__":
	print("Iniciando app")
	app.run()
