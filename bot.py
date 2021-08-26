from warnings import catch_warnings
import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import youtube_dl

client = discord.Client()

LISTA_MUSICAS = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #print(f'Quantidade de musicas: - {len(LISTA_MUSICAS)}')

#captura texto do discord
@client.event
async def on_message(message):
  try:

    print(f'Author - {message.author}')
    if message.author == client.user:
      return

    if message.content.startswith('$hello'):
      textAuthor = message.author
      #textAuthor = textAuthor.split('#')
      await message.channel.send(f'Hello! @{textAuthor}')
    
    if message.content.startswith('$help'):
      await message.channel.send('Help!')

    if message.content.startswith('$m q'):
      await message.channel.send(len(LISTA_MUSICAS))

  except KeyboardInterrupt:
    print('Bot Finalizado')
  except Exception as e:
  #  if message.author == 'Guedes#8500':
  #    await message.channel.send(f'Ocorreu um erro no Bot {e}')
  #  else:
     await message.channel.send(f'Ocorreu um erro no Bot')
  

client.run('ODc5NTEwMzYxMjU3MTc3MDk5.YSQx2g.XfZHM0JxzfJ4Wxtek77RVMI2XSs')

'''import discord
import os
import requests
import json

client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

client.run(os.getenv('ODc5NTEwMzYxMjU3MTc3MDk5.YSQx2g.Vtx-kRFqUUmv8bdK9LNqstDhYfM'))'''