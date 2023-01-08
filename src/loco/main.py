import json
import os
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.utils import send_file


HERE = os.path.dirname(__file__)
LOCO_ENVIRONMENT = os.environ.get('LOCO_ENVIRONMENT') or 'development'

SKELETON_HTML = None


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
def app(rq: Request):
    if rq.path == '/':
        rsp = Response(status=302, headers={'Location': '/home'})
        rsp.set_cookie('LOCO_ENVIRONMENT', LOCO_ENVIRONMENT)
        return rsp
    if rq.path == '/home':
        rsp = serve_skeleton_html(rq)
        rsp.set_cookie('LOCO_ENVIRONMENT', LOCO_ENVIRONMENT)
        return rsp
    if rq.path == '/app.css':
        return rq.sendfile('app.css', 'text/css')
    if rq.path == '/screen/Home':
        html = '<p class=Home>Hello, world!</p>'
        data = {'html': html}
        return Response(json.dumps(data), mimetype='application/json')
    return Response('Not found', status=404)


def serve_skeleton_html(rq):
    if SKELETON_HTML:
        rsp = Response(SKELETON_HTML, mimetype='text/html')
    else:
        rsp = rq.sendfile('skeleton.html', 'text/html')
    return rsp


def main():
    static = {'/static': HERE}
    kwargs = {}
    if os.environ.get('LOCO_ENVIRONMENT') == 'development':
        kwargs['use_debugger'] = True
        kwargs['use_reloader'] = True
    run_simple('0.0.0.0', 8000, app, static_files=static, **kwargs)


if __name__ == '__main__':
    main()
