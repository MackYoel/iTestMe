from db.driverDBExamenes import ExamenesActuales
from db.driverDBConsignas import Consignas
from db.driverDBUsuarios import Usuarios
import sqlite3
import random
import json

consignas = Consignas()
dbUsers = Usuarios()
examenesActuales = ExamenesActuales()



class Examinar():
	def __init__(self, ID_USUARIO):
		self.db = consignas
		print("\n[+]Comprobando si ", ID_USUARIO," esta en un examen actualmente")
		self.datosExamen = examenesActuales.obtenerExamen(ID_USUARIO)
		if(self.datosExamen is False):
			examenesActuales.iniciarExamen(ID_USUARIO, dbUsers)
		self.datosExamen = examenesActuales.obtenerExamen(ID_USUARIO)
		self.id_examen = self.datosExamen[0]
		self.idUsuario = self.datosExamen[1]
		self.progresoActual = self.datosExamen[2]
		self.respuestasAcertadas = self.datosExamen[3]
		self.respuestasDesacertadas = self.datosExamen[4]
		self.notaFinal = self.datosExamen[5]
		try:
			self.datosBuffer = json.loads(self.datosExamen[6])
		except:
			self.datosBuffer = self.datosExamen[6]
		self.dificultad = self.datosExamen[7]
		self.cantidadPreguntas = self.datosExamen[8]	
	
	def Examen(self):
		print("Pregunta actual para %s"%self.idUsuario)
		if(self.progresoActual == self.cantidadPreguntas):
			print("Examen para %s finalizado."%self.idUsuario)
			return self.finalizarExamen(self.idUsuario)
		else:
			print("Haciendo Pregunta numero ",self.progresoActual)
			datos =  self.lanzarPregunta()
			return datos
	
	def evaluar(self, acertadas, invalidas):
		if(invalidas == 0):
			return "Perfecto!"
		elif(acertadas == 0):
			return "Pesimo.."
		elif(acertadas > invalidas):
			return "Bien!"
		elif(acertadas == invalidas):
			return "Regular"
		elif(invalidas > acertadas):
			return "Mal!"
		else:
			return "No se como calificarlo."
					
	def finalizarExamen(self, nombreUsuario):
		print("Finalizacion")
		return None
	
	def desordenarLista(self, lista):
		listaFinal = lista
		for i in range(0,999):
			el = listaFinal.pop(listaFinal.index(random.choice(listaFinal)))
			listaFinal.insert(listaFinal.index(random.choice(listaFinal)), el)
		return listaFinal
	
	def lanzarPregunta(self):
		tipos_c = {
				"choice":self.multipleChoice,
				"consigna":self.gConsigna
		}
		if("null" in self.datosBuffer):#si hay una pregunta aun no contestada se mantiene
			return self.datosBuffer
		else:
			self.pregunta_actual = tipos_c[random.choice(list(tipos_c))]()
			return self.datosBuffer
	
	def procesarDatos(self, add=None):#Actualiza datos en DB
		datos = {
				"aciertos":self.respuestasAcertadas,
				"desaciertos":self.respuestasDesacertadas,
				"progresoActual":self.progresoActual*10
		}
		if add:
			for dato_nuevo in add:
				datos[dato_nuevo] = add[dato_nuevo]
		self.datosBuffer = datos
		datosActualizar = [
							self.id_examen,
							self.idUsuario,
							self.progresoActual, 
							self.respuestasAcertadas,
							self.respuestasDesacertadas,
							self.notaFinal,
							json.dumps(self.datosBuffer),
							self.dificultad,
							self.cantidadPreguntas
							]
		examenesActuales.actualizarExamen(datosActualizar)
		return datos
			
	def multipleChoice(self):
		pElegida = self.db.consignaAleatoria("choice", self.dificultad)
		opciones = pElegida[4].split("++")
		correcta = opciones[0]
		rDesordenadas = self.desordenarLista(opciones)
		datos = {
				"tipo":"choice",
				"pregunta":pElegida[1],
				"categoria":pElegida[2],
				"aclaracion":pElegida[5],
				"opcionCorrecta":correcta,
				"opcionesChoice":rDesordenadas,
				"cantidadOpciones":len(rDesordenadas)
		}
		self.pregunta_actual = "choice"
		return self.procesarDatos(datos)
		
	def compararDatos(self, original, tipeado):
		original = original.lower()
		usuario = tipeado.lower().replace(".",",")
		coinc = 0
		for b in usuario.split(" "):
			if(b in original.split(" ")):
				coinc+=1
		if(coinc >= len(original.split(" "))/2):
			return True
		else:
			return False
			
	def gConsigna(self, arg=None):
		if(arg is None):
			pElegida = self.db.consignaAleatoria("escrita", self.dificultad)
			datos =  {
					"dificultad":pElegida[2],
					"tipo":"consigna",
					"id":pElegida[0],
					"consigna":pElegida[1],
					"aclaracion":pElegida[5],
			}
			return self.procesarDatos(datos)
		else:
			if(self.datosBuffer["tipo"] == "consigna"):
					dato_real = self.db.obtenerPorId(self.datosBuffer["id"])[4]
					dato_comp = arg
					if(self.compararDatos(dato_real, dato_comp)):
						datosEnviar =  {
							"consigna":self.datosBuffer["consigna"],
							"valida":"respuestaValida",
							"aclaracion":self.datosBuffer["aclaracion"],
							"respuestaDada":dato_comp,
						}
						return self.procesarDatos(datosEnviar)
					else:
						datosEnviar =  {
							"consigna":self.datosBuffer["consigna"],
							"valida":"respuestaInvalida",
							"respuestaDada":dato_comp,
						}
						return self.procesarDatos(datosEnviar)
			else:
				return {
						"tipo":"error"
						}
	
	def resetearPregunta(self):
		self.pregunta_actual = -1
		
	def respuestaAcertada(self):
		self.progresoActual += 1
		self.respuestasAcertadas+=1
		self.datosBuffer = "null"
		self.procesarDatos()
			
	def respuestaInvalida(self):
		self.progresoActual += 1
		self.respuestasDesacertadas+= 1
		self.datosBuffer = "null"
		self.procesarDatos()

if __name__ == "__main__":
	Examinar("admin").Examen()
	Examinar("admin").gConsigna("auto")
	
	
	
	
	
	
	
	
	
