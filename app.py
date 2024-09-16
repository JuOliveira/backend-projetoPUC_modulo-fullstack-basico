from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, GameCollection, GameStatus
from schemas import *
from flask_cors import CORS

import requests
import base64

# from schemas.game_collection import GameListSchema, GameSchema, GameDeleteSchema


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

API_KEY = 'f2735556bb694a2190b3f83c59f5ba4c'
base_url = 'https://api.rawg.io/api'

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
game_collection_tag = Tag(name='Coleção de jogos', description='Adição, visualização e remoção de jogos da coleção no banco de dados')
rawg_api_tag = Tag(name='Biblioteca RAWG', description='Busca de dados na biblioteca RAWG')
game_status_tag = Tag(name='Status do jogo', description='Status de andamento do jogo')

# conversão de url de imagem para base64
def get_as_base64(url):
    return base64.b64encode(requests.get(url).content).decode('utf-8')


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/game_collection', tags=[game_collection_tag],
         responses={"200": GameCollectionSchema})
def get_game_collection():
    """Busca os jogos cadastrados na coleção

    Retorna a listagem de jogos com suas devidas informações
    """
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
                "platform": game.platform,
                "release_date": game.release_date,
                "purchase_date": game.purchase_date,
                "is_favorite": game.is_favorite,
                "status": game.status,
                "cover_art": game.cover_art,
            })

        return { "game_collection": result }, 200

@app.post('/game', tags=[game_collection_tag],
          responses={"200": GameSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_game(form: GameSchema):
    """Adiciona um jogo na coleção

    Retorna o jogo adicionado
    """
    game = GameCollection(
        title = form.title,
        platform=form.platform,
        release_date = form.release_date,
        purchase_date = form.purchase_date,
        is_favorite = form.is_favorite,
        status = form.status,
        cover_art = form.cover_art,
    )

    try:
        session = Session()
        session.add(game)
        session.commit()
    
    except IntegrityError as e:
        error_msg = "O jogo já existe na coleção"
        return { "message": error_msg}, 409

    except Exception as e:
        error_msg = "Ocorreu um erro e não foi possível adicionar um novo jogo"
        return { "message": error_msg }, 400

    return { 
        "title": form.title,
        "platform": form.platform,
        "release_date": form.release_date,
        "purchase_date": form.purchase_date,
        "is_favorite": form.is_favorite,
        "status": form.status,
        "cover_art": form.cover_art,
     }, 200

@app.delete('/game', tags=[game_collection_tag])
def delete_game(query: GameDeleteSchema):
    """Remove um jogo da coleção baseado na id do jogo

    Retorna uma message de confirmação de remoção.
    """

    session = Session()
    response = session.query(GameCollection).filter_by(id = query.id).delete()
    session.commit()

    if response:
        return { "message": 'Jogo removido com sucesso'}, 200
    else:
        return { "message": 'Ocorreu um erro e o jogo não pôde ser removido'}, 404

@app.get('/games_list', tags=[rawg_api_tag],
         responses={"200": GameSearchListSchema})
def get_game_list(query: GameListSchema):
    """Faz a busca de jogos na biblioteca auxiliar RAWG a partir do nome do jogo

    Retorna uma lista de possíveis jogos que podem satisfazer a busca feita
    """

    response = requests.get(base_url+'/games', {"search": query, "key": API_KEY})
    results = response.json()
    search_result = []

    for result in results['results']:
        search_result.append({            
            'name': result['name'],
            'cover_art': get_as_base64(result['background_image']),
            'platforms': result['platforms'],
            'release_date': result['released'],
        })

    return {"results": search_result}, 200

@app.get('/platforms', tags=[rawg_api_tag],
         responses={"200": PlatformListSchema})
def get_platforms():
    """Busca as plataformas de jogos cadastradas na biblioteca RAWG

    Retorna a lista de plataformas
    """
    response = requests.get(base_url+'/platforms', {"key": API_KEY})
    results = response.json()
    platforms = []

    for item in results['results']:
        platforms.append({
            "id": item['id'],
            "name": item['name'],
        })

    return { "platforms": platforms } , 200

@app.get('/game_status_list', tags=[game_status_tag],
         responses={"200": GameStatusListSchema})
def get_game_status_list():
    """Busca os status possíveis de andamento de um jogo

    Retorna a lista de status
    """

    session = Session()
    game_status_list = session.query(GameStatus).all()
    result = []

    for game_status in game_status_list:
        result.append({
            "id": game_status.id,
            "status": game_status.status,
        })
 
    return {"game_status_list": result}, 200