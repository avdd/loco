from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


@Request.application
def hello(_):
    return Response('Hello, world!')


def main():
    run_simple('0.0.0.0', 8000, hello, use_reloader=True, use_debugger=True)


if __name__ == '__main__':
    main()
