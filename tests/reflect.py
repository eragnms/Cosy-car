#!/usr/bin/env python

# Orinally written by Nathan Hamiel (2010), see:
# https://gist.github.com/1kastner/e083f9e813c0464e6a2ec8910553e632

from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse

DEFAULT_PORT = 8080
HTTP_LOG_FILE = '/tmp/cosycar_http_log_file.log'
SEND_RESPONSE = True

#import json
#import urllib2
#data = {
#    'ids': [12, 3, 4, 5, 6]
#}
#req = urllib2.Request('http://example.com/api/posts/create')
#req.add_header('Content-Type', 'application/json')
#response = urllib2.urlopen(req, json.dumps(data))


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        request_path = self.path
        with open(HTTP_LOG_FILE, 'a') as log_file:
            log_file.write('{}\n'.format(request_path))

        if SEND_RESPONSE:
            self.send_response(200, "hejsansvejsan")
            print("Sent...")
            #self.send_response(json_data)
            #self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()
            self.flush_headers()
            

    def do_POST(self):

        request_path = self.path
        with open(HTTP_LOG_FILE, 'a') as log_file:
            log_file.write('{}\n'.format(request_path))

        if SEND_RESPONSE:
            self.send_response(200)
            self.end_headers()

    do_PUT = do_POST
    do_DELETE = do_GET


def main():
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
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
