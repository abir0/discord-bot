import discord
from discord.ext import commands
import os

from datetime import datetime
from urllib.request import urlopen
import random
import re

bot = commands.Bot(command_prefix='$', description="This is a Helper Bot")

greetings_list = ['Hey {}', 'Good day, {}!', 'Greetings {}']

quotes_list = [("Jett", "Wash dish."),
               ("Sova", "I'm da hunter.")]

## Commands
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, I\'m robot!')

@bot.command()
async def say(ctx, *words):
    await ctx.send(" ".join(list(words)))

@bot.command()
async def greet(ctx, name):
    await ctx.send(random.choice(greetings_list).format(name))

@bot.command()
async def quote(ctx):
    quote = random.choice(quotes_list)
    await ctx.send('\n"{}"\t ~ {}\n'.format(quote[1], quote[0]))

@bot.command()
async def toss(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    url = random.choice(["https://i.imgur.com/csSP4ce.jpg", "https://i.imgur.com/NSrQtWx.jpg"])
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}",
                          timestamp=datetime.utcnow(),
                          color=discord.Color.blue())
    embed.add_field(name="Server created at", value="{}".format(ctx.guild.created_at.strftime("%m-%d-%Y %H:%M")))
    embed.add_field(name="Server Owner", value="{}".format(ctx.guild.owner))
    embed.add_field(name="Server Region", value="{}".format(ctx.guild.region))
    embed.add_field(name="Total Members", value="{}".format(ctx.guild.member_count))
    embed.add_field(name="Server ID", value="{}".format(ctx.guild.id))
    embed.set_thumbnail(url="{}".format(ctx.guild.icon_url))
    await ctx.send(embed=embed)

@bot.command()
async def youtube(ctx, *search):
    query_string = '+'.join(list(search))
    html_content = urlopen('https://www.youtube.com/results?search_query=' + query_string)
    search_results = re.search(r'\"\/watch\?v=(\S{11})\"', html_content.read().decode())
    # shows the first result
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[1])

## Events
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if 'hi' in message.content.lower():
        await message.channel.send('hi')

if __name__ == '__main__':
    bot.run(os.environ['token'])
