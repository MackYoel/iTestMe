import random
import sqlite3

"""
En esta base de datos estan los usuarios con sus respectivas contraseñas
"""
class Usuarios():
	def __init__(self):
		self.db = sqlite3.connect(":memory:")
		self.iniciarDB()
		
	def registrarUsuario(self ,usuarioID, usuarioPassword):
		idObtenida = self.db.execute("SELECT nick FROM usuarios WHERE nick ='%s'"%usuarioID).fetchall()
		if(idObtenida == []):
			self.db.execute("INSERT INTO usuarios values('%s', '%s')"%(usuarioID, usuarioPassword))
			print("[+]Usuario '%s' registrado."%usuarioID)
		else:
			print("Ya se esta usando ese nick")								

	def verificarDatos(self ,usuarioID, usuarioPassword):
		idObtenida = self.db.execute("SELECT * FROM usuarios WHERE \
										nick='%s' and password='%s'"%(usuarioID,usuarioPassword)).fetchall()
		if(idObtenida):
			print("Nombre y contraseña correcta.")
			return True
		else:
			print("Nombre o contraseña incorrecta.")
			return False
		
	def verificarExistencia(self, usuarioID):
		idObtenida = self.db.execute("SELECT nick from usuarios WHERE nick='%s'"%usuarioID)
		if(idObtenida):
			return usuarioID
		else:
			return False
			
	def iniciarDB(self):
		self.db.execute("""CREATE TABLE usuarios(
						nick varchar primary key,
						password varchar
					  );
					  """)
		print("[+]Memoria usuarios iniciada")
		
		
			
if __name__ == "__main__":
	pass
