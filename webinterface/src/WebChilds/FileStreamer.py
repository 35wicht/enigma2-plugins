from twisted.web import resource, http, http_headers
from urllib import unquote_plus
from os import path as os_path

class FileStreamer(resource.Resource):
	addSlash = True

	def render(self, request):
		try:
			w1 = request.uri.split("?")[1]
			w2 = w1.split("&")
			parts = {}
			for i in w2:
				w3 = i.split("=")
				parts[w3[0]] = w3[1]
		except:
			request.setResponseCode(http.OK)
			request.write("no file given with file=???")
			request.finish()
						
		dir = ""
		
		if parts.has_key("root"):
			#root = parts["root"].replace("%20"," ")
			dir = unquote_plus(parts["root"])
		if parts.has_key("dir"):
			dir = unquote_plus(parts["dir"])
		if parts.has_key("file"):
			#filename = parts["file"].replace("%20"," ")
			filename = unquote_plus(parts["file"])
			
			path = "%s%s" %(dir, filename)
			#dirty backwards compatibility hack
			if not os_path.exists(path):
				path = "/hdd/movie/%s" %filename
			
			if os_path.exists(path):
				s = stream.FileStream(open(path,"r"))
				type = path.split(".")[-1]
				header = http_headers.MimeType('video', 'ts')
				if type == "mp3" or type == "ogg" or type == "wav":
					header = http_headers.MimeType('audio', 'x-mpeg')
				elif type == "avi" or type == "mpg":
					header = http_headers.MimeType('video', 'x-msvideo')
				elif type == "jpg" or type == "jpeg" or type == "jpe":
					header = http_headers.MimeType('image', 'jpeg')

				resp = http.Response(responsecode.OK, {'Content-type': header},stream=s)
				request.setResponseCode(http.OK)
				request.setHeader('Content-type', header)
				request.setHeader('Content-Disposition','attachment; filename="%s"'%filename)
				request.write(s)
				request.finish()
				
			else:
				request.setResponseCode(http.OK)
				request.write("file '%s' was not found"%path)
				request.finish()				
		else:
			request.setResponseCode(http.OK)
			request.write("no file given with file=???")
			request.finish()			




