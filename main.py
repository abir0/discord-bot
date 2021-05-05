import discord
from quote_generator import quote

TOKEN = "ODM5Mzg0OTg3MjkxNzQ2MzA0.YJI4Lw.xtp0Csxr1GXDweWzLSc1q5IqPYk"

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$quote'):
        await message.channel.send(quote.generate_quote())

client.run(TOKEN)
