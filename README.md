# ssslide
View screenshots as a slideshow over http

Run ssslide.py from inside the directory with screenshots and then view them over http with the given url. 

```
$ ~/target/screenshots$ ssslide

              _ _     _
  ___ ___ ___| (_) __| | ___
 / __/ __/ __| | |/ _` |/ _ \
 \__ \__ \__ \ | | (_| |  __/
 |___/___/___/_|_|\__,_|\___|
                 tehryanx

serving 53 images on http://1.2.3.4:8000
```
# Usage
```
$ ~/bounties/lyft/screenshots$ ssslide --help
usage: ssslide [-h] [-p PORT] [-z]

Serve images from the current directory as a slideshow over http.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  The port to listen on. Defaults to 8000
  -z, --zip             Zip all images and serve them at /zip

Happy hacking!
```

### use h and l or j and k to flip through the screenshots in your browser. 
