from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http import HTTPStatus


def main():
    handler_class = BasicHandler
    port = 8000
    listen = ('0.0.0.0', port)
    server = ThreadingHTTPServer(listen, handler_class)
    with server:
        print(f"Serving at http://localhost:{port}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")


class BasicHandler(BaseHTTPRequestHandler):

    server_version = "loco/0"
    encoding = 'UTF-8'
    message = 'Hello, world!'

    def do_GET(self):  # pylint: disable=invalid-name
        self.send_head()
        self.wfile.write(self.message.encode(self.encoding))

    def do_HEAD(self):  # pylint: disable=invalid-name
        self.send_head()

    def send_head(self):
        self.send_response(HTTPStatus.OK)
        content_type = f'text/plain;charset={self.encoding}'
        self.send_header("Content-type", content_type)
        content_length = len(self.message)
        self.send_header('Content-Length', str(content_length))
        self.end_headers()


if __name__ == '__main__':
    main()
