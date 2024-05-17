"""
WSGI config for technop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "technop.settings")

application = get_wsgi_application()


# simple_wsgi.py

import logging

def simple_app(environ, start_response):
    # Настройка логгера
    logger = logging.getLogger('simple_wsgi')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # Логирование запроса
    logger.info(f"Handling request: {environ['REQUEST_METHOD']} {environ.get('PATH_INFO', '')}")

    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)

    method = environ.get('REQUEST_METHOD', 'GET')
    params = environ.get('QUERY_STRING', '')

    if method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        response_body = f"POST parameters: {request_body.decode('utf-8')}\n"
    else:
        response_body = f"GET parameters: {params}\n"

    # Логирование ответа
    logger.info(f"Response body: {response_body.strip()}")

    return [response_body.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8081, simple_app)
    server.serve_forever()
