from flask import Blueprint, jsonify, request
from app.modelos.user import LoginPayLoad
from pydantic import ValidationError
'''
Blueprint é uma forma de organizar rotas em módulos separados dentro do projeto Flask.
Serve para deixar o código mais limpo e dividido por partes.
'''

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um TOKEN
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayLoad(**raw_data)
    
    except ValidationError as e:
        return jsonify({'error' : e.errors()}), 400
    except Exception as e:
        jsonify({'error' : 'Erro durante a requisição do dado'}), 500
        
    return jsonify({'mensagem' : f'Realizar o login do usuário {user_data.model_dump_json()}'})

# RF :O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify({'mensagem' : 'Está é a rota de listagem dos produtos'})

# RF: O sistema deve permitir a criação de um novo produto
@main_bp.route('/products', methods=['POST'])
def create_products():
    return jsonify({'mensagem' : 'Está é a rota de criação de produtos'})

# RF: O sistema deve permitir a visualização dos detalhes de um único produto
@main_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return jsonify({'mensagem' : f'Está é a rota de visualização do detalhe do id do produto {product_id}'})

# RF: O sistema deve permitir a atualização de um único produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({'mensagem' : f'Está é a rota de atualização do produto com o id {product_id}'})

# RF: O sistema deve permitir a deleção de um único produto e produto existente 
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({'mensagem' : f'Está é a rota de deleção do produto com o id {product_id}'})

# RF: O sistema deve permitir a importação de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({'mensagem' : 'Está é a rota de upload do arquivo de vendas'})

@main_bp.route('/')
def index():
    return jsonify({'message' : 'Bem vindo ao StyleSync!'})





