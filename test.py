







def funcion1(func):
	def funcion2():
		print("Holaaa")
		func()
	return funcion2

@funcion1
def hola():
	print("Mundo")

hola()
