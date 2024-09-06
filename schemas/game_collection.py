from pydantic import BaseModel
from typing import List
from model.game_collection import GameCollection

# from schemas import ComentarioSchema

class GameListSchema(BaseModel):
    query: str

class GameSchema(BaseModel):
    title: str
    release_date: str
    purchase_date: str
    is_favorite: bool
    status: str
    cover_art: str

class GameDeleteSchema(BaseModel):
    id: int

# class ProdutoSchema(BaseModel):
#     """ Define como um novo produto a ser inserido deve ser representado
#     """
#     nome: str = "Banana Prata"
#     quantidade: Optional[int] = 12
#     valor: float = 12.50


# class ProdutoBuscaSchema(BaseModel):
#     """ Define como deve ser a estrutura que representa a busca. Que será
#         feita apenas com base no nome do produto.
#     """
#     nome: str = "Teste"


# class ListagemProdutosSchema(BaseModel):
#     """ Define como uma listagem de produtos será retornada.
#     """
#     produtos:List[ProdutoSchema]


def list_games(game_collection: List[GameCollection]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
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

    return {"game_collection": result}


# class ProdutoViewSchema(BaseModel):
#     """ Define como um produto será retornado: produto + comentários.
#     """
#     id: int = 1
#     nome: str = "Banana Prata"
#     quantidade: Optional[int] = 12
#     valor: float = 12.50
#     total_cometarios: int = 1
#     comentarios:List[ComentarioSchema]


# class ProdutoDelSchema(BaseModel):
#     """ Define como deve ser a estrutura do dado retornado após uma requisição
#         de remoção.
#     """
#     mesage: str
#     nome: str

# def apresenta_produto(produto: GameCollection):
#     """ Retorna uma representação do produto seguindo o schema definido em
#         ProdutoViewSchema.
#     """
#     return {
#         "id": produto.id,
#         "nome": produto.nome,
#         "quantidade": produto.quantidade,
#         "valor": produto.valor,
#         "total_cometarios": len(produto.comentarios),
#         "comentarios": [{"texto": c.texto} for c in produto.comentarios]
#     }
