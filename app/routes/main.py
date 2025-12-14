from flask import Blueprint, jsonify, request, current_app
from app.modelos.user import LoginPayLoad
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.modelos.products import *
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

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
        jsonify({'error' : 'Corpo da requisição inválido ou não é um JSON'})
    
    if user_data.username == 'admin' and user_data.password == 'supersecret':
        token = jwt.encode(
            {
                "user_id" : user_data.username,
                "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'access_token': token}), 200

    
    return jsonify({'error' : 'Credenciais Inválidas!'}), 401
        

# RF :O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
    return jsonify(products_list)

# RF: O sistema deve permitir a criação de um novo produto
@main_bp.route('/products', methods=['POST'])
@token_required

def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error" : e.errors()})
    
    result = db.products.insert_one(product.model_dump())
    return jsonify({'mensagem' : 'Está é a rota de criação de produto',
                    "id" : str(result.inserted_id)}), 201

# RF: O sistema deve permitir a visualização dos detalhes de um único produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    print(product_id)
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({'error' : f'Erro ao transformar o {product_id} em ObjectID: {e}'})
    
    product = db.products.find_one({'_id':oid})
    
    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({'error' : f'Produto com id: {product_id}- Não encontrado!'})

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





