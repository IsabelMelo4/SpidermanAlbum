# ===================================================
# Alura Album — API — Versão final
# ===================================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import glob

app = FastAPI()

# Libera o acesso para o frontend (qualquer origem pode chamar a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminhos absolutos: o servidor acha a pasta de imagens
# independente de onde o comando for executado
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_BASE, "figurinhas")

# Lista de figurinhas do álbum.
# As figurinhas sem imagem na pasta figurinhas/ ficam comentadas
# até a imagem ser adicionada.
figurinhas = [
    {"id": 1,  "nome": "Peter Parker",           "categoria": "Homem-Aranha (2002)",              "imagem_url": "/figurinhas/1/imagem"},
    {"id": 2,  "nome": "Mary Jane Watson",       "categoria": "Homem-Aranha (2002)",              "imagem_url": "/figurinhas/2/imagem"},
    {"id": 3,  "nome": "Norman Osborn",          "categoria": "Homem-Aranha (2002)",              "imagem_url": "/figurinhas/3/imagem"},
    {"id": 4,  "nome": "Harry Osborn",           "categoria": "Homem-Aranha (2002)",              "imagem_url": "/figurinhas/4/imagem"},

    {"id": 5,  "nome": "Doutor Octopus",         "categoria": "Homem-Aranha 2",                   "imagem_url": "/figurinhas/5/imagem"},
    {"id": 6,  "nome": "Peter Parker",           "categoria": "Homem-Aranha 2",                   "imagem_url": "/figurinhas/6/imagem"},
    {"id": 7,  "nome": "Mary Jane Watson",       "categoria": "Homem-Aranha 2",                   "imagem_url": "/figurinhas/7/imagem"},
    {"id": 8,  "nome": "Harry Osborn",           "categoria": "Homem-Aranha 2",                   "imagem_url": "/figurinhas/8/imagem"},

    {"id": 9,  "nome": "Venom",                  "categoria": "Homem-Aranha 3",                   "imagem_url": "/figurinhas/9/imagem"},
    {"id": 10, "nome": "Homem-Areia",            "categoria": "Homem-Aranha 3",                   "imagem_url": "/figurinhas/10/imagem"},
    {"id": 11, "nome": "Novo Duende",            "categoria": "Homem-Aranha 3",                   "imagem_url": "/figurinhas/11/imagem"},
    {"id": 12, "nome": "Peter Parker",           "categoria": "Homem-Aranha 3",                   "imagem_url": "/figurinhas/12/imagem"},

    {"id": 13, "nome": "Peter Parker",           "categoria": "O Espetacular Homem-Aranha",       "imagem_url": "/figurinhas/13/imagem"},
    {"id": 14, "nome": "Gwen Stacy",             "categoria": "O Espetacular Homem-Aranha",       "imagem_url": "/figurinhas/14/imagem"},
    {"id": 15, "nome": "Lagarto",                "categoria": "O Espetacular Homem-Aranha",       "imagem_url": "/figurinhas/15/imagem"},

    {"id": 16, "nome": "Electro",                "categoria": "O Espetacular Homem-Aranha 2",     "imagem_url": "/figurinhas/16/imagem"},
    {"id": 17, "nome": "Duende Verde",           "categoria": "O Espetacular Homem-Aranha 2",     "imagem_url": "/figurinhas/17/imagem"},
    {"id": 18, "nome": "Gwen Stacy",             "categoria": "O Espetacular Homem-Aranha 2",     "imagem_url": "/figurinhas/18/imagem"},
    {"id": 19, "nome": "Peter Parker",           "categoria": "O Espetacular Homem-Aranha 2",     "imagem_url": "/figurinhas/19/imagem"},

    {"id": 20, "nome": "Abutre",                 "categoria": "Homem-Aranha: De Volta ao Lar",    "imagem_url": "/figurinhas/20/imagem"},
    {"id": 21, "nome": "Peter Parker",           "categoria": "Homem-Aranha: De Volta ao Lar",    "imagem_url": "/figurinhas/21/imagem"},
    {"id": 22, "nome": "Ned Leeds",              "categoria": "Homem-Aranha: De Volta ao Lar",    "imagem_url": "/figurinhas/22/imagem"},
    {"id": 23, "nome": "Tony Stark",             "categoria": "Homem-Aranha: De Volta ao Lar",    "imagem_url": "/figurinhas/23/imagem"},

    {"id": 24, "nome": "Mysterio",               "categoria": "Homem-Aranha: Longe de Casa",      "imagem_url": "/figurinhas/24/imagem"},
    {"id": 25, "nome": "MJ",                     "categoria": "Homem-Aranha: Longe de Casa",      "imagem_url": "/figurinhas/25/imagem"},
    {"id": 26, "nome": "Peter Parker",           "categoria": "Homem-Aranha: Longe de Casa",      "imagem_url": "/figurinhas/26/imagem"},

    {"id": 27, "nome": "Doutor Estranho",        "categoria": "Homem-Aranha: Sem Volta para Casa","imagem_url": "/figurinhas/27/imagem"},
    {"id": 28, "nome": "Peter Parker",           "categoria": "Homem-Aranha: Sem Volta para Casa","imagem_url": "/figurinhas/28/imagem"},
    {"id": 29, "nome": "Duende Verde",           "categoria": "Homem-Aranha: Sem Volta para Casa","imagem_url": "/figurinhas/29/imagem"},
    {"id": 30, "nome": "Homem-Aranha (Tobey, Andrew e Tom)", "categoria": "Homem-Aranha: Sem Volta para Casa", "imagem_url": "/figurinhas/30/imagem"},
]

@app.get("/figurinhas")
def listar_figurinhas():
    # Devolve o JSON com todas as figurinhas do álbum
    return figurinhas


@app.get("/figurinhas/{id}/imagem")
def imagem_da_figurinha(id: int):
    # Procura o arquivo que começa com o número da figurinha.
    # Tentamos primeiro sem zero à esquerda (ex: "1.peter-parker.jpg")
    # e depois com zero à esquerda (ex: "01.peter-parker.jpg") para compatibilidade.
    padrao = os.path.join(PASTA_IMAGENS, f"{id}[!0-9]*")
    arquivos = glob.glob(padrao)

    if not arquivos:
        padrao_zero = os.path.join(PASTA_IMAGENS, f"{id:02d}[!0-9]*")
        arquivos = glob.glob(padrao_zero)

    # Nenhum arquivo encontrado para esse id
    if not arquivos:
        raise HTTPException(status_code=404, detail="Figurinha não encontrada")

    # Entrega os bytes da imagem (o FastAPI descobre o Content-Type pela extensão)
    return FileResponse(arquivos[0])