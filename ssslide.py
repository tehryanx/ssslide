#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import os, mimetypes, re, signal, argparse
from zipfile import ZipFile
from requests import get
import uuid, base64

parser = argparse.ArgumentParser(description='Serve images from the current directory as a slideshow over http.', epilog='Happy hacking!')
parser.add_argument('-p', '--port', type=int, default="8000", help="The port to listen on. Defaults to 8000")
parser.add_argument('-z', '--zip', action="store_true", default=False, help="Zip all images and serve them at /zip")
args = parser.parse_args()

port=args.port
zipflag=args.zip
key = str(uuid.uuid1())

js_array = ""

def sigint_handler(signum, frame):
	print("Received sigint. Exiting.")
	exit()


class StaticServer(BaseHTTPRequestHandler):


	def do_GET(self):

		if "?" in self.path:
			path = self.path.split("?")[0]
			param = self.path.split("?")[1]
		else: 
			return

		if key not in param: 
			self.send_response(403)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(b"Bad key: Access denied.")
			return

		if len(re.findall("[^=?a-zA-Z0-9._-]", path[1:])):
			print("Bad chars detected in: {}".format(path))
			return

			if path == '/zip':
				if zipflag:
					collection = []
					with os.scandir('.') as files:
					        for f in files:
					                if os.path.isfile(f.name):
					                        if 'image' in mimetypes.guess_type(f.name)[0]:
			                        		        collection.append(f.name)
					zipObj = ZipFile('collection.zip', 'w')

					for file in collection:
						zipObj.write(file)
					zipObj.close()

					self.send_response(200)
					self.send_header('Content-type', 'application/zip')
					self.send_header('Content-disposition', 'attachment; filename="collection.zip')
					self.end_headers()
					with open('collection.zip', 'rb') as fh:
						zip = fh.read()
						self.wfile.write(zip)
				else:
					print ("Attempted to access zip but -z not set.")
					self.send_response(403)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					self.wfile.write(b"Attempted to access zip but -z not set.")
					return

		if path == '/':
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
			filename = os.path.abspath('.') + path
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


signal.signal(signal.SIGINT, sigint_handler)

images = []
with os.scandir('.') as files:
	for f in files:
		if os.path.isfile(f.name):
			if 'image' in mimetypes.guess_type(f.name)[0]:
				images.append(f.name)

delim="?key="+key+"','"
js_array = "'" + delim.join(images) + "/?key="+key+"'"

ip = get('https://icanhazip.com').text.strip()



header="""
\033[92m              _ _     _
  ___ ___ ___| (_) __| | ___
 / __/ __/ __| | |/ _` |/ _ \\
 \__ \__ \__ \ | | (_| |  __/
 |___/___/___/_|_|\__,_|\___|
                 \033[0m\033[94mtehryanx\033[0m
"""
print(header)
print("serving \033[94m{}\033[0m images on \033[92mhttp://{}\033[0m:\033[92m{}\033[0m/?\033[92mkey\033[0m=\033[92m{}\033[0m".format(str(len(images)),ip,port,key))
if zipflag:
	print("zip archive available at \033[92mhttp://{}\033[0m:\033[92m{}/zip/\033[0m?\033[92mkey\033[0m=\033[92m{}\033[0m".format(ip,port,key))
httpd = HTTPServer(('', port), StaticServer)
httpd.serve_forever()
