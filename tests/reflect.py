#!/usr/bin/env python

# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Orinally written by Nathan Hamiel (2010), see:
# https://gist.github.com/1kastner/e083f9e813c0464e6a2ec8910553e632

from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse

DEFAULT_PORT = 8080
HTTP_LOG_FILE = 'tests/data/http_log_file.log'
SEND_RESPONSE = False


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        request_path = self.path
        with open(HTTP_LOG_FILE, 'a') as log_file:
            log_file.write("\n----- GET Request Start ----->\n")
            log_file.write("Request path: {}\n".format(request_path))
            log_file.write("Request headers: {}\n".format(self.headers))
            log_file.write("<----- Request End -----\n")

        if SEND_RESPONSE:
            self.send_response(200)
            self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()

    def do_POST(self):

        request_path = self.path
        with open(HTTP_LOG_FILE, 'a') as log_file:
            log_file.write("\n----- POST Request Start ----->\n")
            log_file.write("Request path: {}\n".format(request_path))
            request_headers = self.headers
            content_length = request_headers.get('Content-Length')
            length = int(content_length) if content_length else 0
            log_file.write("Content Length: {}\n".format(length))
            log_file.write("Request headers: {}\n".format(request_headers))
            payload = self.rfile.read(length)
            log_file.write("Request payload: {}\n".format(payload))
            log_file.write("<----- Request End -----\n")

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
