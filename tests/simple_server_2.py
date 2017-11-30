# from: https://www.junian.net/2014/07/simple-http-server-and-client-in-python.html

#!usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
  
  #handle GET command
  def do_GET(self):
    rootdir = '/home/mats/gitdev/cosycar/tests' #file location
    try:
      print(self.path)
      if self.path.endswith('sdata'):
        f = open(rootdir + "/response_1.html") #open requested file
      elif self.path.endswith('json'):
        f = open(rootdir + "/response_1.html") #open requested file
      elif self.path.endswith('status'):
        f = open(rootdir + "/response_1.html") #open requested file
      elif self.path.endswith('Value=1'):
        f = open(rootdir + "/response_3.html") #open requested file
      elif self.path.endswith('Value=0'):
        f = open(rootdir + "/response_4.html") #open requested file
      else:
        f = open(rootdir + "/response_4.html") #open requested file
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write(f.read().encode())
      f.close()
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
