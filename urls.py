

url_source = {
	"bootstrap":"styles/css/bootstrap.css",
	"animation":"styles/css/animate.css"

}


class Resources():
	def __init__(self):
		pass
	
	def get(self, rName):
		if(rName in url_source):
			return "{{ url_for(\"static\",filename=%s) }}"%str(url_source[rName])
		else:
			return "Resource url not found"


