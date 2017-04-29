import random
import sqlite3
from db.driverDBUsuarios import Usuarios

class ExamenesActuales():
	def __init__(self):
		self.db = sqlite3.connect(":memory:")
		self.iniciar()
	
	def iniciarExamen(self, usuarioID, usuarios):
		usuarioExiste = usuarios.verificarExistencia(usuarioID)
		idObtenida = self.db.execute("SELECT id_examen FROM examenesActuales where id_examen = (select max(id_examen) from examenesActuales)").fetchall()
		if(idObtenida):
			ID= idObtenida[0][0]
		else:
			ID = 0
		if(usuarioExiste):
			print("[+]Inicializando examen para '%s'"%usuarioExiste)
			self.db.execute("""INSERT INTO examenesActuales values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""\
			%(int(ID)+1,usuarioID,1,0,0,0,"False","facil",0))
			return ID+1
		else:
			print("[-]El usuario no existe")
			return False #id del examen iniciado
										
	def verTodo(self):
		for m in self.db.execute("SELECT * FROM examenesActuales"):
			print(m)	
												
	def iniciar(self):
		self.db.execute("""CREATE TABLE examenesActuales
					(
					  id_examen primary key,
					  nick varchar,
					  progresoActual integer,
					  respuestasAcertadas integer,
					  respuestasDesacertadas integer,
					  notaFinal integer,
					  datosBuffer varchar,
					  dificultad varchar,
					  cantidadPreguntas integer
					);""")
					
		print("[+]Memoria ExamenesActuales iniciada")
	
	def actualizarExamen(self, params):
		ID = self.db.execute("SELECT * FROM examenesActuales where id_examen='%s'"%params[0]).fetchall()
		if(ID):
			params.append(params[0])
			self.db.execute("""UPDATE examenesActuales SET \
													progresoActual='%s',
													respuestasAcertadas='%s',
													respuestasDesacertadas='%s',
													notaFinal='%s',
													datosBuffer='%s',
													dificultad='%s',
													cantidadPreguntas='%s' where  id_examen='%s'"""%tuple(params[2:]) )
		else:
			print("[-]No existe el examen '%s'"%params[0])
			
	def obtenerExamen(self, nick):
		ID = self.db.execute("SELECT * FROM examenesActuales where nick='%s'"%nick).fetchall()
		if(ID):
			datos = ID[0]
			return list(datos)
		else:
			return False
		
if __name__ == "__main__":
	dbUsers = Usuarios()
	dbUsers.registrarUsuario("admin","admin123")

	dbExamenes = ExamenesActuales()
	dbExamenes.iniciarExamen("admin")
	dbExamenes.iniciarExamen("admin")
	dbExamenes.verTodo()
	print("Modificando")
	datosNuevos = [2, "admin", 10, 12, 0, 10, "asdas", "facil", 10 ]
	dbExamenes.actualizarExamen(datosNuevos)
	dbExamenes.verTodo()
	print(dbExamenes.obtenerExamen(1))
	
	
	
	
	
	

