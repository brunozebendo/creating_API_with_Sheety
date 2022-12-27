"""A ideia do código é criar um aplicativo onde se informe a quantidade e o tipo de exercício feito em um dia
e isso seja comunicado para uma planilha do Google DOCS que vai indicar a quantidade de caloria gasta, para isso
 será usada a API da Natural Language que reconhece o texto e busca a informação correspondente, ou, no caso,
  acrescenta a informação. Esse código não vai ser explicado pela Angela,
vou tentar entender."""
"""Sheety, site para transformar o Google forms em uma API:
Thousands of people are using Sheety to turn their spreadsheets into powerful APIs to rapidly develop prototypes,
 websites, apps and more. Sheety turns your spreadsheet into a Restful JSON API, meaning you can get data in and out of
  your spreadsheet using simple HTTP requests and URLs. It also means that Sheety can work with pretty much anything 
  you like: if it connects to the Internet, it works with Sheety.
  Traduzindo, o sheety pega as informações na planilha do google docs, usa o título de cada coluna como key e o valor
  da célula como value, depois transforma isso em um endereço de endpoint a ser passado para o programa. Também 
  é preciso dar algumas permissões no google dcs"""

import requests
from datetime import datetime
import os

GENDER = YOUR GENDER
WEIGHT_KG = YOUR WEIGHT
HEIGHT_CM = YOUR HEIGHT
AGE = YOUR AGE

APP_ID = os.environ["YOUR_APP_ID"]
API_KEY = os.environ["YOUR_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["https://docs.google.com/spreadsheets/d/1DHL6Y8XAHSC_KhJsa9QMekwP8b4YheWZY_sxlH3i494/edit#gid=0"]

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)
"""parte do código para obter a data e a hora e repassá-la ao sheet_inputs no formato correto"""
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
"""esse código serve para incluir um novo exercício no google docs, para isso, ele usa um for loop, guardando
na variável sheet_inputs todas as informações aninhadas dentro do workout. Conforme informações na documentação
da API do Sheety, a informação para o POST tem que estar aninhada em uma variável que é a que constará no endereço
do endpoint, depois o código abaixo usa o request.post para incluir as informações no formato json. Reparar que 
foi passada função interna .title() para que exercício fique com a primeira letra em maiúsculo"""
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    #No Auth
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)
"""O sheety por padrão não requer autenticação, mas, se o usuário quiser, existem 2 tipos de autenticação, a básica que 
    faz um requerimento encripitado com o nome e a senha do usuário que estará gravado no sheety:
     With Basic Auth, a request contains a header field called Authorization, with the value set to the username and 
 password encoded as base64. You set the username and password inside of Sheety.
Já o bearer auth encripta o usuário e a senha em uma string (mas não entendi muito bem como funciona)
Bearer auth
Bearer authentication works exactly the same as Basic auth, though instead of username and password encoded as base64,
 it’s simply a token (or secret) of your choosing.
"""
"""todo o código os.environ significa que as informações sensíveis foram guardadas em Environment Variables. Melhor
explicando, o usuário e a senha foram guardadas dentro das variáveis de ambiente, assim, elas não ficam visíveis no código 
e nem quando passadas para outro programa. Como ele funciona como um dicionário, basta passar a key"""
    #Basic Auth
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            os.environ["USERNAME"],
            os.environ["PASSWORD"],
        )
    )

    #Bearer Token
    bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )

    print(sheet_response.text)
