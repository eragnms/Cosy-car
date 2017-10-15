#!/usr/bin/env python

# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Orinally written by Nathan Hamiel (2010), see:
# https://gist.github.com/1kastner/e083f9e813c0464e6a2ec8910553e632

from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

PORT = 8085
HTTP_LOG_FILE = 'tests/data/http_log_file.log'

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        request_path = self.path
        with open(HTTP_LOG_FILE, 'a') as log_file:
            log_file.write("\n----- GET Request Start ----->\n")
            log_file.write("Request path:", request_path)
            log_file.write("Request headers:", self.headers)
            log_file.write("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()
        
    def do_POST(self):
        
        request_path = self.path
        with open(HTTP_LOG_FILE, 'a') as log_file:
            log_file.write("\n----- POST Request Start ----->\n")
            log_file.write("Request path:", request_path)
            request_headers = self.headers
            content_length = request_headers.get('Content-Length')
            length = int(content_length) if content_length else 0
            log_file.write("Content Length:", length)
            log_file.write("Request headers:", request_headers)
            log_file.write("Request payload:", self.rfile.read(length))
            log_file.write("<----- Request End -----\n")
        
        self.send_response(200)
        self.end_headers()
    
    do_PUT = do_POST
    do_DELETE = do_GET
        
def main():
    port = PORT
    #print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    main()
