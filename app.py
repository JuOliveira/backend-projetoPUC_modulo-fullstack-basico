from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, GameCollection, GameStatus
from logger import logger
from schemas import *
from flask_cors import CORS

import requests

from schemas.game_collection import GameListSchema, GameSchema, GameDeleteSchema, list_games


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

API_KEY = 'f2735556bb694a2190b3f83c59f5ba4c'
base_url = 'https://api.rawg.io/api'

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
#produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
game_collection_tag = Tag(name='Coleção de jogos', description='Adição, visualização e remoção de jogos da coleção no banco de dados')
rawg_api_tag = Tag(name='Biblioteca RAWG', description='Busca de dados na biblioteca RAWG')
game_status_tag = Tag(name='Status do jogo', description='Status de andamento do jogo')
# comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/game_collection', tags=[game_collection_tag])
def get_game_collection():
    session = Session()
    game_collection = session.query(GameCollection).all()

    if not game_collection:
        return {"game_collection": []}, 200
    else:
        result = []

        for game in game_collection:
            result.append({
                "id": game.id,
                "title": game.title,
                "release_date": game.release_date,
                "purchase_date": game.purchase_date,
                "is_favorite": game.is_favorite,
                "status": game.status,
                "cover_art": game.cover_art,
            })

        return { "game_collection": result }, 200

@app.post('/game', tags=[game_collection_tag])
def add_game(form: GameSchema):
    game = GameCollection(
        title = form.title,
        release_date = form.release_date,
        purchase_date = form.purchase_date,
        is_favorite = form.is_favorite,
        status = form.status,
        cover_art = form.cover_art,
    )
    session = Session()
    session.add(game)
    session.commit()

    return { "message": 'Jogo adicionado com sucesso' }, 200

@app.delete('/game', tags=[game_collection_tag])
def delete_game(game_id: GameDeleteSchema):
    session = Session()
    response = session.query(GameCollection).filter_by(id = game_id).delete()
    session.commit()

    if response:
        return { "message": 'Jogo removido com sucesso'}, 200
    else:
        return { "message": 'Ocorreu um erro'}, 404

@app.get('/games_list', tags=[rawg_api_tag])
def get_game_list(query: GameListSchema):
    response = requests.get(base_url+'/games', {"search": query, "key": API_KEY})
    return response.json(), 200

@app.get('/platforms', tags=[rawg_api_tag])
def get_plataforms():
    response = requests.get(base_url+'/platforms', {"key": API_KEY})
    return response.json(), 200

@app.get('/game_status_list', tags=[game_status_tag])
def get_game_status_list():
    session = Session()
    game_status_list = session.query(GameStatus).all()

    result = []

    for game_status in game_status_list:
        result.append({
            "id": game_status.id,
            "status": game_status.status,
        })
    
    return {"game_status_list": result}, 200



# @app.post('/produto', tags=[produto_tag],
#           responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
# def add_produto(form: ProdutoSchema):
#     """Adiciona um novo Produto à base de dados

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto = Produto(
#         nome=form.nome,
#         quantidade=form.quantidade,
#         valor=form.valor)
#     logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
#     try:
#         # criando conexão com a base
#         session = Session()
#         # adicionando produto
#         session.add(produto)
#         # efetivando o camando de adição de novo item na tabela
#         session.commit()
#         logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
#         return apresenta_produto(produto), 200

#     except IntegrityError as e:
#         # como a duplicidade do nome é a provável razão do IntegrityError
#         error_msg = "Produto de mesmo nome já salvo na base :/"
#         logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
#         return {"mesage": error_msg}, 409

#     except Exception as e:
#         # caso um erro fora do previsto
#         error_msg = "Não foi possível salvar novo item :/"
#         logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
#         return {"mesage": error_msg}, 400


# @app.get('/produtos', tags=[produto_tag],
#          responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
# def get_produtos():
#     """Faz a busca por todos os Produto cadastrados

#     Retorna uma representação da listagem de produtos.
#     """
#     logger.debug(f"Coletando produtos ")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     produtos = session.query(Produto).all()

#     if not produtos:
#         # se não há produtos cadastrados
#         return {"produtos": []}, 200
#     else:
#         logger.debug(f"%d rodutos econtrados" % len(produtos))
#         # retorna a representação de produto
#         print(produtos)
#         return apresenta_produtos(produtos), 200


# @app.get('/produto', tags=[produto_tag],
#          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
# def get_produto(query: ProdutoBuscaSchema):
#     """Faz a busca por um Produto a partir do id do produto

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto_id = query.id
#     logger.debug(f"Coletando dados sobre produto #{produto_id}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     produto = session.query(Produto).filter(Produto.id == produto_id).first()

#     if not produto:
#         # se o produto não foi encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
#         return {"mesage": error_msg}, 404
#     else:
#         logger.debug(f"Produto econtrado: '{produto.nome}'")
#         # retorna a representação de produto
#         return apresenta_produto(produto), 200


# @app.delete('/produto', tags=[produto_tag],
#             responses={"200": ProdutoDelSchema, "404": ErrorSchema})
# def del_produto(query: ProdutoBuscaSchema):
#     """Deleta um Produto a partir do nome de produto informado

#     Retorna uma mensagem de confirmação da remoção.
#     """
#     produto_nome = unquote(unquote(query.nome))
#     print(produto_nome)
#     logger.debug(f"Deletando dados sobre produto #{produto_nome}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a remoção
#     count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
#     session.commit()

#     if count:
#         # retorna a representação da mensagem de confirmação
#         logger.debug(f"Deletado produto #{produto_nome}")
#         return {"mesage": "Produto removido", "id": produto_nome}
#     else:
#         # se o produto não foi encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
#         return {"mesage": error_msg}, 404


# @app.post('/cometario', tags=[comentario_tag],
#           responses={"200": ProdutoViewSchema, "404": ErrorSchema})
# def add_comentario(form: ComentarioSchema):
#     """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto_id  = form.produto_id
#     logger.debug(f"Adicionando comentários ao produto #{produto_id}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca pelo produto
#     produto = session.query(Produto).filter(Produto.id == produto_id).first()

#     if not produto:
#         # se produto não encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
#         return {"mesage": error_msg}, 404

#     # criando o comentário
#     texto = form.texto
#     comentario = Comentario(texto)

#     # adicionando o comentário ao produto
#     produto.adiciona_comentario(comentario)
#     session.commit()

#     logger.debug(f"Adicionado comentário ao produto #{produto_id}")

#     # retorna a representação de produto
#     return apresenta_produto(produto), 200
