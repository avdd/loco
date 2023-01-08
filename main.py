import time
import os
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.utils import send_file


HERE = os.path.dirname(__file__)
LOCO_ENVIRONMENT = os.environ.get('LOCO_ENVIRONMENT') or 'development'


def relpath(name):
    return os.path.join(HERE, name)


def readfile(name):
    path = relpath(name)
    return open(path, encoding='UTF8').read()


def sendfile(request, name, ctype):
    path = relpath(name)
    return send_file(path, request.environ, mimetype=ctype)


Request.sendfile = sendfile


@Request.application
def hello(rq: Request):  # pylint: disable=invalid-name
    if rq.path == '/':
        rsp = Response(status=302, headers={'Location': '/home'})
        rsp.set_cookie('LOCO_ENVIRONMENT', LOCO_ENVIRONMENT)
        return rsp
    if rq.path == '/home':
        rsp = rq.sendfile('skeleton.html', 'text/html')
        rsp.set_cookie('LOCO_ENVIRONMENT', LOCO_ENVIRONMENT)
        return rsp
    if rq.path == '/app.js':
        time.sleep(1)
        return rq.sendfile('app.js', 'text/javascript')
    return Response('Not found', status=404)


def main():
    run_simple('0.0.0.0', 8000, hello, use_reloader=True, use_debugger=True)


if __name__ == '__main__':
    main()
