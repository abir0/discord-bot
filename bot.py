import os
import asyncio
from datetime import datetime
from urllib.request import urlopen
import requests
from random import choice, randint
import time
import json
import re

import discord
from discord.ext import commands
import youtube_dl


bot = commands.Bot(command_prefix="$", intents=discord.Intents().all(),
                        description="This is yet another discord bot.")


greet_options = ["Hey", "Hi", "Greetings", "Hello"]

coin = ["https://i.imgur.com/csSP4ce.jpg", "https://i.imgur.com/NSrQtWx.jpg"]

games = ["Valorant", "Minecraft", "Paladins"]

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_options = {'format': 'bestaudio/best',
                'outtmpl': '%(title)s-%(id)s.%(ext)s', # output file format
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_options)


## Functions
def youtube_search(*query):
    query_string = "+".join(list(query))
    html_content = urlopen("https://www.youtube.com/results?search_query=" + query_string)
    return re.search(r"\"\/watch\?v=(\S{11})\"", html_content.read().decode())[1]

## General Commands
@bot.command(name="ping", help="Check the bot latency")
async def ping(ctx: commands.Context):
    message = await ctx.send("Pinging...")
    time.sleep(0.5)
    await message.edit(content="Latency = {}ms".format(round(bot.latency * 1000)))

@bot.command(name="say", help="Make the bot say something")
async def say(ctx: commands.Context, *words: str):
    await ctx.send(" ".join(list(words)))

@bot.command(name="quote", help="Get a random quote")
async def quote(ctx: commands.Context):
    response = urlopen("https://zenquotes.io/api/random")
    json_data = json.loads(response.read())
    await ctx.send("\"{}\"\t~ {}".format(json_data[0]["q"], json_data[0]["a"]))

@bot.command(name="toss", help="Toss a coin")
async def toss(ctx: commands.Context):
    embed = discord.Embed(color=discord.Color.blue())
    url = choice(coin)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.command(name="info", help="View relevant info about the server")
async def info(ctx: commands.Context):
    embed = discord.Embed(title="{}".format(ctx.guild.name),
                          timestamp=datetime.utcnow(),
                          color=discord.Color.blue())
    embed.add_field(name="Server created at", value="{}".format(ctx.guild.created_at.strftime("%m-%d-%Y %H:%M")))
    embed.add_field(name="Server Owner", value="{}".format(ctx.guild.owner))
    embed.add_field(name="Server Region", value="{}".format(ctx.guild.region))
    embed.add_field(name="Total Members", value="{}".format(ctx.guild.member_count))
    embed.add_field(name="Server ID", value="{}".format(ctx.guild.id))
    embed.set_thumbnail(url="{}".format(ctx.guild.icon_url))
    await ctx.send(embed=embed)


class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command(name='hello', help='Say hello to the bot')
    async def hello(self, ctx: commands.Context, *, member: discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(choice(greet_options) + ' {0.name}!'.format(member))
        else:
            await ctx.send(choice(greet_options) + ' {0.name}... Hmm this feels familiar.'.format(member))
        self._last_member = member


class Math(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="add", help="Add two numbers")
    async def add(self, ctx: commands.Context, num1: str, num2: str):
        await ctx.send("{}".format(float(num1) + float(num2)))

    @commands.command(name="sub", help="Subtract two numbers")
    async def sub(self, ctx: commands.Context, num1: str, num2: str):
        await ctx.send("{}".format(float(num1) - float(num2)))

    @commands.command(name="mul", help="Multiply two numbers")
    async def mul(self, ctx: commands.Context, num1: str, num2: str):
        await ctx.send("{}".format(float(num1) * float(num2)))

    @commands.command(name="div", help="Divide two numbers")
    async def div(self, ctx: commands.Context, num1: str, num2: str):
        await ctx.send("{}".format(float(num1) / float(num2)))

    @commands.command(name="mod", help="Remainder of two numbers")
    async def mod(self, ctx: commands.Context, num1: str, num2: str):
        await ctx.send("{}".format(float(num1) % float(num2)))


class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="youtube", help="Search youtube and get the result")
    async def youtube(self, ctx: commands.Context, *query: str):
        await ctx.send("https://www.youtube.com/watch?v=" + youtube_search(*query))

    @commands.command(name="wiki", help="Get wikipedia search url")
    async def wikipidea(self, ctx: commands.Context, *query: str):
        await ctx.send("https://en.wikipedia.org/wiki/" + "_".join(list(query)))

    @commands.command(name="google", help="Get google search url")
    async def google(self, ctx: commands.Context, *query: str):
        await ctx.send("https://www.google.com/search?q=" + "+".join(list(query)))


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="meme", help="Get a meme template")
    async def meme_template(self, ctx: commands.Context):
        response = requests.get("https://api.imgflip.com/get_memes")
        json_data = json.loads(response.text)
        memes_list = json_data["data"]["memes"]
        index = randint(0, len(memes_list) - 1)
        await ctx.send("{}".format(memes_list[index]["url"]))

    @commands.command(name="gif", help="Get a random GIF (possibly related to meme)")
    async def gif(self, ctx: commands.Context):
        response = requests.get("https://api.giphy.com/v1/gifs/random?api_key={}&tag=&rating=r".format(os.environ["giphy_api_key"]))
        json_data = json.loads(response.text)
        await ctx.send("{}".format(json_data["data"]["url"]))


## Music Player
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.75):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='join', help='Add bot to the voice channel')
    async def join(self, ctx: commands.Context):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='play', help='Play a song')
    async def play(self, ctx: commands.Context, *query: str):
        voice_client = ctx.message.guild.voice_client
        if voice_client is not None:
            if voice_client.is_playing():
                await voice_client.stop()
            url = "https://www.youtube.com/watch?v=" + youtube_search(*query)

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_client.play(player, after=lambda e: print('Player error: {}'.format(e)) if e else None)
            await ctx.send('Now playing: {}'.format(player.title))
        else:
            await ctx.send("Not connected to a voice channel.")

    @commands.command(name='volume', help='Change the volume')
    async def volume(self, ctx: commands.Context, volume: int):
        voice_client = ctx.message.guild.voice_client
        if voice_client is not None:
            voice_client.source.volume = volume / 100
            await ctx.send("Changed volume to {}%".format(volume))
        else:
            await ctx.send("Not connected to a voice channel.")

    @commands.command(name='pause', help='Pause the song')
    async def pause(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        elif voice_client.is_playing():
            await ctx.send("The bot is already playing a song.")
        else:
            await ctx.send("The bot was not playing anything before this. Use play command.")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='leave', help='Disconnect bot from the voice channel')
    async def leave(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()


## Events
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(choice(games)))
    print("We have logged in as {0.user}".format(bot))
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send('Robot Activated...')
                await channel.send(file=discord.File('robot.png'))
        print('Active in {}\nMember Count : {}'.format(guild.name,guild.member_count))


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return


if __name__ == "__main__":
    bot.add_cog(Greetings(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(Search(bot))
    bot.add_cog(Meme(bot))
    bot.add_cog(Music(bot))
    bot.run(os.environ["token"])
