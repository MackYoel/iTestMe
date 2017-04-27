import random

dbs_index = [
	[{}, "consignas.txt"], 
	[{}, "choices.txt"]
]
for dbs in dbs_index:#Crear dbs
	index = 0
	with open(dbs[1], "r") as archivo_p:
		for fila in archivo_p.read().split("\n"):
			if("=FIN=" in fila):break
			if("=" not in fila):
				if(index not in dbs[0]):
					dbs[0][index] = [fila]
				else:
					dbs[0][index].append(fila)
			else:
				index+=1

class Evaluacion():
	def __init__(self):
		self.db_choice = dbs_index[1][0]
		self.db_consigna = dbs_index[0][0]
		self.progresoActual = 0
		self.respuestasAcertadas = 0
		self.respuestasDesacertadas = 0
		self.notaFinal = 0
		self.pregunta_actual = -1
		self.datos_actual = None
	
	def iniciarExamen(self):
		print("Examen iniciado..")
		for m in range(10):
			self.multipleChoice()
		print("Examen finalizado..")
		
		
	def desordenar_dic(self, lista):
		lista = lista
		listaFinal = {}
		for i in range(1,len(lista)+1):
			extraido = lista.pop(lista.index(random.choice(lista)))
			listaFinal[i] = extraido
		return listaFinal
	
	def desordenar(self, lista):
		listaFinal = lista
		
		for i in range(0,999):
			el = listaFinal.pop(listaFinal.index(random.choice(listaFinal)))
			listaFinal.insert(listaFinal.index(random.choice(listaFinal)), el)
		return listaFinal
	
	def lanzarPregunta(self):
		tipos_c = {
				"choice":self.multipleChoice,
				"consigna":self.lanzarConsigna
		}
		if(self.pregunta_actual != -1):#si hay una pregunta aun no contestada se mantiene
			return self.pregunta_actual
		else:
			self.pregunta_actual = tipos_c[random.choice(list(tipos_c))]()
			return self.pregunta_actual
	
	def crear_datos(self, add=None):#Devuelve los datos para la plantilla
		datos = {
				#datos por defecto
				"aciertos":self.respuestasAcertadas,
				"desaciertos":self.respuestasDesacertadas,
				"progresoActual":self.progresoActual
		}
		if add:
			for dato_nuevo in add:
				datos[dato_nuevo] = add[dato_nuevo]
		self.datos_actual = datos
		return datos
		
	def multipleChoice(self):
		pElegida = self.db_choice[random.choice(list(self.db_choice))]
		rDesordenadas = self.desordenar(pElegida[2:])
		datos = {
				"tipo":"choice",
				"pregunta":pElegida[0],
				"aclaracion":pElegida[1],
				"opcionCorrecta":pElegida[2],
				"opcionesChoice":rDesordenadas,
				"cantidadOpciones":len(rDesordenadas)
		}
		return self.crear_datos(datos)
		
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
			
	def lanzarConsigna(self, arg=None):
		"""
			Si se invoca sin argumento, es para lanzar una consigna
			de lo contrario es para verificar y dar la respuesta
		"""
		if(arg is None):
			elec = random.choice(list(self.db_consigna))
			pElegida = self.db_consigna[elec]
			datos =  {
					"tipo":"consigna",
					"id":elec,
					"consigna":pElegida[0],
					"aclaracion":pElegida[2],
			}
			return self.crear_datos(datos)
		else:
			if(self.datos_actual != -1 and self.datos_actual["tipo"] == "consigna"):
					dato_real = self.db_consigna[self.datos_actual["id"]][1]
					dato_comp = arg
					if(self.compararDatos(dato_real, dato_comp)):
						datosEnviar =  {
							"valida":"respuestaValida",
							"aclaracion":self.datos_actual["aclaracion"]
						}
						return self.crear_datos(datosEnviar)
					else:
						datosEnviar =  {
							"valida":"respuestaInvalida"
						}
						return self.crear_datos(datosEnviar)
			else:
				return {
						"tipo":"error"
						}
	
	def resetearPregunta(self):
		self.pregunta_actual = -1
		
	def respuestaAcertada(self):
		self.progresoActual += 10
		self.respuestasAcertadas+=1
		self.pregunta_actual = -1
		
	def respuestaInvalida(self):
		self.progresoActual += 10
		self.respuestasDesacertadas+= 1
		self.pregunta_actual = -1
		
		
if __name__ == "__main__":
	test = Evaluacion()
	print(test.multipleChoice())
	




