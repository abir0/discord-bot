import discord
from quote_generator import quote
import random
import sys
import re

client = discord.Client()

def toss():
    return random.choice(['Head', 'Tail'])

def greet(man):
    return random.choice(['Hey @{} .', 'Good day, @{} !', 'Greetings @{} .']).format(man)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello, I\'m robot!')

    if message.content.startswith('$quote'):
        await message.channel.send(quote.generate_quote())

    if message.content.startswith('$toss'):
        await message.channel.send(toss())

    if message.content.startswith('$greet'):
        await message.channel.send(greet(message.content.replace('$greet', '').strip()))

if __name__ == '__main__':
    TOKEN = 'ODM5Mzg0OTg3MjkxNzQ2MzA0.YJI4Lw.xtp0Csxr1GXDweWzLSc1q5IqPYk'

    client.run(TOKEN)
