#!usr/bin/env python

# from: https://www.junian.net/2014/07/simple-http-server-and-client-in-python.html

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import argparse

DEFAULT_PORT = 8080
HTTP_LOG_FILE = '/tmp/cosycar_http_log_file.log'

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    rootdir = '../tests/data'
    try:
      with open(HTTP_LOG_FILE, 'a') as log_file:
        log_file.write('{}\n'.format(self.path))
      if self.path.endswith('sdata'):
        f = open(rootdir + "/response_1.html")
      elif self.path.endswith('json'):
        f = open(rootdir + "/response_1.html")
      elif self.path.endswith('status'):
        f = open(rootdir + "/response_1.html")
      elif self.path.endswith('Value=1'):
        f = open(rootdir + "/response_3.html")
      elif self.path.endswith('Value=0'):
        f = open(rootdir + "/response_4.html")
      else:
        f = open(rootdir + "/response_4.html")
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write(f.read().encode())
      f.close()
      return
    except IOError:
      self.send_error(404, 'file not found')
  
def run():
    usage_text = "Creates http-server that will echo GET or POST parameters\n"
    parser = argparse.ArgumentParser(description=usage_text)
    parser.add_argument("-p",
                        "--port",
                        help="port on localhost to monitor, default 8080",
                        type=int)
    args = parser.parse_args()
    if args.port:
        port = args.port
    else:
        port = DEFAULT_PORT
    server_address = ('', port)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    try:
      httpd.serve_forever()
    except KeyboardInterrupt:
      pass

    
if __name__ == '__main__':
  run()
