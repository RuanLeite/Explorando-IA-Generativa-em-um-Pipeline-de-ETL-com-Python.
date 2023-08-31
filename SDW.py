import pandas as pd
import requests
import json
import random
import os

diretorio_atual = os.path.abspath(os.path.dirname(__file__))

caminho_arquivo = os.path.join(diretorio_atual, 'SDW.csv')
caminho_arquivo2 = os.path.join(diretorio_atual, 'msgRandom.txt')

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

df = pd.read_csv(caminho_arquivo)
user_ids = df['UserID'].tolist()
print(user_ids)

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json () if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

with open(caminho_arquivo2, 'r') as arquivo:
  mensagens = arquivo.readlines()

def generate_ai_news(user):
  mensagem = random.choice(mensagens).strip()
  text = (f"Ola {user['name']}, {mensagem}")
  return text

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({"description": news})

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")