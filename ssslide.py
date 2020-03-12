#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import os, mimetypes
from requests import get

js_array = ""

class StaticServer(BaseHTTPRequestHandler):

	def do_GET(self):

		if self.path == '/':
			# serve slideshow code.

			html =  """
<html>
	<head>
		<title>ssslide</title>
		<script>
			images = [""" + js_array + """];
			function slide(dir){
				if (dir == 1) {
					// Add the last image to the front position
					images.unshift(images[images.length-1]);
					// remove it from the last position
					images.pop();
				} else {
					// add the first image to the last position
					images.push(images[0]);
					// remove it from teh first position
					images.shift();
				}

				document.slider.src=images[0];
				document.getElementById('imagelabel').innerHTML=images[0];
				document.title=images[0];
			}
			document.addEventListener("keypress", function onPress(event) {
				if (event.key === "k" || event.key === "l") {
					slide(1);
				} else if (event.key === "h" || event.key === "j"){
					slide(2);
				}
			});
			window.onload = slide;
		</script>
	</head>
	<body>
		<div style="font-size:11px;" name="imagelabel" id="imagelabel"></div>
		<img name="slider" style="width: 100%; height: auto;">
	</body>
</html>
"""
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes(html, 'utf8'))
		else:
			filename = os.path.abspath('.') + self.path
			if os.path.isfile(filename):
				mimetype = mimetypes.guess_type(filename)[0]
				if 'image' not in mimetype:
					self.send_response(403)
					self.end_headers()
					self.wfile.write(b'403')
				else:
					self.send_response(200)
					self.send_header('Content-type', mimetype)
					self.end_headers()
					with open(filename, 'rb') as fh:
						html = fh.read()
						self.wfile.write(html)
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'404: Nothing here.')

images = []
with os.scandir('.') as files:
	for f in files:
		if os.path.isfile(f.name):
			if 'image' in mimetypes.guess_type(f.name)[0]:
				images.append(f.name)

js_array = "'"+"', '".join(images)+"'"

port = 8000
ip = get('https://api.ipify.org').text

print("serving {} images on http://{}:{}".format(str(len(images)),ip,port))
httpd = HTTPServer(('', port), StaticServer)
httpd.serve_forever()
