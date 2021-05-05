import discord
import os
import random

client = discord.Client()

quotes_list = [("Jett", "Wash dish."),
               ("Sova", "I'm da hunter.")]

def toss():
    return random.choice(['Head', 'Tail'])

def greet(man):
    return random.choice(['Hey @{} .', 'Good day, @{} !', 'Greetings @{} .']).format(man)

def generate_quote():
    global quotes_list
    q = random.choice(quotes_list)
    return '\n"{}" \t ~ {}\n'.format(q[1], q[0])

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
        await message.channel.send(generate_quote())

    if message.content.startswith('$toss'):
        await message.channel.send(toss())

    if message.content.startswith('$greet'):
        await message.channel.send(greet(message.content.replace('$greet', '').strip()))

if __name__ == '__main__':
    client.run(os.environ['token'])
