from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


@Request.application
def hello(rq: Request):  # pylint: disable=invalid-name
    if rq.path == '/':
        return Response(status=302, headers={'Location': '/home'})
    if rq.path == '/home':
        html = '''
        <script>
        function StartLoading() {
            setTimeout(AddHome, 100);
        }
        function AddHome() {
            const p = document.createElement('p');
            p.textContent = 'Hello, world!'
            p.className = 'Home';
            document.body.appendChild(p);
        }
        </script>
        '''
        return Response(html, mimetype='text/html')
    return Response('Not found', status=404)


def main():
    run_simple('0.0.0.0', 8000, hello, use_reloader=True, use_debugger=True)


if __name__ == '__main__':
    main()
