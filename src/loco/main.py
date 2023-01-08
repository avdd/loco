import json
import os
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.utils import send_file


HERE = os.path.dirname(__file__)
LOCO_ENVIRONMENT = os.environ.get('LOCO_ENVIRONMENT') or 'development'
SKELETON_HTML = None
URL_REGISTRY = {}


def sendfile(request, name, ctype):
    path = os.path.join(HERE, name)
    return send_file(path, request.environ, mimetype=ctype,
                     conditional=False, etag=False)


Request.sendfile = sendfile


def register(url):
    def register_handler(func):
        URL_REGISTRY[url] = func
    return register_handler


def create_app(registry):
    def wsgi_app(rq: Request):
        func = registry.get(rq.path)
        if func:
            return func(rq)
        return Response('Not found', status=404)
    return Request.application(wsgi_app)


@register('/')
def redirect_root(_):
    rsp = Response(status=302, headers={'Location': '/home'})
    rsp.set_cookie('LOCO_ENVIRONMENT', LOCO_ENVIRONMENT, samesite='Strict')
    return rsp


@register('/home')
def home(rq):
    if SKELETON_HTML:
        rsp = Response(SKELETON_HTML, mimetype='text/html')
    else:
        rsp = rq.sendfile('skeleton.html', 'text/html')
    rsp.set_cookie('LOCO_ENVIRONMENT', LOCO_ENVIRONMENT, samesite='Strict')
    return rsp


@register('/app.css')
def app_css(rq):
    return rq.sendfile('app.css', 'text/css')


@register('/screen/Home')
def home_screen(_):
    html = '<p class=Home>Hello, world!</p>'
    data = {'html': html}
    return Response(json.dumps(data), mimetype='application/json')


def run_devel_server():
    static = {'/static': HERE}
    kwargs = {'static_files': static, 'threaded': True}
    if LOCO_ENVIRONMENT == 'development':
        kwargs['use_debugger'] = True
        kwargs['use_reloader'] = True
        os.environ['WERKZEUG_DEBUG_PIN'] = 'off'
    app = create_app(URL_REGISTRY)
    run_simple('0.0.0.0', 8000, app, **kwargs)


if __name__ == '__main__':
    run_devel_server()
