from wsgiref.simple_server import make_server # Desenvolver o Servidor 

def aplicacao(environ, start_response):
    produtos = [
        {'nome' : 'Notebook', 'valor' : '7499.99'},
        {'nome' : 'Play Station 5', 'valor' : '5877.00'},
        {'nome' : 'Tablet', 'valor' : '1399.99'},
        {'nome' : 'Monitor IPS', 'valor' : '4520.00'},
        {'nome' : 'PC Game', 'valor' : '9.087.00'},
        ]
    start_response('200 OK', [('Content-type', 'text/html;charset=utf-8')])
    
    with open('index.html', 'r', encoding='utf-8') as file:
        html = file.read()
    
    return [html.encode('utf-8')]

make_server('', 5000, aplicacao).serve_forever()