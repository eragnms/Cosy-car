# from: https://www.junian.net/2014/07/simple-http-server-and-client-in-python.html

#!usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
  
  #handle GET command
  def do_GET(self):
    rootdir = './' #file location
    try:
        #if self.path.endswith('.html'):
        #    f = open(rootdir + self.path) #open requested file

        #send code 200 response
        self.send_response(200)

        #send header first
        self.send_header('Content-type','text/html')
        self.end_headers()

        #send file content to client
        #self.wfile.write(f.read())
        self.wfile.write("<html><head><title>Title goes here.</title></head>".encode())
        self.wfile.write("<body><p>This is a test.</p>".encode())
        self.wfile.write("</body></html>".encode())
        #f.close()
        return
      
    except IOError:
      self.send_error(404, 'file not found')
  
def run():
  print('http server is starting...')

  #ip and port of servr
  #by default http server port is 80
  server_address = ('', 8080)
  httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
  print('http server is running...')
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass

    
if __name__ == '__main__':
  run()
