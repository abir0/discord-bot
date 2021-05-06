import discord
from discord.ext import commands
import os
import asyncio
import youtube_dl
from datetime import datetime
from urllib.request import urlopen
from random import choice
import time
import json
import re


intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", intents=intents,
                     description="This is yet another discord bot.")


greet_options = ["Hey", "Hi", "Greetings", "Hello"]

coin = ["https://i.imgur.com/csSP4ce.jpg", "https://i.imgur.com/NSrQtWx.jpg"]

games = ["Valorant", "Minecraft", "Paladins"]

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {'format': 'bestaudio/best',
                                 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


## Functions
def youtube_search(*query):
    query_string = "+".join(list(query))
    html_content = urlopen("https://www.youtube.com/results?search_query=" + query_string)
    return re.search(r"\"\/watch\?v=(\S{11})\"", html_content.read().decode())[1]

## General Commands
@bot.command(name="ping", help="Check the bot latency")
async def ping(ctx):
    message = await ctx.send("Pinging...")
    time.sleep(0.5)
    await message.edit(content="Latency = {}ms".format(round(bot.latency * 1000)))

@bot.command(name="hello", help="Say hello to the bot")
async def hello(ctx):
    await ctx.send(choice(greet_options) + " {0.display_name}!".format(ctx.author))

@bot.command(name="say", help="Make the bot say something")
async def say(ctx, *words):
    await ctx.send(" ".join(list(words)))

@bot.command(name="quote", help="Get a random quote")
async def quote(ctx):
    response = urlopen("https://zenquotes.io/api/random")
    json_data = json.loads(response.read())
    await ctx.send("\"{}\"\t~ {}".format(json_data[0]["q"], json_data[0]["a"]))

@bot.command(name="toss", help="Toss a coin")
async def toss(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    url = choice(coin)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.command(name="info", help="View relevant info about the server")
async def info(ctx):
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


@bot.command(name="youtube", help="Search youtube")
async def youtube(ctx, *query):
    await ctx.send("https://www.youtube.com/watch?v=" + youtube_search(*query))


## Music Player
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
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
        return cls(discord.FFmpegPCMAudio(source=filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='join', help='Join into the voice channel')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='play', help='Play a song')
    async def play(ctx, *query):
        try :
            voice_channel = ctx.message.guild.voice_client
            url = youtube_search(*query)

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_channel.play(player, after=lambda e: print('Player error: {}'.format(e)) if e else None)
            await ctx.send('Now playing: {}'.format(filename))
        except:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @bot.command(name='pause', help='This command pauses the song')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @bot.command(name='resume', help='Resumes the song')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @bot.command(name='stop', help='Stops the song')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command()
    async def leave(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @resume.before_invoke
    @pause.before_invoke
    @stop.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


## Events
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(choice(games)))
    print("We have logged in as {0.user}".format(bot))


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if "hi" in message.content.lower():
        await message.channel.send("hi")


if __name__ == "__main__":
    bot.add_cog(Music(bot))
    bot.run(os.environ["token"])
