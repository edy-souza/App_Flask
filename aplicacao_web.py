from wsgiref.simple_server import make_server # Desenvolver o Servidor 

def aplicacao(environ, start_response):
    
    start_response('200 OK', [('Content-type', 'text/html;charset=utf-8')])
    html = ''
    
    return [html]

make_server('', 5000, aplicacao).serve_forever()