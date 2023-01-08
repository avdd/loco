import time
import os
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.utils import send_file


HERE = os.path.dirname(__file__)
SELENIUM_TEST = os.environ.get('SELENIUM_TEST')


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
        if SELENIUM_TEST:
            rsp.set_cookie('SELENIUM_TEST', '1')
        else:
            rsp.delete_cookie('SELENIUM_TEST')
        return rsp
    if rq.path == '/home':
        return rq.sendfile('skeleton.html', 'text/html')
    if rq.path == '/app.js':
        time.sleep(1)
        return rq.sendfile('app.js', 'text/javascript')
    return Response('Not found', status=404)


def main():
    run_simple('0.0.0.0', 8000, hello, use_reloader=True, use_debugger=True)


if __name__ == '__main__':
    main()
